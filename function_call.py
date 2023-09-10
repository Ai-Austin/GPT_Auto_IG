import openai
import json
import os
import image_generator
import ig_poster

openai.api_key = os.environ.get('OPEN_AI_KEY')
input_tokens = 0
output_tokens = 0
messages = [{'role': 'system', 'content': 'You are a highly intelligent AI capable of running predefined functions to complete user tasks. You have been given the ability to create AI generated art with the "generate_image" function and even post to instagram if the user asks using the "post_to_ig" function. The "generate_image" function MUST RECEIVE INPUT AS "text_input_prompt". The "post_to_ig" function MUST RECEIVE INPUT AS "instagram_caption". You will commonly get prompts from the user that require multiple functions to be called. Think of the logical order the functions must be ran, and run them in order. You will get a second response from the system once the first function finishes, then decide if there are more functions and run them at that point.'}]
functions = [
    {
        'name': 'generate_image',
        'description': 'Uses Midjourney AI image generation to create an image based off the users text input prompt. Extract the details from the users prompt that describes the image they want to pass as input to this function. No response will be returned from this function, it will open an image after generating the image for the user.',
        'parameters': {
            'type': 'object',
            'properties': {
                'text_input_prompt': {
                    'type': 'string',
                    'description': 'The description of the photo the user would like generated.',
                },
            },
            'required': ['text_input_prompt'],
        }
    },
    {
        'name': 'post_to_ig',
        'description': 'Allows you to post to the users instagram. After using the generate_image function in a conversation you can post that image to instagram by passing this function the caption.',
        'parameters':{
            'type': 'object',
            'properties': {
                'instagram_caption': {
                    'type': 'string',
                    'description': 'The text caption for the instagram post.'
                },
            },
            'required': ['instagram_caption']
        },
    }
]

def generate_image(text_input_prompt):
    image_generator.run_bot(text_input_prompt=text_input_prompt)
    return 'Image successfully generated.'

def post_to_ig(instagram_caption):
    ig_poster.auto_post(instagram_caption)
    return 'Instagram post is live!'

def handle_function_call(response):
    available_functions = {
        'generate_image': generate_image,
        'post_to_ig': post_to_ig,
    }  
    
    function_name = response['choices'][0]['message']['function_call']['name']
    function_to_call = available_functions[function_name]
    function_args = json.loads(response['choices'][0]['message']['function_call']['arguments'])

    if function_name == 'generate_image':
        function_response = function_to_call(function_args['text_input_prompt'])
    elif function_name == 'post_to_ig':
        function_response = function_to_call(function_args['instagram_caption'])

    print(function_name + ' function call has completed.')
    messages.append({'role': 'function', 'name': function_name, 'content': function_response})

def run_conversation():
    global messages
    global input_tokens
    global output_tokens
    while True:
        # Makes sure we are only sending 4 total converation messages and system prompt as messages in our new API calls.
        # This will avoid spending unnecessarily for context prompt tokens and prevent input prompt size from exceeding max tokens. 
        if len(messages) > 5:
            messages = [messages[0]] + messages[-4:]
        
        user_prompt = input('User: ')
        messages.append({'role': 'user', 'content': user_prompt})
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0613',
            messages=messages,
            functions=functions,
            function_call='auto',
        )
        input_tokens += response['usage']['prompt_tokens']
        output_tokens += response['usage']['completion_tokens']
        if response['choices'][0]['finish_reason'] == 'function_call':
            handle_function_call(response)
            # Check if a second function needs to be called, if not GPT will create a message response.
            second_response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo-0613',
                messages=messages,
                functions=functions,
                function_call='auto'
            )

            input_tokens += second_response['usage']['prompt_tokens']
            output_tokens += second_response['usage']['completion_tokens']

            if second_response['choices'][0]['finish_reason'] == 'function_call':
                handle_function_call(second_response)
            else:
                print('ChatGPT: ' + response['choices'][0]['message']['content'])
                messages.append({'role': 'assistant', 'content': response['choices'][0]['message']['content']})

        else:
            print('ChatGPT: ' + response['choices'][0]['message']['content'])
            messages.append({'role': 'assistant', 'content': response['choices'][0]['message']['content']})
            
        print('Input tokens: ' + str(input_tokens))
        print('Output tokens: ' + str(output_tokens))
        input_price = input_tokens / 1000 * 0.0015
        output_price = output_tokens / 1000 * 0.002
        print('Task Price in USD: $' + str("{:.5f}".format(input_price + output_price)))

run_conversation()
