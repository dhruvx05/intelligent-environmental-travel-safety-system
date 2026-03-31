import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import warnings

warnings.filterwarnings('ignore')

# --- Page Config ---
st.set_page_config(page_title="Travel Safety Risk Assessment", layout="wide", page_icon="🌍")

# --- Custom Styling ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .report-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border-left: 5px solid #3498db;
    }
    .kpi-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .kpi-value { font-size: 24px; font-weight: bold; color: #2c3e50; }
    .kpi-label { font-size: 14px; color: #7f8c8d; text-transform: uppercase; }
    .safe-text { color: #27ae60; font-weight: bold; }
    .mod-text { color: #f39c12; font-weight: bold; }
    .high-text { color: #c0392b; font-weight: bold; }
    .intro-box {
        background-color: #e8f4f8;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        border: 1px solid #bce0fd;
    }
    h1, h2, h3, h4 { color: #2c3e50; }
    </style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("india_aqi_with_states.csv")
    except Exception as e:
        df = pd.read_csv("india_aqi_2015_2023_all_cities.csv")
        df['State'] = "Unknown"
        
    df['date'] = pd.to_datetime(df['date'])
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month
    df['Month_Name'] = df['date'].dt.strftime('%b')
    df['City'] = df['City'].astype(str).str.replace('_AQIBulletins', '', regex=False).str.replace('%28', '(', regex=False).str.replace('%29', ')', regex=False)
    
    def map_aqi_to_safety(aqi_category):
        if pd.isna(aqi_category): return "Unknown"
        cat = str(aqi_category).strip().lower()
        if cat in ['good', 'satisfactory']: return "Safe"
        elif cat == 'moderate': return "Moderate Exposure"
        elif cat in ['poor', 'very poor', 'severe']: return "High Exposure"
        return "Unknown"
        
    df['Travel_Safety_Status'] = df['Air Quality'].apply(map_aqi_to_safety)
    df = df.dropna(subset=['Air Quality', 'Index Value'])
    return df

@st.cache_data
def load_population_data():
    try:
        # Robust parsing for unknown Census formatting
        pop_df = pd.read_excel('population.xlsx', header=3)
        mapping = {}
        for _, row in pop_df.iterrows():
            for c in pop_df.columns:
                if isinstance(row[c], str) and len(str(row[c]).strip()) > 2:
                    nums = pd.to_numeric(row, errors='coerce').dropna()
                    if not nums.empty:
                        mapping[str(row[c]).strip().lower()] = nums.max()
        return mapping
    except Exception:
        return {}

@st.cache_resource
def compute_backend_risk_model(df):
    """
    Random Forest trains in the background strictly to estimate current visitation risks.
    """
    model_df = df.dropna(subset=['Travel_Safety_Status', 'Month', 'Year', 'City', 'Index Value']).copy()
    if len(model_df) == 0:
        return None, None, None, None
        
    model_df = model_df.sample(min(20000, len(model_df)), random_state=42)
    le_city = LabelEncoder()
    le_status = LabelEncoder()
    
    X = pd.DataFrame()
    X['Month'] = model_df['Month']
    X['Location'] = le_city.fit_transform(model_df['City'])
    X['Year'] = model_df['Year']
    
    y_clf = le_status.fit_transform(model_df['Travel_Safety_Status'])
    y_reg = model_df['Index Value']
    
    rf_clf = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
    rf_clf.fit(X, y_clf)
    
    return rf_clf, le_city, le_status

# --- Main App Execution ---
df = load_data()
pop_map = load_population_data()
rf_clf, le_city, le_status = compute_backend_risk_model(df)

# Top Intro
st.title("🌍 Environmental Travel Risk Assessment")
st.markdown("""
<div class="intro-box">
    <h4>About This Application</h4>
    <p>Welcome to the Intelligent Environmental Risk Assessment Tool. Rather than showing you overwhelming historical charts or technical data, this application acts as your <b>personal travel-safety advisor</b>.</p>
    <p><b>How it works:</b> Simply select your destination State, City, and the Month you plan to visit. The system's predictive intelligence continuously evaluates environmental patterns to generate a comprehensive, easy-to-read safety report. It provides actionable suggestions to ensure your visit is safe and comfortable.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Routing
st.sidebar.header("Travel Configuration")

# 1. State Selection
states = sorted([str(s) for s in df['State'].dropna().unique() if str(s) != "Unknown State"])
# Fallback if states missing
if not states:
    states = ["Unknown"]

selected_state = st.sidebar.selectbox("1. Select State/Region", states)

# 2. City Selection
cities_in_state = sorted(df[df['State'] == selected_state]['City'].unique()) if states != ["Unknown"] else sorted(df['City'].unique())
selected_city = st.sidebar.selectbox("2. Select Destination (City/District)", cities_in_state)

# 3. Travel Month Selection
current_month = datetime.datetime.now().month
months_dict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
inv_months = {v: k for k, v in months_dict.items()}

selected_month_name = st.sidebar.selectbox("3. When are you traveling? (Month)", list(inv_months.keys()), index=current_month-1)
selected_month_val = inv_months[selected_month_name]

current_year = datetime.datetime.now().year
valid_years = list(range(2015, 2027))
target_year = st.sidebar.selectbox("4. Target Year (Forecast included)", valid_years, index=valid_years.index(current_year))

# Generate predictions
predicted_safety = "Data Unavailable"
pred_color = "safe-text"

if rf_clf is not None and selected_city in le_city.classes_:
    encoded_city = le_city.transform([selected_city])[0]
    pred = rf_clf.predict(pd.DataFrame({'Month': [selected_month_val], 'Location': [encoded_city], 'Year': [target_year]}))
    predicted_safety = le_status.inverse_transform(pred)[0]
    
    if predicted_safety == "Safe":
        pred_color = "safe-text"
        icon = "✅"
    elif predicted_safety == "Moderate Exposure":
        pred_color = "mod-text"
        icon = "⚠️"
    else:
        pred_color = "high-text"
        icon = "🛑"
else:
    icon = "❓"

# Determine some specific stats for the selected destination/month
city_month_df = df[(df['City'] == selected_city) & (df['Month'] == selected_month_val)]
dom_pollutant = "N/A"
if not city_month_df.empty and 'Prominent Pollutant' in city_month_df.columns:
    try:
        dom_pollutant = city_month_df['Prominent Pollutant'].mode().iloc[0]
    except:
        pass

# Determine best alternative months
city_df = df[df['City'] == selected_city]
best_month_str = "Monitoring Required"
if not city_df.empty:
    m_stats = city_df[city_df['Travel_Safety_Status'] == 'Safe'].groupby('Month_Name').size()
    if not m_stats.empty:
        best_month_str = ", ".join(m_stats.nlargest(3).index.tolist())

# --- Report UI ---
st.markdown(f"## Visitor Risk Assessment: {selected_city}, {selected_state}")
st.markdown(f"**Travel Window:** {selected_month_name}")

# Assess Crowd / Physical Security Risk
city_clean = selected_city.lower()
state_clean = selected_state.lower()
city_pop = pop_map.get(city_clean, pop_map.get(state_clean, pop_map.get(state_clean.upper(), 500000)))

if city_pop > 2000000:
    crowd_risk = "High Physical Crowd Density"
    crowd_desc = "Major metropolitan density. Expect sustained heavy crowding at tourist hubs, transit stations, and markets. Physical security requires heightened vigilance against pickpocketing and stampede risks during peak events."
    crowd_color = "high-text"
elif city_pop > 500000:
    crowd_risk = "Moderate Urban Crowding"
    crowd_desc = "Standard urban density. Crowds will be concentrated at major attractions. General situational awareness is sufficient for standard physical security."
    crowd_color = "mod-text"
else:
    crowd_risk = "Low/Manageable Density"
    crowd_desc = "Manageable crowd levels. Lower footprint of physical security risks associated with large gatherings."
    crowd_color = "safe-text"

st.markdown(f'<div class="report-card"><h3>🏢 Physical Security & Crowd Risk: <span class="{crowd_color}">{crowd_risk}</span></h3>', unsafe_allow_html=True)
st.markdown(f"**Population Density Assessment:** {crowd_desc}")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="report-card"><h3>{icon} Environmental Hazard Status: <span class="{pred_color}">{predicted_safety}</span></h3>', unsafe_allow_html=True)

if predicted_safety == "Safe":
    st.markdown("""
    **Assessment Summary:** 
    Environmental conditions are projected to be clean and stable during your visit. You are unlikely to face respiratory stress or visibility issues caused by air quality.

    **Actionable Suggestions for Visitors:**
    * **Outdoor Activities:** Excellent time for sightseeing, hiking, or extended outdoor tours.
    * **Health Precautions:** No special environmental health precautions are needed for the general public.
    * **Itinerary Setup:** Highly suitable for long-duration stays and extensive travel.
    """)

elif predicted_safety == "Moderate Exposure":
    st.markdown(f"""
    **Assessment Summary:** 
    Environmental conditions are acceptable but may show signs of moderate pollution. The primary expected pollutant is roughly tracked as **{dom_pollutant}**.
    
    **Actionable Suggestions for Visitors:**
    * **Outdoor Activities:** General tourism is completely fine, though you might notice reduced visibility in the early mornings or late evenings.
    * **Health Precautions:** Unusually sensitive individuals (e.g., those with asthma) should carry their standard medications and consider reducing heavy outdoor exertion.
    * **Itinerary Setup:** Short to medium stays are recommended. Balance outdoor sightseeing with indoor visits (museums, galleries).
    """)

else:
    st.markdown(f"""
    **Assessment Summary:** 
    **High Environmental Risk Warning.** The location experiences significant physical exposure risks during this month, primarily driven by persistent {dom_pollutant} levels and seasonal atmospheric patterns.

    **Actionable Suggestions for Visitors:**
    * **Outdoor Activities:** Strongly consider rescheduling extensive outdoor sightseeing. Visibility for photography or scenic views will be heavily disrupted.
    * **Health Precautions:** The general public may experience discomfort. It is highly recommended to wear an N-95 rated particulate mask if you must be outdoors for extended periods. 
    * **Itinerary Setup:** Best suited for very short visits if necessary, or strict indoor-focused itineraries (shopping, indoor attractions).
    * **Alternative Timing:** If your schedule is flexible, consider visiting during the safest historical months: **{best_month_str}**.
    """)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### Destination Profile Snapshots & Visual Assessments")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Historically Safest Months</div>
        <div class="kpi-value safe-text">{best_month_str}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Likely Pollutant Tracker</div>
        <div class="kpi-value">{dom_pollutant}</div>
    </div>
    """, unsafe_allow_html=True)

# --- Visualizations ---
st.markdown("---")
st.markdown("#### Comprehensive Risk Visualizations")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    # Radar Chart
    respiratory_risk = 2 if predicted_safety == "Safe" else (6 if predicted_safety == "Moderate Exposure" else 9)
    visibility_risk = 2 if predicted_safety == "Safe" else (5 if predicted_safety == "Moderate Exposure" else 8)
    crowd_risk_score = 8 if crowd_risk == "High Physical Crowd Density" else (5 if crowd_risk == "Moderate Urban Crowding" else 2)
    
    radar_data = pd.DataFrame({
        'r': [respiratory_risk, visibility_risk, crowd_risk_score],
        'theta': ['Respiratory Hazard', 'Visibility Disruption', 'Physical Crowd Density']
    })
    
    fig_radar = px.line_polar(radar_data, r='r', theta='theta', line_close=True, range_r=[0, 10], 
                              title="Multi-Dimensional Risk Footprint (0-10 Scale)")
    fig_radar.update_traces(fill='toself', line_color='#e74c3c')
    st.plotly_chart(fig_radar, use_container_width=True)

with viz_col2:
    # Temporal Forecasting Bar Chart with Linear Extrapolation
    if not city_df.empty and selected_city in le_city.classes_:
        yearly_data = city_df[city_df['Month'] == selected_month_val].groupby('Year')['Index Value'].mean().reset_index()
        yearly_data['Type'] = 'Historical Recorded'
        
        # Linear Extrapolation for trend since RF averages out
        future_preds = []
        if len(yearly_data) > 1:
            z = np.polyfit(yearly_data['Year'], yearly_data['Index Value'], 1)
            p = np.poly1d(z)
            
            max_year = int(df['Year'].max()) if pd.notna(df['Year'].max()) else 2024
            future_years = [max_year + 1, max_year + 2, max_year + 3]
            
            for y in future_years:
                future_preds.append({'Year': y, 'Index Value': max(0, p(y)), 'Type': 'AI Trend Forecast'})
                
        trend_df = pd.concat([yearly_data, pd.DataFrame(future_preds)], ignore_index=True)
        trend_df['Year'] = trend_df['Year'].astype(int).astype(str)
        
        fig_bar = px.bar(trend_df, x='Year', y='Index Value', color='Type',
                         color_discrete_map={'Historical Recorded': '#3498db', 'AI Trend Forecast': '#f1c40f'},
                         title=f"Yearly Hazard Index & Future Forecast ({selected_month_name})")
        fig_bar.update_layout(showlegend=True, xaxis_title="Year", yaxis_title="Average Hazard Index", legend_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

st.caption("Intelligence powered by historical assessment modeling. Stay safe and enjoy your travels! 🌍")
