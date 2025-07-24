'''
Interfaces are a way to define what a class should do, without specifying how.
'''

from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self):
        raise NotImplementedError

class TSMOM_Strategy(BaseStrategy):
    def custom_func(self):
        print('Custom Func')
        return 1
    
    def generate_signals(self):
        print('generate signals')

strat = TSMOM_Strategy()
strat.custom_func()