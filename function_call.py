import openai
import json
import os
import re
import image_generator
import ig_poster
import finances


openai.api_key = os.environ.get('OPEN_AI_KEY')

def generate_image(text_input_prompt):
    image_generator.run_bot(text_input_prompt=text_input_prompt)
    return 'Image successfully generated.'

def post_to_ig(instagram_caption):
    ig_poster.auto_post(instagram_caption)
    return 'Instagram post is live!'

def get_grocery_transactions():
    return finances.get_grocery_transactions()

def clean_dictionary(s):
    # Replace Unicode escape sequences
    s = re.sub(r'\\u[0-9a-fA-F]{4}', '', s)
    # Replace newline characters
    s = s.replace('\\n', '')
    s = s.replace('\\', '')
    if s[1] == ' ':
        s = s[0] + s[2:]
    d = json.loads(s)
    return d

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "system", "content": 'You are a highly intelligent AI capable of running predefined functions to complete user tasks. You have been given the ability to create AI generated art with the "generate_image" function and even post to instagram if the user asks using the "post_to_ig" function. The "generate_image" function MUST RECEIVE INPUT AS "text_input_prompt". The "post_to_ig" function MUST RECEIVE INPUT AS "instagram_caption". You will commonly get prompts from the user that require multiple functions to be called. Think of the logical order the functions must be ran, and run them in order. You will get a second response from the system once the first function finishes, then decide if there are more functions and run them at that point.'},
                {"role": "user", "content": input('ChatGPT: What can I help you with today?')}]
    functions = [
    {
            "name": "generate_image",
            "description": "Uses Midjourney AI image generation to create a image based off the users text input prompt. Extract the details from the users prompt that describes the image they want to pass as input to this function. No response will be returned from this function, it will open an image after generating the image for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text_input_prompt": {
                        "type": "string",
                        "description": "The description of the photo the user would like generated.",
                    },
                },
                "required": ["text_input_prompt"],
            },
            "name": "post_to_ig",
            "description": "Allows you to post to the users instagram. After using the generate_image function in a conversation you can post that image to instagram by passing this function the caption.",
            "parameters":{
                "type": "object",
                "properties": {
                    "instagram_caption": {
                        "type": "string",
                        "description": "The text caption for the instagram post."
                    },
                },
                "required": ["instagram_caption"]
            },
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "generate_image": generate_image,
            "post_to_ig": post_to_ig,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        if function_name == "generate_image":
            print('GPT running generate_image code.')
            function_response = function_to_call(text_input_prompt=function_args.get("text_input_prompt"))
        elif function_name == "post_to_ig":
            print('GPT running post_to_ig code.')
            function_response = function_to_call(instagram_caption=function_args.get("instagram_caption"))

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        if second_response["choices"][0]["finish_reason"] == "function_call":
            available_functions = {
                "generate_image": generate_image,
                "post_to_ig": post_to_ig,
            }  
            function_name = second_response["choices"][0]["message"]["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = clean_dictionary(second_response["choices"][0]["message"]["function_call"]["arguments"])
            if function_name == "generate_image":
                function_response = function_to_call(text_input_prompt=function_args['text_input_prompt'])
            elif function_name == "post_to_ig":
                function_response = function_to_call(instagram_caption=function_args['instagram_caption'])
        if second_response['choices'][0]['message']['content'] != None:
            return second_response['choices'][0]['message']['content']
        print('Task completed!')

print(run_conversation())