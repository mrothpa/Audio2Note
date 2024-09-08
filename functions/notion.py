from notion_client import Client
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../auth')))

from notion_keys import NOTION_API_TOKEN, DATABASE_ID

notion = Client(auth=NOTION_API_TOKEN)

response = notion.databases.query(database_id=DATABASE_ID)

for result in response.get('results', []):
    task_title = result['properties']['Name']['title'][0]['text']['content']
    print(f"Task: {task_title}")