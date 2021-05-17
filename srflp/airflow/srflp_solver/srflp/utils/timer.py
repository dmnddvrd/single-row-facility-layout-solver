import time

def stopwatch(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        val = func(*args, **kwargs)
        time_spent = (time.time() - start_time)
        print(f'Function {func.__name__} execution time: {time_spent}')
        return val
    return wrapper