from promptflow import tool
import json

# Function to parse JSON-like data from a string
def parse_json_string(json_string):
    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}


def validate_address(address, provider_name=""):
    """validate addresss"""
    if "12345" in address:
        address_info = {
            "valid": "false",
            "reason": "provider does not exist at the given address"
        }
    else:    
        address_info = {
            "valid": "true",
            "reason": f"provider {provider_name} exists at the given address"
        }
    return json.dumps(address_info)


def validate_DIN(DIN):
    """validate DIN"""
    if "10001-0022-20" in DIN:
        din_info = {
            "valid": "false",
            "reason": "din NOT found in drug database"
        }
    else:     
        din_info = {
            "valid": "true",
            "reason": "din found in drug database"
        }
    return json.dumps(din_info)


@tool
def run_function(response: dict, sys_prompt: str) :
    messages=[
                {"role": "user", "content": sys_prompt}
             ]
    #response = parse_json_string(response_str)
    response_message = response['choices'][0]['message']
    tool_calls = response_message['tool_calls']
    messages.append(response_message)  # extend conversation with assistant's reply

    if tool_calls:
       
        # send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call['function']['name']
            function_args = json.loads(tool_call['function']['arguments'])
            print(function_args)
            function_response = globals()[function_name](**function_args)
            messages.append(
                {
                    "tool_call_id": tool_call['id'],
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        return messages   
    else:
        print("No function call")
        return messages

# as_dict = completion.model_dump()
# reconstructed = openai.types.chat.chat_completion.ChatCompletion(**as_dict)
# https://github.com/openai/openai-python/issues/777#issuecomment-1907781584