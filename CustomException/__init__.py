import traceback
import os
import sys
async def handle_exception(exception : Exception):
    exception_type = type(exception).__name__
    exception_message = str(exception)
    exception_traceback = traceback.extract_tb(exception.__traceback__)
    line_number = exception_traceback[-1].lineno
    print(f"Exception Type: {exception_type}")
    print(f"Exception Message: {exception_message}")
    print(f"Line Number: {line_number}")
    print("Full Traceback:")
    print("".join(traceback.format_tb(exception.__traceback__)))

    return {'error': str(exception)}