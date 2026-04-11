import datetime
import os
import json
import time
from flask.cli import load_dotenv
from jaraco.functools import retry
from mistralai.client import Mistral
from calendar_manager import Calendar

class Chatbot:
    def __init__(self):

        # api_key = os.environ.get("MISTRAL_API_KEY")
        # self.client = Mistral(api_key=api_key)
        # self.inputs = [
        #     {"role": "user", "content": "The year is 2026. You are a helpful assistant that can manage calendar events for the user. You can create, update, delete, and list calendar events based on the user's requests. Time zone is Hong Kong."}
        # ]

        self.inputs = [
            {
                "role": "system",
                "content": f"Today is {datetime.date.today()}. You are a helpful assistant that can manage calendar events for the user. You can create, update, delete, and list calendar events based on the user's requests. Time zone is Hong Kong."
            }
        ]

        # response = self.client.beta.conversations.start(
        #     agent_id="ag_019d7cd9d8e9742b8470826d4118d190",
        #     inputs=self.inputs
        # )

        with open('tools.json', 'r') as f:
            self.tools = json.load(f)
        
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        self.model = "mistral-large-latest"
        self.client = Mistral(api_key=self.api_key)
        self.temperature = 0.1
        self.top_p = 0.9

        # print(type(response))
        # print(response.conversation_id)
        # print(response.outputs)

        # self.conversation_id = response.conversation_id

        self.calendar = Calendar()

        # self.names_to_functions = {
        #     'retrieve_payment_status': retrieve_payment_status,
        #     'retrieve_payment_date': retrieve_payment_date,
        # }


    def continue_conversation(self, message):
        print("NEW CONVERSATION MESSAGE", message)
        # inputs = [
        #     {"role":"user","content": message}
        # ]
        self.inputs.append({"role": "user", "content": message})

        response = self.client.chat.complete(
            model = self.model,
            messages = self.inputs,
            tools = self.tools,
            temperature = self.temperature,
            top_p = self.top_p
        )

        self.inputs.append(response.choices[0].message)

        while response.choices[0].message.tool_calls:
            if response.choices[0].message.content:
                print("Assistant:", response.choices[0].message.content)

            # Handle each tool call
            for tool_call in response.choices[0].message.tool_calls:

                function_name = tool_call.function.name # The function name to call
                function_params = json.loads(tool_call.function.arguments) # The function arguments
                # function_result = names_to_functions[function_name](**function_params) # The function result
                function_result = self.execute_tools(function_name, function_params)

                # Print the function call
                print(f"Tool {tool_call.id}:", f"{function_name}({function_params}) -> {function_result}")

                # Add the function result to the messages list and call model
                self.inputs.append({
                    "role":"tool",
                    "name":function_name,
                    "content":function_result,
                    "tool_call_id":tool_call.id
                })

            response = self.client.chat.complete(
                model = self.model,
                messages = self.inputs,
                tools = self.tools,
                temperature = self.temperature,
                top_p = self.top_p
            )

            # Add the new response message to the messages list
            self.inputs.append(response.choices[0].message)

        # Print the final answer
        print("Assistant:", response.choices[0].message.content)

        return response.choices[0].message.content


    def execute_tools(self, tool_name, arguments):
        print("Executing tool:", tool_name, arguments)
        if tool_name == 'list_upcoming_events':
            result = self.calendar.list_upcoming_events(**arguments)
            print(f"Tool: {tool_name}, Arguments: {arguments}, Result: {result}")
        elif tool_name == 'set_new_event':
            result = self.calendar.set_new_event(**arguments)
            print(f"Tool: {tool_name}, Arguments: {arguments}, Result: {result}")
        elif tool_name == 'update_event':
            result = self.calendar.update_event(**arguments)
            print(f"Tool: {tool_name}, Arguments: {arguments}, Result: {result}")
        elif tool_name == 'delete_event':
            result = self.calendar.delete_event(**arguments)
            print(f"Tool: {tool_name}, Arguments: {arguments}, Result: {result}")
        elif tool_name == 'get_event_ids':
            result = self.calendar.get_event_ids(**arguments)
            print(f"Tool: {tool_name}, Arguments: {arguments}, Result: {result}")
        else:
            print(f"Unknown tool: {tool_name}")
        # return "good"
        return result


# print(response)



# client = Mistral(api_key=api_key)
# response = client.beta.conversations.append(
#     conversation_id="conv_019d78a0a6e277968bdb348db5d3b13b",
#     inputs = inputs, # The message history, in this example we have a system (optional) + user query.
#     # tools = tools, # The tools specifications
#     # tool_choice = "any",
#     # parallel_tool_calls = False,
# )


# load_dotenv()

# c = Chatbot()
# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ['exit', 'quit']:
#         break
#     c.continue_conversation(user_input)


    # print("Response:", response)
# c.continue_conversation("Make a team meeting event for 3 hours at 1pm next Monday. then, update that team meeting to 6pm.")
# c.continue_conversation("Arrange a 2 hour stargazing at midnight sunday night")
# c.execute_tools("set_new_event", {"start": "2026-04-12T14:00:00", "end": "2026-04-12T15:00:00", "summary": "Meeting with Bob"})

# conversation = Mistral(api_key=os.environ["MISTRAL_API_KEY"]).beta.conversations.get_history(
#     conversation_id='conv_019d7ce24336742f959965a995464da4'
# )
# print(conversation)