class ExecutionNotFoundError(Exception):
    MESSAGE = "Execution not found"
    
class ExecutionTriesError(Exception):
    MESSAGE = "Tries of procedure exceeded"