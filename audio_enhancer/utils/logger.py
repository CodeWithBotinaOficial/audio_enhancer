import logging

# Singleton Pattern: Ensures a class has only one instance and provides a global point of access to it.
# Here, we use it to create a single logging instance for the entire application.

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            # Configure logger
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            cls._instance.logger = logging.getLogger("AudioEnhancer")
        return cls._instance

    def get_logger(self):
        return self.logger

# Global logger instance
logger = Logger().get_logger()
