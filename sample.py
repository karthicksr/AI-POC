from openai import OpenAI

client = OpenAI(
  api_key="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"
)

response = client.responses.create(
  model="gpt-5.4-mini",
  input="write a haiku about ai",
  store=True,
)

print(response.output_text);
