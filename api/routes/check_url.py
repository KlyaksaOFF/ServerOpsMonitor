from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
import requests
router = APIRouter()

@router.get('/checkurl/', response_class=HTMLResponse)
async def checkurl_main(request: Request):
    pass

@router.post('/checkurl/', response_class=HTMLResponse)
async def checkurl_result(request: Request):
    pass