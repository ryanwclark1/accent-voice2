# Copyright 2023 Accent Communications


from unittest import TestCase
from unittest.mock import Mock, patch
from unittest.mock import sentinel as s

from hamcrest import assert_that, calling, equal_to, none, raises

from ..handler import (
    CachedHandlerFactoryDecorator,
    FrontendHandlerFactory,
    MultiHandlerFactory,
    NoSuchHandler,
    NullHandlerFactory,
    PluginHandlerFactory,
)


class TestCachedHandlerFactoryDecorator(TestCase):
    def test_that_two_gets_give_the_same_result(self):
        decorated = Mock()
        decorated.get.side_effect = [1, 2]

        factory = CachedHandlerFactoryDecorator(decorated)

        result_1 = factory.get(s.resource, s.filename)
        result_2 = factory.get(s.resource, s.filename)

        assert_that(result_1, equal_to(result_2))
        decorated.get.assert_called_once_with(s.resource, s.filename)

    def test_given_decorated_raises_when_get_then_raise(self):
        decorated = Mock()
        decorated.get.side_effect = NoSuchHandler

        factory = CachedHandlerFactoryDecorator(decorated)

        assert_that(
            calling(factory.get).with_args(s.resource, s.filename),
            raises(NoSuchHandler),
        )


class TestMultiHandlerFactory(TestCase):
    def test_given_no_fail_when_get_then_first_result_is_returned(self):
        factory1 = Mock()
        factory1.get.return_value = 1
        factory2 = Mock()
        factory2.get.return_value = 2
        multi_factory = MultiHandlerFactory([factory1, factory2])

        result = multi_factory.get(s.resource, s.filename)

        assert_that(result, equal_to(1))

    def test_given_first_factory_fails_when_get_then_second_result_is_returned(self):
        factory1 = Mock()
        factory1.get.side_effect = NoSuchHandler()
        factory2 = Mock()
        factory2.get.return_value = 2
        multi_factory = MultiHandlerFactory([factory1, factory2])

        result = multi_factory.get(s.resource, s.filename)

        assert_that(result, equal_to(2))

    def test_given_all_factories_fail_when_get_then_raise(self):
        factory1 = Mock()
        factory1.get.side_effect = NoSuchHandler()
        factory2 = Mock()
        factory2.get.side_effect = NoSuchHandler()
        multi_factory = MultiHandlerFactory([factory1, factory2])

        assert_that(
            calling(multi_factory.get).with_args(s.resource, s.filename),
            raises(NoSuchHandler),
        )


class TestPluginHandlerFactory(TestCase):
    @patch('accent_confgend.handler.driver')
    def test_given_no_driver_found_when_get_then_raise(self, stevedore_driver):
        stevedore_driver.DriverManager.side_effect = RuntimeError
        resource = 'resource'
        filename = 'filename'
        config = {'plugins': {'resource.filename': s.driver_name}}
        factory = PluginHandlerFactory(config, s.dependencies)

        assert_that(
            calling(factory.get).with_args(resource, filename), raises(NoSuchHandler)
        )

    def test_given_no_config_when_get_then_raise(self):
        resource = 'resource'
        filename = 'filename'
        config = {'plugins': {}}
        factory = PluginHandlerFactory(config, s.dependencies)

        assert_that(
            calling(factory.get).with_args(resource, filename), raises(NoSuchHandler)
        )

    @patch('accent_confgend.handler.driver')
    def test_given_driver_found_when_get_then_return_handler(self, stevedore_driver):
        handler = stevedore_driver.DriverManager.return_value.driver.generate = Mock()
        resource = 'resource'
        filename = 'filename'
        config = {'plugins': {'resource.filename': s.driver_name}}
        factory = PluginHandlerFactory(config, s.dependencies)

        result = factory.get(resource, filename)

        assert_that(result, equal_to(handler))


class TestFrontendHandlerFactory(TestCase):
    def test_given_no_frontend_found_when_get_then_raise(self):
        resource = 'resource'
        filename = 'filename'
        frontends = {}
        factory = FrontendHandlerFactory(frontends)

        assert_that(
            calling(factory.get).with_args(resource, filename), raises(NoSuchHandler)
        )

    def test_given_frontend_has_no_callback_when_get_then_raise(self):
        resource = 'resource'
        filename = 'filename'
        frontend = Mock()
        del frontend.filename
        frontends = {'resource': frontend}
        factory = FrontendHandlerFactory(frontends)

        assert_that(
            calling(factory.get).with_args(resource, filename), raises(NoSuchHandler)
        )

    def test_given_frontend_found_when_get_then_return_frontend(self):
        resource = 'resource'
        filename = 'filename'
        frontend = Mock()
        frontends = {'resource': frontend}
        factory = FrontendHandlerFactory(frontends)

        result = factory.get(resource, filename)

        assert_that(result, equal_to(frontend.filename))


class TestNullHandlerFactory(TestCase):
    def test_when_get_then_return_null_handler(self):
        factory = NullHandlerFactory()

        result = factory.get(s.resource, s.filename)

        assert_that(result(), none())
