# query_templates.py
class QueryTemplates:
    TEMPLATES = {
        "yearly_orders": """
            Analyze the entire dataset and provide:
            - Total number of orders for each year
            - Present in chronological order
            - Include percentage of total orders
            Use exact numbers and format consistently.
        """,
        "top_customer_by_orders": """
            Analyze the dataset to find:
            - Customer with highest number of orders
            - Include their total order count
            - Include customer name and ID
            - Show what percentage of total orders they represent
            Use exact numbers and format consistently.
        """,
        "top_5_customers_by_sales": """
            Find and list the top 5 customers by total sales value:
            For each customer provide:
            - Customer name
            - Total sales amount
            - Number of orders
            - Average order value
            Sort by total sales descending and use exact numbers.
        """,
        "product_line_sales": """
            Analyze sales performance by product line:
            - List each product line with total sales
            - Sort by sales value (highest first)
            - Include percentage of total sales
            - Include total number of orders
            Use exact numbers and format consistently.
        """,
        "country_sales_distribution": """
            Analyze sales distribution across countries:
            For each country show:
            - Total sales value
            - Number of orders
            - Number of unique customers
            - Percentage of global sales
            Sort by total sales and use exact numbers.
        """,
        "order_status_counts": """
            Provide exact counts for:
            - Total number of orders
            - Orders by status (shipped, disputed, canceled)
            - Include percentage for each status
            Use exact numbers and format consistently.
        """,
        "monthly_orders": """
            Analyze orders for {year}:
            For each month provide:
            - Order count
            - Total sales value
            - Average order value
            Sort chronologically and use exact numbers.
        """,
        "customers_by_country": """
            Analyze customer distribution by country:
            - Number of unique customers per country
            - Sort by customer count (highest first)
            - Include percentage of total customers
            - Include total sales per country
            Use exact numbers and format consistently.
        """
    }