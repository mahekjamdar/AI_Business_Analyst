import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# ==================================================
# TOTAL SALES AND PROFIT
# ==================================================

def get_total_sales_profit():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(sales), SUM(profit)
        FROM sales_data
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


# ==================================================
# CATEGORY ANALYSIS
# ==================================================

def get_category_analysis():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(sales), SUM(profit)
        FROM sales_data
        GROUP BY category
        ORDER BY SUM(sales) DESC
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==================================================
# REGION ANALYSIS
# ==================================================

def get_region_analysis():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT region, SUM(sales), SUM(profit)
        FROM sales_data
        GROUP BY region
        ORDER BY SUM(profit) DESC
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==================================================
# TOP PRODUCTS BY SALES
# ==================================================

def get_top_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_name, SUM(sales), SUM(profit)
        FROM sales_data
        GROUP BY product_name
        ORDER BY SUM(sales) DESC
        LIMIT 10
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==================================================
# MONTHLY SALES
# ==================================================

def get_monthly_sales():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            DATE_FORMAT(order_date, '%Y-%m'),
            SUM(sales),
            SUM(profit)
        FROM sales_data
        WHERE order_date IS NOT NULL
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY DATE_FORMAT(order_date, '%Y-%m')
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==================================================
# TOP REGIONS BY PROFIT
# ==================================================

def get_top_regions(limit=5):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT region, SUM(sales), SUM(profit)
        FROM sales_data
        GROUP BY region
        ORDER BY SUM(profit) DESC
        LIMIT %s
    """, (limit,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==================================================
# BOTTOM REGIONS BY PROFIT
# ==================================================

def get_bottom_regions(limit=5):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT region, SUM(sales), SUM(profit)
        FROM sales_data
        GROUP BY region
        ORDER BY SUM(profit) ASC
        LIMIT %s
    """, (limit,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==================================================
# TOP CATEGORIES BY PROFIT
# ==================================================

def get_top_categories(limit=5):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(sales), SUM(profit)
        FROM sales_data
        GROUP BY category
        ORDER BY SUM(profit) DESC
        LIMIT %s
    """, (limit,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==================================================
# TOP PRODUCTS BY PROFIT
# ==================================================

def get_top_products_by_profit(limit=5):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_name, SUM(sales), SUM(profit)
        FROM sales_data
        GROUP BY product_name
        ORDER BY SUM(profit) DESC
        LIMIT %s
    """, (limit,))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

# ==================================================
# REGION COMPARISON
# ==================================================

def compare_regions(region1, region2):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT region, SUM(sales), SUM(profit)
        FROM sales_data
        WHERE LOWER(region) IN (LOWER(%s), LOWER(%s))
        GROUP BY region
    """, (region1, region2))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


# ==================================================
# CATEGORY COMPARISON
# ==================================================

def compare_categories(category1, category2):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(sales), SUM(profit)
        FROM sales_data
        WHERE LOWER(category) IN (LOWER(%s), LOWER(%s))
        GROUP BY category
    """, (category1, category2))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results

# ==================================================
# BUSINESS KPIs
# ==================================================

def get_business_kpis():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(DISTINCT order_id),
            COUNT(DISTINCT product_id),
            AVG(sales),
            AVG(discount),
            SUM(sales),
            SUM(profit)
        FROM sales_data
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_highest_sales_region():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT region, SUM(sales)
        FROM sales_data
        GROUP BY region
        ORDER BY SUM(sales) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def get_highest_sales_category():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, SUM(sales)
        FROM sales_data
        GROUP BY category
        ORDER BY SUM(sales) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result

# ==================================================
# HIGHEST PROFIT REGION
# ==================================================

def get_highest_profit_region():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT region, SUM(profit)
        FROM sales_data
        GROUP BY region
        ORDER BY SUM(profit) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result