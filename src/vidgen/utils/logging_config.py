# Logging setup

import logging
import os
from vidgen.core.config import VideoGenConfig

def configure_logging(log_to_file=False):
    """
    Configure logging for the VidGen application.
    
    Args:
        log_to_file (bool): Whether to log to a file
    """
    # Root logger configuration
    logger = logging.getLogger("VidGen")
    logger.setLevel(VideoGenConfig.LOG_LEVEL)
    
    # Format for log messages
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(VideoGenConfig.OUTPUT_DIR, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create file handler
        file_handler = logging.FileHandler(
            os.path.join(logs_dir, "vidgen.log")
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Set up component-specific loggers
    component_loggers = [
        "models", "services", "ui", "utils", "core"
    ]
    
    for component in component_loggers:
        component_logger = logging.getLogger(f"VidGen.{component}")
        component_logger.setLevel(VideoGenConfig.LOG_LEVEL)
        # Component loggers inherit the handlers from the root logger
    
    return logger

class ProgressTracker:
    """
    Progress tracking utility for long-running operations.
    """
    
    def __init__(self, total_steps, description="Processing"):
        self.total_steps = total_steps
        self.current_step = 0
        self.description = description
        self.logger = logging.getLogger("VidGen.progress")
        self.callbacks = []
    
    def add_callback(self, callback):
        """Add a progress callback function"""
        self.callbacks.append(callback)
    
    def update(self, step=None, message=None):
        """Update progress"""
        if step is not None:
            self.current_step = step
        else:
            self.current_step += 1
        
        percentage = (self.current_step / self.total_steps) * 100
        
        if message:
            log_message = f"{self.description}: {message} ({percentage:.1f}%)"
        else:
            log_message = f"{self.description}: Step {self.current_step}/{self.total_steps} ({percentage:.1f}%)"
        
        self.logger.info(log_message)
        
        # Call registered callbacks
        for callback in self.callbacks:
            try:
                callback(self.current_step, self.total_steps, message or log_message)
            except Exception as e:
                self.logger.warning(f"Progress callback failed: {e}")
    
    def finish(self, message="Completed"):
        """Mark as finished"""
        self.current_step = self.total_steps
        final_message = f"{self.description}: {message} (100%)"
        self.logger.info(final_message)
        
        for callback in self.callbacks:
            try:
                callback(self.total_steps, self.total_steps, final_message)
            except Exception as e:
                self.logger.warning(f"Progress callback failed: {e}")

class VidGenLogger:
    """
    Enhanced logger with context and structured logging.
    """
    
    def __init__(self, component_name):
        self.logger = logging.getLogger(f"VidGen.{component_name}")
        self.component = component_name
        self.context = {}
    
    def set_context(self, **kwargs):
        """Set context for all subsequent log messages"""
        self.context.update(kwargs)
    
    def clear_context(self):
        """Clear the current context"""
        self.context = {}
    
    def _format_message(self, message):
        """Format message with context"""
        if self.context:
            context_str = " | ".join(f"{k}={v}" for k, v in self.context.items())
            return f"[{context_str}] {message}"
        return message
    
    def debug(self, message, **kwargs):
        self.set_context(**kwargs)
        self.logger.debug(self._format_message(message))
    
    def info(self, message, **kwargs):
        self.set_context(**kwargs)
        self.logger.info(self._format_message(message))
    
    def warning(self, message, **kwargs):
        self.set_context(**kwargs)
        self.logger.warning(self._format_message(message))
    
    def error(self, message, **kwargs):
        self.set_context(**kwargs)
        self.logger.error(self._format_message(message))
    
    def critical(self, message, **kwargs):
        self.set_context(**kwargs)
        self.logger.critical(self._format_message(message))

def setup_performance_logging():
    """Setup performance monitoring and logging"""
    import time
    import functools
    
    def log_performance(func):
        """Decorator to log function performance"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = VidGenLogger(f"performance.{func.__module__}")
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"{func.__name__} completed in {duration:.2f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"{func.__name__} failed after {duration:.2f}s: {e}")
                raise
        
        return wrapper
    return log_performance

def create_operation_logger(operation_name, total_steps=None):
    """
    Create a logger and progress tracker for a specific operation.
    
    Args:
        operation_name (str): Name of the operation
        total_steps (int): Total number of steps (for progress tracking)
    
    Returns:
        tuple: (logger, progress_tracker)
    """
    logger = VidGenLogger(operation_name)
    
    if total_steps:
        progress = ProgressTracker(total_steps, operation_name)
    else:
        progress = None
    
    return logger, progress

# Structured logging for errors
def log_error_with_context(logger, error, context=None, recovery_suggestion=None):
    """
    Log an error with full context and recovery suggestions.
    
    Args:
        logger: Logger instance
        error: Exception or error message
        context: Additional context information
        recovery_suggestion: Suggested recovery action
    """
    error_msg = str(error)
    
    if context:
        logger.error(f"Error occurred: {error_msg}", **context)
    else:
        logger.error(f"Error occurred: {error_msg}")
    
    if hasattr(error, 'original_exception') and error.original_exception:
        logger.debug(f"Original exception: {error.original_exception}")
    
    if recovery_suggestion:
        logger.info(f"Recovery suggestion: {recovery_suggestion}")
    elif hasattr(error, 'recovery_suggestion') and error.recovery_suggestion:
        logger.info(f"Recovery suggestion: {error.recovery_suggestion}")

# Memory and resource monitoring
def log_system_resources():
    """Log current system resource usage"""
    try:
        import psutil
        
        logger = VidGenLogger("system")
        
        # Memory usage
        memory = psutil.virtual_memory()
        logger.info(f"Memory usage: {memory.percent}% ({memory.used / 1024**3:.1f}GB used)")
        
        # Disk usage
        disk = psutil.disk_usage('/')
        logger.info(f"Disk usage: {disk.percent}% ({disk.free / 1024**3:.1f}GB free)")
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        logger.info(f"CPU usage: {cpu_percent}%")
        
    except ImportError:
        pass  # psutil not available
    except Exception as e:
        logger = VidGenLogger("system")
        logger.warning(f"Could not get system resources: {e}")
