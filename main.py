from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
import time

app = FastAPI()

# 템플릿 디렉토리 설정 (HTML 파일 위치)
templates = Jinja2Templates(directory="templates")


# 1. 메인 페이지 (실습 목록)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    html_content = """
    <html>
        <head>
            <title>Selenium 실습 센터</title>
            <style>
                body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; text-align: center; }
                h1 { color: #333; }
                .card { border: 1px solid #ddd; padding: 20px; margin: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                a { text-decoration: none; color: white; background-color: #007bff; padding: 10px 20px; border-radius: 5px; display: inline-block; margin-top: 10px; }
                a:hover { background-color: #0056b3; }
            </style>
        </head>
        <body>
            <h1>Selenium 크롤링 실습 센터</h1>
            <div class="card">
                <h2>실습 1: AJAX 지연 로딩 (Explicit Wait)</h2>
                <p>버튼을 누르면 3초 뒤에 데이터가 나타납니다. WebDriverWait 연습용입니다.</p>
                <a href="/ajax">실습하러 가기</a>
            </div>
            <div class="card">
                <h2>실습 2: 무한 스크롤 (Infinite Scroll)</h2>
                <p>스크롤을 내리면 계속 데이터가 추가됩니다. 동적 페이지 제어 연습용입니다.</p>
                <a href="/scroll">실습하러 가기</a>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# 2. AJAX 실습 페이지 렌더링
@app.get("/ajax", response_class=HTMLResponse)
async def get_ajax_page(request: Request):
    return templates.TemplateResponse("ajax.html", {"request": request})


# 3. [API] 3초 지연 데이터 (Selenium이 기다려야 하는 대상)
@app.get("/api/data")
async def get_delayed_data():
    # 3초 대기 (네트워크 지연 시뮬레이션)
    await asyncio.sleep(3)
    return {"message": "데이터 로드 성공!", "secret_code": "SELENIUM_MASTER_2024"}


# 4. 무한 스크롤 실습 페이지 렌더링
@app.get("/scroll", response_class=HTMLResponse)
async def get_scroll_page(request: Request):
    return templates.TemplateResponse("scroll.html", {"request": request})


# 5. [API] 무한 스크롤 데이터 제공
@app.get("/api/items")
async def get_scroll_items(page: int = Query(1, ge=1)):
    # 서버 보호를 위해 최대 10페이지까지만 제공
    if page > 10:
        return []

    # 페이지당 6개의 아이템 생성
    start_id = (page - 1) * 6 + 1
    items = []
    for i in range(start_id, start_id + 6):
        items.append({
            "id": i,
            "title": f"크롤링 연습 상품 {i}",
            "price": i * 1500,
            "description": f"이 상품은 {i}번째 데이터입니다. 스크롤을 내려 더 찾아보세요."
        })

    # 약간의 로딩 느낌을 주기 위해 0.5초 지연
    await asyncio.sleep(0.5)
    return items