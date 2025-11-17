from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from api.models.errors.error_response import ErrorResponse


class ApplicationException(HTTPException):
    def __init__(self, status_code: int, message: str, code: str = None, debug_message: str = None):
        super().__init__(status_code=status_code, detail=message)
        self.code = code
        self.debug_message = debug_message


def create_error_response(status_code: int, code: str = None, message: str = None, debug_message: str = None):
    error_response = ErrorResponse(code=code, message=message, debug_message=debug_message)
    return JSONResponse(
        status_code=status_code,
        content=error_response.model_dump(),
    )


# Custom exception handler for application exceptions
async def application_exception_handler(request: Request, exc: ApplicationException):
    return create_error_response(exc.status_code, exc.code, exc.detail, exc.debug_message)


# Fast API exceptions
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and exc.detail == "Not authenticated":
        return create_error_response(
            status_code=401,
            code="SVC-4001",
            message="Authentication required",
            debug_message="Missing or invalid authentication token"
        )

    if exc.status_code == 403:
        return create_error_response(
            status_code=403,
            code="SVC-4003",
            message="Access forbidden",
            debug_message="You do not have permission to access this resource"
        )
    
    return create_error_response(exc.status_code,
                                 "SVC-5001",
                                 "Unknown error, support is notified and issue will be resolved as soon as possible",
                                 str(exc.detail))


# Handle Validation Errors (e.g., 422)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return create_error_response(status_code=422,
                                 code="SVC-4222",
                                 message="Validation errors",
                                 debug_message=str(exc.body))


async def exception_handler(request: Request, exc: Exception):
    return create_error_response(500,
                                 "SVC-5000",
                                 "Internal Server error, support is notified and issue will be resolved as soon as possible",
                                 str(exc))


async def runtime_error_handler(request: Request, exc: RuntimeError):
    return exception_handler(request, exc)

