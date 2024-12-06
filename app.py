import streamlit as st
from query_engine import SalesDataQueryEngine

def main():
    st.title("Sales Data Analytics")
    st.write("Ask questions about your sales data!")

    # Initialize query engine
    @st.cache_resource
    def get_query_engine():
        return SalesDataQueryEngine()

    query_engine = get_query_engine()

    # Example queries
    example_queries = [
        "Show me the total orders for each year",
        "Who is our top customer by number of orders?",
        "What are our top 5 customers by sales value?",
        "How are sales distributed across product lines?",
        "Show me the sales distribution across countries",
        "What are the current order status counts?",
        "Show me monthly orders for 2023",
        "How many customers do we have in each country?"
    ]

    # Query input
    user_query = st.text_area("Enter your query:", height=100)
    
    # Example query selector
    selected_example = st.selectbox(
        "Or select an example query:",
        [""] + example_queries
    )

    # Use selected example if no custom query
    query_to_use = user_query or selected_example

    if st.button("Submit Query") and query_to_use:
        with st.spinner("Processing query..."):
            result = query_engine.query(query_to_use)
            st.markdown("### Results")
            st.write(result)

if __name__ == "__main__":
    main()