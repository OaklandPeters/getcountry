

class GetCountyException(Exception):
    """Base exception type for the getcounty package."""

class ProcessingException(GetCountyException):
    """Exception generated during one of the processing
    steps in the pipeline."""

class NotFoundException(ProcessingException):
    """Exception thrown by a processing step which cannot generate valid output
    because a necessary value was not found.
    For example, GetZipCode(state, city) - when city is not found.
    """
    


