from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app_config import get_app_config
from common.logger import initialize_logging
from error_handling.error_handling import ApplicationException, application_exception_handler, exception_handler, http_exception_handler, runtime_error_handler, validation_exception_handler
from common.middleware import CorrelationIDMiddleware

config = get_app_config()
log = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.config = config
    initialize_logging(config)
    log.info(f"{config.app_name} service started")
    
    yield 

    log.info(f"{app.state.config.app_name} service shutdown")

app = FastAPI(lifespan=lifespan)

app.add_middleware(CorrelationIDMiddleware)

# Define error handling
app.add_exception_handler(ApplicationException, application_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(RuntimeError, runtime_error_handler)


@app.get("/")
async def root():
    return {"message": "Hello World"}

