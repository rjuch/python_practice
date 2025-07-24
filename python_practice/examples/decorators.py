import time

# Decorators 
def log_decorator(func):
    def wrapper():
        print(f'Before function call: {func.__name__}')
        func()
        print(f'After function call: {func.__name__}')

    return wrapper

def timeit_decorator(func):
    def wrapper(*args):
        start_time = time.time()
        result = func(*args)
        print(f'function {func.__name__} executed in : {time.time() - start_time} seconds')
        return result
    return wrapper

def param_decorator(func):
    def wrapper(*args, **kwargs):
        print(f'{func.__name__} executed with args: {args}, kwargs: {kwargs}')
        result = func(*args, **kwargs)
        print(f'{func.__name__} finished execution')
        return result

    return wrapper

@log_decorator
def say_hello():
    print('Hello!')

@param_decorator
def print_params(a, b, c, **kwargs):
    # print(f'Parameters received: a={a}, b={b}, c={c}, kwargs={kwargs}')
    print(f'Positional args Received: {a}, {b}, {c}')
    print(f'Keyword args Received: {kwargs}')
    print(type(kwargs))
    return 'done'

@timeit_decorator
def looper(n=100000):
    for i in range(n):
        pass
    return 1

def print_message(msg: str):
    print(msg)

if __name__ == "__main__":
    # # using no parameters
    # say_hello()

    # # using parameterized decorator
    # output = print_params(1, 2, 3, generic='testing', another='example')
    # print('function output:', output)

    # using timeit decorator
    looper(10000000)
