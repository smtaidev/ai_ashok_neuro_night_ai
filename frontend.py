import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime

st.set_page_config(page_title="Clarhet Zenith", layout="wide")
st.title("🧠 Clarhet Zenith: Test Site")

if "selected_tone" not in st.session_state:
    st.session_state.selected_tone = "coach"

with st.sidebar:
    st.selectbox(
        "🎤 Select Tone",
        options=["coach", "advisor", "challenger"],
        index=["coach", "advisor", "challenger"].index(st.session_state.selected_tone),
        key="selected_tone"
    )

BASE_URL = "http://127.0.0.1:8027/api"

trend_areas = [
    "customer_insights", "competitor_landscape", "technological_advances",
    "regulatory_and_legal", "economic_considerations", "supply_chain_logistics",
    "global_market_trends", "environmental_social_impact", "collaboration_partnerships",
    "scenarios_risk_assessment", "emerging_markets_opportunities", "on_the_radar"
]



if "identity_inputs" not in st.session_state:
    st.session_state.identity_inputs = {
        "mission": "",
        "value": "",
        "purpose": "",
        "customers": "",
        "value_proposition": ""
    }

if "competitors" not in st.session_state:
    st.session_state.competitors = {
        "name": "",
        "description": ""
    }

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

if "trend_summary" not in st.session_state:
    st.session_state.trend_summary = ""

# --- Render Competitors ---
def render_competitors_section():
    st.header("🏢 Competitors")

    if "competitors" not in st.session_state or not isinstance(st.session_state.competitors, list):
        st.session_state.competitors = [{
            "name": "",
            "description": ""
        }]
    elif any(not isinstance(c, dict) for c in st.session_state.competitors):
        st.session_state.competitors = [{
            "name": "",
            "description": ""
        }]

    if "competitors_submitted" not in st.session_state:
        st.session_state.competitors_submitted = False

    # Render each competitor input
    for i, competitor in enumerate(st.session_state.competitors):
        with st.container():
            col1, col2 = st.columns([3, 1])

            competitor["name"] = col1.text_input(
                f"Competitor Name {i + 1}",
                value=competitor["name"],
                placeholder="Enter competitor name",
                key=f"competitor_name_{i}"
            )

            competitor["description"] = col1.text_area(
                f"Description {i + 1}",
                value=competitor["description"],
                height=100,
                placeholder="Enter competitor description",
                key=f"competitor_desc_{i}"
            )

            if col2.button("❌", key=f"remove_competitor_{i}") and len(st.session_state.competitors) > 1:
                st.session_state.competitors.pop(i)
                st.rerun()

    # Add competitor button (only if less than 3)
    if len(st.session_state.competitors) < 3:
        if st.button("➕ Add Competitor"):
            st.session_state.competitors.append({
                "name": "",
                "description": ""
            })
            st.rerun()
    else:
        st.info("You can only add up to 3 competitors.")

    # Submit button
    if st.button("✅ Submit Competitor Info"):
        all_filled = all(c["name"].strip() and c["description"].strip() for c in st.session_state.competitors)
        if all_filled:
            st.session_state.competitors_submitted = True
            st.success("✔️ Competitor information has been stored in session.")
        else:
            st.warning("⚠️ We need to know more details about your competitors.")

   

#  Render Identity Inputs 
def render_identity_section():
    st.header("🏢 Company Identity and Zero-In")

    mission = st.text_area(
        "📌 Mission Statement",
        value=st.session_state.identity_inputs.get("mission", ""),
        placeholder="Enter your company's mission..."
    )

    value = st.text_area(
        "💎 Core Values",
        value=st.session_state.identity_inputs.get("value", ""),
        placeholder="What values guide your company?"
    )

    purpose = st.text_area(
        "🎯 Purpose",
        value=st.session_state.identity_inputs.get("purpose", ""),
        placeholder="Why does your company exist?"
    )

    customers = st.text_area(
        "👥 Customers",
        value=st.session_state.identity_inputs.get("customers", ""),
        placeholder="Who are your customers?"
    )

    value_proposition = st.text_area(
        "💡 Value Proposition",
        value=st.session_state.identity_inputs.get("value_proposition", ""),
        placeholder="What is your value proposition?"
    )

    if st.button("✅ Submit Identity Info"):
        if mission.strip() and value.strip() and purpose.strip() and customers.strip() and value_proposition.strip():
            st.session_state.identity_inputs = {
                "mission": mission.strip(),
                "value": value.strip(),
                "purpose": purpose.strip(),
                "customers": customers.strip(),
                "value_proposition": value_proposition.strip()
            }
            st.success("✔️ Identity inputs are stored in session and ready to be used later.")
        else:
            st.warning("⚠️ Almost there! Please fill out all fields before submitting.")

# Render Trend Input 
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

        with st.spinner("Just a moment, analyzing market trends and patterns for you..."):
            try:
                resp = requests.post(f"{BASE_URL}/trends/analyze", json=trends_payload)
                resp.raise_for_status()
                response_data = resp.json()
                st.header("📋 Trend Output")

                
                if "trend_synthesis" in response_data and response_data["trend_synthesis"]:
                    st.markdown("### 📈 Trend Synthesis")
                    for trends in response_data["trend_synthesis"]:
                        st.markdown(f"- {trends}")
                if "early_warnings" in response_data:
                    st.markdown("### 🚨 Early Warnings")
                    st.markdown(response_data["early_warnings"])
                
                if "strategic_opportunities" in response_data and response_data["strategic_opportunities"]:
                    st.markdown("### 🌟 Strategic Opportunities")
                    for opportunity in response_data["strategic_opportunities"]:
                        st.markdown(f"- {opportunity}")
                
                if "analyst_recommendations" in response_data:
                    st.session_state.trend_summary = response_data["analyst_recommendations"]
                    st.markdown("### 📝 Analyst Recommendations")
                    st.markdown(response_data["analyst_recommendations"])

                if "radar_executive_summary" in response_data and response_data["radar_executive_summary"]:
                    st.markdown("### 🔮 On the Radar Summary")
                    for summary in response_data["radar_executive_summary"]:
                        st.markdown(f"- {summary}")
                
                if "radar_recommendation" in response_data and response_data["radar_recommendation"]:
                    st.markdown("### 🛠 On the Radar Recommendations")
                    for rec in response_data["radar_recommendation"]:
                            st.markdown(f"- {rec}")
                
                if response_data['error']:
                    st.markdown("### ⚠️ Some of the answers were not relevant or did not match the expected format.")
                    st.error(f"{response_data['error']}")

                    
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


#  Render SWOT Input 
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
            with st.spinner("Cooking the recommendations for SWOT analysis..."):
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
            st.warning("We need to know at least one SWOT category to proceed!!")

    st.session_state.swot_payload = swot_payload
    return swot_payload

#  Render Challenge Input 
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

                        
                        with st.spinner("Calculating risk score..."):
                            try:
                                resp = requests.post(f"{BASE_URL}/challenge/evaluate", json=payload)
                                response_data = resp.json()
                                st.write(response_data)
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
                        st.warning("We can't move forward without a title and description.")
            
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
            with st.spinner("Just a moment, generating strategic recommendations..."):
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
                        st.warning("Sorry we couldn't process any recommendations for the challenges provided.")
                        
                except requests.exceptions.HTTPError as e:
                    error_response = e.response.json() if e.response else "No response details"
                    st.error(f"API Error: {e}\nDetails: {error_response}")
                except Exception as e:
                    st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please evaluate at least one challenge with title and description to get recommendations.")

#  Render Vision Input 
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
        payload = {
            "vision_statement": st.session_state.vision_input.strip(),
            "tone": st.session_state.get("tone", "coach")
        }

        with st.spinner("We're analyzing your insights — this won't take long!"):
            try:
                resp = requests.post(f"{BASE_URL}/blueprint/vision", json=payload)
                resp.raise_for_status()
                response_data = resp.json()


                if response_data["error"] is not None:
                    st.warning(f"Oops!! something is wrong. {response_data['error']}")
                    st.session_state.run_analysis = False
                    return  
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
                        'threshold': {
                            'line': {'color': "black", 'width': 10},
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
                            st.rerun()

            except requests.exceptions.HTTPError as e:
                st.error(f"API Error: {e}")
                st.session_state.run_analysis = False
            except Exception as e:
                st.error(f"Unexpected Error: {e}")
                st.session_state.run_analysis = False
            finally:
                st.session_state.run_analysis = False
    elif st.session_state.run_analysis:
        st.warning("Let's know about your vision first!")
        st.session_state.run_analysis = False

#  Render Strategic Theme Input 
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
                    "Title", value=theme.get("name", ""), key=f"theme_name_{i}",
                    placeholder="Enter strategic theme title"
                )
                theme["description"] = st.text_area(
                    "Description", value=theme.get("description", ""),
                    key=f"theme_desc_{i}", height=100,
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
            st.warning("We are missing something in one of your strategic themes!! Please ensure all fields are filled out.")
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
                "vision": vision_input.strip() if vision_input else "",
                "swot": {
                    "strengths": [s.strip() for s in swot_input.get("strengths", []) if s.strip()],
                    "weaknesses": [w.strip() for w in swot_input.get("weaknesses", []) if w.strip()],
                    "opportunities": [o.strip() for o in swot_input.get("opportunities", []) if o.strip()],
                    "threats": [t.strip() for t in swot_input.get("threats", []) if t.strip()]
                },
                "challenges": valid_challenges,
                "mission": st.session_state.identity_inputs.get("mission", "").strip(),
                "value": st.session_state.identity_inputs.get("value", "").strip(),
                "purpose": st.session_state.identity_inputs.get("purpose", "").strip(),
                "customers": st.session_state.identity_inputs.get("customers", "").strip(),
                "value_proposition": st.session_state.identity_inputs.get("value_proposition", "").strip(),
                "competitors": st.session_state.competitors,
                "trends": st.session_state.trend_summary if st.session_state.trend_summary else "",
                "capabilities": st.session_state.capabilities,
            },
            "tone": st.session_state.get("tone", "coach"),
        }

        with st.spinner("We're conducting strategic theme analysis and identifying gaps..."):
            try:
                resp = requests.post(f"{BASE_URL}/strategic-theme2/combined-analysis", json=payload)
                resp.raise_for_status()
                response_data = resp.json()

                if response_data.get("error"):
                    st.warning(f"⚠️ Oops!! something is wrong. {response_data['error']}")
                    return

                # GAP DETECTION
                gap = response_data.get("gap_detection", {})
                if gap:
                    st.subheader("🕳️ Gap Detection")
                    st.markdown("#### Missing Themes")
                    st.warning(gap.get("missing_themes", "✅ None") or "✅ None")
                    
                    st.markdown("#### Overlapping Themes")
                    st.write(gap.get("overlapping_themes", "✅ None"))
                    
                    st.markdown("#### Unused Elements")
                    st.warning(gap.get("unused_elements", "✅ None") or "✅ None")

                # WORDING SUGGESTIONS
                wording = response_data.get("wording_suggestions", {})
                suggestions = wording.get("suggestions", [])
                if suggestions:
                    st.subheader("📝 Wording Suggestions")
                    for suggestion in suggestions:
                        with st.container():
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Original Name:** {suggestion.get('original_name', 'N/A')}")
                                st.write(f"**Original Description:** {suggestion.get('original_description', 'N/A')}")
                            with col2:
                                st.write(f"**Improved Name:** {suggestion.get('improved_name', 'N/A')}")
                                st.write(f"**Improved Description:** {suggestion.get('improved_description', 'N/A')}")
                            st.write(f"**Rationale:** {suggestion.get('rationale', 'N/A')}")

                # GOAL MAPPING
                goal_mapping = response_data.get("goal_mapping", {})
                mapped_themes = goal_mapping.get("mapped_themes", [])
                if mapped_themes:
                    st.subheader("🎯 Goal Mapping")
                    for theme in mapped_themes:
                        st.write(f"**Theme:** {theme.get('theme_name', 'N/A')}")
                        for goal in theme.get("goals", []):
                            st.write(f"- {goal.get('goal', 'N/A')} ({goal.get('goal_type', 'Unknown')})")

            except requests.exceptions.HTTPError as e:
                try:
                    error_response = e.response.json()
                except Exception:
                    error_response = str(e)
                st.error(f"❌ API Error: {error_response}")
            except Exception as e:
                st.error(f"❌ Unexpected Error: {e}")

        st.session_state.theme_result_counter = st.session_state.get("theme_result_counter", 0) + 1


#  Render Capabilities Input 
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
        
        payload = {"capabilities": differentiating_caps}

        with st.spinner("We are analyzing differentiating capabilities and competitive advantages..."):
            try:
                resp = requests.post(f"{BASE_URL}/differentiation/analyze", json=payload)
                resp.raise_for_status()
                response_data = resp.json()
                
                st.subheader("Differentiating Capabilities Analysis")
                with st.container():
                    if response_data.get("error"):
                        st.error(f"Oops!! something is wrong. {response_data['error']}")
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

#  Render Business Goals Input 
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
                st.session_state.business_goals[i]["title"] = st.text_input(
                    "Goal Title",
                    value=st.session_state.business_goals[i].get("title", ""),
                    key=f"goal_title_{i}",
                    placeholder="Enter goal title"
                )

                st.session_state.business_goals[i]["description"] = st.text_area(
                    "Goal Description",
                    value=st.session_state.business_goals[i].get("description", ""),
                    key=f"goal_desc_{i}",
                    height=100,
                    placeholder="Enter detailed description of the goal"
                )

                theme = []
                for theme_name in st.session_state.strategic_themes:
                    if theme_name["name"].strip():
                        theme.append(theme_name["name"].strip())

                st.session_state.business_goals[i]["strategic_themes"] = st.multiselect(
                    "What Strategic Themes is this business goal tied to?",
                    options=theme,
                    default=st.session_state.business_goals[i].get("strategic_themes", theme[0] if theme else []),
                    key=f"goal_themes_{i}"
                )

                st.session_state.business_goals[i]["owner"] = st.selectbox(
                    "Goal Owner",
                    options=["Ash", "Mat", "Brad", "Smith"],
                    index=["Ash", "Mat", "Brad", "Smith"].index(st.session_state.business_goals[i].get("owner", "Ash")),
                    key=f"goal_owner_{i}"
                )

                st.session_state.business_goals[i]["funding"] = st.number_input(
                    "Funding Allocated (in $)",
                    min_value=0,
                    value=st.session_state.business_goals[i].get("funding", 0),
                    step=1000,
                    key=f"goal_funding_{i}"
                )

                st.session_state.business_goals[i]["business_function"] = st.selectbox(
                    "Assign to Business Function(s)",
                    options=["IT", "Sales", "Marketing", "Operations"],
                    index=["IT", "Sales", "Marketing", "Operations"].index(st.session_state.business_goals[i].get("business_function", "IT")),
                    key=f"goal_function_{i}"
                )
                
            with col2:
                st.session_state.business_goals[i]["term"] = st.selectbox(
                    "Is this a Long-term or Short-term goal?",
                    options=["Long-term", "Short-term"],
                    index=["Long-term", "Short-term"].index(st.session_state.business_goals[i].get("term", "Long-term")),
                    key=f"goal_term_{i}"
                )

                st.session_state.business_goals[i]["start_date"] = st.text_input(
                    "Start Date and Time (YYYY-MM-DD HH:MM)",
                    value=st.session_state.business_goals[i].get("start_date", datetime.now().strftime("%Y-%m-%d %H:%M")),
                    key=f"goal_start_{i}",
                    placeholder="YYYY-MM-DD HH:MM"
                )

                st.session_state.business_goals[i]["end_date"] = st.text_input(
                    "End Date and Time (YYYY-MM-DD HH:MM)",
                    value=st.session_state.business_goals[i].get("end_date", datetime.now().strftime("%Y-%m-%d %H:%M")),
                    key=f"goal_end_{i}",
                    placeholder="YYYY-MM-DD HH:MM"
                )

                st.session_state.business_goals[i]["priority"] = st.selectbox(
                    "Goal Priority",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(st.session_state.business_goals[i].get("priority", "Medium")),
                    key=f"goal_priority_{i}"
                )

                st.session_state.business_goals[i]["progress"] = st.number_input(
                    "Goal Progress (%)",
                    min_value=0,
                    max_value=100,
                    value=st.session_state.business_goals[i].get("progress", 0),
                    step=1,
                    key=f"goal_progress_{i}"
                )

                st.session_state.business_goals[i]["specific_strategic"] = st.selectbox(
                    "Is this goal both specific and strategic?",
                    options=["Yes", "Only Specific", "Only Strategic"],
                    index=["Yes", "Only Specific", "Only Strategic"].index(st.session_state.business_goals[i].get("specific_strategic", "Yes")),
                    key=f"goal_specific_{i}"
                )

                st.session_state.business_goals[i]["resources_available"] = st.selectbox(
                    "Do we possess the necessary resources (human and material)?",
                    options=["Yes", "No"],
                    index=["Yes", "No"].index(st.session_state.business_goals[i].get("resources_available", "Yes")),
                    key=f"goal_resources_{i}"
                )

                st.session_state.business_goals[i]["resources_explanation"] = st.text_area(
                    "If no, please explain",
                    value=st.session_state.business_goals[i].get("resources_explanation", ""),
                    key=f"goal_res_explain_{i}",
                    height=100,
                    placeholder="Explain resource gaps"
                )

                st.session_state.business_goals[i]["env_social_issues"] = st.selectbox(
                    "Are there any environmental and social issues to address?",
                    options=["Yes", "No"],
                    index=["Yes", "No"].index(st.session_state.business_goals[i].get("env_social_issues", "No")),
                    key=f"goal_env_social_{i}"
                )
                

                st.session_state.business_goals[i]["env_social_details"] = st.text_area(
                    "What specific environmental and social issues need to be addressed, and how might they impact the goal?",
                    value=st.session_state.business_goals[i].get("env_social_details", ""),
                    key=f"goal_env_details_{i}",
                    height=100,
                    placeholder="Describe issues and their impact"
                )

                st.session_state.business_goals[i]["env_social_impact"] = st.selectbox(
                    "Environmental/Social Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(st.session_state.business_goals[i].get("env_social_impact", "Low")),
                    key=f"goal_env_impact_{i}"
                )
            
            if st.button("➕ Additional Information", key=f"goal_additional_{i}"):
                goal["show_additional"] = not goal.get("show_additional", False)
                st.rerun()
            
            if goal.get("show_additional", False):
                st.markdown("### Additional Information")
                st.session_state.business_goals[i]["risks_challenges"] = st.text_area(
                    "Are there any potential risks and challenges that could hinder our progress toward the goal?",
                    value=st.session_state.business_goals[i].get("risks_challenges", ""),
                    key=f"goal_risks_{i}",
                    height=100,
                    placeholder="Describe risks and challenges"
                )
                st.session_state.business_goals[i]["risks_impact"] = st.selectbox(
                    "Risks and Challenges Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(st.session_state.business_goals[i].get("risks_impact", "Low")),
                    key=f"goal_risks_impact_{i}"
                )

                st.session_state.business_goals[i]["regulatory_compliance"] = st.text_area(
                    "Is there any regulatory compliance to address to ensure goal achievement?",
                    value=st.session_state.business_goals[i].get("regulatory_compliance", ""),
                    key=f"goal_regulatory_{i}",
                    height=100,
                    placeholder="Describe regulatory requirements"
                )
                st.session_state.business_goals[i]["regulatory_impact"] = st.selectbox(
                    "Regulatory Compliance Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(st.session_state.business_goals[i].get("regulatory_impact", "Low")),
                    key=f"goal_regulatory_impact_{i}"
                )

                st.session_state.business_goals[i]["cultural_realignment"] = st.text_area(
                    "What cultural realignment is necessary to bolster the goal's success?",
                    value=st.session_state.business_goals[i].get("cultural_realignment", ""),
                    key=f"goal_cultural_{i}",
                    height=100,
                    placeholder="Describe cultural changes needed"
                )
                st.session_state.business_goals[i]["cultural_impact"] = st.selectbox(
                    "Cultural Realignment Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(st.session_state.business_goals[i].get("cultural_impact", "Low")),
                    key=f"goal_cultural_impact_{i}"
                )

                st.session_state.business_goals[i]["change_management"] = st.text_area(
                    "What change/transformation should be addressed to achieve this goal? (Change Management)",
                    value=st.session_state.business_goals[i].get("change_management", ""),
                    key=f"goal_change_{i}",
                    height=100,
                    placeholder="Describe change management needs"
                )
                st.session_state.business_goals[i]["change_impact"] = st.selectbox(
                    "Change Management Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(st.session_state.business_goals[i].get("change_impact", "Low")),
                    key=f"goal_change_impact_{i}"
                )

                st.session_state.business_goals[i]["learning_development"] = st.text_area(
                    "How will learning and development initiatives be integrated to enhance skills and capabilities?",
                    value=st.session_state.business_goals[i].get("learning_development", ""),
                    key=f"goal_learning_{i}",
                    height=100,
                    placeholder="Describe learning and development plans"
                )

                st.session_state.business_goals[i]["learning_impact"] = st.selectbox(
                    "Learning and Development Impact",
                    options=["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(st.session_state.business_goals[i].get("learning_impact", "Low")),
                    key=f"goal_learning_impact_{i}"
                )

                st.session_state.business_goals[i]["existing_capabilities_to_enhance"] = st.selectbox(
                    "Does this goal require enhancing existing capabilities to achieve it?",
                    options=["Yes", "No"],
                    index=["Yes", "No"].index(st.session_state.business_goals[i].get("existing_capabilities_to_enhance", "No")),
                    key=f"goal_existing_capabilities_{i}"
                )

                st.session_state.business_goals[i]["new_capabilities_needed"] = st.selectbox(
                    "Does this goal require adding new capabilities to achieve it?",
                    options=["Yes", "No"],
                    index=["Yes", "No"].index(st.session_state.business_goals[i].get("new_capabilities_needed", "No")),
                    key=f"goal_new_capabilities_{i}"
                )

                st.session_state.business_goals[i]["other_detail"] = st.text_area(
                    "Other Detail (Optional)",
                    value=st.session_state.business_goals[i].get("other_detail", ""),
                    key=f"goal_other_{i}",
                    height=100,
                    placeholder="Enter any additional details"
                )
            
            if len(st.session_state.business_goals) > 1:
                if st.button("❌ Remove Goal", key=f"remove_goal_{i}"):
                    st.session_state.business_goals.pop(i)
                    st.rerun()

    if st.button("💡 Business Goal Recommendations"):
        valid_goals = []

        for goal in st.session_state.business_goals:
            temp_goal = {
                "title": goal["title"].strip(),
                "description": goal["description"].strip(),
                "related_strategic_theme": goal["strategic_themes"][0],
                "priority": goal["priority"],
                "resource_readiness": goal["resources_available"],
                "assigned_functions": [goal["business_function"]],
                "duration": goal["term"],
                "impact_ratings": {
                    "risks": goal["risks_impact"],
                    "compliance": goal["regulatory_impact"],
                    "culture": goal["cultural_impact"],
                    "change_management": goal["change_impact"],
                    "l_and_d": goal["learning_impact"],
                },
                "esg_issues": goal["env_social_issues"],
                "new_capabilities_needed": goal["new_capabilities_needed"],
                "existing_capabilities_to_enhance": goal["existing_capabilities_to_enhance"]
            }
            valid_goals.append(temp_goal)

        if not valid_goals:
            st.warning("We need to know more about your goals to provide recommendations.")
            return
        
        payload = {
            "vision": st.session_state.vision_input.strip() if st.session_state.vision_input else "",
            "strategic_themes": st.session_state.strategic_themes,
            "challenges": st.session_state.challenges,
            "tone": st.session_state.get("tone", "coach"),
            "goals": valid_goals
        }

        with st.spinner("We're studying your business goal — this won't take long!"):
            try:
                resp = requests.post(f"{BASE_URL}/business-goal/analyze2", json=payload)

                response_data = resp.json()

                if response_data["error"]:
                    st.error(f"Oops!! something is wrong. {response_data['error']}")
                else:       
                    st.subheader("Business Goal Recommendations")
                    with st.container():
                        st.markdown("### Alignment Summary")
                        st.write(response_data.get("alignment_summary"))
                    
                    with st.container():
                        if "smart_suggestions" in response_data:
                            st.markdown("### SMART Suggestions")
                            for suggestion in response_data["smart_suggestions"]:
                                st.write(f"Title: {suggestion.get('title', 'looks fine')}")
                                st.write(f"Description: {suggestion.get('description', 'nicely stated')}\n")

                    with st.container():
                        if "strategic_priorities" in response_data:
                            st.markdown("### Strategic Priorities")
                            for priority in response_data["strategic_priorities"]:
                                st.write(f"- {priority}")
                    
                    with st.container():
                        if "strategic_fit_scores" in response_data:
                            st.markdown("### Strategic Fit Scores")
                            for score in response_data["strategic_fit_scores"]:
                                st.write(f"##### **{score.get('goal_title', 'N/A')}**")
                                st.write(f"Score: {score.get('score', 'N/A')}")
                                st.write(f"Explanation: {score.get('comment', 'N/A')}")

                    with st.container():
                        if "execution_watchouts" in response_data:
                            st.markdown("### Execution Watchouts")
                            for watchout in response_data["execution_watchouts"]:
                                st.write(f"- {watchout}")
                    
                    def format_value(val):
                        if isinstance(val, list):
                            return ", ".join(map(str, val))
                        return str(val) if val is not None else "N/A"

                    with st.container():
                        if "dashboard_insights" in response_data:
                            di = response_data["dashboard_insights"]
                            st.markdown("### Dashboard Insights")
                            st.markdown("**Risk**: " + format_value(di.get("risk", "No risk identified")))
                            st.markdown("**Regulatory Compliance**: " + format_value(di.get("regulatory_compliances", "Just fine")))
                            st.markdown("**Roadblocks**: " + format_value(di.get("roadblocks", "Smooth sailing")))
                            st.markdown("**Talent**: " + format_value(di.get("talent", "Looking good")))
                            st.markdown("**Cultural Realignment**: " + format_value(di.get("cultural_realignment", "Perfectly aligned")))
                            st.markdown("**Change Management**: " + format_value(di.get("change_management", "manageable")))
                            st.markdown("**Learning and Development**: " + format_value(di.get("learning_and_development", "on track")))

                    
            except requests.exceptions.HTTPError as e:
                error_response = e.response.json() if e.response else "No response details"
                st.error(f"API Error: {e}\nDetails: {error_response}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")

#  Render Chatbot Section 
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
        st.session_state.chat_history.append({"role": "user", "message": user_input.strip()})
        
        # payload
        payload = {
            "message": user_input.strip(),
            "history": st.session_state.chat_history
        }
        
        with st.spinner("Let me think..."):
            try:
                resp = requests.post(f"{BASE_URL}/chatbot/chatbot", json=payload)
                resp.raise_for_status()
                response_data = resp.json()
                
                # Add AI response to history
                st.session_state.chat_history.append({"role": "assistant", "message": response_data.get("response", "No response received.")})
                
            except (requests.exceptions.RequestException, ValueError) as e:
                st.error("Failed to connect to the AI service. Please try again.")
                st.session_state.chat_history.append({"role": "assistant", "message": "Sorry, I'm having trouble connecting. Please try again!"})
            
        st.rerun()
    elif user_input:
        st.warning("Please enter a non-empty message.")

#  Main Rendering with Tabs 
tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["🏢 Identity", "🛠️ Capabilities", "🔍 Trends", "🧭 SWOT", "🚨 Challenges", "🛠️ Competitors", "🌟 Vision", "🎯 Strategic Themes", "🏆 Business Goals", "🤖 Chatbot"])

with tab0:
    identity = render_identity_section()
with tab1:
    render_capabilities_section()
with tab2:
    trends = render_trend_section()
with tab3:
    swot = render_swot_section()
with tab4:
    render_challenge_section(swot, trends)
with tab5:
    render_competitors_section()
with tab6:
    render_vision_section()
with tab7:
    render_strategic_theme_section(
        vision_input=st.session_state.get("vision_input", ""),
        swot_input=st.session_state.get("swot_payload", {}),
        challenges_input=st.session_state.get("challenges", [])
    )
with tab8:
    render_business_goals_section()
with tab9:
    render_chatbot_section()