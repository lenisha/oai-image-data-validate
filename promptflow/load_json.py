from promptflow.core import tool
import json


# Function to parse JSON-like data from a string
def parse_json_string(json_string):
    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}
        
@tool
def load_json(input1: str) -> str:
    json_string1 = input1.replace("```json\n", "").replace("```", "")
    data1 = parse_json_string(json_string1)
    
    return data1