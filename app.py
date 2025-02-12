from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Order(BaseModel):
    num : Optional[int] = None
    add_date : Optional[date] = None
    device : Optional[str] = None
    problem_description : Optional[str] = None
    problem_type : Optional[str] = None
    client : Optional[str] = None
    status : Optional[str] = None
    master : Optional[str] = None
    end_date : Optional[date] = None
    master_comment : Optional[str] = None

repo = [
    Order(num = 1, add_date = date(2011,10,10), device = "slomano", problem_description = "asda", problem_type = "asdasd", FIO = "asdasd", status = "done", end_date = date(2020,10,10))
]

@app.get("/orders")
def get_orders():
    return repo

@app.post("/orders")
def post_orders(data: Order):
    repo.append(data)


@app.post("/update",response_model = Order)
def update_orders(data: Order):
    
    for o in repo:
        if o.num == data.num:
            if data.status is not None:
                o.status = data.status
                if data.status == "done":
                    o.end_date = date.today()

            if data.problem_type is not None:
                o.problem_type = data.problem_type
            
            if data.master is not None:
                o.master = data.master

            if data.master_comment is not None:
                o.master_comment = data.master_comment
            return o
        
@app.get("/findbynum/{num}")
def get_order_by_id(num : int):
    for o in repo:
        if o.num == num:
            return o
    if o.num != num:
        return "Заявка с таким номером не найдена"

@app.get("/stats")
def get_stats():
    completed_orders = []
    total_days = 0
    problem_type_counts = {}

    for o in repo:
        if o.status == "done":
            completed_orders.append(o)
            total_days += (o.end_date - o.add_date).days

            if o.problem_type:
                if o.problem_type in problem_type_counts:
                    problem_type_counts[o.problem_type] += 1
                else:
                    problem_type_counts[o.problem_type] = 1

    avg_time = total_days // len(completed_orders) if completed_orders else 0

    return {
        "Количество готовых заявок": len(completed_orders),
        "Среднее количество дней": avg_time,
        "Статистика по типам неисправностей": problem_type_counts
    }