import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Creates a MySQL database connection.
    Works with .env locally and Streamlit secrets when deployed.
    """

    try:
        import streamlit as st

        # Streamlit Cloud secrets
        if hasattr(st, "secrets") and "DB_HOST" in st.secrets:
            host = st.secrets["DB_HOST"]
            port = int(st.secrets.get("DB_PORT", 3306))
            user = st.secrets["DB_USER"]
            password = st.secrets["DB_PASSWORD"]
            database = st.secrets["DB_NAME"]

        else:
            # Local .env
            host = os.getenv("DB_HOST")
            port = int(os.getenv("DB_PORT", 3306))
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            database = os.getenv("DB_NAME")

    except Exception:
        host = os.getenv("DB_HOST")
        port = int(os.getenv("DB_PORT", 3306))
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )


# ============================================================
# TOTAL SALES AND PROFIT
# ============================================================

def get_total_sales_profit():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                COALESCE(SUM(sales), 0),
                COALESCE(SUM(profit), 0)
            FROM sales_data
        """)

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# BUSINESS KPIs
# ============================================================

def get_business_kpis():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                COUNT(DISTINCT order_id),
                COUNT(DISTINCT product_id),
                COALESCE(AVG(sales), 0),
                COALESCE(AVG(discount), 0),
                COALESCE(SUM(sales), 0),
                COALESCE(SUM(profit), 0)
            FROM sales_data
        """)

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# HIGHEST SALES REGION
# ============================================================

def get_highest_sales_region():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                region,
                SUM(sales)
            FROM sales_data
            GROUP BY region
            ORDER BY SUM(sales) DESC
            LIMIT 1
        """)

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# HIGHEST SALES CATEGORY
# ============================================================

def get_highest_sales_category():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                category,
                SUM(sales)
            FROM sales_data
            GROUP BY category
            ORDER BY SUM(sales) DESC
            LIMIT 1
        """)

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# HIGHEST PROFIT REGION
# ============================================================

def get_highest_profit_region():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                region,
                SUM(profit)
            FROM sales_data
            GROUP BY region
            ORDER BY SUM(profit) DESC
            LIMIT 1
        """)

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

def get_category_analysis():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                category,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            GROUP BY category
            ORDER BY SUM(sales) DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# REGION ANALYSIS
# ============================================================

def get_region_analysis():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                region,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            GROUP BY region
            ORDER BY SUM(profit) DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# TOP PRODUCTS BY SALES
# ============================================================

def get_top_products(limit=10):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                product_name,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            GROUP BY product_name
            ORDER BY SUM(sales) DESC
            LIMIT %s
        """, (limit,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# MONTHLY SALES
# ============================================================

def get_monthly_sales():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                DATE_FORMAT(order_date, '%Y-%m') AS month,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            WHERE order_date IS NOT NULL
            GROUP BY DATE_FORMAT(order_date, '%Y-%m')
            ORDER BY month
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# TOP REGIONS BY PROFIT
# ============================================================

def get_top_regions(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                region,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            GROUP BY region
            ORDER BY SUM(profit) DESC
            LIMIT %s
        """, (limit,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# BOTTOM REGIONS BY PROFIT
# ============================================================

def get_bottom_regions(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                region,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            GROUP BY region
            ORDER BY SUM(profit) ASC
            LIMIT %s
        """, (limit,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# TOP CATEGORIES BY PROFIT
# ============================================================

def get_top_categories(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                category,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            GROUP BY category
            ORDER BY SUM(profit) DESC
            LIMIT %s
        """, (limit,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# TOP PRODUCTS BY PROFIT
# ============================================================

def get_top_products_by_profit(limit=5):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                product_name,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            GROUP BY product_name
            ORDER BY SUM(profit) DESC
            LIMIT %s
        """, (limit,))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# COMPARE REGIONS
# ============================================================

def compare_regions(region1, region2):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                region,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            WHERE LOWER(region) IN (
                LOWER(%s),
                LOWER(%s)
            )
            GROUP BY region
        """, (region1, region2))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


# ============================================================
# COMPARE CATEGORIES
# ============================================================

def compare_categories(category1, category2):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                category,
                SUM(sales),
                SUM(profit)
            FROM sales_data
            WHERE LOWER(category) IN (
                LOWER(%s),
                LOWER(%s)
            )
            GROUP BY category
        """, (category1, category2))

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
