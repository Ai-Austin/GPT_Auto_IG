import discord
from discord.ext import commands
import aiohttp  # <-- Added
from PIL import Image
import os
import asyncio
import time
import subprocess
import pyautogui

discord_token = os.environ.get("DISCORD_BOT_TOKEN")
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())
directory = os.getcwd()

def split_image(image_file):
    with Image.open(image_file) as im:
        width, height = im.size
        mid_x = width // 2
        mid_y = height // 2
        top_left = im.crop((0, 0, mid_x, mid_y))
        top_right = im.crop((mid_x, 0, width, mid_y))
        bottom_left = im.crop((0, mid_y, mid_x, height))
        bottom_right = im.crop((mid_x, mid_y, width, height))

        return top_left, top_right, bottom_left, bottom_right

async def download_image(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.read()

                input_folder = "input"
                output_folder = "output"
                
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                if not os.path.exists(input_folder):
                    os.makedirs(input_folder)

                with open(f"{directory}/{input_folder}/{filename}", "wb") as f:
                    f.write(data)

                print(f"Image downloaded: {filename}")
                input_file = os.path.join(input_folder, filename)  

                if "UPSCALED_" not in filename:
                    quadrant = '1'
                else:
                    file_prefix = "UPSCALED_"
                    
                top_left, top_right, bottom_left, bottom_right = split_image(input_file)

                if quadrant == "1":
                    top_left.save(os.path.join(output_folder, "ig_img.jpg"))
                elif quadrant == "2":
                    top_right.save(os.path.join(output_folder, "ig_img.jpg"))
                elif quadrant == "3":
                    bottom_left.save(os.path.join(output_folder, "ig_img.jpg"))
                elif quadrant == "4":
                    bottom_right.save(os.path.join(output_folder, "ig_img.jpg"))
                os.remove(f"{directory}/{input_folder}/{filename}")
                pyautogui.hotkey('command', 'm')
                await client.close()

def run_bot(text_input_prompt):
    @client.event
    async def on_ready():
        print("Discord bot connected.")
        asyncio.create_task(send_prompt(text_input_prompt))

    async def send_prompt(text_input_prompt):
        print('Running Discord GUI automation to send /imagine prompt to your Midjourney channel.')
        subprocess.call(['open', '-a', 'Discord'])
        time.sleep(2)
        my_midjourney_server_button = pyautogui.locateOnScreen('pyautogui_images/my_mj_button.png')
        my_midjourney_server_button_point = pyautogui.center(my_midjourney_server_button)
        pyautogui.click(my_midjourney_server_button_point)
        time.sleep(2)
        chat_input = pyautogui.locateOnScreen('pyautogui_images/chat.png')
        pyautogui.click(chat_input)
        time.sleep(.5)
        pyautogui.write('/imagine')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(.5)
        pyautogui.write(text_input_prompt) 
        pyautogui.press('enter')

    @client.event
    async def on_message(message):
        for attachment in message.attachments:
            await download_image(attachment.url, attachment.filename)
        await client.process_commands(message)
    client.run(discord_token)

if __name__ == "__main__":
    sample_prompt = 'futuristic AI robot in New York living among human cyborgs in year 2500.'
    run_bot(sample_prompt)
