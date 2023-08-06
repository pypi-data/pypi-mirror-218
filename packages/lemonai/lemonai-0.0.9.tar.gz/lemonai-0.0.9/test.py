import os
from langchain.llms import OpenAI
from src.lemonai.execute_workflow import execute_workflow

os.environ["OPENAI_API_KEY"] = "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"
os.environ["DISCORD_WEBHOOK_URL"] = "https://discord.com/api/webhooks/983839012324253716/g_3ZS_ldf1K8vaGFhhhY1juO5iZUBYXJDqSguGQYdXU4vIbTWVLxgvnyBlQtz3df__Ql"

llm = OpenAI(temperature=0)

prompt = "Send a message 'Hello world I am Abdus' to my Discord channel"

execute_workflow(llm=llm, prompt_string=prompt)
