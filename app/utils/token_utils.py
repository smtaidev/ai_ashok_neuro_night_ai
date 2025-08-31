# app/utils/token_utils.py

import tiktoken
from app.core import AI_models
def count_tokens(text: str, model: str = AI_models.MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def count_chat_tokens(messages: list[dict], model: str = AI_models.MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens_per_message = 3
    tokens_per_name = 1
    total_tokens = 0

    for message in messages:
        total_tokens += tokens_per_message
        for key, value in message.items():
            total_tokens += len(encoding.encode(value))
            if key == "name":
                total_tokens += tokens_per_name

    total_tokens += 2  # Priming tokens for the reply
    return total_tokens
