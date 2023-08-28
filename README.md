# This is a research project to test the new GPT function calling 
In order to use this code you will need a mid to advanced level understanding of Python. The function_call.py code will function as is and serve as a good example of how to communicate with the OpenAI API to automate a task that requires two function calls from one prompt input. But in order for the image_generator.py and ig_poster.py files to work will require quite a few setup steps.

## Set API keys as system variable
```
OPEN_AI_KEY
DISCORD_BOT_TOKEN
```

## To get image_generator.py to work: 
* Create your own Discord channel and add the Midjourney bot. 
* Create a Discord bot and give it permissions to access that channel.
* Replace the images in the 'pyautogui_images' directory with screenshots of the correct places to click for automating sending the /imagine prompt to midjourney in the Discord GUI.

## To get ig_poster.py to work:
* Login to your instagram account in Safari on mac
    * If not on mac login with your desired browser and change the subprocess call to open that application name. 
* Again replace the images in the 'pyautogui_images' directory of screenshots of the correct buttons on your screen.

