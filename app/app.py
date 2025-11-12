from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from error_handling.error_handling import ApplicationException, application_exception_handler, exception_handler, http_exception_handler, runtime_error_handler, validation_exception_handler

app = FastAPI()

# Define error handling
app.add_exception_handler(ApplicationException, application_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(RuntimeError, runtime_error_handler)


@app.get("/")
async def root():
    return {"message": "Hello World"}

