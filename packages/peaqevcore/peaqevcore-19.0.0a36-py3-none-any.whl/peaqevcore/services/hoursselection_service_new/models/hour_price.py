from dataclasses import dataclass, field
from datetime import date, datetime, time
from .hour_type import HourType
from .list_type import ListType
from .datetime_model import DateTimeModel


@dataclass
class HourPrice:
    dt: datetime = datetime.now()
    quarter: int = 0
    price: float = 0.0
    permittance: float = field(init=False)
    passed: bool = False
    hour_type: HourType = HourType.Regular
    list_type: ListType = ListType.Hourly

    @property
    def hour(self) -> int:
        return self.dt.hour

    def __post_init__(self):
        assert 0 <= self.quarter <= 3, "Quarter must be between 0 and 3"
        assert 0 <= self.dt.hour <= 23, "Hour must be between 0 and 23"
        self.permittance = 1.0 if self.hour_type == HourType.BelowMin else 0.0

    @staticmethod
    def set_hour_type(max_price, min_price, price):
        if price > max_price:
            return HourType.AboveMax
        elif price < min_price:
            return HourType.BelowMin
        return HourType.Regular

    def set_passed(self, dt: DateTimeModel):
        if dt.hdate > self.dt.date():
            self.passed = True
        elif dt.hdate == self.dt.date():
            if self.hour < dt.hour:
                self.passed = True
            elif all(
                [
                    self.hour == dt.hour,
                    self.quarter < dt.quarter,
                    self.list_type == ListType.Quarterly,
                ]
            ):
                self.passed = True
        else:
            self.passed = False
