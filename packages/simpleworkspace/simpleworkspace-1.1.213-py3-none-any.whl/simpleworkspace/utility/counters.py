from typing import Callable
from time import time
from sys import stdout
from ..types import TimeEnum, TimeUnit


class ProgressBar:
    def __init__(self, iterable=None, total=None, style_length=20, style_fill='█'):
        if(total is None and iterable is not None):
            if hasattr(iterable, "__len__"):
                total = len(iterable)
        
        self.total = total
        self._iterable = iterable
        if(self._iterable is not None):
            self._iterator = iter(iterable)
        self._currentProgress = 0
        self._style_length = style_length
        self._style_fill = style_fill
        self._start_time = time()  # Track start time
        self._previous_time = self._start_time  # Track previous time for increment
        self._remaining_time = 0
        self._incrementsPerSeconds = 0
        
    def Increment(self, increment=1):
        self._currentProgress += increment

        # Calculate speed
        current_time = time()
        elapsed_time = current_time - self._previous_time
        self._incrementsPerSeconds = 0 if elapsed_time == 0 else increment / elapsed_time
        self._previous_time = current_time

        if(self.total is None):
            return
        # Calculate remaining time
        self._remaining_time = 0 if self._incrementsPerSeconds == 0 else (self.total - self._currentProgress) / self._incrementsPerSeconds

    def Print(self) -> str:
        elapsedTime = self._FormatTime(time() - self._start_time)
        if(self.total is None):
            stdout.write(f"\rProgress: {self._currentProgress}, elapsed={elapsedTime}")
            return
        
        filled_length = int(self._style_length * self._currentProgress / self.total)
        bar = self._style_fill * filled_length + '-' * (self._style_length - filled_length)
        percentage = round(self._currentProgress * 100 / self.total,1)
        speed = round(self._incrementsPerSeconds, 1)
        
        remainingTime = self._FormatTime(self._remaining_time)

        stdout.write(f"\rProgress: |{bar}| {percentage}% [elapsed={elapsedTime}|remaining={remainingTime}|speed={speed}/s|pcs={self._currentProgress}/{self.total}]")


    def _FormatTime(self, seconds: float):
        timeUnit = TimeUnit(seconds, TimeEnum.Second)
        timeParts = timeUnit.GetParts(minPart=TimeEnum.Second,maxPart=TimeEnum.Hour)
        for i in timeParts.keys():
            timeParts[i] = round(timeParts[i]) #remove all decimals
        return "{0:02d}:{1:02d}:{2:02d}".format( #00:00:00 format
            timeParts[TimeEnum.Hour], timeParts[TimeEnum.Minute], timeParts[TimeEnum.Second]
        )

    def __len__(self):
        return self.total
    
    def __iter__(self):
        return self

    def __next__(self):
        try:
            value = next(self._iterator)
            self.Increment()
            self.Print()
            return value
        except StopIteration:
            raise StopIteration