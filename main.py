from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    html_content = """
    <html>
        <head>
            <title>Selenium 실습 센터</title>
            <style>
                body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; text-align: center; }
                .card { border: 1px solid #ddd; padding: 20px; margin: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                a { text-decoration: none; color: white; background-color: #007bff; padding: 10px 20px; border-radius: 5px; display: inline-block; margin-top: 10px; }
            </style>
        </head>
        <body>
            <h1>Selenium 크롤링 실습 센터</h1>
            <div class="card">
                <h2>실습 1: AJAX 지연 로딩</h2>
                <a href="/ajax">/ajax 접속하기</a>
            </div>
            <div class="card">
                <h2>실습 2: 무한 스크롤</h2>
                <a href="/scroll">/scroll 접속하기</a>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


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


# ✅ 수정됨: 한 번에 20개씩 반환하여 스크롤 유도
@app.get("/api/items")
async def get_scroll_items(page: int = Query(1, ge=1)):
    if page > 10: return []

    # 20개씩 생성 (화면이 큰 모니터 대응)
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