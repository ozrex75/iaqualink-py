from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

import pytest

from iaqualink.device import (
    AqualinkBinarySensor,
    AqualinkDevice,
    AqualinkLight,
    AqualinkThermostat,
    AqualinkToggle,
)

from .base_test_device import TestBaseThermostat


class TestAqualinkDevice(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        system = MagicMock()
        data = {"foo": "bar"}
        self.obj = AqualinkDevice(system, data)

    async def test_repr(self):
        assert repr(self.obj) == "AqualinkDevice(data={'foo': 'bar'})"

    async def test_label_not_implemented(self):
        with pytest.raises(NotImplementedError):
            self.obj.label

    async def test_state_not_implemented(self):
        with pytest.raises(NotImplementedError):
            self.obj.state

    async def test_name_not_implemented(self):
        with pytest.raises(NotImplementedError):
            self.obj.name

    async def test_manufacturer(self):
        with pytest.raises(NotImplementedError):
            self.obj.manufacturer

    async def test_model(self):
        with pytest.raises(NotImplementedError):
            self.obj.model


class TestAqualinkBinarySensor(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        system = MagicMock()
        data = {}
        self.obj = AqualinkBinarySensor(system, data)

    async def test_is_on_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await self.obj.is_on()


class TestAqualinkToggle(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        system = MagicMock()
        data = {}
        self.obj = AqualinkToggle(system, data)

    async def test_is_on_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await self.obj.is_on()

    async def test_toggle_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await self.obj.toggle()


class TestAqualinkLight(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        system = MagicMock()
        data = {}
        self.obj = AqualinkLight(system, data)

    async def test_is_on_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await self.obj.is_on()

    async def test_turn_on_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await self.obj.turn_on()

    async def test_turn_off_not_implemented(self):
        with pytest.raises(NotImplementedError):
            await self.obj.turn_off()

    async def test_set_brightness_noop(self):
        res = await self.obj.set_brightness(100)
        assert res is None

    async def test_set_brightness_not_implemented(self):
        with patch.object(
            type(self.obj),
            "supports_brightness",
            new_callable=PropertyMock(return_value=True),
        ):
            with pytest.raises(NotImplementedError):
                print(await self.obj.set_brightness(100))

    async def test_set_effect_by_name_noop(self):
        res = await self.obj.set_effect_by_name("blue")
        assert res is None

    async def test_set_effect_by_name_not_implemented(self):
        with patch.object(
            type(self.obj),
            "supports_effect",
            new_callable=PropertyMock(return_value=True),
        ):
            with pytest.raises(NotImplementedError):
                await self.obj.set_effect_by_name("blue")

    async def test_set_effect_by_id_noop(self):
        res = await self.obj.set_effect_by_id(0)
        assert res is None

    async def test_set_effect_by_id_not_implemented(self):
        with patch.object(
            type(self.obj),
            "supports_effect",
            new_callable=PropertyMock(return_value=True),
        ):
            with pytest.raises(NotImplementedError):
                await self.obj.set_effect_by_id(0)


class TestAqualinkThermostat(TestBaseThermostat):
    def setUp(self) -> None:
        system = AsyncMock()
        data = {}
        self.sut = AqualinkThermostat(system, data)
        self.sut_class = AqualinkThermostat

    async def test_property_is_on(self):
        with pytest.raises(NotImplementedError):
            self.sut.is_on

    async def test_property_name(self):
        with pytest.raises(NotImplementedError):
            self.sut.name

    async def test_property_label(self):
        with pytest.raises(NotImplementedError):
            self.sut.label

    async def test_property_state(self):
        with pytest.raises(NotImplementedError):
            self.sut.state

    async def test_property_unit_f(self):
        with pytest.raises(NotImplementedError):
            self.sut.unit

    async def test_property_unit_c(self):
        with pytest.raises(NotImplementedError):
            self.sut.unit

    async def test_property_min_temperature_f(self):
        with pytest.raises(NotImplementedError):
            self.sut.min_temperature

    async def test_property_min_temperature_c(self):
        with pytest.raises(NotImplementedError):
            self.sut.min_temperature

    async def test_property_max_temperature_f(self):
        with pytest.raises(NotImplementedError):
            self.sut.max_temperature

    async def test_property_max_temperature_c(self):
        with pytest.raises(NotImplementedError):
            self.sut.max_temperature

    async def test_property_current_temperature(self):
        with pytest.raises(NotImplementedError):
            self.sut.current_temperature

    async def test_property_target_temperature(self):
        with pytest.raises(NotImplementedError):
            self.sut.target_temperature

    async def test_turn_on(self):
        with pytest.raises(NotImplementedError):
            return await super().test_turn_on()

    async def test_turn_on_noop(self):
        with pytest.raises(NotImplementedError):
            await super().test_turn_on_noop()

    async def test_turn_off(self):
        with pytest.raises(NotImplementedError):
            await super().test_turn_off()

    async def test_turn_off_noop(self):
        with pytest.raises(NotImplementedError):
            await super().test_turn_off_noop()

    async def test_toggle(self):
        with pytest.raises(NotImplementedError):
            await super().test_toggle()

    async def test_set_temperature_86f(self):
        with pytest.raises(NotImplementedError):
            await super().test_set_temperature_86f()

    async def test_set_temperature_30c(self):
        with pytest.raises(NotImplementedError):
            await super().test_set_temperature_30c()

    async def test_set_temperature_invalid_400f(self):
        with pytest.raises(NotImplementedError):
            await super().test_set_temperature_invalid_400f()

    async def test_set_temperature_invalid_204c(self):
        with pytest.raises(NotImplementedError):
            await super().test_set_temperature_invalid_204c()
