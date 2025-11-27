from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ajax", response_class=HTMLResponse)
async def get_ajax_page(request: Request):
    return templates.TemplateResponse("ajax.html", {"request": request})


@app.get("/api/data")
async def get_delayed_data():
    await asyncio.sleep(3)
    return {"message": "데이터 로드 성공!", "secret_code": "SELENIUM_MASTER_2024"}


@app.get("/scroll", response_class=HTMLResponse)
async def get_scroll_page(request: Request):
    return templates.TemplateResponse("scroll.html", {"request": request})


@app.get("/api/items")
async def get_scroll_items(page: int = Query(1, ge=1)):
    if page > 10: return []

    items_per_page = 20
    start_id = (page - 1) * items_per_page + 1

    items = []
    for i in range(start_id, start_id + items_per_page):
        items.append({
            "id": i,
            "title": f"크롤링 연습 상품 {i}",
            "price": i * 1000,
            "description": f"스크롤 실습용 데이터 {i}번 입니다. 화면을 채우기 위해 길게 작성했습니다."
        })

    await asyncio.sleep(0.5)
    return items