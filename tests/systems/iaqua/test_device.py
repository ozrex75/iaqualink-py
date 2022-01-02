from __future__ import annotations

import copy
import unittest
from unittest.mock import AsyncMock, MagicMock

import pytest

from iaqualink.exception import AqualinkInvalidParameterException
from iaqualink.systems.iaqua.device import (
    IAQUA_TEMP_CELSIUS_HIGH,
    IAQUA_TEMP_CELSIUS_LOW,
    IAQUA_TEMP_FAHRENHEIT_HIGH,
    IAQUA_TEMP_FAHRENHEIT_LOW,
    IaquaColorLight,
    IaquaDevice,
    IaquaDimmableLight,
    IaquaHeater,
    IaquaLightToggle,
    IaquaSensor,
    IaquaThermostat,
)

from ...base_test_device import TestBaseThermostat
from ...common import async_noop


class TestIaquaDevice(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        system = MagicMock()
        data = {"name": "Test Device"}
        self.obj = IaquaDevice(system, data)

    def test_equal(self) -> None:
        assert self.obj == self.obj

    def test_not_equal(self) -> None:
        obj2 = copy.deepcopy(self.obj)
        obj2.data["name"] = "Test Device 2"
        assert self.obj != obj2

    def test_not_equal_different_type(self) -> None:
        assert (self.obj == {}) is False


class TestIaquaSensor(unittest.IsolatedAsyncioTestCase):
    pass


class TestIaquaToggle(unittest.IsolatedAsyncioTestCase):
    pass


class TestIaquaPump(unittest.IsolatedAsyncioTestCase):
    pass


class TestIaquaHeater(unittest.IsolatedAsyncioTestCase):
    pass


class TestIaquaAuxToggle(unittest.IsolatedAsyncioTestCase):
    pass


class TestIaquaLightToggle(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        system = MagicMock()
        system.set_aux = async_noop
        data = {"name": "Test Pool Light", "state": "0", "aux": "1"}
        self.obj = IaquaLightToggle(system, data)

    async def test_turn_off_noop(self) -> None:
        self.obj.system.set_aux.reset_mock()
        self.obj.data["state"] = "0"
        await self.obj.turn_off()
        self.obj.system.set_aux.assert_not_called()

    async def test_turn_off(self) -> None:
        self.obj.system.set_aux.reset_mock()
        self.obj.data["state"] = "1"
        await self.obj.turn_off()
        self.obj.system.set_aux.assert_called_once()

    async def test_turn_on(self) -> None:
        self.obj.system.set_aux.reset_mock()
        self.obj.data["state"] = "0"
        await self.obj.turn_on()
        self.obj.system.set_aux.assert_called_once()

    async def test_turn_on_noop(self) -> None:
        self.obj.system.set_aux.reset_mock()
        self.obj.data["state"] = "1"
        await self.obj.turn_on()
        self.obj.system.set_aux.assert_not_called()

    async def test_no_brightness(self) -> None:
        assert self.obj.brightness is None

    async def test_no_effect(self) -> None:
        assert self.obj.effect is None


class TestIaquaDimmableLight(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        system = MagicMock()
        system.set_light = async_noop
        data = {"name": "aux_1", "state": "0", "aux": "1", "subtype": "0"}
        self.obj = IaquaDimmableLight(system, data)

    def test_supports_brightness(self) -> None:
        assert self.obj.supports_brightness is True

    def test_supports_effect(self) -> None:
        assert self.obj.supports_effect is False

    def test_is_on_false(self) -> None:
        assert self.obj.is_on is False

    def test_is_on_true(self) -> None:
        self.obj.data["state"] = "1"
        self.obj.data["subtype"] = "50"
        assert self.obj.is_on is True

    async def test_turn_on(self) -> None:
        self.obj.system.set_light.reset_mock()
        await self.obj.turn_on()
        data = {"aux": "1", "light": "100"}
        self.obj.system.set_light.assert_called_once_with(data)

    async def test_turn_on_noop(self) -> None:
        self.obj.system.set_light.reset_mock()
        self.obj.data["state"] = "1"
        self.obj.data["subtype"] = "100"
        await self.obj.turn_on()
        self.obj.system.set_light.assert_not_called()

    async def test_turn_off(self) -> None:
        self.obj.system.set_light.reset_mock()
        self.obj.data["state"] = "1"
        self.obj.data["subtype"] = "100"
        await self.obj.turn_off()
        data = {"aux": "1", "light": "0"}
        self.obj.system.set_light.assert_called_once_with(data)

    async def test_turn_off_noop(self) -> None:
        self.obj.system.set_light.reset_mock()
        await self.obj.turn_off()
        self.obj.system.set_light.assert_not_called()

    async def test_bad_brightness(self) -> None:
        self.obj.system.set_light.reset_mock()
        with pytest.raises(Exception):
            await self.obj.set_brightness(89)

    async def test_set_brightness(self) -> None:
        self.obj.system.set_light.reset_mock()
        await self.obj.set_brightness(75)
        data = {"aux": "1", "light": "75"}
        self.obj.system.set_light.assert_called_once_with(data)


class TestIaquaColorLight(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        system = MagicMock()
        system.set_light = async_noop
        data = {
            "name": "aux_1",
            "aux": "1",
            "state": "0",
            "type": "2",
            "subtype": "5",
        }
        self.obj = IaquaColorLight(system, data)

    def test_supports_brightness(self) -> None:
        assert self.obj.supports_brightness is False

    def test_supports_effect(self) -> None:
        assert self.obj.supports_effect is True

    def test_is_on_false(self) -> None:
        assert self.obj.is_on is False

    def test_is_on_true(self) -> None:
        self.obj.data["state"] = "2"
        assert self.obj.is_on is True

    async def test_turn_off_noop(self) -> None:
        self.obj.system.set_light.reset_mock()
        await self.obj.turn_off()
        self.obj.system.set_light.assert_not_called()

    async def test_turn_off(self) -> None:
        self.obj.system.set_light.reset_mock()
        self.obj.data["state"] = "1"
        await self.obj.turn_off()
        data = {"aux": "1", "light": "0", "subtype": "5"}
        self.obj.system.set_light.assert_called_once_with(data)

    async def test_turn_on(self) -> None:
        self.obj.system.set_light.reset_mock()
        await self.obj.turn_on()
        data = {"aux": "1", "light": "1", "subtype": "5"}
        self.obj.system.set_light.assert_called_once_with(data)

    async def test_turn_on_noop(self) -> None:
        self.obj.system.set_light.reset_mock()
        self.obj.data["state"] = "1"
        await self.obj.turn_on()
        self.obj.system.set_light.assert_not_called()

    async def test_set_effect(self) -> None:
        self.obj.system.set_light.reset_mock()
        data = {"aux": "1", "light": "2", "subtype": "5"}
        await self.obj.set_effect_by_id(2)
        self.obj.system.set_light.assert_called_once_with(data)

    async def test_set_effect_invalid(self) -> None:
        self.obj.system.set_light.reset_mock()
        with pytest.raises(Exception):
            await self.obj.set_effect_by_name("bad effect name")


class TestIaquaThermostat(TestBaseThermostat):
    def setUp(self) -> None:
        self.system = system = AsyncMock()
        self.system.temp_unit = "F"
        pool_set_point = {"name": "pool_set_point", "state": "86"}
        self.pool_set_point = IaquaThermostat(system, pool_set_point)
        pool_temp = {"name": "pool_temp", "state": "65"}
        self.pool_temp = IaquaSensor(system, pool_temp)
        pool_heater = {"name": "pool_heater", "state": "0"}
        self.pool_heater = IaquaHeater(system, pool_heater)
        spa_set_point = {"name": "spa_set_point", "state": "102"}
        self.spa_set_point = IaquaDevice.from_data(system, spa_set_point)
        devices = [
            self.pool_set_point,
            self.pool_heater,
            self.pool_temp,
        ]
        system.devices = {x.name: x for x in devices}

        self.sut = self.pool_set_point
        self.sut_class = IaquaThermostat

    def test_property_is_on(self):
        assert self.pool_set_point.is_on is False

    def test_property_label(self):
        assert self.sut.label == "Pool Set Point"

    def test_property_name(self):
        assert self.sut.name == "pool_set_point"

    def test_property_state(self):
        assert self.sut.state == "86"

    def test_property_unit_f(self):
        self.sut.system.temp_unit = "F"
        super().test_property_unit_f()

    def test_property_unit_c(self):
        self.sut.system.temp_unit = "C"
        super().test_property_unit_c()

    def test_property_min_temperature_f(self):
        self.sut.system.temp_unit = "F"
        assert self.sut.min_temperature == IAQUA_TEMP_FAHRENHEIT_LOW

    def test_property_min_temperature_c(self):
        self.sut.system.temp_unit = "C"
        assert self.sut.min_temperature == IAQUA_TEMP_CELSIUS_LOW

    def test_property_max_temperature_f(self):
        self.sut.system.temp_unit = "F"
        assert self.sut.max_temperature == IAQUA_TEMP_FAHRENHEIT_HIGH

    def test_property_max_temperature_c(self):
        self.sut.system.temp_unit = "C"
        assert self.sut.max_temperature == IAQUA_TEMP_CELSIUS_HIGH

    def test_property_current_temperature(self):
        assert self.sut.current_temperature == "65"

    def test_property_target_temperature(self):
        assert self.sut.target_temperature == "86"

    async def test_turn_on(self):
        self.pool_heater.data["state"] = "0"
        await super().test_turn_on()

    async def test_turn_on_noop(self):
        self.pool_heater.data["state"] = "1"
        await super().test_turn_on_noop()

    async def test_turn_off(self):
        self.pool_heater.data["state"] = "1"
        await super().test_turn_off()

    async def test_turn_off_noop(self):
        self.pool_heater.data["state"] = "0"
        await super().test_turn_off_noop()

    async def test_toggle(self):
        await super().test_toggle()
        self.sut.system.set_heater.assert_called_with("set_pool_heater")

    async def test_set_temperature_86f(self):
        await super().test_set_temperature_86f()
        self.sut.system.set_temps.assert_called_with({"temp1": "86"})

    async def test_set_temperature_30c(self):
        await super().test_set_temperature_30c()
        self.sut.system.set_temps.assert_called_with({"temp1": "30"})

    async def test_set_temperature_invalid_400f(self):
        with pytest.raises(AqualinkInvalidParameterException):
            await super().test_set_temperature_invalid_400f()

    async def test_set_temperature_invalid_204c(self):
        with pytest.raises(AqualinkInvalidParameterException):
            await super().test_set_temperature_invalid_204c()

    async def test_temp_name_spa_present(self):
        self.sut.system.devices["spa_set_point"] = self.spa_set_point
        assert self.spa_set_point._temperature == "temp1"
        assert self.pool_set_point._temperature == "temp2"

    async def test_temp_name_no_spa(self):
        assert self.pool_set_point._temperature == "temp1"
