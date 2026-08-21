import streamlit as st
import pandas as pd
import plotly.express as px

from analyst import (
    get_business_kpis,
    get_highest_sales_region,
    get_highest_sales_category,
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
    compare_categories,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD DATABASE DATA
# ============================================================

@st.cache_data(ttl=300)
def load_data():

    sales, profit = get_total_sales_profit()

    kpis = get_business_kpis()

    return {
        "sales": float(sales or 0),
        "profit": float(profit or 0),
        "kpis": kpis,

        "highest_region": get_highest_sales_region(),
        "highest_category": get_highest_sales_category(),

        "region_data": get_region_analysis(),
        "category_data": get_category_analysis(),

        "top_regions": get_top_regions(5),
        "bottom_regions": get_bottom_regions(5),

        "top_categories": get_top_categories(5),

        "top_products": get_top_products(10),
        "top_products_profit": get_top_products_by_profit(5),

        "monthly_data": get_monthly_sales()
    }


# ============================================================
# DATABASE ERROR HANDLING
# ============================================================

try:

    data = load_data()

except Exception as e:

    st.error("❌ Could not connect to the MySQL database.")

    st.error(str(e))

    st.info(
        "Check your database credentials and Streamlit Secrets."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

sales = data["sales"]

profit = data["profit"]

kpis = data["kpis"]

total_orders = int(kpis[0] or 0)

unique_products = int(kpis[1] or 0)

average_sales = float(kpis[2] or 0)

average_discount = float(kpis[3] or 0)

average_order_value = (
    sales / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    profit / sales * 100
    if sales > 0
    else 0
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📊 AI Business Analyst")

    st.caption(
        "Business Intelligence Platform"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "Regional Analysis",
            "Category Analysis",
            "Product Analysis",
            "Monthly Trends",
            "Ask the Analyst"
        ]
    )

    st.divider()

    st.caption("Data Source")

    st.write("MySQL")

    st.caption("Analytics")

    st.write("Python + SQL")

    st.caption("Dashboard")

    st.write("Streamlit")


# ============================================================
# HEADER
# ============================================================

st.title("📊 AI Business Analyst")

st.caption(
    "Interactive business intelligence and performance analytics platform"
)


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "Executive Dashboard":

    st.header("Executive Overview")

    # KPI CARDS

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Sales",
        f"₹{sales:,.2f}"
    )

    c2.metric(
        "Total Profit",
        f"₹{profit:,.2f}"
    )

    c3.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    c4.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

    # ADDITIONAL KPIs

    st.subheader("Additional KPIs")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Order Value",
        f"₹{average_order_value:,.2f}"
    )

    c2.metric(
        "Unique Products",
        f"{unique_products:,}"
    )

    c3.metric(
        "Average Discount",
        f"{average_discount:.2%}"
    )

    # BUSINESS INSIGHTS

    st.subheader("Key Business Insights")

    c1, c2 = st.columns(2)

    region = data["highest_region"]

    category = data["highest_category"]

    with c1:

        if region:

            st.info(
                f"""
                **Region with Highest Sales**

                ### {region[0]}

                Sales: ₹{float(region[1]):,.2f}
                """
            )

    with c2:

        if category:

            st.info(
                f"""
                **Category with Highest Sales**

                ### {category[0]}

                Sales: ₹{float(category[1]):,.2f}
                """
            )

    # REGIONAL PROFIT CHART

    st.subheader("Regional Profit Performance")

    region_data = data["region_data"]

    if region_data:

        df = pd.DataFrame(
            region_data,
            columns=[
                "Region",
                "Sales",
                "Profit"
            ]
        )

        df["Sales"] = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        )

        df["Profit"] = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        )

        df = df.sort_values(
            "Profit",
            ascending=True
        )

        fig = px.bar(
            df,
            x="Profit",
            y="Region",
            orientation="h",
            text="Profit",
            title="Profit by Region"
        )

        fig.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        fig.update_layout(
            height=450,
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# REGIONAL ANALYSIS
# ============================================================

elif page == "Regional Analysis":

    st.header("🌎 Regional Analysis")

    region_data = data["region_data"]

    if not region_data:

        st.warning("No regional data available.")

    else:

        df = pd.DataFrame(
            region_data,
            columns=[
                "Region",
                "Sales",
                "Profit"
            ]
        )

        df["Sales"] = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        )

        df["Profit"] = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        )

        df["Profit Margin"] = (
            df["Profit"] /
            df["Sales"] *
            100
        ).fillna(0)

        # CHART

        fig = px.bar(
            df.sort_values(
                "Profit",
                ascending=True
            ),
            x="Profit",
            y="Region",
            orientation="h",
            text="Profit",
            title="Profit by Region"
        )

        fig.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # TABLE

        st.subheader("Regional Performance")

        display_df = df.copy()

        display_df["Sales"] = display_df["Sales"].map(
            lambda x: f"₹{x:,.2f}"
        )

        display_df["Profit"] = display_df["Profit"].map(
            lambda x: f"₹{x:,.2f}"
        )

        display_df["Profit Margin"] = display_df[
            "Profit Margin"
        ].map(
            lambda x: f"{x:.2f}%"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # TOP REGIONS

        st.subheader("Top 5 Regions by Profit")

        top_regions = pd.DataFrame(
            data["top_regions"],
            columns=[
                "Region",
                "Sales",
                "Profit"
            ]
        )

        top_regions["Sales"] = top_regions["Sales"].map(
            lambda x: f"₹{float(x):,.2f}"
        )

        top_regions["Profit"] = top_regions["Profit"].map(
            lambda x: f"₹{float(x):,.2f}"
        )

        st.dataframe(
            top_regions,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

elif page == "Category Analysis":

    st.header("📦 Category Analysis")

    category_data = data["category_data"]

    if not category_data:

        st.warning("No category data available.")

    else:

        df = pd.DataFrame(
            category_data,
            columns=[
                "Category",
                "Sales",
                "Profit"
            ]
        )

        df["Sales"] = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        )

        df["Profit"] = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        )

        # CHART

        fig = px.bar(
            df.sort_values(
                "Profit",
                ascending=True
            ),
            x="Profit",
            y="Category",
            orientation="h",
            text="Profit",
            title="Profit by Category"
        )

        fig.update_traces(
            texttemplate="₹%{text:,.0f}",
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # TABLE

        st.subheader("Category Performance")

        display_df = df.copy()

        display_df["Sales"] = display_df["Sales"].map(
            lambda x: f"₹{x:,.2f}"
        )

        display_df["Profit"] = display_df["Profit"].map(
            lambda x: f"₹{x:,.2f}"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # TOP CATEGORIES

        st.subheader("Top Categories by Profit")

        top_cat = pd.DataFrame(
            data["top_categories"],
            columns=[
                "Category",
                "Sales",
                "Profit"
            ]
        )

        top_cat["Sales"] = top_cat["Sales"].map(
            lambda x: f"₹{float(x):,.2f}"
        )

        top_cat["Profit"] = top_cat["Profit"].map(
            lambda x: f"₹{float(x):,.2f}"
        )

        st.dataframe(
            top_cat,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

elif page == "Product Analysis":

    st.header("🛍️ Product Analysis")

    # TOP SALES PRODUCTS

    st.subheader("Top Products by Sales")

    sales_products = pd.DataFrame(
        data["top_products"],
        columns=[
            "Product",
            "Sales",
            "Profit"
        ]
    )

    sales_products["Sales"] = sales_products["Sales"].map(
        lambda x: f"₹{float(x):,.2f}"
    )

    sales_products["Profit"] = sales_products["Profit"].map(
        lambda x: f"₹{float(x):,.2f}"
    )

    st.dataframe(
        sales_products,
        use_container_width=True,
        hide_index=True
    )

    # TOP PROFIT PRODUCTS

    st.subheader("Top Products by Profit")

    profit_products = pd.DataFrame(
        data["top_products_profit"],
        columns=[
            "Product",
            "Sales",
            "Profit"
        ]
    )

    profit_products["Sales"] = profit_products["Sales"].map(
        lambda x: f"₹{float(x):,.2f}"
    )

    profit_products["Profit"] = profit_products["Profit"].map(
        lambda x: f"₹{float(x):,.2f}"
    )

    st.dataframe(
        profit_products,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MONTHLY TRENDS
# ============================================================

elif page == "Monthly Trends":

    st.header("📈 Monthly Trends")

    monthly_data = data["monthly_data"]

    if not monthly_data:

        st.warning("No monthly data available.")

    else:

        df = pd.DataFrame(
            monthly_data,
            columns=[
                "Month",
                "Sales",
                "Profit"
            ]
        )

        df["Month"] = df["Month"].astype(str)

        df["Sales"] = pd.to_numeric(
            df["Sales"],
            errors="coerce"
        )

        df["Profit"] = pd.to_numeric(
            df["Profit"],
            errors="coerce"
        )

        # SALES

        st.subheader("Monthly Sales")

        sales_fig = px.line(
            df,
            x="Month",
            y="Sales",
            markers=True,
            title="Monthly Sales Trend"
        )

        st.plotly_chart(
            sales_fig,
            use_container_width=True
        )

        # PROFIT

        st.subheader("Monthly Profit")

        profit_fig = px.line(
            df,
            x="Month",
            y="Profit",
            markers=True,
            title="Monthly Profit Trend"
        )

        st.plotly_chart(
            profit_fig,
            use_container_width=True
        )

        # TABLE

        st.subheader("Monthly Performance Data")

        display_df = df.copy()

        display_df["Sales"] = display_df["Sales"].map(
            lambda x: f"₹{x:,.2f}"
        )

        display_df["Profit"] = display_df["Profit"].map(
            lambda x: f"₹{x:,.2f}"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ASK THE ANALYST
# ============================================================

elif page == "Ask the Analyst":

    st.header("🤖 Ask the Analyst")

    st.write(
        "Ask a business question about your sales data."
    )

    question = st.text_input(
        "Business Question",
        placeholder="Example: Which region has the highest profit?"
    )

    if question:

        q = question.lower().strip()

        # AVERAGE ORDER VALUE

        if "average order value" in q:

            st.success(
                f"Average order value: ₹{average_order_value:,.2f}"
            )

        # PROFIT MARGIN

        elif "profit margin" in q:

            st.success(
                f"Overall profit margin: {profit_margin:.2f}%"
            )

        # TOTAL ORDERS

        elif (
            "total orders" in q
            or "number of orders" in q
            or "how many orders" in q
        ):

            st.success(
                f"Total orders: {total_orders:,}"
            )

        # TOTAL SALES

        elif (
            "total sales" in q
            or "total revenue" in q
        ):

            st.success(
                f"Total sales: ₹{sales:,.2f}"
            )

        # TOTAL PROFIT

        elif "total profit" in q:

            st.success(
                f"Total profit: ₹{profit:,.2f}"
            )

        # HIGHEST PROFIT REGION

        elif (
            "highest profit" in q
            and "region" in q
        ):

            rows = data["region_data"]

            if rows:

                best = max(
                    rows,
                    key=lambda x: float(x[2])
                )

                st.success(
                    f"The region with the highest profit "
                    f"is {best[0]}, with profit of "
                    f"₹{float(best[2]):,.2f}."
                )

        # LOWEST PROFIT REGION

        elif (
            "lowest profit" in q
            and "region" in q
        ):

            rows = data["region_data"]

            if rows:

                worst = min(
                    rows,
                    key=lambda x: float(x[2])
                )

                st.success(
                    f"The region with the lowest profit "
                    f"is {worst[0]}, with profit of "
                    f"₹{float(worst[2]):,.2f}."
                )

        # HIGHEST PROFIT CATEGORY

        elif (
            "highest profit" in q
            and "categor" in q
        ):

            rows = data["category_data"]

            if rows:

                best = max(
                    rows,
                    key=lambda x: float(x[2])
                )

                st.success(
                    f"The category with the highest profit "
                    f"is {best[0]}, with profit of "
                    f"₹{float(best[2]):,.2f}."
                )

        # HIGHEST SALES REGION

        elif (
            "highest sales" in q
            and "region" in q
        ):

            region = data["highest_region"]

            if region:

                st.success(
                    f"The region with the highest sales "
                    f"is {region[0]}, with sales of "
                    f"₹{float(region[1]):,.2f}."
                )

        # HIGHEST SALES CATEGORY

        elif (
            "highest sales" in q
            and "categor" in q
        ):

            category = data["highest_category"]

            if category:

                st.success(
                    f"The category with the highest sales "
                    f"is {category[0]}, with sales of "
                    f"₹{float(category[1]):,.2f}."
                )

        # TOP REGIONS

        elif (
            "top" in q
            and "region" in q
        ):

            result = pd.DataFrame(
                data["top_regions"],
                columns=[
                    "Region",
                    "Sales",
                    "Profit"
                ]
            )

            result["Sales"] = result["Sales"].map(
                lambda x: f"₹{float(x):,.2f}"
            )

            result["Profit"] = result["Profit"].map(
                lambda x: f"₹{float(x):,.2f}"
            )

            st.subheader("Top 5 Regions by Profit")

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

        # COMPARE REGIONS

        elif "compare" in q:

            regions = [
                "west",
                "east",
                "south",
                "central"
            ]

            found = [
                region
                for region in regions
                if region in q
            ]

            if len(found) >= 2:

                result = compare_regions(
                    found[0].title(),
                    found[1].title()
                )

                result_map = {
                    str(row[0]).lower(): row
                    for row in result
                }

                first = result_map.get(found[0])

                second = result_map.get(found[1])

                if first and second:

                    first_profit = float(first[2])

                    second_profit = float(second[2])

                    if first_profit >= second_profit:

                        winner = first
                        loser = second

                    else:

                        winner = second
                        loser = first

                    difference = abs(
                        first_profit -
                        second_profit
                    )

                    st.success(
                        f"{winner[0]} is more profitable "
                        f"than {loser[0]}."
                    )

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        f"{first[0]} Profit",
                        f"₹{first_profit:,.2f}"
                    )

                    c2.metric(
                        f"{second[0]} Profit",
                        f"₹{second_profit:,.2f}"
                    )

                    c3.metric(
                        "Profit Difference",
                        f"₹{difference:,.2f}"
                    )

                else:

                    st.warning(
                        "Could not find both regions."
                    )

            else:

                st.warning(
                    "Example: Compare West and East"
                )

        # UNKNOWN

        else:

            st.info(
                """
                Try questions like:

                • What is the average order value?

                • What is our profit margin?

                • Which region has the highest profit?

                • Which region has the lowest profit?

                • Which category has the highest profit?

                • Which region has the highest sales?

                • Show me the top 5 regions by profit

                • Compare West and East
                """
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Business Analyst | Python + SQL + MySQL + Streamlit"
)
