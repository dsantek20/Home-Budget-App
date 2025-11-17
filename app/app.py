from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from api.routes.auth_router import auth_router
from api.routes.category_router import category_router
from api.routes.expense_router import expense_router
from api.routes.income_router import income_router
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

app.include_router(auth_router, prefix="/auth", tags=["AUTH"])
app.include_router(category_router, prefix="/category", tags=["CATEGORY"])
app.include_router(expense_router, prefix="/expense", tags=["EXPENSE"])
app.include_router(income_router, prefix="/income", tags=["INCOME"])



