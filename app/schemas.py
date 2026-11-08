from pydantic import BaseModel
from datetime import date

# Описываем, как будет выглядеть ответ API (для Swagger и валидации)
class DailyRevenue(BaseModel):
    order_date: date
    total_revenue: float
    total_orders: int

class TopProduct(BaseModel):
    stock_code: str
    total_sold: int
    revenue: float
