# Count Cars
This workflow is designed to automate the counting of red cars in two separate images. The primary use of this flow is to accurately identify and tally the number of red cars present in each image and then compute the total count across both images.

## Tools Utilized in the Flow
- **LLM tool**
- **Python tool**

## Prerequisites for Executing the Flow
- **Image*: Images containing various claims to be analyzed.
- **Azure OpenAI Access**: Necessary credentials and access rights to Azure OpenAI GPT-4 Turbo with Vision.

## Process Overview
- **Image Analysis**: Each image is independently analyzed by Azure OpenAI GPT-4 Turbo with Vision to count the number of red cars.
- **JSON Output**: The counts are output in JSON format, with a structure like: `{"red cars": <number_of_red_cars>}`.
- **Total Count Calculation**: The custom script reads the JSON outputs from both images and calculates the total number of red cars.

## Knowledge Acquired from This Flow
- Integrating Azure OpenAI GPT-4 Turbo with Vision for specific image analysis tasks.
- Handling and parsing JSON data.
- Scripting to aggregate data from multiple sources.

How to do tools/functions calling:
https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/function-calling?tabs=python-new
https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/tools-reference/azure-open-ai-gpt-4v-tool?view=azureml-api-2

https://learn.microsoft.com/en-us/azure/ai-studio/how-to/flow-process-image

