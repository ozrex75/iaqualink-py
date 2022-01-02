from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, PropertyMock, patch


class TestBaseDevice(unittest.IsolatedAsyncioTestCase):
    def __init_subclass__(cls) -> None:
        if cls.__name__.startswith("TestBase"):
            setattr(cls, "__test__", False)
        else:
            setattr(cls, "__test__", True)
        return super().__init_subclass__()

    def test_property_name(self):
        raise NotImplementedError

    def test_property_label(self):
        raise NotImplementedError

    def test_property_state(self):
        raise NotImplementedError


class TestBaseThermostat(TestBaseDevice):
    def test_from_data(self) -> None:
        if hasattr(self, "sut_class"):
            assert isinstance(self.sut, self.sut_class)

    def test_property_is_on(self):
        raise NotImplementedError

    def test_property_unit_f(self):
        assert self.sut.unit == "F"

    def test_property_unit_c(self):
        assert self.sut.unit == "C"

    def test_property_min_temperature_f(self):
        raise NotImplementedError

    def test_property_min_temperature_c(self):
        raise NotImplementedError

    def test_property_max_temperature_f(self):
        raise NotImplementedError

    def test_property_max_temperature_c(self):
        raise NotImplementedError

    def test_property_current_temperature(self):
        raise NotImplementedError

    def test_property_target_temperature(self):
        raise NotImplementedError

    async def test_turn_on(self):
        with patch.object(self.sut, "toggle", new_callable=AsyncMock):
            await self.sut.turn_on()
            self.sut.toggle.assert_called_once()

    async def test_turn_on_noop(self):
        with patch.object(self.sut, "toggle", new_callable=AsyncMock):
            await self.sut.turn_on()
            self.sut.toggle.assert_not_called()

    async def test_turn_off(self):
        with patch.object(self.sut, "toggle", new_callable=AsyncMock):
            await self.sut.turn_off()
            self.sut.toggle.assert_called_once()

    async def test_turn_off_noop(self):
        with patch.object(self.sut, "toggle", new_callable=AsyncMock):
            await self.sut.turn_off()
            self.sut.toggle.assert_not_called()

    async def test_toggle(self):
        await self.sut.toggle()

    async def test_set_temperature_86f(self):
        with patch.object(
            type(self.sut), "unit", new_callable=PropertyMock
        ) as mock_unit:
            mock_unit.return_value = "F"
            await self.sut.set_temperature(86)

    async def test_set_temperature_30c(self):
        with patch.object(
            type(self.sut), "unit", new_callable=PropertyMock
        ) as mock_unit:
            mock_unit.return_value = "C"
            await self.sut.set_temperature(30)

    async def test_set_temperature_invalid_400f(self):
        with patch.object(
            type(self.sut), "unit", new_callable=PropertyMock
        ) as mock_unit:
            mock_unit.return_value = "F"
            await self.sut.set_temperature(400)

    async def test_set_temperature_invalid_204c(self):
        with patch.object(
            type(self.sut), "unit", new_callable=PropertyMock
        ) as mock_unit:
            mock_unit.return_value = "C"
            await self.sut.set_temperature(204)
