from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get('/checkurl/', response_class=HTMLResponse)
async def checkurl_main(request: Request):
    pass


@router.post('/checkurl/', response_class=HTMLResponse)
async def checkurl_result(request: Request):
    pass