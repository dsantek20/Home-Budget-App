import json
import logging
import uuid
from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

crid_context: ContextVar[str] = ContextVar('crid', default='N/A')

log = logging.getLogger(__name__)

class CorrelationIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        crid = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
        crid_context.set(crid) 

        request.state.crid = crid

        client_ip = request.client.host

        try:
            request_body = ""
            if "multipart/form-data" not in request.headers.get("content-type", ""):
                request_body = await request.body()
                if request_body:
                    request_body = request_body.decode('utf-8')

                    if request.headers.get("Content-Type") == "application/json":
                        try:
                            request_body = json.dumps(json.loads(request_body), indent=2)
                        except:
                            pass

            request_log = (
                f"CRID: {crid} | "
                f"IP: {client_ip} | "
                f"Method: {request.method} | "
                f"Path: {request.url.path} | "
                f"Query: {request.url.query} | "
                f"Headers: {dict(request.headers)} | "
                f"Body: {request_body}"
            )
            log.info(f"Incoming Request: {request_log}")
        except Exception as e:
            log.error(f"Error logging incoming request: {e}")

        response = await call_next(request)

        response.headers['X-Correlation-ID'] = crid

        body = b"".join([chunk async for chunk in response.body_iterator])
        try:
            response_body = body
            if response_body:
                response_body = response_body.decode('utf-8')
                if response.media_type == "application/json":
                    try:
                        response_body = json.dumps(json.loads(response_body), indent=2)
                    except:
                        pass

            response_log = (
                f"CRID: {crid} | "
                f"Status Code: {response.status_code} | "
                f"Headers: {dict(response.headers)} | "
                f"Body: {response_body}"
            )
            log.info(f"Outgoing Response: {response_log}")
        except Exception as e:
            log.error(f"Error logging outgoing response: {e}")

        return Response(content=body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)