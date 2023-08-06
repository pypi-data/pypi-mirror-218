from enum import Enum as _Enum
from simpleworkspace.types import iunit
from .iunit import IUnit

class TimeEnum(_Enum):
    '''relative to seconds'''
    Second = 1
    Minute = 60
    Hour = Minute * 60
    Day = 24 * Hour


class TimeUnit(IUnit):
    def __init__(self, amount: float, unit: TimeEnum):
        self.amount = amount
        self.unit = unit

    def To(self, desiredUnit: TimeEnum):
        return self._converter(self.amount, self.unit, desiredUnit)

    @classmethod
    def _converter(cls, amount: float, unit: TimeEnum, desiredUnit: TimeEnum) -> 'TimeUnit':
        totalSeconds = amount * unit.value # since TimeEnum is relative to seconds, anything multiplied by it will result in seconds
        convertedAmount = totalSeconds / desiredUnit.value
        return TimeUnit(convertedAmount, desiredUnit)

    def __eq__(self, other) -> bool:
        if not isinstance(other, TimeUnit):
            return NotImplemented
        return self.To(TimeEnum.Second).amount == other.To(TimeEnum.Second).amount
    
    def __str__(self) -> str:
        return f'{round(self.amount, 2)} {self.unit.name}'
    
    #region archimetric overloading
    def __iadd__(self, other:'TimeUnit|float') -> 'TimeUnit':
        if isinstance(other, TimeUnit):
            self.amount += other.To(self.unit).amount
        else:
            self.amount += other
        return self

    def __imul__(self, other:'TimeUnit|float') -> 'TimeUnit':
        if isinstance(other, TimeUnit):
            self.amount *= other.To(self.unit).amount
        else:
            self.amount *= other
        return self

    def __itruediv__(self, other:'TimeUnit|float') -> 'TimeUnit':
        if isinstance(other, TimeUnit):
            self.amount /= other.To(self.unit).amount
        else:
            self.amount /= other
        return self

    def __isub__(self, other:'TimeUnit|float') -> 'TimeUnit':
        if isinstance(other, TimeUnit):
            self.amount -= other.To(self.unit).amount
        else:
            self.amount -= other
        return self
    #endregion archimetric overloading