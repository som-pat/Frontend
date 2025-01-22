#please do testenv/Scripts/Activate
# please install libraries using pip install -r requirements.txt
#run using uvicorn main:app --reload

# Importing required libraries
from fastapi import FastAPI, Form, Request, Response      
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
symbols = []


class SymbolData(BaseModel):
    symbol: str
    industry: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

@app.get("/", response_class=HTMLResponse)
async def get_overlay(request: Request):


    return templates.TemplateResponse("Dashboard.html", {
        "request": request
    })


@app.post("/add-symbol/")
def add_symbol(symbol: str = Form(...), industry: str = Form(...)):
    global symbols

    # Validate inputs
    if not symbol.isupper() or not industry.isalpha():
        return {"error": "Invalid input"}
    if any(s.symbol == symbol for s in symbols):
        return {"error": f"Symbol {symbol} is already subscribed."}

    # Generate random data
    open_price = round(random.uniform(100, 5000), 2)
    high_price = round(random.uniform(open_price, open_price + 50), 2)
    low_price = round(random.uniform(open_price - 50, open_price), 2)
    close_price = round(random.uniform(low_price, high_price), 2)
    volume = random.randint(1000, 100000)

    # Add to storage
    new_symbol = SymbolData(
        symbol=symbol,
        industry=industry.capitalize(),
        open_price=open_price,
        high_price=high_price,
        low_price=low_price,
        close_price=close_price,
        volume=volume,
    )
    symbols.append(new_symbol)
    return {"success": True, "symbols": symbols}


@app.get("/symbols/")
def get_symbols():
    global symbols
    return symbols


@app.post("/update-symbols/")
def update_symbols():
    global symbols

    # Randomly update all symbols
    for sym in symbols:
        sym.open_price += round(random.uniform(-5, 5), 2)
        sym.high_price += round(random.uniform(-5, 5), 2)
        sym.low_price += round(random.uniform(-5, 5), 2)
        sym.close_price += round(random.uniform(-5, 5), 2)
        sym.volume += random.randint(-500, 500)

    return {"success": True, "symbols": symbols}
