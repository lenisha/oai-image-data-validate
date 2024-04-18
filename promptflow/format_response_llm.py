from promptflow.core import tool
import logging,json 
from openai import AzureOpenAI
from promptflow.connections import AzureOpenAIConnection

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(messages: object, deployment_name: str, 
                  oaiConn: AzureOpenAIConnection ):
    logging.basicConfig(level=logging.INFO) 

    logging.info(f"Prompt for query: {messages}")

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
        'response_format': { "type": "json_object" }
    }
    resp = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        **kwargs
    )

    logging.info(f"Response: {resp.choices[0]}")
    response_model = resp.model_dump(exclude_unset=True, exclude_none=True)
    content = response_model['choices'][0]['message']['content']
 
    return json.loads(content.replace("```json\n", "").replace("```", ""))

   
