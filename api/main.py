from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import requests

app = FastAPI()

# ✅ Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["https://your-frontend.com"] to restrict access
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

NUMBERS_API_URL = "http://numbersapi.com"

# Utility functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    num_str = str(n)
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == n

def is_perfect(n):
    return sum(i for i in range(1, n) if n % i == 0) == n

def get_digit_sum(n):
    return sum(int(digit) for digit in str(n))

@app.get("/api/classify-number")
async def classify_number(number: int):
    try:
        properties = ["odd" if number % 2 != 0 else "even"]
        if is_armstrong(number):
            properties.insert(0, "armstrong")

        # Get fun fact from Numbers API
        fun_fact = requests.get(f"{NUMBERS_API_URL}/{number}/math").text

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": get_digit_sum(number),
            "fun_fact": fun_fact
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Adapt FastAPI for Vercel
handler = Mangum(app)
