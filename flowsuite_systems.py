import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
import time

# Page Configuration
st.set_page_config(
    page_title="FlowSuite Pro™ | High-Intent Business Leads",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .urgency-badge {
        background: #ff4444;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .high-intent {
        background: #ff6b35;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
    }
    .pain-point {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .conversion-msg {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">⚡ FlowSuite Pro™ Lead Intelligence System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Identify chaos-driven business owners ready to invest $1,000 TODAY in operational transformation</div>', unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("🎯 Target Parameters")
st.sidebar.markdown("---")

# API Key Input
api_key = st.sidebar.text_input(
    "Google Places API Key",
    type="password",
    help="Get your free API key from Google Cloud Console. First $200/month is free."
)

st.sidebar.markdown("[📝 Get Free API Key](https://console.cloud.google.com/google/maps-apis/start)")

# Location targeting
location = st.sidebar.text_input("Target City/ZIP Code", "New York, NY")
radius = st.sidebar.slider("Search Radius (miles)", 1, 50, 10)

# Business type filters
business_types = st.sidebar.multiselect(
    "Target Business Types",
    [
        "Cleaning Services",
        "Restaurants & Cafes",
        "Beauty Salons & Spas",
        "Real Estate Agencies",
        "Auto Repair Shops",
        "Law Firms",
        "Medical Practices",
        "Fitness Studios",
        "Photography Studios",
        "Consulting Firms",
        "Landscaping Services",
        "HVAC Services"
    ],
    default=["Cleaning Services", "Restaurants & Cafes", "Beauty Salons & Spas"]
)

# Urgency filters
min_reviews = st.sidebar.slider("Min Reviews (growth indicator)", 10, 200, 50)
max_rating = st.sidebar.slider("Max Rating (room for improvement)", 3.0, 5.0, 4.2)

st.sidebar.markdown("---")
run_search = st.sidebar.button("🔍 Find High-Intent Leads", type="primary", use_container_width=True)

# Business type mapping to Google Places categories
BUSINESS_CATEGORY_MAP = {
    "Cleaning Services": "cleaning_service",
    "Restaurants & Cafes": "restaurant",
    "Beauty Salons & Spas": "beauty_salon",
    "Real Estate Agencies": "real_estate_agency",
    "Auto Repair Shops": "car_repair",
    "Law Firms": "lawyer",
    "Medical Practices": "doctor",
    "Fitness Studios": "gym",
    "Photography Studios": "photographer",
    "Consulting Firms": "consultant",
    "Landscaping Services": "landscaping",
    "HVAC Services": "plumber"
}

# Pain point identification engine
def identify_pain_points(business_data):
    """Analyze business data to identify operational pain points"""
    pain_points = []
    urgency_score = 0
    
    rating = business_data.get('rating', 0)
    review_count = business_data.get('user_ratings_total', 0)
    
    # High demand, low structure indicators
    if review_count > 100 and rating < 4.3:
        pain_points.append("High customer volume overwhelming current systems")
        urgency_score += 30
    
    if review_count > 50 and rating < 4.0:
        pain_points.append("Client dissatisfaction indicating service delivery breakdown")
        urgency_score += 40
    
    if 50 <= review_count <= 150:
        pain_points.append("Rapid growth phase without infrastructure")
        urgency_score += 35
    
    if rating < 4.5 and review_count > 30:
        pain_points.append("Inconsistent customer experience - broken workflows")
        urgency_score += 25
    
    # Always add relevant operational challenges
    if review_count > 75:
        pain_points.append("Scaling bottlenecks - team overwhelm")
        urgency_score += 20
    
    return pain_points, min(urgency_score, 100)

# Conversion messaging generator
def generate_conversion_message(business_name, pain_points, urgency_score):
    """Generate high-converting outreach messaging"""
    
    if urgency_score >= 80:
        urgency_level = "CRITICAL"
        opener = f"{business_name} is hemorrhaging money through operational chaos RIGHT NOW."
    elif urgency_score >= 60:
        urgency_level = "HIGH"
        opener = f"{business_name} is at a breaking point - growth is stalling due to systems failure."
    else:
        urgency_level = "MODERATE"
        opener = f"{business_name} has untapped potential locked behind disorganized operations."
    
    message = f"""
**{urgency_level} URGENCY | FlowSuite Pro™ Strategy & Structure Consultation**

{opener}

**What we see:**
{chr(10).join([f"• {p}" for p in pain_points[:3]])}

**The cost of waiting:** $10,000-$50,000 in lost revenue per month through inefficiency, client churn, and team burnout.

**The FlowSuite Pro™ solution:** We architect bulletproof systems that eliminate chaos, streamline client flow, and build operational infrastructure that scales.

**Your next step:** Book your $1,000 FlowSuite Pro™ Strategy & Structure Consultation where we:
- Audit your current operational chaos (all of it)
- Blueprint your custom flow architecture  
- Map your 90-day transformation roadmap
- Provide immediate actionable fixes

This isn't consulting. This is operational warfare. We fix what's broken, build what's missing, and install systems that run without you.

**Limited availability:** 3 strategy calls this week. Book now or stay stuck.
"""
    
    return message, urgency_level

# Geocode location
def geocode_location(location, api_key):
    """Convert address to lat/lng"""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            location_data = data['results'][0]['geometry']['location']
            return location_data['lat'], location_data['lng']
    except Exception as e:
        st.error(f"Geocoding error: {str(e)}")
    
    return None, None

# Search businesses using Google Places API
def search_businesses(api_key, lat, lng, radius_miles, business_type):
    """Search for businesses using Google Places API"""
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    radius_meters = radius_miles * 1609.34
    
    params = {
        "location": f"{lat},{lng}",
        "radius": int(radius_meters),
        "type": business_type,
        "key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            return data.get('results', [])
        else:
            st.warning(f"API Status: {data['status']}")
    except Exception as e:
        st.error(f"Search error: {str(e)}")
    
    return []

# Main execution
if run_search and api_key:
    with st.spinner("🔍 Scanning for high-intent business owners experiencing operational chaos..."):
        # Geocode location
        lat, lng = geocode_location(location, api_key)
        
        if lat and lng:
            all_leads = []
            
            # Search for each business type
            for biz_type in business_types:
                category = BUSINESS_CATEGORY_MAP.get(biz_type)
                if category:
                    time.sleep(0.5)  # Rate limiting
                    results = search_businesses(api_key, lat, lng, radius, category)
                    
                    for business in results:
                        rating = business.get('rating', 0)
                        reviews = business.get('user_ratings_total', 0)
                        
                        # Filter based on criteria
                        if reviews >= min_reviews and rating <= max_rating:
                            pain_points, urgency = identify_pain_points(business)
                            conversion_msg, urgency_level = generate_conversion_message(
                                business.get('name'),
                                pain_points,
                                urgency
                            )
                            
                            lead = {
                                'business_name': business.get('name'),
                                'address': business.get('vicinity'),
                                'rating': rating,
                                'reviews': reviews,
                                'business_type': biz_type,
                                'urgency_score': urgency,
                                'urgency_level': urgency_level,
                                'pain_points': pain_points,
                                'conversion_message': conversion_msg,
                                'place_id': business.get('place_id')
                            }
                            all_leads.append(lead)
            
            # Sort by urgency score
            all_leads = sorted(all_leads, key=lambda x: x['urgency_score'], reverse=True)
            
            # Display results
            if all_leads:
                st.success(f"✅ Found {len(all_leads)} high-intent businesses experiencing operational chaos")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Leads", len(all_leads))
                with col2:
                    critical = len([l for l in all_leads if l['urgency_score'] >= 80])
                    st.metric("🔥 Critical Urgency", critical)
                with col3:
                    avg_reviews = sum([l['reviews'] for l in all_leads]) / len(all_leads)
                    st.metric("Avg Reviews", f"{avg_reviews:.0f}")
                with col4:
                    potential_revenue = len(all_leads) * 1000
                    st.metric("Pipeline Value", f"${potential_revenue:,}")
                
                st.markdown("---")
                
                # Display leads
                for idx, lead in enumerate(all_leads, 1):
                    with st.expander(
                        f"{'🔥' if lead['urgency_score'] >= 80 else '⚡'} #{idx} | {lead['business_name']} | "
                        f"{lead['urgency_level']} URGENCY ({lead['urgency_score']}/100)"
                    ):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Business:** {lead['business_name']}")
                            st.markdown(f"**Type:** {lead['business_type']}")
                            st.markdown(f"**Location:** {lead['address']}")
                            st.markdown(f"**Rating:** {lead['rating']} ⭐ ({lead['reviews']} reviews)")
                            
                            st.markdown("### 🚨 Identified Pain Points:")
                            for pain in lead['pain_points']:
                                st.markdown(f'<div class="pain-point">• {pain}</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"### Urgency Score")
                            st.progress(lead['urgency_score'] / 100)
                            st.markdown(f"**{lead['urgency_score']}/100**")
                            
                            if lead['urgency_score'] >= 80:
                                st.error("🔥 CLOSE TODAY")
                            elif lead['urgency_score'] >= 60:
                                st.warning("⚡ HIGH PRIORITY")
                            else:
                                st.info("📊 QUALIFIED LEAD")
                        
                        st.markdown("---")
                        st.markdown("### 💬 High-Converting Outreach Message:")
                        st.markdown(f'<div class="conversion-msg">{lead["conversion_message"]}</div>', unsafe_allow_html=True)
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.button(f"📧 Email {lead['business_name']}", key=f"email_{idx}")
                        with col2:
                            st.button(f"📞 Call Now", key=f"call_{idx}")
                        with col3:
                            st.button(f"➕ Add to CRM", key=f"crm_{idx}")
                
                # Export functionality
                st.markdown("---")
                df = pd.DataFrame(all_leads)
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Export All Leads to CSV",
                    csv,
                    f"flowsuite_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No businesses found matching your criteria. Try adjusting filters.")
        else:
            st.error("Unable to geocode location. Please check the address.")

elif run_search and not api_key:
    st.error("⚠️ Please enter your Google Places API Key in the sidebar")
    st.info("""
    **To get your FREE Google Places API Key:**
    1. Go to [Google Cloud Console](https://console.cloud.google.com/)
    2. Create a new project
    3. Enable "Places API"
    4. Create credentials (API Key)
    5. You get $200 FREE credit per month!
    """)

# Information panel
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Pain Point Categories")
    st.markdown("""
    **Overwhelm Indicators:**
    - High review volume + declining rating
    - Inconsistent service delivery
    - Growth without infrastructure
    
    **System Failure Signs:**
    - Client dissatisfaction patterns
    - Operational bottlenecks
    - Team burnout signals
    
    **Revenue Leak Triggers:**
    - Poor workflow efficiency
    - Scheduling chaos
    - Communication breakdowns
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Conversion Strategy")
    st.markdown("""
    **Language Framework:**
    - Speak their pain (chaos, overwhelm)
    - Quantify the cost (lost revenue)
    - Present the solution (systems)
    - Create urgency (limited availability)
    
    **$1,000 Consultation Positioning:**
    - Not consulting → Operational warfare
    - Not advice → Transformation roadmap
    - Not theory → Immediate fixes
    """)

# Footer
st.markdown("---")
st.caption("⚡ FlowSuite Pro™ Lead Intelligence System | Built for High-Authority Systems Strategists")
st.caption("💡 Powered by real-time Google Places data + Urgency Intelligence Engine")
