import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Clarhet AI - Challenge Analyzer", layout="wide")
st.title("🧠 Clarhet AI: Trends, SWOT & Challenge Analyzer")

BASE_URL = "http://127.0.0.1:8000/api"

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

# --- Render Trend Input ---
def render_trend_section():
    st.header("🔍 Trends Input")
    
    for area in trend_areas:
        st.subheader(area.replace("_", " ").title())
        
        # Check if add button was pressed for this area
        if st.button(f"➕ Add Question to {area.replace('_', ' ').title()}", key=f"add_{area}"):
            st.session_state.trend_data[area].append({"question": "", "answer": "", "impact": "Medium"})
            st.rerun()
        
        # Render existing entries
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
                
                # Remove button for entries (except the first one)
                if i > 0 or len(st.session_state.trend_data[area]) > 1:
                    if col4.button("❌", key=f"remove_{area}_{i}", help="Remove this entry"):
                        st.session_state.trend_data[area].pop(i)
                        st.rerun()

    if st.button("📄 Get Trend Summary"):
        # Prepare trends payload in the required format
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
            print(trends_payload)
            resp = requests.post(f"{BASE_URL}/trends/analyze", json=trends_payload)
            print(resp)
            resp.raise_for_status()  # Raise an exception for non-200 responses
            response_data = resp.json()
            st.subheader("📋 Trend Summary")
            
            # Handle the nested response structure
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
                l = len(response_data["summary"]["irrelevant_answers"])
                for i in range(l):
                    st.markdown(f"{i+1}. {response_data['summary']['irrelevant_answers'][i]}")
                
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
            st.error(f"API Error: {e}")
        except Exception as e:
            st.error(f"Unexpected Error: {e}")

    # Return formatted trends data
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

                # Prepare the names and percentages from the response data
                names = ['Strengths', 'Weaknesses', 'Opportunities', 'Threats']
                percentages = [
                    int(response_data['scores']['strengths_percentage']),
                    int(response_data['scores']['weaknesses_percentage']),
                    int(response_data['scores']['opportunities_percentage']),
                    int(response_data['scores']['threats_percentage'])
                ]

                # Display the SWOT Scores chart
                st.markdown("### 📊 SWOT Scores")

                # Create a DataFrame for proper plotting
                df = pd.DataFrame({
                    'Category': names,
                    'Percentage': percentages
                })

                # Plotting the bar chart using st.bar_chart
                st.bar_chart(df.set_index('Category')['Percentage'])

                # Display the breakdown of the SWOT scores
                st.markdown("### 📈 SWOT Recommendations")
                st.markdown("#### Strengths")
                st.markdown(response_data['recommendations']['strengths_recommendation'])
                st.markdown("#### Weaknesses")
                st.markdown(response_data['recommendations']['weaknesses_recommendation'])
                st.markdown("#### Opportunities")
                st.markdown(response_data['recommendations']['opportunities_recommendation'])
                st.markdown("#### Threats")
                st.markdown(response_data['recommendations']['threats_recommendation'])
                
                
                # Handle the actual API response structure
                # if "recommendations" in response_data:
                #     st.markdown("### 💡 SWOT Recommendations")
                #     st.markdown(response_data["recommendations"])
                # elif "analysis" in response_data:
                #     st.markdown("### 📊 SWOT Analysis")
                #     st.markdown(response_data["analysis"])
                # else:
                #     # If response has multiple keys, display them all
                #     for key, value in response_data.items():
                #         if isinstance(value, str) and value.strip():
                #             st.markdown(f"### {key.replace('_', ' ').title()}")
                #             st.markdown(value)
                
                if not response_data:
                    st.warning("No SWOT analysis generated.")
                    
            except requests.exceptions.HTTPError as e:
                st.error(f"API Error: {e}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please enter at least one item in any SWOT category.")

    return swot_payload

# --- Render Challenge Input ---
def render_challenge_section(swot_input, trend_input):
    st.header("🚨 Challenge Input")

    # Add new challenge button
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

    # Render existing challenges
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
                        # Format payload according to API specification
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
                            
                            # Display additional evaluation details if available
                            if "evaluation" in response_data:
                                st.markdown("**Evaluation Details:**")
                                st.markdown(response_data["evaluation"])
                                
                        except requests.exceptions.HTTPError as e:
                            st.error(f"API Error: {e}")
                        except Exception as e:
                            st.error(f"Unexpected Error: {e}")
                    else:
                        st.warning("Please fill in at least the title and description.")
            
            with col_remove:
                if len(st.session_state.challenges) > 1:
                    if st.button(f"❌ Remove", key=f"remove_ch_{i}"):
                        st.session_state.challenges.pop(i)
                        st.rerun()
            
            # Display current risk score if available
            if ch.get("risk_score") is not None:
                st.info(f"Current Risk Score: {ch['risk_score']}")

    # Challenge recommendations
    if st.button("💡 Get Challenge Recommendations"):
        valid_challenges = []
        for ch in st.session_state.challenges:
            if (ch.get("title", "").strip() and 
                ch.get("description", "").strip() and 
                ch.get("risk_score") is not None):
                valid_challenges.append({
                    "title": ch["title"].strip(),
                    "category": ch["category"].strip(),
                    "impact_on_business": ch["impact_on_business"],
                    "ability_to_address": ch["ability_to_address"],
                    "description": ch["description"].strip(),
                    "risk_score": ch["risk_score"]
                })
        
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
                
                # Handle the actual API response structure
                if "recommendations" in response_data:
                    st.markdown("### 💡 Recommendations")
                    st.markdown(response_data["recommendations"])
                elif "analysis" in response_data:
                    st.markdown("### 📊 Analysis")
                    st.markdown(response_data["analysis"])
                else:
                    # If response has multiple keys, display them all
                    for key, value in response_data.items():
                        if isinstance(value, str) and value.strip():
                            st.markdown(f"### {key.replace('_', ' ').title()}")
                            st.markdown(value)
                
                if not response_data:
                    st.warning("No recommendations generated.")
                    
            except requests.exceptions.HTTPError as e:
                st.error(f"API Error: {e}")
            except Exception as e:
                st.error(f"Unexpected Error: {e}")
        else:
            st.warning("Please evaluate at least one challenge with title and description to get recommendations.")

# --- Main Rendering ---
trends = render_trend_section()
swot = render_swot_section()
render_challenge_section(swot, trends)