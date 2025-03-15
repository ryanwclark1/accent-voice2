# integration_tests/suite/helpers/base.py
# ... other imports ...
from accent_chatd.core.bus import (
    BusConsumer,
    BusPublisher,
    get_bus_consumer,
    get_bus_publisher,
)
# ...


class _BaseAssetLaunchingTestCase(AssetLaunchingTestCase):
    # ... other methods ...
    @classmethod
    def make_bus(cls):
        try:
            port = cls.service_port(5672, "rabbitmq")
        except (NoSuchService, NoSuchPort):
            return WrongClient("rabbitmq")

        # Directly instantiate, no need to inject yet.
        return BusPublisher(f"amqp://guest:guest@127.0.0.1:{port}", "accent-headers")

    @classmethod
    def make_bus_consumer(cls):
        try:
            port = cls.service_port(5672, "rabbitmq")
        except (NoSuchService, NoSuchPort):
            return WrongClient("rabbitmq")

        # Directly instantiate, no need to inject yet.
        return BusConsumer(
            f"amqp://guest:guest@127.0.0.1:{port}", "accent-headers", "test-queue"
        )

    @classmethod
    def reset_clients(cls):
        super().reset_clients()
        cls.bus = cls.asset_cls.make_bus()  # publisher
        cls.bus_consumer = cls.asset_cls.make_bus_consumer()


# Add the classes
class APIIntegrationTest(_BaseIntegrationTest):
    asset_cls = APIAssetLaunchingTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reset_clients()  # Reset on class setup


class InitIntegrationTest(_BaseIntegrationTest):
    asset_cls = InitAssetLaunchingTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reset_clients()  # Reset on class setup


class DBIntegrationTest(_BaseIntegrationTest):
    asset_cls = DBAssetLaunchingTestCase
    # Dont need the reset here.
