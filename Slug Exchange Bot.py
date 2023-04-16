import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

INPUT_CHANNEL_ID = 1096958617116233789
OUTPUT_CHANNEL_ID = 1096958650263810059
TOKEN = 'MTA5NjY1NTcyMzEwODI0NTYxNA.GvDZVS.aYyApuXPQjWKOi0iHO84JbjIhOGJIljfQX3QeI'

entered_loop = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')
    # Set the channel variable outside the if statement
    channel = bot.get_channel(INPUT_CHANNEL_ID)
    await channel.send("Hi there. To get started, type 'START'.")

@bot.event
async def on_message(message):
    global entered_loop  # declare entered_loop as global variable
    if message.author == bot.user:
        return
    # Check if the message is not from the bot and in the input channel
    if message.channel.id == INPUT_CHANNEL_ID:
        # Check if the message content is START
        if message.content == 'START':
            entered_loop = True
            await message.channel.send("Welcome to the listing creation process. Please answer the following questions:")
            questions = [
                "What is the full name of the item you want to sell?",
                "What do you want in exchange? Ex. 10 swipes into College Nine, 10 Naked Juices, etc.",
                "How would you like to be contacted? Insert your phone, email, or discord profile",
                "Upload an image of your item. If none type N/A"
            ]
            prefixes = ["HAVE: ","WANT: ","CONTACT INFO: ","IMAGE: "]
            answers = []

            for i, question in enumerate(questions):
                await message.channel.send(prefixes[i] + question)
                # Set waiting_for_response flag to True
                waiting_for_response = True
                while waiting_for_response:
                    # Wait for a response from the same user
                    answer = await bot.wait_for('message', check=lambda m: m.author == message.author)
                    # Check if the response is not from the bot and in the input channel
                    if answer.channel.id == INPUT_CHANNEL_ID and answer.author != bot.user:
                        # Set waiting_for_response flag to False
                        waiting_for_response = False
                        if i == 3:
                            # Check if an image was uploaded
                            if answer.attachments:
                                attachment_url = answer.attachments[0].url
                                answers.append((prefixes[i], attachment_url))
                            else:
                                answers.append((prefixes[i], "N/A"))
                        else:
                            answers.append((prefixes[i], answer.content))
            await message.channel.send("Thanks, your listing has been created.")
            response = "\n".join([f"{prefix}{answer}" for prefix, answer in answers])
            await bot.get_channel(OUTPUT_CHANNEL_ID).send("##########################################")
            await bot.get_channel(OUTPUT_CHANNEL_ID).send("NEW LISTING")
            await bot.get_channel(OUTPUT_CHANNEL_ID).send(response)
            await bot.get_channel(OUTPUT_CHANNEL_ID).send("##########################################")
            await message.channel.send("Hi there. To get started, type 'START'.")
            entered_loop = False
        elif not entered_loop:
            await message.channel.send("Hi there. To get started, type 'START'.")

    await bot.process_commands(message)

bot.run(TOKEN)
