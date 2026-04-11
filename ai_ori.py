import os
import json
import time
from jaraco.functools import retry
from mistralai.client import Mistral
from calendar_manager import Calendar

class Chatbot:
    def __init__(self):
        api_key = os.environ.get("MISTRAL_API_KEY")
        self.client = Mistral(api_key=api_key)
        self.inputs = [
            {"role": "user", "content": "The year is 2026. You are a helpful assistant that can manage calendar events for the user. You can create, update, delete, and list calendar events based on the user's requests. Time zone is Hong Kong."}
        ]

        

        response = self.client.beta.conversations.start(
            agent_id="ag_019d7cd9d8e9742b8470826d4118d190",
            inputs=self.inputs
        )

        with open('tools.json', 'r') as f:
            self.tools = json.load(f)

        # model = "mistral-large-latest"

        # print(type(response))
        print(response.conversation_id)
        print(response.outputs)

        self.conversation_id = response.conversation_id

        self.calendar = Calendar()


    def continue_conversation(self, message):
        print("NEW CONVERSATION MESSAGE", message)
        # inputs = [
        #     {"role":"user","content": message}
        # ]
        self.inputs.append({"role":"user","content": message})


        retry = True
        while retry:
            try:
                response = self.client.beta.conversations.append(
                    conversation_id=self.conversation_id,
                    inputs=self.inputs,
                    # tools=self.tools,
                    # tool_choice="any",
                    # parallel_tool_calls=False,
                )
                # response = self.client.beta.conversations.start(
                #     agent_id="ag_019d7757d3e2708898840d8b95fb7a36",
                #     inputs=self.inputs,
                #     # tools=self.tools,
                #     # tool_choice="any",
                #     # parallel_tool_calls=False,
                # )
                
                print("response:", response)
                
                responses = []
                return_back = []
                for output in response.outputs:
                    self.inputs.append({
                        "role":"assistant","content":output.content
                    })
                    # return_back.append({
                    #     "type": "function.result",
                    #     "tool_call_id": output.tool_call_id,  # CRITICAL - must match original call
                    #     "result": json.dumps(response)  # JSON string
                    # })

                    if output.type == 'message.output':
                        content = json.loads(output.content)
                        if 'message' in content:
                            return content['message'], False
                        elif 'follow_up' in content:
                            return content['follow_up'], False
                        elif 'response' in content:
                            return content['response'], False
                        elif 'output' in content:
                            return content['output'], False
                        # return json.loads(output.content)["message"], False

                        # response = self.execute_tools(content['function_call']['name'], content['function_call']['arguments'])
                        # responses.append(response)
                    else:
                        response = self.execute_tools(output.name, json.loads(output.arguments))
                        responses.append(response)

                        self.inputs.append({
                            "type": "function.result",
                            "tool_call_id": output.tool_call_id,  # CRITICAL - must match original call
                            "result": json.dumps(response)  # JSON string
                        })

                self.client.beta.conversations.append(
                    conversation_id=self.conversation_id,
                    inputs=self.inputs
                )
                # response = self.client.beta.conversations.start(
                #     agent_id="ag_019d7757d3e2708898840d8b95fb7a36",
                #     inputs=self.inputs,
                #     # tools=self.tools,
                #     # tool_choice="any",
                #     # parallel_tool_calls=False,
                # )

                retry = False

            except Exception as e:
                print(e)
                time.sleep(0.5)
                # inputs = [
                #     {"role":"user","content":"Make a meeting with Bob tomorrow at 2pm"}
                # ]
                
                continue
            

        # self.execute_tools(response.outputs)
        return responses, True


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
        else:
            print(f"Unknown tool: {tool_name}")

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

# c = Chatbot()
# c.continue_conversation("Make a team meeting event for 3 hours at 1pm next Monday. then, update that team meeting to 6pm.")
# c.continue_conversation("Arrange a 2 hour stargazing at midnight sunday night")
# c.execute_tools("set_new_event", {"start": "2026-04-12T14:00:00", "end": "2026-04-12T15:00:00", "summary": "Meeting with Bob"})

# conversation = Mistral(api_key=os.environ["MISTRAL_API_KEY"]).beta.conversations.get_history(
#     conversation_id='conv_019d7ce24336742f959965a995464da4'
# )
# print(conversation)