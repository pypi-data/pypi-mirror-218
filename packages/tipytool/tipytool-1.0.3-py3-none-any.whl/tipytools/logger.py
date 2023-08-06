from typing import Optional
import sys


class Log:
    def __init__(self, param: str, type: Optional[str] = None):

        if type is not None and not isinstance(type, str):

            raise ValueError("type parameter must be a string")
        
        if type in [None, 'info']:
            sys.stdout.write('\n\033[34mℹ {}\033[0m'.format(param))  # Blue color for info
            ...
        elif type == 'warning':
            sys.stdout.write('\n\033[33m⚠ {}\033[0m'.format(param))  # Yellow color for warning
            ...
        elif type == 'error':
            sys.stdout.write('\n\033[31m❌ {}\033[0m'.format(param))  # Red color for error
            ...
        elif type == 'success':
            sys.stdout.write('\n\033[32m✓ {}\033[0m'.format(param))  # Green color for success
            ...
        else:
            sys.stdout.write("invalid log type: [ {} ]".format(type))
            ...