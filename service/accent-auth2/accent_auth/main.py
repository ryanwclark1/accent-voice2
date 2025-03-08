# main.py
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from accent_auth.auth.routes import router as auth_router
from accent_auth.config.app import settings
from accent_auth.config.db import settings as db_settings
from accent_auth.db.engine import AsyncSessionLocal, async_engine
from accent_auth.logging_config import configure_logging
from accent_auth.users.routes import router as users_router
from accent_auth.tenants.routes import router as tenants_router
from accent_auth.groups.routes import router as groups_router
from accent_auth.policies.routes import router as policies_router
from accent_auth.core.routes import router as core_router
from accent_auth.auth.external import (
    google,
    microsoft,
    mobile,
)  # Import external auth modules
from accent_auth.services import (
    AllUsersService,
    DefaultGroupService,
    DefaultPolicyService,
)
from accent_auth.db import DAO
from accent_auth.bus import BusPublisher  # Moved from services
from accent_auth import bootstrap
from accent_auth.utils.status import StatusAggregator

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Starting up...")

    dao = DAO.from_defaults()

    bus_publisher = BusPublisher.from_config(settings.uuid, settings.amqp.model_dump())
    # Instantiate services that need to run at startup
    default_policy_service = DefaultPolicyService(dao, settings.default_policies)
    default_group_service = DefaultGroupService(dao, settings.tenant_default_groups)
    all_users_service = AllUsersService(dao, settings.all_users_policies)

    # Run database migrations (Alembic) - best practice is to run this
    # *outside* the application, but this is for demonstration.  In a
    # production environment, you'd run `alembic upgrade head` separately.
    if db_settings.db_upgrade_on_startup:
        logger.info("Running database migrations...")
        # from alembic.config import Config
        # from alembic import command
        # alembic_config = Config("alembic.ini")  # Use the correct path
        # command.upgrade(alembic_config, "head")
        logger.warning(
            "Skipping database migrations. Run 'alembic upgrade head' manually."
        )

    # Apply default policies and groups
    if settings.update_policy_on_startup:
        logger.info("Updating default policies and groups...")
        async with AsyncSessionLocal() as session:
            async with session.begin():
                top_tenant_uuid = await dao.tenant.find_top_tenant(session=session)
                await default_policy_service.update_policies(
                    top_tenant_uuid, session=session
                )
                visible_tenants = await dao.tenant.list_visible_tenants(
                    top_tenant_uuid, session=session
                )
                tenant_uuids = [tenant.uuid for tenant in visible_tenants]
                await all_users_service.update_policies(tenant_uuids, session=session)
                await default_group_service.update_groups(tenant_uuids, session=session)
                await default_policy_service.delete_orphan_policies(session=session)

    if settings.bootstrap_user_on_startup:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                await bootstrap.create_initial_user(
                    db_settings.db_uri,
                    settings.bootstrap_user_username,
                    settings.bootstrap_user_password,
                    settings.bootstrap_user_purpose,
                    bootstrap.AUTHENTICATION_METHOD,
                    settings.bootstrap_user_policy_slug,
                    session=session,
                )

    # if settings.get("service_discovery", {}).get("enabled", False): #Example of service discovery
    #   # Example of service registration.  Adapt to your needs.
    #   registerer = NotifyingRegisterer(...) # Create your registerer
    #   registerer.register()
    #   # Store the registerer *somewhere* so you can deregister it later.
    #   # A good place is in app.state:
    #   app.state.registerer = registerer

    yield  # This is where the application runs

    # Shutdown logic
    logger.info("Shutting down...")
    # if hasattr(app.state, "registerer"):
    #     await app.state.registerer.deregister()
    await async_engine.dispose()
    logger.info("Shutdown complete.")


app = FastAPI(lifespan=lifespan)

# Added for status check
status_aggregator = StatusAggregator()
app.dependency_overrides[StatusAggregator] = lambda: status_aggregator

# Include routers from other modules
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tenants_router)
app.include_router(groups_router)
app.include_router(policies_router)
app.include_router(core_router)
app.include_router(google.router)  # External auth
app.include_router(microsoft.router)  # External auth
app.include_router(mobile.router)  # External auth


@app.get("/")
async def root():
    return {"message": "Accent Auth Service is running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9497)
