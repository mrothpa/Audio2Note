from notion_client import Client
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../auth')))

from notion_credentials import NOTION_API_TOKEN, DATABASE_ID

def add_page(name, id_, translation, summary):
    notion = Client(auth=NOTION_API_TOKEN)
    
    chunks = [translation[i:i + 2000] for i in range(0, len(translation), 2000)]
    text_blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": chunk
                        }
                    }
                ]
            }
        }
        for chunk in chunks
    ]
    summary_block = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": summary
                    }
                }
            ]
        }
    }
    divider_block = {
        "object": "block",
        "type": "divider",
        "divider": {}
    }
    audio_block = {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Link zur Audio-Datei: https://drive.google.com/drive/folders/" + id_,
                        "link": {
                            "url": "https://drive.google.com/drive/folders/" + id_
                        }
                    }
                }
            ]
        }
    }
    
    # Die neue Seite erstellen
    if summary:
        children_blocks = [summary_block] + [divider_block] + text_blocks + [divider_block] + [audio_block]
        new_page = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": name
                            }
                        }
                    ]
                }
            },
            "children": children_blocks,
            "icon": {
                "type": "external",
                "external": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Pencil-icon.png/800px-Pencil-icon.png"
                }
            }
        }
        
        response = notion.pages.create(**new_page)
        print(f"Seite {name} erfolgreich hinzugefügt: {response}")
        print()
        
    else:
        children_blocks = text_blocks + [divider_block] + [audio_block]
        new_page = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": name
                            }
                        }
                    ]
                }
            },
            "children": children_blocks,
            "icon": {
                "type": "external",
                "external": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Pencil-icon.png/800px-Pencil-icon.png"
                }
            }
        }
        
        response = notion.pages.create(**new_page)
        print(f"Seite {name} erfolgreich hinzugefügt: {response}")
        print()

# add_page("TEST-NOTIZ", "12345", "THIS is a random lorem ipsum text.", "lorem ipsum summary")