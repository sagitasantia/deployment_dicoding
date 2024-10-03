import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title='E-commerce Data Analysis', page_icon=':shopping_cart:', layout='wide')

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('all_data.csv')  # Pastikan file all_data.csv ada di folder yang sama
    return data

# Pastikan df terdefinisi sebelum digunakan
df = load_data()

# Custom CSS for improved styling
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f7f7f7;
        padding: 20px;
    }
    .main-header {
        font-family: Arial, sans-serif;
        color: #4CAF50;
        text-align: center;
    }
    .metric-header {
        font-family: Arial, sans-serif;
        color: #333;
        font-size: 20px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar with filters
st.sidebar.title('Filter Data')

# Example filters
season = st.sidebar.selectbox('Season', ['Spring', 'Summer', 'Fall', 'Winter'])
weather = st.sidebar.selectbox('Weather Condition', ['Clear/Partly Cloudy', 'Light Snow/Rain', 'Misty/Cloudy', 'Severe Weather'])
temp_group = st.sidebar.selectbox('Temperature Group', ['Cool', 'Warm', 'Hot', 'Dingin'])

if st.sidebar.checkbox('Show filtered data'):
    st.write('Filtered data is shown here')

# Main section
st.markdown("<h1 class='main-header'>E-commerce Data Analysis Dashboard</h1>", unsafe_allow_html=True)

# Key Metrics Section
st.markdown("<h2 class='metric-header'>Key Metrics</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Users", "3,292", "50")
col2.metric("Average Temperature", "15°C", "-0.5°C")
col3.metric("Total Casual Users", "620,017", "5%")
col4.metric("Total Registered Users", "2,672,392", "-2%")

# Tab layout for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales Trends", "📦 Product Insights", "🛒 Customer Behavior", "📊 Additional Insights"])

with tab1:
    st.subheader('Sales Trends Over Time :calendar:')
    
    # Periksa apakah kolom yang digunakan ada di dataset
    if 'order_purchase_timestamp' in df.columns and 'price' in df.columns:
        sales_by_date = df.groupby('order_purchase_timestamp')['price'].sum().reset_index()
        sales_by_date['order_purchase_timestamp'] = pd.to_datetime(sales_by_date['order_purchase_timestamp'])
        sales_by_date = sales_by_date.set_index('order_purchase_timestamp').resample('M').sum()

        # Enhanced sales trend chart with color
        sales_chart = alt.Chart(sales_by_date.reset_index()).mark_line(color='#4CAF50').encode(
            x='order_purchase_timestamp:T',
            y=alt.Y('price:Q', title='Total Sales'),
            tooltip=[alt.Tooltip('order_purchase_timestamp:T', title='Date'), 
                     alt.Tooltip('price:Q', title='Total Sales', format=',.2f')]
        ).properties(
            title="Monthly Sales Trends",
            width=800,
            height=400
        ).interactive()

        st.altair_chart(sales_chart, use_container_width=True)
    else:
        st.error("Data yang diperlukan tidak ada dalam dataset.")

with tab2:
    st.subheader('Top and Least Selling Products by Category :package:')
    
    # Periksa apakah kolom yang digunakan ada di dataset
    if 'product_category_name_english' in df.columns and 'product_id' in df.columns and 'price' in df.columns:
        category = st.selectbox('Select Category', df['product_category_name_english'].unique())
        product_sales = df[df['product_category_name_english'] == category].groupby('product_id')['price'].sum().reset_index()
        
        top_selling = product_sales.sort_values(by='price', ascending=False).head(10)
        least_selling = product_sales.sort_values(by='price').head(10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write('Top 10 Selling Products')
            st.dataframe(top_selling)
        
        with col2:
            st.write('Least 10 Selling Products')
            st.dataframe(least_selling)
    else:
        st.error("Data yang diperlukan tidak ada dalam dataset.")

with tab3:
    st.subheader('Customer Spending in Recent Months :moneybag:')
    
    if 'customer_id' in df.columns and 'price' in df.columns:
        customer_spending = df.groupby('customer_id')['price'].sum().reset_index()
        customer_spending['price'] = customer_spending['price'].apply(lambda x: round(x, 2))
        st.write(customer_spending)
    else:
        st.error("Data yang diperlukan tidak ada dalam dataset.")
    
    st.subheader('Last Purchase Date per Customer :calendar:')
    
    if 'customer_id' in df.columns and 'order_purchase_timestamp' in df.columns:
        last_purchase = df.groupby('customer_id')['order_purchase_timestamp'].max().reset_index()
        last_purchase['order_purchase_timestamp'] = pd.to_datetime(last_purchase['order_purchase_timestamp'])
        st.write(last_purchase)
    else:
        st.error("Data yang diperlukan tidak ada dalam dataset.")

with tab4:
    st.subheader('Payment Installments :credit_card:')
    
    if 'payment_installments' in df.columns and 'price' in df.columns:
        installments = df.groupby('payment_installments')['price'].count().reset_index()
        installment_chart = alt.Chart(installments).mark_bar().encode(
            x='payment_installments:O',
            y='price:Q',
            color=alt.Color('price:Q', scale=alt.Scale(scheme='tealblues')),
            tooltip=['payment_installments:O', 'price:Q']
        ).properties(
            width=600,
            height=400
        ).interactive()
        
        st.altair_chart(installment_chart, use_container_width=True)
    else:
        st.error("Data yang diperlukan tidak ada dalam dataset.")

    # Enhanced seller ratings chart
    st.subheader('Seller Ratings :star:')
    
    if 'seller_id' in df.columns and 'seller_rating' in df.columns:
        seller_ratings = df.groupby('seller_id')['seller_rating'].mean().reset_index()
        seller_chart = alt.Chart(seller_ratings).mark_bar().encode(
            x=alt.X('seller_id:N', title='Seller ID'),
            y=alt.Y('seller_rating:Q', title='Average Rating'),
            color=alt.Color('seller_rating:Q', scale=alt.Scale(scheme='viridis')),
            tooltip=[alt.Tooltip('seller_id:N', title='Seller ID'), alt.Tooltip('seller_rating:Q', title='Avg Rating')]
        ).properties(
            width=600,
            height=400
        ).interactive()

        st.altair_chart(seller_chart, use_container_width=True)
    else:
        st.error("Data yang diperlukan tidak ada dalam dataset.")
    
    # Enhanced product ratings chart
    st.subheader('Product Ratings :star2:')
    
    if 'product_id' in df.columns and 'product_rating' in df.columns:
        product_ratings = df.groupby('product_id')['product_rating'].mean().reset_index()
        product_chart = alt.Chart(product_ratings).mark_bar().encode(
            x=alt.X('product_id:N', title='Product ID'),
            y=alt.Y('product_rating:Q', title='Average Rating'),
            color=alt.Color('product_rating:Q', scale=alt.Scale(scheme='reds')),
            tooltip=[alt.Tooltip('product_id:N', title='Product ID'), alt.Tooltip('product_rating:Q', title='Avg Rating')]
        ).properties(
            width=600,
            height=400
        ).interactive()

        st.altair_chart(product_chart, use_container_width=True)
    else:
        st.error("Data yang diperlukan tidak ada dalam dataset.")
