import time

def stopwatch(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        val = func(*args, **kwargs)
        time_delta = (time.time() - start_time)
        print(f'Function {func.__name__} execution time: {time_delta}')
        return val
    return wrapper