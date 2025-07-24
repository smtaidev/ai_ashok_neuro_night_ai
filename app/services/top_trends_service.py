# # Step 3: Create service to extract top 3 trends

# # app/services/top_trends_service.py
# from openai import AsyncOpenAI
# from ..core.config import settings
# from ..memory import store

# client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# async def get_top_3_trends() -> list[str]:
#     if not store.last_trend_input:
#         return ["No trend input submitted yet via /summary"]

#     raw_data = ""  # simple raw concatenation for now
#     for section in store.last_trend_input.model_dump().values():
#         for item in section:
#             if item.get("answer"):
#                 raw_data += f"- {item['answer']}\n"

#     system_prompt = """
#     You are an analyst. Your task is to extract the top 3 emerging trends from the following information.
#     Focus on relevance, recurrence, and strategic importance.
#     Respond with a simple list format.
#     """

#     response = await client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": raw_data},
#         ],
#         temperature=0.3,
#         max_tokens=500,
#     )

#     # Very basic parsing: return each line as an item
#     lines = response.choices[0].message.content.strip().split("\n")
#     return [line.strip("- ") for line in lines if line.strip()]
