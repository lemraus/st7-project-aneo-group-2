from time import time

def timer(f):
    def wrapped(*args, **kwargs):
        t1 = time()
        result = f(*args, **kwargs)
        t2 = time()
        print(f"Function {f.__name__}, time ellapsed: {t2 - t1} seconds.")
        return result
    return wrapped