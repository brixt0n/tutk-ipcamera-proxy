import logging

log = logging.getLogger(__name__)

def debug_log(func):
    """
    Logs arguments passed to the wrapped function.
    """
    def wrapper(*args,
                **kwargs):
        log.debug(f'function={func.__name__}, args={args}, kwargs={kwargs}')
        
        return func(*args, 
                    **kwargs)

    return wrapper