from . import utils

__all__ = ()

class ExampleException(Exception):
    def __init__(self, e: Exception = None) -> None:
        super().__init__()
        self.e = e
    
    def __str__(self) -> str:
        if self.e:
            classname = utils.get_full_class_name(self.e)
            errormessage = str(self.e)
            return f"An error occurred while loading {classname}: {errormessage}"
        else:
            return "An error occurred while loading."