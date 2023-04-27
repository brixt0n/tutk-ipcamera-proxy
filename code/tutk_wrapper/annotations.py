from exceptions import (
    TutkAVLibraryNotInitializedException,
    TutkLibraryNotLoadedException
)
from wrapper import (
    av_initialized,
    library_instance
)


def requires_av_initialized(func):
    """
    Ensures av library is initialized as a pre-req
    """
    def wrapper(
        *args,
        **kwargs
    ):
        if not av_initialized:
            raise TutkAVLibraryNotInitializedException()
        
        return func(
            *args, 
            **kwargs
        )

    return wrapper


def requires_tutk_library(func):
    """
    Ensures library is loaded as a pre-req
    """
    def wrapper(
        *args,
        **kwargs
    ):
        if not library_instance:
            raise TutkLibraryNotLoadedException()
        
        return func(
            *args, 
            **kwargs
        )

    return wrapper