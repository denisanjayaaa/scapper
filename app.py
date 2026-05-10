import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Real-Time Marketplace Price Aggregator", layout="wide")

st.title("🛒 Real-Time Marketplace Price Aggregator (Indonesia)")
st.write("Search for products across multiple marketplaces in real-time. We use AI to verify specs and filter bait prices.")
st.write("**Note**: Ensure the FastAPI backend is running on `http://localhost:8000`")

query = st.text_input("Enter product name (e.g., 'DDR4 8GB 3200MHz'):")

if st.button("Search Now"):
    if not query.strip():
        st.warning("Please enter a product name.")
    else:
        status_placeholder = st.empty()
        status_placeholder.info("Starting search engine... This will take a moment as it scrapes multiple sites.")

        try:
            response = requests.post("http://localhost:8000/search", json={"query": query}, timeout=300)

            if response.status_code == 200:
                results = response.json().get("results", [])
                status_placeholder.success("Search complete!")

                if results:
                    df = pd.DataFrame(results)
                    df['price'] = pd.to_numeric(df['price'], errors='coerce')
                    df = df.dropna(subset=['price'])
                    df = df.sort_values(by='price', ascending=True).reset_index(drop=True)

                    st.subheader(f"Results for '{query}' (Sorted by Cheapest)")
                    df['price_formatted'] = df['price'].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))

                    display_df = df[['platform', 'store_name', 'product_name', 'price_formatted', 'condition', 'link']].copy()

                    st.dataframe(
                        display_df,
                        column_config={
                            "link": st.column_config.LinkColumn("Buy Now"),
                            "price_formatted": "Price"
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.error("No valid results found. The AI might have filtered out bait prices or misaligned specs.")
            else:
                status_placeholder.error(f"Error from backend: {response.text}")
        except Exception as e:
            status_placeholder.error(f"Failed to connect to backend: {e}")
