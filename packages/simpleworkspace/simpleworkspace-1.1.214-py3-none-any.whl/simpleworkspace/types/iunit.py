from abc import ABC, abstractclassmethod, abstractmethod
class IUnit(ABC):
    @abstractmethod
    def To(self, desiredUnit) -> 'IUnit':
        '''converts current instance to desired unit'''
    
    @abstractclassmethod
    def _converter(cls, amount, unit, desiredUnit) -> 'IUnit':
        '''Base converter is responsible for the conversion between units for the unit implementation'''

    @abstractmethod
    def __eq__(self, other) -> bool:
        return self.__eq__(other)
        '''comparator for this type of unit implementation'''

    @abstractmethod
    def __str__(self) -> str:
        return self.__str__()
        '''dictates how the unit is represented in string format'''
    
    #region archimetric overloading
    @abstractmethod
    def __iadd__(self, other) -> 'IUnit':
        '''inplace addition of another unit type or directly a value(interpretted as current unit)'''
    @abstractmethod
    def __imul__(self, other) -> 'IUnit':
        '''inplace multiplication of another unit type or directly a value(interpretted as current unit)'''
    @abstractmethod
    def __itruediv__(self, other) -> 'IUnit':
        '''inplace division of another unit type or directly a value(interpretted as current unit)'''
    @abstractmethod
    def __isub__(self, other) -> 'IUnit':
        '''inplace subtraction of another unit type or directly a value(interpretted as current unit)'''
    #endregion archimetric overloading