import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime

st.set_page_config(page_title="Clarhet AI - Challenge Analyzer", layout="wide")
st.title("🧠 Clarhet AI: Test Site")

BASE_URL = "http://172.252.13.69:8026/api"

# --- Initialize Session State ---
trend_areas = [
    "customer_insights", "competitor_landscape", "technological_advances",
    "regulatory_and_legal", "economic_considerations", "supply_chain_logistics",
    "global_market_trends", "environmental_social_impact", "collaboration_partnerships",
    "scenarios_risk_assessment", "emerging_markets_opportunities", "on_the_radar"
]

if "trend_data" not in st.session_state:
    st.session_state.trend_data = {area: [{"question": "", "answer": "", "impact": "Medium"}] for area in trend_areas}

if "challenges" not in st.session_state:
    st.session_state.challenges = [{"title": "", "category": "", "impact_on_business": "moderate", "ability_to_address": "moderate", "description": "", "risk_score": None}]

if "vision_input" not in st.session_state:
    st.session_state.vision_input = ""

if "selected_vision" not in st.session_state:
    st.session_state.selected_vision = None

if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

if "strategic_themes" not in st.session_state:
    st.session_state.strategic_themes = [{"name": "", "description": ""}]

if "swot_payload" not in st.session_state:
    st.session_state.swot_payload = {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []}

if "capabilities" not in st.session_state:
    st.session_state.capabilities = [{"capability": "", "type": "Core"}]

if "business_goals" not in st.session_state:
    st.session_state.business_goals = [{
        "title": "", "description": "", "strategic_themes": [], "owner": "Ash",
        "funding": 0, "business_function": "IT", "term": "Long-term",
        "start_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "end_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "priority": "Medium", "progress": 0, "specific_strategic": "Yes",
        "resources_available": "Yes", "resources_explanation": "",
        "env_social_issues": "No", "env_social_details": "", "env_social_impact": "Low",
        "show_additional": False,
        "risks_challenges": "", "risks_impact": "Low",
        "regulatory_compliance": "", "regulatory_impact": "Low",
        "cultural_realignment": "", "cultural_impact": "Low",
        "change_management": "", "change_impact": "Low",
        "learning_development": "", "learning_impact": "Low",
        "other_detail": ""
    }]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Render Trend Input ---
def render_trend_section():
    st.header("🔍 Trends Input")
    
    for area in trend_areas:
        st.subheader(area.replace("_", " ").title())
        
        if st.button(f"➕ Add Question to {area.replace('_', ' ').title()}", key=f"add_{area}"):
            st.session_state.trend_data[area].append({"question": "", "answer": "", "impact": "Medium"})
            st.rerun()
        
        for i, entry in enumerate(st.session_state.trend_data[area]):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 3, 2, 1])
                
                entry["question"] = col1.text_input(
                    f"Question", 
                    value=entry["question"], 
                    key=f"{area}_q_{i}",
                    placeholder="Enter question"
                )
                
                entry["answer"] = col2.text_input(
                    f"Answer", 
                    value=entry["answer"], 
                    key=f"{area}_a_{i}",
                    placeholder="Enter answer"
                )
                
                entry["impact"] = col3.selectbox(
                    f"Impact", 
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(entry["impact"]),
                    key=f"{area}_i_{i}"
                )
                
                if i > 0 or len(st.session_state.trend_data[area]) > 1:
                    if col4.button("❌", key=f"remove_{area}_{i}", help="Remove this entry"):
                        st.session_state.trend_data[area].pop(i)
                        st.rerun()

    if st.button("📄 Get Trend Summary"):
        trends_payload = {}
        for area in trend_areas:
            valid_entries = []
            for entry in st.session_state.trend_data[area]:
                if entry["question"].strip() and entry["answer"].strip():
                    valid_entries.append({
                        "question": entry["question"].strip(),
                        "answer": entry["answer"].strip(),
                        "impact": entry["impact"]
                    })
            trends_payload[area] = valid_entries
        
        try:
            resp = requests.post(f"{BASE_URL}/trends/analyze", json=trends_payload)
            resp.raise_for_status()
            response_data = resp.json()
            st.subheader("📋 Trend Summary")
            
            if "summary" in response_data:
                st.markdown("### 🌟 Key Opportunities")
                st.markdown(response_data["summary"]["key_opportunities"] if "key_opportunities" in response_data["summary"] else "N/A")
                st.markdown("### 💪 Strengths")
                st.markdown(response_data["summary"]["strengths"] if "strengths" in response_data["summary"] else "N/A")
                st.markdown("### ⚠️ Significant Risks")
                st.markdown(response_data["summary"]["significant_risks"] if "significant_risks" in response_data["summary"] else "N/A")
                st.markdown("### 🏔 Challenges")
                st.markdown(response_data["summary"]["challenges"] if "challenges" in response_data["summary"] else "N/A")
                st.markdown("### 💡 Strategic Recommendations")
                st.markdown(response_data["summary"]["strategic_recommendations"] if "strategic_recommendations" in response_data["summary"] else "N/A")
                st.markdown("### ❌ Irrelevant Answers")
                for i, answer in enumerate(response_data["summary"].get("irrelevant_answers", [])):
                    st.markdown(f"{i+1}. {answer}")
                
                if "top_trends" in response_data and response_data["top_trends"]:
                    st.markdown("### 📈 Top Trends")
                    for trend in response_data["top_trends"]:
                        st.markdown(f"- {trend}")
                
                if "radar_executive_summary" in response_data and response_data["radar_executive_summary"]:
                    st.markdown("### 🔮 Radar Executive Summary")
                    for summary in response_data["radar_executive_summary"]:
                        st.markdown(f"- {summary}")
                
                if "radar_recommendation" in response_data and response_data["radar_recommendation"]:
                    st.markdown("### 🛠 Radar Recommendations")
                    for rec in response_data["radar_recommendation"]:
                        st.markdown(f"- {rec}")
            else:
                st.warning("No summary generated.")
                
        except requests.exceptions.HTTPError as e:
            error_response = e.response.json() if e.response else "No response details"
            st.error(f"API Error: {e}\nDetails: {error_response}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")

    trends_output = {}
    for area in trend_areas:
        valid_entries = []
        for entry in st.session_state.trend_data[area]:
            if entry["question"].strip() and entry["answer"].strip():
                valid_entries.append({
                    "question": entry["question"].strip(),
                    "answer": entry["answer"].strip(),
                    "impact": entry["impact"]
                })
        trends_output[area] = valid_entries
    
    return trends_output


# --- Render SWOT Input ---
def render_swot_section():
    st.header("🧭 SWOT Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Strengths")
        strengths = st.text_area(
            "Strengths (one per line)", 
            key="strengths_input",
            height=100,
            placeholder="Enter strengths, one per line"
        ).splitlines()
        
        st.subheader("Opportunities")
        opportunities = st.text_area(
            "Opportunities (one per line)", 
            key="opportunities_input",
            height=100,
            placeholder="Enter opportunities, one per line"
        ).splitlines()
    
    with col2:
        st.subheader("Weaknesses")
        weaknesses = st.text_area(
            "Weaknesses (one per line)", 
            key="weaknesses_input",
            height=100,
            placeholder="Enter weaknesses, one per line"
        ).splitlines()
        
        st.subheader("Threats")
        threats = st.text_area(
            "Threats (one per line)", 
            key="threats_input",
            height=100,
            placeholder="Enter threats, one per line"
        ).splitlines()

    swot_payload = {
        "strengths": [s.strip() for s in strengths if s.strip()],
        "weaknesses": [w.strip() for w in weaknesses if w.strip()],
        "opportunities": [o.strip() for o in opportunities if o.strip()],
        "threats": [t.strip() for t in threats if t.strip()]
    }

    if st.button("📊 Analyze SWOT"):
        if any(swot_payload.values()):
            try:
                resp = requests.post(f"{BASE_URL}/swot/analysis", json=swot_payload)
                resp.raise_for_status()
                response_data = resp.json()

                names = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
                percentages = [
                    int(response_data['scores']['strengths_percentage']),
                    int(response_data['scores']['weaknesses_percentage']),
                    int(response_data['scores']['opportunities_percentage']),
                    int(response_data['scores']['threats_percentage'])
                ]

                st.subheader("SWOT Scores")
                df = pd.DataFrame({
                    'Category': names,
                    'Percentage': percentages
                })
                st.bar_chart(df.set_index('Category')['Percentage'])

                with st.container():
                    st.markdown("### SWOT Recommendations")
                    st.markdown("#### Strengths")
                    st.write(response_data['recommendations']['strengths_recommendation'])
                    st.markdown("#### Weaknesses")
                    st.write(response_data['recommendations']['weaknesses_recommendation'])
                    st.markdown("#### Opportunities")
                    st.write(response_data['recommendations']['opportunities_recommendation'])
                    st.markdown("#### Threats")
                    st.write(response_data['recommendations']['threats_recommendation'])
                
            except requests.exceptions.HTTPError as e:
                error_response = e.response.json() if e.response else "No response details"
                st.error(f"API Error: {e}\nDetails: {error_response}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please enter at least one item in any SWOT category.")

    st.session_state.swot_payload = swot_payload
    return swot_payload

# --- Render Challenge Input ---
def render_challenge_section(swot_input, trend_input):
    st.header("🚨 Challenge Input")

    if st.button("➕ Add New Challenge"):
        st.session_state.challenges.append({
            "title": "", 
            "category": "", 
            "impact_on_business": "moderate", 
            "ability_to_address": "moderate", 
            "description": "", 
            "risk_score": None
        })
        st.rerun()

    for i, ch in enumerate(st.session_state.challenges):
        with st.expander(f"Challenge #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                ch["title"] = st.text_input(
                    "Title", 
                    value=ch.get("title", ""), 
                    key=f"ch_title_{i}",
                    placeholder="Enter challenge title"
                )
                
                ch["category"] = st.text_input(
                    "Category", 
                    value=ch.get("category", ""), 
                    key=f"ch_cat_{i}",
                    placeholder="Enter challenge category"
                )
                
            with col2:
                ch["impact_on_business"] = st.selectbox(
                    "Impact on Business", 
                    options=["very low", "low", "moderate", "high", "very high"], 
                    index=["very low", "low", "moderate", "high", "very high"].index(ch.get("impact_on_business", "moderate")), 
                    key=f"ch_imp_{i}"
                )
                
                ch["ability_to_address"] = st.selectbox(
                    "Ability to Address", 
                    options=["very low", "low", "moderate", "high", "very high"], 
                    index=["very low", "low", "moderate", "high", "very high"].index(ch.get("ability_to_address", "moderate")), 
                    key=f"ch_addr_{i}"
                )
            
            ch["description"] = st.text_area(
                "Description", 
                value=ch.get("description", ""), 
                key=f"ch_desc_{i}",
                placeholder="Enter detailed description of the challenge"
            )
            
            col_eval, col_remove = st.columns([3, 1])
            
            with col_eval:
                if st.button(f"⚖️ Evaluate Challenge #{i+1}", key=f"eval_ch_{i}"):
                    if ch["title"].strip() and ch["description"].strip():
                        challenge_data = {
                            "title": ch["title"].strip(),
                            "category": ch["category"].strip(),
                            "impact_on_business": ch["impact_on_business"],
                            "ability_to_address": ch["ability_to_address"],
                            "description": ch["description"].strip()
                        }
                        
                        payload = {
                            "challenge": challenge_data,
                            "swot": swot_input,
                            "trends": trend_input
                        }
                        
                        try:
                            resp = requests.post(f"{BASE_URL}/challenge/evaluate", json=payload)
                            resp.raise_for_status()
                            response_data = resp.json()
                            ch["risk_score"] = response_data.get("risk_score", "N/A")
                            
                            st.success(f"✅ Risk Score: {ch['risk_score']}")
                            if "evaluation" in response_data:
                                st.write("Evaluation Details:")
                                st.write(response_data["evaluation"])
                                
                        except requests.exceptions.HTTPError as e:
                            error_response = e.response.json() if e.response else "No response details"
                            st.error(f"API Error: {e}\nDetails: {error_response}")
                        except Exception as e:
                            st.error(f"Unexpected Error: {e}")
                    else:
                        st.warning("Please fill in at least the title and description.")
            
            with col_remove:
                if len(st.session_state.challenges) > 1:
                    if st.button(f"❌ Remove", key=f"remove_ch_{i}"):
                        st.session_state.challenges.pop(i)
                        st.rerun()
            
            if ch.get("risk_score") is not None:
                st.info(f"Current Risk Score: {ch['risk_score']}")

    if st.button("💡 Get Challenge Recommendations"):
        valid_challenges = [
            {
                "title": ch["title"].strip(),
                "category": ch["category"].strip(),
                "impact_on_business": ch["impact_on_business"],
                "ability_to_address": ch["ability_to_address"],
                "description": ch["description"].strip(),
                "risk_score": ch["risk_score"]
            }
            for ch in st.session_state.challenges
            if ch.get("title", "").strip() and ch.get("description", "").strip() and ch.get("risk_score") is not None
        ]
        
        if valid_challenges:
            try:
                payload = {
                    "challenges": valid_challenges,
                    "swot": swot_input,
                    "trends": trend_input
                }
                resp = requests.post(f"{BASE_URL}/challenge/recommendations", json=payload)
                resp.raise_for_status()
                response_data = resp.json()
                st.subheader("📋 Challenge Recommendations")
                
                with st.container():
                    if "recommendations" in response_data:
                        st.markdown("### Recommendations")
                        st.write(response_data["recommendations"])
                    elif "analysis" in response_data:
                        st.markdown("### Analysis")
                        st.write(response_data["analysis"])
                    else:
                        for key, value in response_data.items():
                            if isinstance(value, str) and value.strip():
                                st.markdown(f"### {key.replace('_', ' ').title()}")
                                st.write(value)
                
                if not response_data:
                    st.warning("No recommendations generated.")
                    
            except requests.exceptions.HTTPError as e:
                error_response = e.response.json() if e.response else "No response details"
                st.error(f"API Error: {e}\nDetails: {error_response}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please evaluate at least one challenge with title and description to get recommendations.")

# --- Render Vision Input ---
def render_vision_section():
    st.header("🌟 Vision Input")
    
    st.text_area(
        "Organization Vision",
        value=st.session_state.vision_input,
        key="vision_input",
        height=100,
        placeholder="Enter the organization's vision statement"
    )
    
    if st.button("🚀 Analyze Vision"):
        st.session_state.run_analysis = True
    
    if st.session_state.run_analysis and st.session_state.vision_input.strip():
        payload = {"vision_statement": st.session_state.vision_input.strip()}
        st.write("Payload sent to API:", payload)
        
        try:
            resp = requests.post(f"{BASE_URL}/blueprint/vision", json=payload)
            resp.raise_for_status()
            response_data = resp.json()
            
            st.session_state.vision_response = response_data
            
            st.subheader("📊 Vision Score")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=response_data.get("vision_score", 0),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Vision Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#00cc96"},
                    'steps': [
                        {'range': [0, 33], 'color': "#ff6961"},
                        {'range': [33, 66], 'color': "#ffb347"},
                        {'range': [66, 100], 'color': "#77dd77"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': response_data.get("vision_score", 0)
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📝 Vision Summary")
            st.write(response_data.get("vision_summary", "N/A"))
            
            st.subheader("💡 Vision Recommendations")
            for rec in response_data.get("vision_recommendations", []):
                st.write(f"- {rec}")
            
            st.subheader("🔄 Alternative Visions")
            cols = st.columns(3)
            for i, alt_vision in enumerate(response_data.get("vision_alt", [])):
                with cols[i]:
                    if st.button(alt_vision, key=f"alt_vision_{i}", help="Click to select this vision"):
                        st.session_state.vision_input = alt_vision
                        st.session_state.selected_vision = alt_vision
                        st.session_state.run_analysis = True
                        if "vision_input" in st.session_state:
                            st.session_state["vision_input"] = alt_vision
                        st.rerun()
            
        except requests.exceptions.HTTPError as e:
            error_response = e.response.json() if e.response else "No response details"
            st.error(f"API Error: {e}\nDetails: {error_response}")
            st.session_state.run_analysis = False
        except Exception as e:
            st.error(f"Unexpected Error: {e}")
            st.session_state.run_analysis = False
        finally:
            st.session_state.run_analysis = False
    elif st.session_state.run_analysis:
        st.warning("Please enter a valid vision statement.")
        st.session_state.run_analysis = False

# --- Render Strategic Theme Input ---
def render_strategic_theme_section(vision_input, swot_input, challenges_input):
    st.header("🎯 Strategic Themes")
    
    if st.button("➕ Add New Strategic Theme"):
        st.session_state.strategic_themes.append({"name": "", "description": ""})
        st.rerun()

    for i, theme in enumerate(st.session_state.strategic_themes):
        with st.expander(f"Strategic Theme #{i+1}", expanded=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                theme["name"] = st.text_input(
                    "Title",
                    value=theme.get("name", ""),
                    key=f"theme_name_{i}",
                    placeholder="Enter strategic theme title"
                )
                
                theme["description"] = st.text_area(
                    "Description",
                    value=theme.get("description", ""),
                    key=f"theme_desc_{i}",
                    height=100,
                    placeholder="Enter detailed description of the strategic theme"
                )
            
            with col2:
                if len(st.session_state.strategic_themes) > 1:
                    if st.button("❌ Remove", key=f"remove_theme_{i}"):
                        st.session_state.strategic_themes.pop(i)
                        st.rerun()

    if st.button("💡 Clarhet AI Recommendations"):
        valid_themes = [
            {"name": theme["name"].strip(), "description": theme["description"].strip()}
            for theme in st.session_state.strategic_themes
            if theme["name"].strip() and theme["description"].strip()
        ]
        
        if not valid_themes:
            st.warning("Please enter at least one valid strategic theme with title and description.")
            return
        
        valid_challenges = [
            {
                "title": ch.get("title", "").strip(),
                "category": ch.get("category", "").strip(),
                "impact_on_business": ch.get("impact_on_business", "moderate"),
                "ability_to_address": ch.get("ability_to_address", "moderate"),
                "description": ch.get("description", "").strip(),
                "risk_score": ch.get("risk_score", None)
            }
            for ch in challenges_input
            if ch.get("title", "").strip() and ch.get("description", "").strip() and ch.get("risk_score") is not None
        ]
        
        payload = {
            "themes": valid_themes,
            "context": {
                "vision_statement": vision_input.strip() if vision_input else "",
                "swot": {
                    "strengths": [s.strip() for s in swot_input.get("strengths", []) if s.strip()],
                    "weaknesses": [w.strip() for w in swot_input.get("weaknesses", []) if w.strip()],
                    "opportunities": [o.strip() for o in swot_input.get("opportunities", []) if o.strip()],
                    "threats": [t.strip() for t in swot_input.get("threats", []) if t.strip()]
                },
                "challenges": valid_challenges
            }
        }
        
        st.write("Payload sent to APIs:", payload)
        
        endpoints = [
            "strategic-theme2/gap-detection",
            "strategic-theme2/wording-suggestions",
            "strategic-theme2/goal-mapping"
        ]
        
        for endpoint in endpoints:
            try:
                resp = requests.post(f"{BASE_URL}/{endpoint}", json=payload)
                resp.raise_for_status()
                response_data = resp.json()
                
                st.subheader(f"{endpoint.split('/')[-1].replace('-', ' ').title()}")
                with st.container():
                    if response_data.get("error"):
                        st.error(f"API Error: {response_data['error']}")
                        continue
                    
                    if endpoint.endswith("gap-detection"):
                        st.markdown("#### Missing Themes")
                        missing = response_data.get("missing_themes", "None")
                        if missing != "None":
                            st.warning(f"🚨 {missing}")
                        else:
                            st.write("✅ None")
                            
                        st.markdown("#### Overlapping Themes")
                        st.write(response_data.get("overlapping_themes", "None"))
                            
                        st.markdown("#### Unused Elements")
                        unused = response_data.get("unused_elements", "None")
                        if unused != "None":
                            st.warning(f"⚠️ {unused}")
                        else:
                            st.write("✅ None")
                    
                    elif endpoint.endswith("wording-suggestions"):
                        for suggestion in response_data.get("suggestions", []):
                            with st.container():
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"Original Name: {suggestion.get('original_name', 'N/A')}")
                                    st.write(f"Original Description: {suggestion.get('original_description', 'N/A')}")
                                with col2:
                                    st.write(f"Improved Name: {suggestion.get('improved_name', 'N/A')}")
                                    st.write(f"Improved Description: {suggestion.get('improved_description', 'N/A')}")
                                st.write(f"Rationale: {suggestion.get('rationale', 'N/A')}")
                    
                    elif endpoint.endswith("goal-mapping"):
                        for theme in response_data.get("mapped_themes", []):
                            with st.container():
                                st.write(f"Theme: {theme.get('theme_name', 'N/A')}")
                                for goal in theme.get("goals", []):
                                    st.write(f"- {goal.get('goal', 'N/A')} ({goal.get('goal_type', 'Unknown')})")
                    
            except requests.exceptions.HTTPError as e:
                error_response = e.response.json() if e.response else "No response details"
                st.error(f"API Error for {endpoint}: {e}\nDetails: {error_response}")
            except Exception as e:
                st.error(f"Unexpected Error for {endpoint}: {e}")
        
        st.session_state.theme_result_counter = st.session_state.get("theme_result_counter", 0) + 1

# --- Render Capabilities Input ---
def render_capabilities_section():
    st.header("🛠️ Capabilities Input")
    
    if st.button("➕ Add New Capability"):
        st.session_state.capabilities.append({"capability": "", "type": "Core"})
        st.rerun()

    for i, cap in enumerate(st.session_state.capabilities):
        with st.expander(f"Capability #{i+1}", expanded=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                cap["capability"] = st.text_input(
                    "Capability",
                    value=cap.get("capability", ""),
                    key=f"cap_text_{i}",
                    placeholder="Enter capability description"
                )
            
            with col2:
                cap["type"] = st.selectbox(
                    "Type",
                    options=["Core", "Differentiating"],
                    index=["Core", "Differentiating"].index(cap.get("type", "Core")),
                    key=f"cap_type_{i}"
                )
            
            with col3:
                if len(st.session_state.capabilities) > 1:
                    if st.button("❌ Remove", key=f"remove_cap_{i}"):
                        st.session_state.capabilities.pop(i)
                        st.rerun()

    if st.button("💡 Differentiating AI Recommendations"):
        differentiating_caps = [cap["capability"].strip() for cap in st.session_state.capabilities if cap["capability"].strip() and cap["type"] == "Differentiating"]
        
        if not differentiating_caps:
            st.warning("Please enter at least one Differentiating capability.")
            return
        
        payload = {"capability": differentiating_caps}
        st.write("Payload sent to API:", payload)
        
        try:
            resp = requests.post(f"{BASE_URL}/capabilities/analyze", json=payload)
            resp.raise_for_status()
            response_data = resp.json()
            
            st.subheader("Differentiating Capabilities Analysis")
            with st.container():
                if response_data.get("error"):
                    st.error(f"API Error: {response_data['error']}")
                    return
                
                st.markdown("### Summary")
                st.write(response_data.get("summary", "N/A"))
                
                st.markdown("### Differentiating Factors")
                for factor in response_data.get("differentiating_factors", []):
                    st.write(f"- {factor}")
                
        except requests.exceptions.HTTPError as e:
            error_response = e.response.json() if e.response else "No response details"
            st.error(f"API Error: {e}\nDetails: {error_response}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")

# --- Render Business Goals Input ---
def render_business_goals_section():
    st.header("🏆 Business Goals Input")
    
    if st.button("➕ Add New Business Goal"):
        st.session_state.business_goals.append({
            "title": "", "description": "", "strategic_themes": [], "owner": "Ash",
            "funding": 0, "business_function": "IT", "term": "Long-term",
            "start_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "end_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "priority": "Medium", "progress": 0, "specific_strategic": "Yes",
            "resources_available": "Yes", "resources_explanation": "",
            "env_social_issues": "No", "env_social_details": "", "env_social_impact": "Low",
            "show_additional": False,
            "risks_challenges": "", "risks_impact": "Low",
            "regulatory_compliance": "", "regulatory_impact": "Low",
            "cultural_realignment": "", "cultural_impact": "Low",
            "change_management": "", "change_impact": "Low",
            "learning_development": "", "learning_impact": "Low",
            "other_detail": ""
        })
        st.rerun()

    theme_options = [theme["name"].strip() for theme in st.session_state.strategic_themes if theme["name"].strip()] or ["No themes available"]

    for i, goal in enumerate(st.session_state.business_goals):
        with st.expander(f"Business Goal #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                goal["title"] = st.text_input(
                    "Goal Title",
                    value=goal.get("title", ""),
                    key=f"goal_title_{i}",
                    placeholder="Enter goal title"
                )
                
                goal["description"] = st.text_area(
                    "Goal Description",
                    value=goal.get("description", ""),
                    key=f"goal_desc_{i}",
                    height=100,
                    placeholder="Enter detailed description of the goal"
                )
                
                goal["strategic_themes"] = st.multiselect(
                    "What Strategic Themes is this business goal tied to?",
                    options=theme_options,
                    default=goal.get("strategic_themes", []),
                    key=f"goal_themes_{i}"
                )
                
                goal["owner"] = st.selectbox(
                    "Goal Owner",
                    options=["Ash", "Mat", "Brad", "Smith"],
                    index=["Ash", "Mat", "Brad", "Smith"].index(goal.get("owner", "Ash")),
                    key=f"goal_owner_{i}"
                )
                
                goal["funding"] = st.number_input(
                    "Funding Allocated (in $)",
                    min_value=0,
                    value=goal.get("funding", 0),
                    step=1000,
                    key=f"goal_funding_{i}"
                )
                
                goal["business_function"] = st.selectbox(
                    "Assign to Business Function(s)",
                    options=["IT", "Sales", "Marketing", "Operations"],
                    index=["IT", "Sales", "Marketing", "Operations"].index(goal.get("business_function", "IT")),
                    key=f"goal_function_{i}"
                )
                
            with col2:
                goal["term"] = st.selectbox(
                    "Is this a Long-term or Short-term goal?",
                    options=["Long-term", "Short-term"],
                    index=["Long-term", "Short-term"].index(goal.get("term", "Long-term")),
                    key=f"goal_term_{i}"
                )
                
                goal["start_date"] = st.text_input(
                    "Start Date and Time (YYYY-MM-DD HH:MM)",
                    value=goal.get("start_date", datetime.now().strftime("%Y-%m-%d %H:%M")),
                    key=f"goal_start_{i}",
                    placeholder="YYYY-MM-DD HH:MM"
                )
                
                goal["end_date"] = st.text_input(
                    "End Date and Time (YYYY-MM-DD HH:MM)",
                    value=goal.get("end_date", datetime.now().strftime("%Y-%m-%d %H:%M")),
                    key=f"goal_end_{i}",
                    placeholder="YYYY-MM-DD HH:MM"
                )
                
                goal["priority"] = st.selectbox(
                    "Goal Priority",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(goal.get("priority", "Medium")),
                    key=f"goal_priority_{i}"
                )
                
                goal["progress"] = st.number_input(
                    "Goal Progress (%)",
                    min_value=0,
                    max_value=100,
                    value=goal.get("progress", 0),
                    step=1,
                    key=f"goal_progress_{i}"
                )
                
                goal["specific_strategic"] = st.selectbox(
                    "Is this goal both specific and strategic?",
                    options=["Yes", "Only Specific", "Only Strategic"],
                    index=["Yes", "Only Specific", "Only Strategic"].index(goal.get("specific_strategic", "Yes")),
                    key=f"goal_specific_{i}"
                )
                
                goal["resources_available"] = st.selectbox(
                    "Do we possess the necessary resources (human and material)?",
                    options=["Yes", "No"],
                    index=["Yes", "No"].index(goal.get("resources_available", "Yes")),
                    key=f"goal_resources_{i}"
                )
                
                if goal["resources_available"] == "No":
                    goal["resources_explanation"] = st.text_area(
                        "If no, please explain",
                        value=goal.get("resources_explanation", ""),
                        key=f"goal_res_explain_{i}",
                        height=100,
                        placeholder="Explain resource gaps"
                    )
                
                goal["env_social_issues"] = st.selectbox(
                    "Are there any environmental and social issues to address?",
                    options=["Yes", "No"],
                    index=["Yes", "No"].index(goal.get("env_social_issues", "No")),
                    key=f"goal_env_social_{i}"
                )
                
                if goal["env_social_issues"] == "Yes":
                    goal["env_social_details"] = st.text_area(
                        "What specific environmental and social issues need to be addressed, and how might they impact the goal?",
                        value=goal.get("env_social_details", ""),
                        key=f"goal_env_details_{i}",
                        height=100,
                        placeholder="Describe issues and their impact"
                    )
                    goal["env_social_impact"] = st.selectbox(
                        "Environmental/Social Impact",
                        options=["High", "Medium", "Low"],
                        index=["High", "Medium", "Low"].index(goal.get("env_social_impact", "Low")),
                        key=f"goal_env_impact_{i}"
                    )
            
            if st.button("➕ Additional Information", key=f"goal_additional_{i}"):
                goal["show_additional"] = not goal.get("show_additional", False)
                st.rerun()
            
            if goal.get("show_additional", False):
                st.markdown("### Additional Information")
                goal["risks_challenges"] = st.text_area(
                    "Are there any potential risks and challenges that could hinder our progress toward the goal?",
                    value=goal.get("risks_challenges", ""),
                    key=f"goal_risks_{i}",
                    height=100,
                    placeholder="Describe risks and challenges"
                )
                goal["risks_impact"] = st.selectbox(
                    "Risks and Challenges Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(goal.get("risks_impact", "Low")),
                    key=f"goal_risks_impact_{i}"
                )
                
                goal["regulatory_compliance"] = st.text_area(
                    "Is there any regulatory compliance to address to ensure goal achievement?",
                    value=goal.get("regulatory_compliance", ""),
                    key=f"goal_regulatory_{i}",
                    height=100,
                    placeholder="Describe regulatory requirements"
                )
                goal["regulatory_impact"] = st.selectbox(
                    "Regulatory Compliance Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(goal.get("regulatory_impact", "Low")),
                    key=f"goal_regulatory_impact_{i}"
                )
                
                goal["cultural_realignment"] = st.text_area(
                    "What cultural realignment is necessary to bolster the goal's success?",
                    value=goal.get("cultural_realignment", ""),
                    key=f"goal_cultural_{i}",
                    height=100,
                    placeholder="Describe cultural changes needed"
                )
                goal["cultural_impact"] = st.selectbox(
                    "Cultural Realignment Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(goal.get("cultural_impact", "Low")),
                    key=f"goal_cultural_impact_{i}"
                )
                
                goal["change_management"] = st.text_area(
                    "What change/transformation should be addressed to achieve this goal? (Change Management)",
                    value=goal.get("change_management", ""),
                    key=f"goal_change_{i}",
                    height=100,
                    placeholder="Describe change management needs"
                )
                goal["change_impact"] = st.selectbox(
                    "Change Management Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(goal.get("change_impact", "Low")),
                    key=f"goal_change_impact_{i}"
                )
                
                goal["learning_development"] = st.text_area(
                    "How will learning and development initiatives be integrated to enhance skills and capabilities?",
                    value=goal.get("learning_development", ""),
                    key=f"goal_learning_{i}",
                    height=100,
                    placeholder="Describe learning and development plans"
                )
                goal["learning_impact"] = st.selectbox(
                    "Learning and Development Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(goal.get("learning_impact", "Low")),
                    key=f"goal_learning_impact_{i}"
                )
                
                goal["other_detail"] = st.text_area(
                    "Other Detail (Optional)",
                    value=goal.get("other_detail", ""),
                    key=f"goal_other_{i}",
                    height=100,
                    placeholder="Enter any additional details"
                )
            
            if len(st.session_state.business_goals) > 1:
                if st.button("❌ Remove Goal", key=f"remove_goal_{i}"):
                    st.session_state.business_goals.pop(i)
                    st.rerun()

    if st.button("💡 Business Goal Recommendations"):
        valid_goals = [
            {
                "potential_risks_and_challenges": {
                    "answer": goal["risks_challenges"].strip(),
                    "impact": goal["risks_impact"]
                },
                "regulatory_compliance": {
                    "answer": goal["regulatory_compliance"].strip(),
                    "impact": goal["regulatory_impact"]
                },
                "cultural_realignment": {
                    "answer": goal["cultural_realignment"].strip(),
                    "impact": goal["cultural_impact"]
                },
                "change_management": {
                    "answer": goal["change_management"].strip(),
                    "impact": goal["change_impact"]
                },
                "learning_and_development": {
                    "answer": goal["learning_development"].strip(),
                    "impact": goal["learning_impact"]
                }
            }
            for goal in st.session_state.business_goals
            if goal.get("show_additional", False) and any([
                goal["risks_challenges"].strip(),
                goal["regulatory_compliance"].strip(),
                goal["cultural_realignment"].strip(),
                goal["change_management"].strip(),
                goal["learning_development"].strip()
            ])
        ]
        
        if not valid_goals:
            st.warning("Please provide additional information for at least one goal to get recommendations.")
            return
        
        payload = valid_goals[0]  # Assuming one goal for simplicity; adjust if multiple goals needed
        st.write("Payload sent to API:", payload)
        
        try:
            resp = requests.post(f"{BASE_URL}/business-goals/recommendations", json=payload)
            resp.raise_for_status()
            response_data = resp.json()
            
            st.subheader("Business Goal Recommendations")
            with st.container():
                if response_data.get("error"):
                    st.error(f"API Error: {response_data['error']}")
                    return
                
                st.markdown("### Risks Summary")
                st.write(response_data.get("risks_summary", "N/A"))
                
                st.markdown("### Regulatory Compliance Summary")
                st.write(response_data.get("regulatory_compliance_summary", "N/A"))
                
                st.markdown("### Roadblocks Summary")
                st.write(response_data.get("roadblocks_summary", "N/A"))
                
                st.markdown("### Culture Realignment Summary")
                st.write(response_data.get("culture_realignment_summary", "N/A"))
                
                st.markdown("### Change Management Summary")
                st.write(response_data.get("change_management_summary", "N/A"))
                
                st.markdown("### Learning and Development Summary")
                st.write(response_data.get("learning_and_development_summary", "N/A"))
                
        except requests.exceptions.HTTPError as e:
            error_response = e.response.json() if e.response else "No response details"
            st.error(f"API Error: {e}\nDetails: {error_response}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")

# --- Render Chatbot Section ---
def render_chatbot_section():
    st.header("🤖 Chatbot")
    
    # Chat container
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            with st.chat_message(chat["role"]):
                st.write(chat["message"])
    
    # Input area
    user_input = st.chat_input("Ask anything...")
    
    # Handle send action
    if user_input and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "message": user_input.strip()})
        
        # Prepare payload
        payload = {
            "message": user_input.strip(),
            "history": st.session_state.chat_history
        }
        
        try:
            resp = requests.post(f"{BASE_URL}/chatbot/chatbot", json=payload)
            resp.raise_for_status()
            response_data = resp.json()
            
            # Add AI response to history
            st.session_state.chat_history.append({"role": "assistant", "message": response_data.get("response", "No response received.")})
            
        except (requests.exceptions.RequestException, ValueError) as e:
            # Handle any network or JSON errors
            st.error("Failed to connect to the AI service. Please try again.")
            st.session_state.chat_history.append({"role": "assistant", "message": "Sorry, I'm having trouble connecting. Please try again!"})
        
        # Rerun to update UI
        st.rerun()
    elif user_input:
        st.warning("Please enter a non-empty message.")

# --- Main Rendering with Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["🔍 Trends", "🧭 SWOT", "🚨 Challenges", "🌟 Vision", "🎯 Strategic Themes", "🛠️ Capabilities", "🏆 Business Goals", "🤖 Chatbot"])

with tab1:
    trends = render_trend_section()
with tab2:
    swot = render_swot_section()
with tab3:
    render_challenge_section(swot, trends)
with tab4:
    render_vision_section()
with tab5:
    render_strategic_theme_section(
        vision_input=st.session_state.get("vision_input", ""),
        swot_input=st.session_state.get("swot_payload", {}),
        challenges_input=st.session_state.get("challenges", [])
    )
with tab6:
    render_capabilities_section()
with tab7:
    render_business_goals_section()
with tab8:
    render_chatbot_section()