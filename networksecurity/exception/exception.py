import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message
        
        exc_type, exc_value, exc_traceback = error_details.exc_info()

        self.lineno = exc_traceback.tb_lineno
        self.file_name = exc_traceback.tb_frame.f_code.co_filename

    def __str__(self):
        return (
            f"Error occured in python script name [{self.file_name}] "
            f"line number [{self.lineno}] error message [{self.error_message}]"
        )
