# import os

# from mistralai.client import Mistral

# client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

# inputs = [
#     {"role":"user","content":"Hi"}
# ]

# response = client.beta.conversations.start(
#     agent_id="ag_019d7cd9d8e9742b8470826d4118d190",
#     inputs=inputs,
# )

# inputs.append({
#     "role":"assistant","content":response.outputs[0].content
# })

# print(response)

# inputs.append(
#     {"role":"user","content":"Make a new event of Lunch with Bob"}
# )

# response = client.beta.conversations.start(
#     agent_id="ag_019d7cd9d8e9742b8470826d4118d190",
#     inputs=inputs,
# )

# inputs.append({
#     "role":"assistant","content":response.outputs[0].content
# })

# print(response)

# inputs.append(
#     {"role":"user","content":"Tomorrow at 2pm for 1 hour, and set location to Central"}
# )

# response = client.beta.conversations.start(
#     agent_id="ag_019d7cd9d8e9742b8470826d4118d190",
#     inputs=inputs,
# )

# print(response)

# Imports
import pandas as pd
import os
from mistralai.client import Mistral
import json

# Example Dataset to query from
data = {
    'transaction_id': ['T1001', 'T1002', 'T1003', 'T1004', 'T1005'],
    'customer_id': ['C001', 'C002', 'C003', 'C002', 'C001'],
    'payment_amount': [125.50, 89.99, 120.00, 54.30, 210.20],
    'payment_date': ['2021-10-05', '2021-10-06', '2021-10-07', '2021-10-05', '2021-10-08'],
    'payment_status': ['Paid', 'Unpaid', 'Paid', 'Paid', 'Pending']
}
df = pd.DataFrame(data)

# Functions to be used as tools
def retrieve_payment_status(transaction_id: str) -> str:
    "Get payment status of a transaction"
    if transaction_id in df.transaction_id.values:
        return json.dumps({'status': df[df.transaction_id == transaction_id].payment_status.item()})
    return json.dumps({'error': 'transaction id not found.'})
def retrieve_payment_date(transaction_id: str) -> str:
    "Get payment date of a transaction"
    if transaction_id in df.transaction_id.values:
        return json.dumps({'date': df[df.transaction_id == transaction_id].payment_date.item()})
    return json.dumps({'error': 'transaction id not found.'})

# Map function names to the functions
names_to_functions = {
    'retrieve_payment_status': retrieve_payment_status,
    'retrieve_payment_date': retrieve_payment_date,
}

# Define the system prompt
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. You can use the following tools to help answer the user's questions related to payment transactions."
    }
]

# Define the tools specifications
tools = [
    {
        "type": "function",
        "function": {
            "name": "retrieve_payment_status",
            "description": "Get payment status of a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "The transaction id.",
                    }
                },
                "required": ["transaction_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_payment_date",
            "description": "Get payment date of a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "The transaction id.",
                    }
                },
                "required": ["transaction_id"],
            },
        },
    }
]
# Note: You can specify multiple parameters for each function in the `properties` object.

# Initialize the client and model
api_key = os.environ.get("MISTRAL_API_KEY")
model = "mistral-large-latest"
client = Mistral(api_key=api_key)
temperature = 0.1
top_p = 0.9

# Chat loop
while True:

    # The user query, example: "What's the status of my transaction T1001? After receiving the answer, provide the current status of T1001. Afte that, look for the next one between T1002 if previous status was 'Paid' and T1003 if previous status was 'Unpaid'."
    user_query = input("User: ")
    if not user_query:
        break
    messages.append({"role": "user", "content": user_query})

    # Call the model
    response = client.chat.complete(
        model = model,
        messages = messages,
        tools = tools,
        temperature = temperature,
        top_p = top_p
    )

    print(response)
    # Add the response message to the messages list
    messages.append(response.choices[0].message)


    # Retrieve the function name and arguments if any, interactively until the model returns a final answer
    while response.choices[0].message.tool_calls:

        # Print content in case we have interleaved tool calls and text content
        if response.choices[0].message.content:
            print("Assistant:", response.choices[0].message.content)

        # Handle each tool call
        for tool_call in response.choices[0].message.tool_calls:

            function_name = tool_call.function.name # The function name to call
            function_params = json.loads(tool_call.function.arguments) # The function arguments
            function_result = names_to_functions[function_name](**function_params) # The function result

            # Print the function call
            print(f"Tool {tool_call.id}:", f"{function_name}({function_params}) -> {function_result}")

            # Add the function result to the messages list and call model
            messages.append({
                "role":"tool",
                "name":function_name,
                "content":function_result,
                "tool_call_id":tool_call.id
            })

        response = client.chat.complete(
            model = model,
            messages = messages,
            tools = tools,
            temperature = temperature,
            top_p = top_p
        )

        # Add the new response message to the messages list
        messages.append(response.choices[0].message)

    # Print the final answer
    print("Assistant:", response.choices[0].message.content)