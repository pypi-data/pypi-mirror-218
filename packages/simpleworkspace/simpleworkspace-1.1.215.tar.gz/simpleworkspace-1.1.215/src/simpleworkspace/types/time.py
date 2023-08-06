from enum import Enum as _Enum
from simpleworkspace.types import iunit
from .iunit import IUnit

class TimeEnum(_Enum):
    '''relative to seconds'''
    MilliSecond = 0.001
    Second = 1
    Minute = 60
    Hour = Minute * 60
    Day = 24 * Hour


class TimeUnit(IUnit):
    def __init__(self, amount: float, unit: TimeEnum):
        self.amount = amount
        self.unit = unit

    def To(self, desiredUnit: TimeEnum):
        self.GetParts()
        return self._converter(self.amount, self.unit, desiredUnit)

    def GetParts(self, minPart:TimeEnum=None, maxPart:TimeEnum=None) -> dict[TimeEnum, float]:
        """Splits the current amount of relative time to individual parts

        :param minPart: The smallest part that should be included in the resulting dict. \
            if there are smaller parts available than minPart, they will be added as decimals to minPart 
        :param maxPart:  The highest part that should be included in the resulting dict. \
            If there are bigger parts available than maxPart, they will be added as the maxPart unit instead.
            This implies that when maxPart is specified to say hours, in the case \
            that there is 1 complete day, it will instead be added to hours as 24
        :return: dictionary of all time enums as keys, and their corresponding amount as values

        Example Usage:

        >>> TimeUnit(2.5, TimeEnum.Minute).GetParts()
        {
            TimeEnum.MilliSeconds: 0.0,
            TimeEnum.Seconds: 30.0,
            TimeEnum.Minute: 2.0,
            TimeEnum.Hour: 0.0,
            TimeEnum.Day: 0.0,
        }
        >>> TimeUnit(1, TimeEnum.Day).GetParts(maxPart=TimeEnum.Hour)
        {
            TimeEnum.MilliSeconds: 0.0,
            TimeEnum.Seconds: 0.0,
            TimeEnum.Minute: 0.0,
            TimeEnum.Hour: 24.0,
            TimeEnum.Day: 0.0,
        }
        >>> TimeUnit(3601.1, TimeEnum.Second).GetParts(minPart=TimeEnum.Second, maxPart=TimeEnum.Minute)
        {
            TimeEnum.MilliSeconds: 0.0,
            TimeEnum.Seconds: 1.1,
            TimeEnum.Minute: 60.0,
            TimeEnum.Hour: 0.0,
            TimeEnum.Day: 0.0,
        }

        """
        parts = {}
        remaining_seconds = self.amount * self.unit.value

        # sort by size and reverse it to get biggest parts to smallest
        reversed_time_enum = sorted(TimeEnum, key=lambda x: x.value, reverse=True)
        for time_unit in reversed_time_enum:
            if maxPart and (time_unit.value > maxPart.value):
                continue
            unit_seconds = time_unit.value
            if unit_seconds <= remaining_seconds:
                part = remaining_seconds // unit_seconds
                parts[time_unit] = part
                remaining_seconds %= unit_seconds
            else:
                parts[time_unit] = 0.0
            
            if minPart and (minPart == time_unit):
                break
        
        #gather the leftovers to the smallest part if any
        if(remaining_seconds > 0):
            #use last timeunit in loop since that will be the smallest part
            parts[time_unit] = parts[time_unit] + remaining_seconds / time_unit.value
        return parts

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