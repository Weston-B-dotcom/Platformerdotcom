from typing import Callable

def FunctionA() -> int:
    print("A")
    return 1

def FunctionB(func: Callable[[], int]) -> int:
    print("B")
    return func()

def FunctionC(value: int) -> Callable[[], int]:
    print("C")
    def InnerFunction() -> int:
        print("Inner")
        return value
    return InnerFunction


print(FunctionB(FunctionC(234)))