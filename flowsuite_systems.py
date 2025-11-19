import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Business Systems Lead Finder",
    page_icon="🎯",
    layout="wide"
)

# Title and description
st.title("🎯 Business Systems & Automation Lead Finder")
st.markdown("""
Find service-based businesses that could benefit from:
- Business systems & operational frameworks
- Automation workflows
- Client-flow mapping
- Strategic operational tools
""")

# Sidebar filters
st.sidebar.header("Filters")
industry = st.sidebar.selectbox(
    "Industry Focus",
    ["All", "Technology", "Consulting", "Healthcare", "Education", "Finance"]
)

company_size = st.sidebar.selectbox(
    "Company Size",
    ["All", "1-10", "11-50", "51-200", "201+"]
)

# Function to fetch data from free API
@st.cache_data(ttl=3600)
def fetch_business_data():
    """Fetch business data from JSONPlaceholder (demo API)"""
    try:
        # Using JSONPlaceholder as a free API demo
        # In production, replace with real business API
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        
        if response.status_code == 200:
            users = response.json()
            
            # Transform data to simulate business leads
            businesses = []
            for user in users:
                business = {
                    "Company": user['company']['name'],
                    "Contact": user['name'],
                    "Email": user['email'],
                    "Phone": user['phone'],
                    "Website": user['website'],
                    "Industry": ["Technology", "Consulting", "Healthcare", "Education", "Finance"][user['id'] % 5],
                    "Size": ["1-10", "11-50", "51-200", "201+"][user['id'] % 4],
                    "Pain Points": get_pain_points(user['id']),
                    "Opportunity Score": (user['id'] * 7) % 100,
                    "City": user['address']['city']
                }
                businesses.append(business)
            
            return pd.DataFrame(businesses)
        else:
            st.error("Failed to fetch data")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return pd.DataFrame()

def get_pain_points(user_id):
    """Generate relevant pain points based on user_id"""
    pain_points_list = [
        "Manual client onboarding",
        "Inefficient scheduling systems",
        "Poor workflow documentation",
        "Lack of automation",
        "Disorganized client data",
        "Time-consuming reporting",
        "Unclear business processes",
        "Manual invoicing"
    ]
    return pain_points_list[user_id % len(pain_points_list)]

# Fetch data
with st.spinner("Loading business leads..."):
    df = fetch_business_data()

# Apply filters
if not df.empty:
    filtered_df = df.copy()
    
    if industry != "All":
        filtered_df = filtered_df[filtered_df["Industry"] == industry]
    
    if company_size != "All":
        filtered_df = filtered_df[filtered_df["Size"] == company_size]
    
    # Sort by opportunity score
    filtered_df = filtered_df.sort_values("Opportunity Score", ascending=False)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(filtered_df))
    with col2:
        st.metric("Avg Opportunity Score", f"{filtered_df['Opportunity Score'].mean():.0f}%")
    with col3:
        st.metric("High Priority", len(filtered_df[filtered_df['Opportunity Score'] > 70]))
    with col4:
        st.metric("Industries", filtered_df['Industry'].nunique())
    
    st.markdown("---")
    
    # Display lead cards
    st.subheader("📋 Active Business Leads")
    
    for idx, row in filtered_df.iterrows():
        with st.expander(f"🏢 {row['Company']} - {row['Industry']} ({row['Opportunity Score']}% match)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Contact:** {row['Contact']}")
                st.markdown(f"**Email:** {row['Email']}")
                st.markdown(f"**Phone:** {row['Phone']}")
                st.markdown(f"**Website:** {row['Website']}")
                st.markdown(f"**Location:** {row['City']}")
            
            with col2:
                st.markdown(f"**Company Size:** {row['Size']} employees")
                st.markdown(f"**Industry:** {row['Industry']}")
                st.markdown(f"**Key Pain Point:** {row['Pain Points']}")
                
                # Opportunity indicator
                if row['Opportunity Score'] > 70:
                    st.success("🔥 High Priority")
                elif row['Opportunity Score'] > 40:
                    st.info("⚡ Medium Priority")
                else:
                    st.warning("📌 Low Priority")
            
            st.markdown("**Recommended Solutions:**")
            solutions = [
                "✅ Custom workflow automation",
                "✅ Client onboarding system",
                "✅ Process documentation framework",
                "✅ Strategic operations consulting"
            ]
            for solution in solutions[:3]:
                st.markdown(solution)
    
    # Download option
    st.markdown("---")
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Leads as CSV",
        data=csv,
        file_name=f"business_leads_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.warning("No data available. Please check your connection.")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Use filters in the sidebar to narrow down your target leads.")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
