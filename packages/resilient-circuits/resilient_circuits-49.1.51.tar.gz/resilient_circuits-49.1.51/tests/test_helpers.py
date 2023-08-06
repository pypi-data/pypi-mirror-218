#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) Copyright IBM Corp. 2010, 2022. All Rights Reserved.

import time

import pkg_resources
import pytest
from resilient_circuits import ResilientComponent, constants, function, helpers
from resilient_circuits.stomp_events import HeartbeatTimeout

from tests import (AppFunctionMockComponent, MockInboundAppComponent,
                   mock_constants)
from tests.shared_mock_data import mock_paths

resilient_mock = mock_constants.RESILIENT_MOCK
config_data = mock_constants.CONFIG_DATA


def test_get_fn_names():

    class FunctionComponentA(ResilientComponent):
        @function("mock_fn")
        def _mock_function(self):
            return True

    assert helpers.get_fn_names(FunctionComponentA) == ["mock_fn"]

    class FunctionComponentB(ResilientComponent):
        @function("mock_fn_2a")
        def _other_name_a(self):
            return True

        @function("mock_fn_2b")
        def _other_name_b(self):
            return True

    assert helpers.get_fn_names(FunctionComponentB) == ["mock_fn_2a", "mock_fn_2b"]

    with pytest.raises(ValueError, match=r"Usage: @function\(api_name\)"):
        class FunctionComponentC(ResilientComponent):
            @function("mock_fn_3a", "mock_fn_3b")
            def _other_name_a(self):
                return True


def test_get_handlers_inbound_handler():
    mock_cmp_class = MockInboundAppComponent(mock_constants.MOCK_OPTS)
    mock_handlers = helpers.get_handlers(mock_cmp_class, "inbound_handler")
    assert isinstance(mock_handlers, list)
    assert mock_handlers[0][0] == "_inbound_app_mock_one"
    assert mock_handlers[0][1].channel == "{0}.{1}".format(constants.INBOUND_MSG_DEST_PREFIX, "mock_inbound_q")


def test_check_exists():
    assert helpers.check_exists("mock", {"mock": "data"}) == "data"
    assert helpers.check_exists("mock", {}) is False
    assert helpers.check_exists("mock", None) is False
    with pytest.raises(AssertionError):
        helpers.check_exists("mock", "abc")


def test_get_configs(fx_clear_cmd_line_args):
    configs = helpers.get_configs(path_config_file=mock_paths.MOCK_APP_CONFIG)
    assert isinstance(configs, dict)
    assert configs.get("host") == "resilient"


def test_validate_configs():
    mock_configs = {
        "mock_config_1": "unicode å æ ç è é unicode",
        "mock_config_2": 11,
        "mock_config_3": "<mock_config_3_here>",
        "mock_config_4": ""
    }

    mock_required_config = {
        "required": True
    }

    mock_config_2 = {
        "required": True,
        "valid_condition": lambda x: True if x >= 1 and x <= 10 else False,
        "invalid_msg": "mock_config_2 must be in range"
    }

    mock_config_3 = {
        "required": True,
        "placeholder_value": "<mock_config_3_here>"
    }

    # test unicode
    helpers.validate_configs(mock_configs, {"mock_config_1": mock_required_config})

    # test required
    with pytest.raises(ValueError, match=r"'mock_config_5' is mandatory and is not set in the config file"):
        helpers.validate_configs(mock_configs, {"mock_config_5": mock_required_config})

    # test empty string
    with pytest.raises(ValueError, match=r"'mock_config_4' is mandatory and is not set in the config file"):
        helpers.validate_configs(mock_configs, {"mock_config_4": mock_required_config})

    # test placeholder_value
    with pytest.raises(ValueError, match=r"'mock_config_3' is mandatory and still has its placeholder value of '<mock_config_3_here>' in the config file"):
        helpers.validate_configs(mock_configs, {"mock_config_3": mock_config_3})

    # test valid_condition fails
    with pytest.raises(ValueError, match=r"mock_config_2 must be in range"):
        helpers.validate_configs(mock_configs, {"mock_config_2": mock_config_2})

    # test valid_condition passes
    mock_configs["mock_config_2"] = 5
    helpers.validate_configs(mock_configs, {"mock_config_2": mock_config_2})


def test_get_packages():

    pkgs = helpers.get_packages(pkg_resources.working_set)

    for pkg in pkgs:
        assert len(pkg) == 2
        assert isinstance(pkg[0], str)
        assert isinstance(pkg[1], str)


def test_get_packages_not_a_working_set_obj():

    invalid_ws = "this is not a working set"

    pkgs = helpers.get_packages(invalid_ws)

    assert pkgs == invalid_ws


def test_env_str():

    env_str = helpers.get_env_str(pkg_resources.working_set)

    assert "Environment" in env_str
    assert "Python Version" in env_str
    assert "Installed packages" in env_str
    assert "\n\tresilient-circuits" in env_str


def test_env_str_with_env_var(fx_add_proxy_env_var):

    env_str = helpers.get_env_str(pkg_resources.working_set)

    assert "Environment" in env_str
    assert "Python Version" in env_str
    assert "Installed packages" in env_str
    assert "\n\tresilient-circuits" in env_str
    assert "Connecting through proxy: 'https://192.168.0.5:3128'" in env_str


def test_get_queue(caplog):
    assert helpers.get_queue("/queue/actions.201.fn_main_mock_integration") == ("actions", "201", "fn_main_mock_integration")
    assert helpers.get_queue("/queue/inbound_destination.111.inbound_app_mock") == ("inbound_destination", "111", "inbound_app_mock")
    assert helpers.get_queue("inbound_destination.111.inbound_app_mock") == ("inbound_destination", "111", "inbound_app_mock")
    assert helpers.get_queue("111.inbound_app_mock") is None
    assert helpers.get_queue("") is None
    assert helpers.get_queue(None) is None
    assert "Could not get queue name" in caplog.text


class TestIsASelftestActionsComponent:
    @pytest.mark.parametrize("circuits_app", [{"IS_SELFTEST": True}], indirect=True)
    def test_is_this_a_selftest_action_component(self, circuits_app):
        assert helpers.is_this_a_selftest(circuits_app.app.action_component) is True


class TestIsNotASelftestActionsComponent:
    @pytest.mark.parametrize("circuits_app", [{"IS_SELFTEST": False}], indirect=True)
    def test_is_this_a_selftest_action_component(self, circuits_app):
        assert helpers.is_this_a_selftest(circuits_app.app.action_component) is False


class TestIsASelftestResilientComponent:
    @pytest.mark.parametrize("circuits_app", [{"IS_SELFTEST": True}], indirect=True)
    def test_is_this_a_selftest_base_component(self, circuits_app):
        c = AppFunctionMockComponent(opts=mock_constants.MOCK_OPTS).register(circuits_app.app)
        assert helpers.is_this_a_selftest(c) is True


class TestIsNotASelftestResilientComponent:
    @pytest.mark.parametrize("circuits_app", [{"IS_SELFTEST": False}], indirect=True)
    def test_is_this_a_selftest_base_component(self, circuits_app):
        c = AppFunctionMockComponent(opts=mock_constants.MOCK_OPTS).register(circuits_app.app)
        assert helpers.is_this_a_selftest(c) is False


def test_should_timeout():
    start_time = time.time()
    time.sleep(2)
    assert helpers.should_timeout(start_time, 1) is True


def test_should_not_timeout():
    start_time = time.time()
    assert helpers.should_timeout(start_time, 10) is False


def test_get_usr():
    assert helpers.get_user({"api_key_id": "abc", "email": None}) == "abc"
    assert helpers.get_user({"api_key_id": None, "email": "def"}) == "def"
    assert helpers.get_user({"api_key_id": "", "email": ""}) is None
    assert helpers.get_user({"api_key_id": None, "email": None}) is None


def test_filter_heartbeat_timeout_events():
    hb1 = HeartbeatTimeout(10)
    hb2 = HeartbeatTimeout(20)
    hb3 = HeartbeatTimeout(30)
    hb4 = HeartbeatTimeout()

    heartbeat_timeouts = [hb2, hb4, hb3, hb1]

    filtered_hbs = helpers.filter_heartbeat_timeout_events(heartbeat_timeouts)

    for hb in filtered_hbs:
        assert hb.ts != -1

    assert filtered_hbs[0].ts == 10
    assert filtered_hbs[1].ts == 20
    assert filtered_hbs[-1].ts == 30


def test_filter_heartbeat_timeout_events_empty():
    assert helpers.filter_heartbeat_timeout_events([]) == []
