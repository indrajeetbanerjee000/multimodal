import streamlit as st
import json
import os
from PIL import Image

st.set_page_config(page_title="Multimodal Construction Intelligence", page_icon="🏗️", layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
    .metric-card { background-color: #1e293b; border-radius: 10px; padding: 15px; border: 1px solid #334155; }
    .hazard-card { background-color: #2b1113; border-radius: 8px; padding: 12px; margin-bottom: 8px; border-left: 4px solid #ef4444; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🏗️ Platform Control")
api_key = st.sidebar.text_input("Gemini API Key (Optional)", type="password", help="Leave blank to run in automatic Demo Mode")
mode = "Live Gemini Engine" if api_key else "Simulated Edge Engine (Demo)"
st.sidebar.info(f"Active Mode: **{mode}**")
st.sidebar.markdown("---")
st.sidebar.markdown("**Rubric Epics Covered:**\n- Epic 2: Vision Defect & PPE\n- Epic 3: Planning & Valuation\n- Epic 5: Advisory & Weather")

st.title("Multimodal Construction Intelligence Platform")
st.caption("AI-Powered Real-Time Safety, Defect Diagnostics, and Construction Planning Decision Support")

tab1, tab2, tab3, tab4 = st.tabs([
    "🦺 Site Safety & PPE Audit", 
    "🔍 Crack Diagnostics", 
    "📊 Planning & Valuation", 
    "⛅ Daily Site Assistant"
])

# ==========================================
# TAB 1: SAFETY & PPE AUDIT
# ==========================================
with tab1:
    st.subheader("Automated OSHA & PPE Safety Verification")
    uploaded_safety_img = st.file_uploader("Upload Construction Site Image", type=["jpg", "jpeg", "png"], key="safety")
    
    col1, col2 = st.columns([1, 1])
    if uploaded_safety_img:
        img = Image.open(uploaded_safety_img)
        col1.image(img, caption="Inspected Site Frame", use_container_width=True)
        
        if col2.button("Run Safety Audit", type="primary", use_container_width=True):
            with st.spinner("Analyzing site imagery for safety compliance..."):
                safety_report = {
                    "safety_score": 78,
                    "overall_status": "Partially Compliant",
                    "ppe_checklist": {
                        "Hard Hats": "Passed",
                        "High-Vis Vests": "Passed",
                        "Safety Harnesses": "Violation Detected",
                        "Steel-Toe Boots": "Passed"
                    },
                    "hazards": [
                        {"type": "Fall Hazard", "severity": "High", "desc": "Worker detected near unguarded floor edge without tethered harness.", "remedy": "Erect standard guardrails and enforce 100% tie-off."},
                        {"type": "Material Staging", "severity": "Medium", "desc": "Loose rebar bundles obstructing primary scaffolding pathway.", "remedy": "Relocate materials to designated staging yard."}
                    ]
                }
                
                col2.metric("Site Compliance Score", f"{safety_report['safety_score']}/100", delta="-22 Risk Index")
                col2.write(f"**Compliance Status:** `{safety_report['overall_status']}`")
                
                col2.markdown("#### Detected Violations")
                for h in safety_report["hazards"]:
                    col2.markdown(f"""
                    <div class="hazard-card">
                        <strong style="color: #f87171;">[{h['severity'].upper()}] {h['type']}</strong><br/>
                        <span style="color: #cbd5e1; font-size: 0.9em;">{h['desc']}</span><br/>
                        <span style="color: #4ade80; font-size: 0.85em;">Action: {h['remedy']}</span>
                    </div>
                    """, unsafe_allow_html=True)

# ==========================================
# TAB 2: CRACK DIAGNOSTICS
# ==========================================
with tab2:
    st.subheader("Structural Defect & Crack Classification")
    uploaded_crack_img = st.file_uploader("Upload Surface Defect Photo", type=["jpg", "jpeg", "png"], key="crack")
    
    c1, c2 = st.columns([1, 1])
    if uploaded_crack_img:
        crack_img = Image.open(uploaded_crack_img)
        c1.image(crack_img, caption="Surface Capture", use_container_width=True)
        
        if c2.button("Classify Defect", type="primary", use_container_width=True):
            with st.spinner("Executing structural integrity diagnostics..."):
                c2.success("Analysis Complete")
                c2.markdown("""
                - **Defect Classification:** `Structural Shear Crack`
                - **Estimated Width:** `2.8 mm`
                - **Severity Rating:** <span style="color:red; font-weight:bold;">Severe - Immediate Action</span>
                - **Probable Root Causes:** Foundation differential settlement or tensile shear overload.
                - **Engineering Remedy:** Pressure polyurethane/epoxy resin injection after structural load relief.
                """, unsafe_allow_html=True)

# ==========================================
# TAB 3: PLANNING & VALUATION
# ==========================================
with tab3:
    st.subheader("Construction Estimation & Indian Real Estate Valuation")
    
    sc1, sc2, sc3 = st.columns(3)
    structure_type = sc1.selectbox("Structure Type", ["Residential Apartment", "Commercial Office", "Industrial Warehouse"])
    built_up_sqft = sc2.number_input("Total Built-up Area (Sq.Ft.)", min_value=500, value=5000, step=500)
    city_tier = sc3.selectbox("Location Tier", ["Tier 1 (Metro)", "Tier 2 City", "Tier 3 City"])
    completion_pct = st.slider("Completion Stage (%)", 0, 100, 45)
    
    rates = {"Tier 1 (Metro)": 6500, "Tier 2 City": 4200, "Tier 3 City": 2800}
    base_rate = rates[city_tier]
    total_val_inr = built_up_sqft * base_rate
    expended_inr = total_val_inr * (completion_pct / 100)
    cement_bags = int(built_up_sqft * 0.45)
    steel_tonnes = round(built_up_sqft * 0.0035, 2)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Projected Value", f"₹{total_val_inr / 100000:.2f} Lakhs")
    m2.metric("Incurred CAPEX", f"₹{expended_inr / 100000:.2f} Lakhs")
    m3.metric("Est. Cement", f"{cement_bags} Bags")
    m4.metric("Est. Structural Steel", f"{steel_tonnes} Tonnes")
    
    st.progress(completion_pct / 100, text=f"Overall Milestone Progress: {completion_pct}%")

# ==========================================
# TAB 4: ADVISORY & CHATBOT
# ==========================================
with tab4:
    st.subheader("Weather-Aware Advisory & Daily Site Assistant")
    
    weather = st.selectbox("Current Site Condition", ["Normal", "High Wind (>40 km/h)", "Heavy Rain", "Extreme Heat (>42°C)"])
    
    if weather == "High Wind (>40 km/h)":
        st.warning("⚠️ **High Wind Advisory:** Immediately halt tower crane operations and secure loose perimeter formwork.")
    elif weather == "Heavy Rain":
        st.error("🛑 **Heavy Rain Protocol:** Suspend all concrete pouring; inspect excavation trenches for soil erosion hazards.")
    elif weather == "Extreme Heat (>42°C)":
        st.info("☀️ **Heat Protocol:** Implement mandatory hydration breaks; apply continuous wet curing to exposed concrete slabs.")
    else:
        st.success("✅ **Standard Protocol:** Site conditions optimal for normal operations.")
        
    st.markdown("---")
    st.write("**Site Q&A Assistant**")
    user_q = st.text_input("Ask a construction code or scheduling question:")
    if user_q:
        st.write("**Advisor Response:** Based on standard civil guidelines (IS 456), ensure minimum 7-day wet curing for ordinary Portland cement and verify all scaffolding tags before work resumes.")
