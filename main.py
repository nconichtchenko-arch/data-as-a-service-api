from fastapi import FastAPI, HTTPException
from typing import List
from app.database import get_db_connection
from app.schemas import DailyRevenue, TopProduct
import datetime

app = FastAPI(
    title="Data-as-a-Service API",
    description="Микросервис для отдачи бизнес-метрик из DWH (PostgreSQL). Pet-проект.",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """Проверка живости сервиса и БД."""
    try:
        conn, cur = get_db_connection()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/api/v1/revenue/daily", response_model=List[DailyRevenue])
def get_daily_revenue(limit: int = 10):
    """Возвращает выручку и количество заказов по дням (последние N дней)."""
    conn, cur = get_db_connection()
    try:
        # Запрос к нашей витрине fct_sales (агрегация по датам)
        query = """
            SELECT 
                order_date,
                SUM(total_revenue) as total_revenue,
                COUNT(DISTINCT invoice_no) as total_orders
            FROM dbt_schema.fct_sales
            GROUP BY order_date
            ORDER BY order_date DESC
            LIMIT %s;
        """
        cur.execute(query, (limit,))
        results = cur.fetchall()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/v1/products/top", response_model=List[TopProduct])
def get_top_products(limit: int = 10):
    """Возвращает топ-N товаров по выручке."""
    conn, cur = get_db_connection()
    try:
        query = """
            SELECT 
                stock_code,
                SUM(total_quantity) as total_sold,
                SUM(total_revenue) as revenue
            FROM dbt_schema.fct_sales
            GROUP BY stock_code
            ORDER BY revenue DESC
            LIMIT %s;
        """
        cur.execute(query, (limit,))
        results = cur.fetchall()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()