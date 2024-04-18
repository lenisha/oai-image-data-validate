from promptflow.core import tool
import logging
from openai import AzureOpenAI
from promptflow.connections import AzureOpenAIConnection

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(sys_prompt: str, deployment_name: str, 
                  oaiConn: AzureOpenAIConnection ):
    logging.basicConfig(level=logging.INFO) 

    logging.info(f"Prompt for query: {sys_prompt}")

    tools = [
            {
                "type": "function",
                "function": {
                    "name": "validate_address",
                    "description": "Validate address given location with city and postal code ",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "address": {
                            "type": "string",
                            "description": "The address and city and province, and postal code  e.g. 222 Front str. ,Toronto, ON M65 L9X"
                        },
                        "provider_name": {
                            "type": "string",
                            "description": "The name of provider"
                        }
                        },
                        "required": [
                        "address","provider_name"
                        ]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "validate_DIN",
                    "description": "Validate drug DIN number agains Canadian Drug Database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "DIN": {
                            "type": "string",
                            "description": "the DIN number for drug in prescription"
                        }
                        },
                        "required": [
                        "DIN"
                        ]
                    }
                }
            }
            ]

    client = AzureOpenAI(
        api_key=oaiConn.api_key,
        azure_endpoint=oaiConn.api_base,
        api_version=oaiConn.api_version
    )
    kwargs = {
        'temperature': 0.0,
        'top_p': 1.0,
        'n': 1,
        'stream': False,
        'stop': None,
        'max_tokens': 700,
        'presence_penalty': 0.0,
        'frequency_penalty': 0.0,
        'response_format': None
    }
    resp = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": sys_prompt}
        ],
        tools=tools,
        tool_choice="auto",
        **kwargs
    )

    logging.info(f"Response: {resp.choices[0]}")
    return resp.model_dump(exclude_unset=True, exclude_none=True)

