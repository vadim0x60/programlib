import pexpect

def pexpect_exceptions(f):
    def wrapped_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except pexpect.exceptions.TIMEOUT as e:
            raise RuntimeError('Program did not receive expected input') from e
        except pexpect.exceptions.EOF as e:
            raise RuntimeError('Program exited unexpectedly') from e
        except pexpect.exceptions.ExceptionPexpect as e:
            raise RuntimeError('Program failed') from e
    return wrapped_f