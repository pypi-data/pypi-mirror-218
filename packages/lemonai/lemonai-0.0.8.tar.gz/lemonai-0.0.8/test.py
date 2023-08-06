import os
from src.lemonai import execute_workflow
from langchain import OpenAI


os.environ["OPENAI_API_KEY"] = "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"
# os.environ["AIRTABLE_SECRET_TOKEN"] = "patJoC5EBAvPKdAjY.42c1c66934da89b3935cad9c41c88d7de750101dfcc111e1958a3c679b01599a"
os.environ["NOTION_SECRET_KEY"] = "secret_G5te2ouZNJUWKFdGApAd7p6SxfD3W4YplsTnKbP1L66"

# prompt = "Read information from Hackernews for user kimburgess and then write the results to my Airtable with BaseId app2VdQRffkyAiIcc and tableId tblscnilGk6BHVkVn. Only write the fields 'username', 'karma' and 'created_at_i'. Please make sure that Airtable does NOT automatically convert the field types."
# prompt = "Run the Hackernews Airtable User Workflow for user kimburgess, baseId app2VdQRffkyAiIcc and tableId tblscnilGk6BHVkVn. Only write the fields 'username', 'karma' and 'created_at_i' to the Airtable table. Please make sure that Airtable does NOT automatically convert the field types."
prompt = "Get hackernews data for user kimburgess and article 13431133"
# prompt = "Get me information from my Notion database with id d46a3735b9944339b6fd4438fbd53820"
# prompt = "Get me information all my Notion databases"
# prompt = "Get all Notion users"
# prompt = "Append a block to Notion page id 7e8255e52be640c19678968d726a6fb4 with 'Hello I am testing'"
# prompt = "Get all Notion child blocks from my page with id 7e8255e52be640c19678968d726a6fb4"
# prompt = "Search Notion database id d46a3735b9944339b6fd4438fbd53820 for Mohammed"
# prompt = "Update my database page in Notion (id 2fd2dd70ed88418a8ee622e063858169) to have title HelloCito"
# prompt = "Get all database pages (id d46a3735b9944339b6fd4438fbd53820) from Notion"
# prompt = "Create a database page in my Notion (id d46a3735b9944339b6fd4438fbd53820) with Name Abdus and Email abdus@citodata.com"
# prompt = "Archive my Notion page (id 70b0189f2b0944b1b99ae2f20dd1c0fc)"
# prompt = "Create a Notion page with id 7e8255e52be640c19678968d726a6fb4 and title Hello World"


model = OpenAI(temperature=0)
execute_workflow(llm=model, prompt_string=prompt)




