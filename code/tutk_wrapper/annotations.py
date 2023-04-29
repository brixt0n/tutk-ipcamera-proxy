from .exceptions import (
    TutkAVLibraryNotInitializedException,
    TutkLibraryNotLoadedException
)
import tutk_wrapper.shared as shared


def requires_av_initialized(func):
    """
    Ensures av library is initialized as a pre-req
    """
    def wrapper(
        *args,
        **kwargs
    ):
        if not shared.av_initialized:
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
        if not shared.library_instance:
            raise TutkLibraryNotLoadedException()
        
        return func(
            *args, 
            **kwargs
        )

    return wrapper