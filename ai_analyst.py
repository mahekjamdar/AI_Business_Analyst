from analyst import (
    get_business_kpis,
    get_highest_sales_region,
    get_highest_sales_category,
    get_highest_profit_region,
    get_total_sales_profit,
    get_category_analysis,
    get_region_analysis,
    get_top_products,
    get_monthly_sales,
    get_top_regions,
    get_bottom_regions,
    get_top_categories,
    get_top_products_by_profit,
    compare_regions,
    compare_categories
)


# ============================================================
# QUESTION UNDERSTANDING
# ============================================================

def understand_question(question):

    q = question.lower().strip()

    # ========================================================
    # BUSINESS KPIs
    # ========================================================

    if "average order value" in q or "average order" in q:
        return "average_order_value"

    if (
        "how many orders" in q
        or "number of orders" in q
        or "total orders" in q
    ):
        return "total_orders"

    if (
        "how many products" in q
        or "number of products" in q
        or "total products" in q
    ):
        return "total_products"

    if "average discount" in q:
        return "average_discount"

    if (
        "profit margin" in q
        or "profit percentage" in q
    ):
        return "profit_margin"

    # ========================================================
    # HIGHEST SALES / PROFIT
    # ========================================================

    if (
        "highest sales region" in q
        or "region has the highest sales" in q
        or "which region has the highest sales" in q
    ):
        return "highest_sales_region"

    if (
        "highest sales category" in q
        or "category has the highest sales" in q
        or "which category has the highest sales" in q
    ):
        return "highest_sales_category"

    if (
        "highest profit region" in q
        or "region has the highest profit" in q
        or "most profitable region" in q
        or "which region has the highest profit" in q
    ):
        return "highest_profit_region"

    # ========================================================
    # COMPARISON
    # ========================================================

    region_names = [
        "west",
        "east",
        "south",
        "central"
    ]

    category_names = [
        "technology",
        "furniture",
        "office supplies"
    ]

    is_comparison = (
        "compare" in q
        or "versus" in q
        or " vs " in q
        or "which is better" in q
        or "which is higher" in q
        or "which performs better" in q
    )

    if is_comparison:

        found_regions = [
            r for r in region_names
            if r in q
        ]

        found_categories = [
            c for c in category_names
            if c in q
        ]

        if len(found_regions) >= 2:
            return "compare_regions"

        if len(found_categories) >= 2:
            return "compare_categories"

    # ========================================================
    # TOP REGIONS
    # ========================================================

    if (
        ("top" in q or "highest" in q or "best" in q)
        and
        ("region" in q or "regions" in q or "area" in q)
    ):
        return "top_regions"

    # ========================================================
    # LOWEST REGIONS
    # ========================================================

    if (
        ("lowest" in q or "bottom" in q or "worst" in q)
        and
        ("region" in q or "regions" in q or "area" in q)
    ):
        return "bottom_regions"

    # ========================================================
    # TOP CATEGORIES
    # ========================================================

    if (
        ("top" in q or "highest" in q or "best" in q)
        and
        ("category" in q or "categories" in q)
    ):
        return "top_categories"

    # ========================================================
    # TOP PRODUCTS
    # ========================================================

    if (
        ("top" in q or "highest" in q or "best" in q)
        and
        ("product" in q or "products" in q)
    ):
        return "top_products_profit"

    # ========================================================
    # MONTHLY
    # ========================================================

    if (
        "month" in q
        or "monthly" in q
        or "trend" in q
    ):
        return "monthly"

    # ========================================================
    # TOTAL SALES + PROFIT
    # ========================================================

    if "sales" in q and "profit" in q:
        return "total"

    # ========================================================
    # CATEGORY
    # ========================================================

    if "category" in q or "categories" in q:
        return "category"

    # ========================================================
    # REGION
    # ========================================================

    if (
        "region" in q
        or "regions" in q
        or "area" in q
    ):
        return "region"

    # ========================================================
    # PRODUCT
    # ========================================================

    if "product" in q or "products" in q:
        return "product"

    # ========================================================
    # SALES
    # ========================================================

    if (
        "sales" in q
        or "revenue" in q
        or "turnover" in q
    ):
        return "total_sales"

    # ========================================================
    # PROFIT
    # ========================================================

    if (
        "profit" in q
        or "profitable" in q
        or "earnings" in q
    ):
        return "total_profit"

    return "unknown"


# ============================================================
# FIND TWO ITEMS
# ============================================================

def find_two_items(question, items):

    q = question.lower()

    found = []

    for item in items:

        if item.lower() in q:
            found.append(item)

    return found[:2]


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question):

    analysis_type = understand_question(question)

    # ========================================================
    # AVERAGE ORDER VALUE
    # ========================================================

    if analysis_type == "average_order_value":

        data = get_business_kpis()

        total_orders = data[0]
        total_sales = data[4]

        if not total_orders:
            return "No orders found."

        average_order_value = total_sales / total_orders

        return (
            f"The average order value is "
            f"₹{average_order_value:,.2f}."
        )

    # ========================================================
    # TOTAL ORDERS
    # ========================================================

    if analysis_type == "total_orders":

        data = get_business_kpis()

        total_orders = data[0]

        return (
            f"The total number of orders is "
            f"{total_orders:,}."
        )

    # ========================================================
    # TOTAL PRODUCTS
    # ========================================================

    if analysis_type == "total_products":

        data = get_business_kpis()

        total_products = data[1]

        return (
            f"The total number of products is "
            f"{total_products:,}."
        )

    # ========================================================
    # AVERAGE DISCOUNT
    # ========================================================

    if analysis_type == "average_discount":

        data = get_business_kpis()

        average_discount = data[3]

        return (
            f"The average discount is "
            f"{average_discount:.2%}."
        )

    # ========================================================
    # PROFIT MARGIN
    # ========================================================

    if analysis_type == "profit_margin":

        data = get_business_kpis()

        total_sales = data[4]
        total_profit = data[5]

        if not total_sales:
            return "Sales data is not available."

        margin = (total_profit / total_sales) * 100

        return (
            f"The overall profit margin is "
            f"{margin:.2f}%."
        )

    # ========================================================
    # HIGHEST SALES REGION
    # ========================================================

    if analysis_type == "highest_sales_region":

        data = get_highest_sales_region()

        if not data:
            return "No region sales data found."

        return (
            f"The region with the highest sales is "
            f"{data[0]}, with sales of "
            f"₹{data[1]:,.2f}."
        )

    # ========================================================
    # HIGHEST SALES CATEGORY
    # ========================================================

    if analysis_type == "highest_sales_category":

        data = get_highest_sales_category()

        if not data:
            return "No category sales data found."

        return (
            f"The category with the highest sales is "
            f"{data[0]}, with sales of "
            f"₹{data[1]:,.2f}."
        )

    # ========================================================
    # HIGHEST PROFIT REGION
    # ========================================================

    if analysis_type == "highest_profit_region":

        data = get_highest_profit_region()

        if not data:
            return "No region profit data found."

        return (
            f"The region with the highest profit is "
            f"{data[0]}, with profit of "
            f"₹{data[1]:,.2f}."
        )

    # ========================================================
    # COMPARE REGIONS
    # ========================================================

    if analysis_type == "compare_regions":

        regions = [
            "West",
            "East",
            "South",
            "Central"
        ]

        selected = find_two_items(
            question,
            regions
        )

        if len(selected) != 2:

            return (
                "Please mention two regions.\n"
                "Example: Compare West and East"
            )

        data = compare_regions(
            selected[0],
            selected[1]
        )

        if len(data) < 2:
            return "Data for both regions could not be found."

        first = data[0]
        second = data[1]

        if first[2] >= second[2]:

            winner = first
            loser = second

        else:

            winner = second
            loser = first

        difference = winner[2] - loser[2]

        return (
            f"{winner[0]} is more profitable than "
            f"{loser[0]}.\n\n"
            f"{winner[0]} profit: ₹{winner[2]:,.2f}\n"
            f"{loser[0]} profit: ₹{loser[2]:,.2f}\n"
            f"Profit difference: ₹{difference:,.2f}"
        )

    # ========================================================
    # COMPARE CATEGORIES
    # ========================================================

    if analysis_type == "compare_categories":

        categories = [
            "Technology",
            "Furniture",
            "Office Supplies"
        ]

        selected = find_two_items(
            question,
            categories
        )

        if len(selected) != 2:

            return (
                "Please mention two categories.\n"
                "Example: Compare Technology and Furniture"
            )

        data = compare_categories(
            selected[0],
            selected[1]
        )

        if len(data) < 2:
            return "Data for both categories could not be found."

        first = data[0]
        second = data[1]

        if first[2] >= second[2]:

            winner = first
            loser = second

        else:

            winner = second
            loser = first

        difference = winner[2] - loser[2]

        return (
            f"{winner[0]} is more profitable than "
            f"{loser[0]}.\n\n"
            f"{winner[0]} profit: ₹{winner[2]:,.2f}\n"
            f"{loser[0]} profit: ₹{loser[2]:,.2f}\n"
            f"Profit difference: ₹{difference:,.2f}"
        )

    # ========================================================
    # TOP REGIONS
    # ========================================================

    if analysis_type == "top_regions":

        data = get_top_regions(5)

        if not data:
            return "No region data found."

        answer = "Top regions by profit:\n\n"

        for i, row in enumerate(data, 1):

            answer += (
                f"{i}. {row[0]} - "
                f"₹{row[2]:,.2f}\n"
            )

        return answer

    # ========================================================
    # BOTTOM REGIONS
    # ========================================================

    if analysis_type == "bottom_regions":

        data = get_bottom_regions(5)

        if not data:
            return "No region data found."

        answer = "Lowest-performing regions by profit:\n\n"

        for i, row in enumerate(data, 1):

            answer += (
                f"{i}. {row[0]} - "
                f"₹{row[2]:,.2f}\n"
            )

        return answer

    # ========================================================
    # TOP CATEGORIES
    # ========================================================

    if analysis_type == "top_categories":

        data = get_top_categories(5)

        if not data:
            return "No category data found."

        answer = "Top categories by profit:\n\n"

        for i, row in enumerate(data, 1):

            answer += (
                f"{i}. {row[0]} - "
                f"₹{row[2]:,.2f}\n"
            )

        return answer

    # ========================================================
    # TOP PRODUCTS
    # ========================================================

    if analysis_type == "top_products_profit":

        data = get_top_products_by_profit(5)

        if not data:
            return "No product data found."

        answer = "Top products by profit:\n\n"

        for i, row in enumerate(data, 1):

            answer += (
                f"{i}. {row[0]} - "
                f"₹{row[2]:,.2f}\n"
            )

        return answer

    # ========================================================
    # CATEGORY ANALYSIS
    # ========================================================

    if analysis_type == "category":

        data = get_category_analysis()

        if not data:
            return "No category data found."

        best = max(
            data,
            key=lambda x: x[2]
        )

        return (
            f"The category with the highest profit is "
            f"{best[0]}, with a profit of "
            f"₹{best[2]:,.2f}."
        )

    # ========================================================
    # REGION ANALYSIS
    # ========================================================

    if analysis_type == "region":

        data = get_region_analysis()

        if not data:
            return "No region data found."

        best = max(
            data,
            key=lambda x: x[2]
        )

        return (
            f"The region with the highest profit is "
            f"{best[0]}, with a profit of "
            f"₹{best[2]:,.2f}."
        )

    # ========================================================
    # PRODUCT ANALYSIS
    # ========================================================

    if analysis_type == "product":

        data = get_top_products()

        if not data:
            return "No product data found."

        best = max(
            data,
            key=lambda x: x[2]
        )

        return (
            f"Among the top products by sales, "
            f"{best[0]} has the highest profit of "
            f"₹{best[2]:,.2f}."
        )

    # ========================================================
    # MONTHLY ANALYSIS
    # ========================================================

    if analysis_type == "monthly":

        data = get_monthly_sales()

        if not data:
            return "No monthly data found."

        best = max(
            data,
            key=lambda x: x[1]
        )

        return (
            f"The month with the highest sales is "
            f"{best[0]}, with sales of "
            f"₹{best[1]:,.2f}."
        )

    # ========================================================
    # TOTAL SALES + PROFIT
    # ========================================================

    if analysis_type == "total":

        sales, profit = get_total_sales_profit()

        return (
            f"Total sales are ₹{sales:,.2f} "
            f"and total profit is ₹{profit:,.2f}."
        )

    # ========================================================
    # TOTAL SALES
    # ========================================================

    if analysis_type == "total_sales":

        sales, profit = get_total_sales_profit()

        return f"Total sales are ₹{sales:,.2f}."

    # ========================================================
    # TOTAL PROFIT
    # ========================================================

    if analysis_type == "total_profit":

        sales, profit = get_total_sales_profit()

        return f"Total profit is ₹{profit:,.2f}."

    # ========================================================
    # UNKNOWN QUESTION
    # ========================================================

    return (
        "I don't understand that business question yet.\n"
        "Try asking about sales, profit, categories, "
        "regions, products, comparisons, KPIs, "
        "or monthly trends."
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

while True:

    question = input(
        "\nAsk your business question "
        "(type 'exit' to quit): "
    )

    if question.lower().strip() == "exit":

        print("Goodbye!")
        break

    answer = generate_answer(question)

    print("\nAnswer:")
    print(answer)
