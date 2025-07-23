from openai import AsyncOpenAI
import json
from app.core.config import settings
from app.utils import business_goal_parsers as parsers
from app.api.models.business_goal_model import BusinessGoalRequest, BusinessGoalResponse

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def _call_openai_for_json(system_prompt: str, user_prompt: str) -> str:
    """Helper function to call the OpenAI API in JSON mode."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return json.dumps({"error": f"OpenAI API call failed: {e}"})

async def analyze_business_goal(request: BusinessGoalRequest) -> BusinessGoalResponse:
    system_prompt = "You are a senior business strategist and risk analyst. Your job is to analyze detailed information about a business goal and synthesize it into six key summary sections. Your response must be a single, valid JSON object."
    json_schema = BusinessGoalResponse.model_json_schema()
    
    # Format the input data into a clean text block for the prompt
    input_data_text = f"""
    ### Goal Analysis Input

    **1. Potential Risks and Challenges:**
    - Answer: {request.potential_risks_and_challenges.answer or "Not provided"}
    - Impact: {request.potential_risks_and_challenges.impact or "N/A"}

    **2. Regulatory Compliance:**
    - Answer: {request.regulatory_compliance.answer or "Not provided"}
    - Impact: {request.regulatory_compliance.impact or "N/A"}

    **3. Cultural Realignment:**
    - Answer: {request.cultural_realignment.answer or "Not provided"}
    - Impact: {request.cultural_realignment.impact or "N/A"}

    **4. Change Management:**
    - Answer: {request.change_management.answer or "Not provided"}
    - Impact: {request.change_management.impact or "N/A"}

    **5. Learning and Development:**
    - Answer: {request.learning_and_development.answer or "Not provided"}
    - Impact: {request.learning_and_development.impact or "N/A"}

    **6. Capability Analysis:**
    - Influenced Capabilities: {', '.join(request.capability_info.influenced_capabilities) or "None"}
    - Owner: {request.capability_info.owner or "Not assigned"}
    - Enhancing Existing Capabilities Required: {'Yes' if request.capability_info.require_enhancing_capabilities else 'No'}
    - Enhancement Details: {request.capability_info.enhancement_details or "N/A"}
    - Adding New Capabilities Required: {'Yes' if request.capability_info.require_new_capabilities else 'No'}
    - New Capability Details: {request.capability_info.new_capability.model_dump_json(indent=2) if request.capability_info.new_capability else 'N/A'}
    """
    
    user_prompt = f"""
    Based on the following detailed input about a business goal, generate a comprehensive analysis.
    
    {input_data_text}

    Your task is to produce a JSON object containing six summaries. For each summary, provide a concise, bulleted list of the top 3-4 most important points derived from the corresponding input section.

    The JSON object must contain exactly these six keys: 'risks_summary', 'regulatory_compliance_summary', 'roadblocks_summary', 'culture_realignment_summary', 'change_management_summary', 'learning_and_development_summary'.

    The JSON must conform to this schema:
    {json.dumps(json_schema, indent=2)}
    """

    raw_response = await _call_openai_for_json(system_prompt, user_prompt)
    return parsers.json_to_business_goal_response(raw_response)