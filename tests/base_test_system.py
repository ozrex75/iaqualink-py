from .base import TestBase


class TestBaseSystem(TestBase):
    def setUp(self):
        super().setUp()

    def test_from_data(self) -> None:
        if sut_class := getattr(self, "sut_class", None):
            assert isinstance(self.sut, sut_class)
