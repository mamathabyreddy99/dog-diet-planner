from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2

router = APIRouter()

DB_PARAMS = {
    "host": "localhost",
    "database": "dog_diet_db",
    "user": "postgres",
    "password": "Southern@2025"
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

@router.get("/groups", response_model=List[str])
def get_group_tables():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE'
              AND table_name LIKE 'group_%'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return tables
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/group/{group_name}")
def get_ingredients_by_group(group_name: str):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {group_name};")
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
