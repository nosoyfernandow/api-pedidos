from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from datetime import date
from db import conn, commit
from uvicorn import run

# Definir el modelo Pydantic para los pedidos
class Order(BaseModel):
    first_name: str
    last_name: str
    order_date: date

app = FastAPI()

@app.get("/orders")
async def get_orders():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    orders = [{"id": row[0], "first_name": row[1], "last_name": row[2], "order_date": row[3]} for row in rows]
    return orders

@app.get("/orders/{order_id}")
async def get_order(order_id: int = Path(..., title="The ID of the order to get")):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "first_name": row[1], "last_name": row[2], "order_date": row[3]}
    else:
        raise HTTPException(status_code=404, detail="Order not found")

@app.post("/orders")
async def create_order(order: Order):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (first_name, last_name, order_date) VALUES (%s, %s, %s)",
                   (order.first_name, order.last_name, order.order_date))
    commit()
    return {"message": "Order created successfully"}

@app.put("/orders/{order_id}")
async def update_order(order_id: int, order: Order):
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET first_name=%s, last_name=%s, order_date=%s WHERE id=%s",
                   (order.first_name, order.last_name, order.order_date, order_id))
    commit()
    return {"message": "Order updated successfully"}

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id=%s", (order_id,))
    commit()
    return {"message": "Order deleted successfully"} 

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8003)