from typing import Callable


class TriggerFunc:
    def __init__(self, func, do_once: bool = False,  *f_args, **f_kwargs):
        self.func: Callable = func
        self.f_args = f_args
        self.f_kwargs = f_kwargs
        self.do_once: bool = do_once
