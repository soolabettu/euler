# Runs a minimal OpenAI API smoke test that requests a haiku and prints the response.

import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

response = client.responses.create(
    model="gpt-5-nano",
    input="write a haiku about ai",
    store=True,
)

print(response.output_text)
