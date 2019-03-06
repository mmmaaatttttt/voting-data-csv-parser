from functools import wraps


def log_start_and_end(fn):
    @wraps(fn)
    def wrapped_fn(*args, **kwargs):
        print(f"Running {fn.__name__}...")
        output = fn(*args, **kwargs)
        print(f"{fn.__name__} complete.")
        return output
    return wrapped_fn
