import inspect
import logging
import logging.handlers
import os
import sys


class Log:
    __logger_instance = logging.getLogger(__name__)

    def __init__(self) -> None:
        # Creating log file during run time and writing logs into that file
        file_path = logging.FileHandler(os.path.dirname(__file__) + '/../testOutput.log')
        consoleHandler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        file_path.setFormatter(formatter)
        consoleHandler.setFormatter(formatter)
        if not self.__logger_instance.handlers:
            self.__logger_instance.addHandler(file_path)
            self.__logger_instance.addHandler(consoleHandler)
        self.__logger_instance.setLevel(logging.INFO)
        logging.getLogger("openapi_spec_validator").setLevel(logging.INFO)

    @staticmethod
    def __get_stack_info():
        stack = inspect.stack()

        # as test need to return customized file name from the stack hence hardcoded with index value.
        # get info for the code that called log
        file_last = stack[2][1].split('/')[-1]
        line_last = stack[2][2]
        func_last = stack[2][3]

        # get the info for the ext line initiating the log call
        file_first = line_first = method_first = ''
        for i in range(3, len(stack)):
            # could build the whole stack here, but just saving initiating call
            if '/tests/extensibility/' in stack[i][1]:
                file_first = stack[i][1].split('/')[-1]
                line_first = stack[i][2]
                method_first = stack[i][3]
            else:
                break
        file_last = file_last[file_last.find('\Lens\\test\\')+6:]
        
        stack = f'{file_last}:{line_last}:{func_last}'
        if file_first:
            stack = f'{file_first}:{line_first}:{method_first}...' + stack

        return stack

    @property
    def logger(self):
        """A logger instance"""
        self.__logger_instance.info('\n')
        return self.__logger_instance

    def info(self, message):
        """Provides info level log messages

        Gives log messages in specific format
        ex:- INFO : filename : testname : line_num : message
        Args:
            self: reads class level variables
            message: message to display in logs
        """
        message = f'{self.__get_stack_info()}: {message}'
        self.__logger_instance.info(': INFO : ' + message)
        return message

    def error(self, message):
        """Provides error level log messages

        Gives log messages in specific format
        ex:- ERROR : filename : testname : line_num : message
        Args:
            self: reads class level variables
            message: message to display in logs
        """
        message = f'{self.__get_stack_info()}: {message}'
        self.__logger_instance.error(': ERROR: ' + message)
        return message

    def step(self, message):
        """Provides info level log messages

        Gives log messages in specific format
        ex:- LOG STEP : filename : testname : line_num : message
        Args:
            self: reads class level variables
            message: message to display in logs
        """
        message = f'{self.__get_stack_info()}: {message}'
        self.__logger_instance.info(': STEP : ' + message)
        return message
