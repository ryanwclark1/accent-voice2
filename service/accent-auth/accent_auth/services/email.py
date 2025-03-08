# accent_auth/services/email.py

import logging
import smtplib
import time
from collections import namedtuple
from email import utils as email_utils
from email.mime.text import MIMEText
from functools import partial  # Import functools.partial
import asyncio
from accent_auth.db import DAO
from accent_auth.services.token import TokenService  # Import TokenService
from accent_auth.utils.template import TemplateFormatter  # Import TemplateFormatter
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

EmailDestination = namedtuple("EmailDestination", ["name", "address"])

# NOTE: default socket timeout is None on linux
# Our client http client is 10s, since sending mail is currently synchronous
# we have to be sure we return before the 10s, so we set the SMTP timeout.
SMTP_TIMEOUT = 4


class EmailService:  # No longer inherits from BaseService
    def __init__(self, dao: DAO, config: dict, template_formatter: TemplateFormatter):
        self._dao = dao
        self._formatter = template_formatter
        self._smtp_host = config["smtp"]["hostname"]
        self._smtp_port = config["smtp"]["port"]
        self._confirmation_token_expiration = config["email_confirmation_expiration"]
        self._reset_token_expiration = config["password_reset_expiration"]
        self._confirmation_from = EmailDestination(
            config["email_confirmation_from_name"],
            config["email_confirmation_from_address"],
        )
        self._password_reset_from = EmailDestination(
            config["password_reset_from_name"], config["password_reset_from_address"]
        )
        self._get_body = template_formatter.get_confirmation_email_get_body_template()

    async def confirm(self, email_uuid: str, db: AsyncSession) -> None:  # Added db
        """Confirms an email address."""
        await self._dao.email.confirm(email_uuid, session=db)

    async def send_confirmation_email(
        self,
        username: str,
        email_uuid: str,
        email_address: str,
        connection_params: dict,
        db: AsyncSession,
        token_service: TokenService,
    ) -> None:
        """Sends a confirmation email."""
        template_context = dict(connection_params)
        template_context.update(
            {
                "token": await token_service.new_token_internal(  # Use injected token_service
                    expiration=self._confirmation_token_expiration,
                    acl=[f"auth.emails.{email_uuid}.confirm.edit"],
                    db=db,
                ),
                "username": username,
                "email_uuid": email_uuid,
                "email_address": email_address,
            }
        )

        body = self._formatter.format_confirmation_email(template_context)
        subject = self._formatter.format_confirmation_subject(template_context)
        to = EmailDestination(username, email_address)
        await self._send_msg(
            to, self._confirmation_from, subject, body
        )  # Make send_msg async

    async def send_reset_email(
        self,
        user_uuid: str,
        username: str,
        email_address: str,
        connection_params: dict,
        db: AsyncSession,
        token_service: TokenService,
    ) -> None:
        """Sends a password reset email."""
        template_context = dict(connection_params)
        template_context.update(
            {
                "token": await token_service.new_token_internal(  # Use injected token_service
                    expiration=self._reset_token_expiration,
                    acl=[f"auth.users.password.reset.{user_uuid}.create"],
                    db=db,
                ),
                "username": username,
                "user_uuid": user_uuid,
                "email_address": email_address,
            }
        )

        body = self._formatter.format_password_reset_email(template_context)
        subject = self._formatter.format_password_reset_subject(template_context)
        to = EmailDestination(username, email_address)
        await self._send_msg(to, self._password_reset_from, subject, body)

    # pylint: disable=unused-argument
    async def _send_msg(
        self,
        to: EmailDestination,
        from_: EmailDestination,
        subject: str,
        body: str,
        db: AsyncSession = None,
    ) -> None:  # Made async
        """Sends an email message."""
        msg = MIMEText(body)
        msg["To"] = email_utils.formataddr(to)
        msg["From"] = email_utils.formataddr(from_)
        msg["Subject"] = subject

        # Corrected: run in a thread pool, since smtplib is blocking.
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(
            None, self._sendmail, from_.address, [to.address], msg.as_string()
        )

    def _sendmail(self, from_addr, to_addrs, msg):
        """Helper function to send email, for use with run_in_executor"""
        with smtplib.SMTP(
            self._smtp_host, self._smtp_port, timeout=SMTP_TIMEOUT
        ) as server:
            server.sendmail(from_addr, to_addrs, msg)

    # async def _new_email_confirmation_token(self, email_uuid: str) -> str: # Removed
    #     acl = f"auth.emails.{email_uuid}.confirm.edit"
    #     return await self._token_service.new_token_internal(self._confirmation_token_expiration, acl) #Removed

    # async def _new_email_reset_token(self, user_uuid: str) -> str: # Removed
    #     acl = f"auth.users.password.reset.{user_uuid}.create"
    #     return await self._token_service.new_token_internal(self._reset_token_expiration, acl) #Removed

    # async def _new_generic_token(self, expiration, *acl):#Removed
    #     t = time.time()
    #     token_payload = {
    #         'auth_id': 'accent-auth',
    #         'pbx_user_uuid': None,
    #         'accent_uuid': None,
    #         'expire_t': t + expiration,
    #         'issued_t': t,
    #         'acl': acl,
    #         'metadata': {'tenant_uuid': self.top_tenant_uuid}, # Use top_tenant method
    #         'user_agent': 'accent-auth-email-reset',
    #         'remote_addr': '127.0.0.1'
    #     }
    #     session_payload = {}
    #     token_uuid, session_uuid = self._dao.token.create(token_payload, session_payload)
    #     return token_uuid
