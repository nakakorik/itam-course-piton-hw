from fastapi import FastAPI, Path, Response, HTTPException, status
from pydantic import BaseModel
from services.link_service import LinkService
from loguru import logger
import time
from typing import Callable, Awaitable
from fastapi import Request, Response
from fastapi.exception_handlers import http_exception_handler


#text

class linkRequest(BaseModel):
    link:str

class linkResponce(BaseModel):
    short_link:str

def create_app() -> FastAPI:
    
    app = FastAPI()
    
    link_service = LinkService()

    @app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request:Request, exc:Exception):
        logger.error(f"Exception: {exc} in Request {request.method} {request.url} {dict(request.headers)}")
        return await http_exception_handler(request=request,exc=exc)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

    
        t0 = time.time()
        
        response = await call_next(request)

        elapsed_ms = round((time.time() - t0) * 1000, 2)
        response.headers["X-Process-Time"] = str(elapsed_ms)
        logger.debug( f'{request.method} done in {elapsed_ms} ms')
        
        return response

    @app.post("/link")
    def create_link(payload: linkRequest) -> linkResponce:

        short_link = link_service.create_link(payload.link)
        if short_link is None: raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="invalid link ")
        return linkResponce(short_link=f'http://localhost:8000/{short_link}')
    

    @app.get("/{link}")
    def get_link(link:str)-> Response:

        long_link = link_service.get_link(link)
        
        if long_link is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="link not found ")

        return Response(
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
            headers={"location": long_link}
            )
    return app 