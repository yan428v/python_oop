from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class OperationRequest(BaseModel):
    a: float
    b: float

class ExpressionRequest(OperationRequest):
    op: str

class FullExpressionReq(BaseModel):
    expr: str
@app.post("/add")
def add(request: OperationRequest):
    result = request.a + request.b
    return {"operation": "addition", "a": request.a, "b": request.b, "result": result}

@app.post("/sub")
def sub(request: OperationRequest):
    result = request.a - request.b
    return {"operation": "subtraction", "a": request.a, "b": request.b, "result": result}

@app.post("/mult")
def mult(request: OperationRequest):
    result = request.a * request.b
    return {"operation": "multiplication", "a": request.a, "b": request.b, "result": result}

@app.post("/div")
def div(request: OperationRequest):
    if request.b == 0:
        raise HTTPException(status_code=400, detail="нельзя делить на 0")
    result = request.a / request.b
    return {"operation": "division", "a": request.a, "b": request.b, "result": result}

@app.post("/expr")
def expr(request: ExpressionRequest):
    if request.op == "/" and request.b == 0:
        raise HTTPException(status_code=400, detail="нельзя делить на 0")

    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    return operations[request.op](request.a, request.b)

@app.post("/calc")
def calc(req: FullExpressionReq):
    regex = r'^[0-9+\-*/().\s]+$'
    if re.match(regex, req.expr):
        try:
            return eval(req.expr)
        except ZeroDivisionError:
            raise HTTPException(status_code=400, detail="нельзя делить на 0")
        except SyntaxError:
            raise HTTPException(status_code=400, detail="ошибка в выражении")
    else:
        raise HTTPException(status_code=400, detail="недопустимые символы в выражении")

