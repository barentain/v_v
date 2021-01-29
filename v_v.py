import discord
import asyncio
import logging
import time
from time import localtime, strftime

client = discord.Client()
timestamp = strftime("%m/%d/%Y %I:%M:%S %p", localtime())
token = ""
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

# on_ready event, prints out welcome message when initialized
@client.event
async def on_ready():
	print(f"\n[v_v] Welcome, {client.user.name}#{client.user.discriminator}\n")

# clears open DMs of everyone you've msg'd
@client.event
async def on_message(message):
	# implemented from micah's selfbot | cleardms (https://github.com/girl/owo/blob/master/owo.py)
	commands = []
	z = 0
	for index, a in enumerate(message.content):
		if a == " ":
			commands.append(message.content[z:index])
			z = index + 1
	commands.append(message.content[z:])
	channel = message.channel

	if commands[0] == ".melvinscat":
		if message.author == client.user:
			for channel in client.private_channels:
				if isinstance(channel, discord.DMChannel):
					async for msg in channel.history(limit=9999):
						try:
							if msg.author == client.user:
								await msg.delete()
								print(msg)
						except Exception as x:
							logging.critical(x)
							pass

	if commands[0] == ".save": # .save 9999 > file_name
		if message.author == client.user:
			split = message.content.split(" ")
			filename = split[3]
			limit = int(split[1])
			try:
				if not split[2]:
					pass
				else:
					await message.delete() # Delete message to hide the command
					await save_msgs(message, filename, limit)
			except Exception as x:
				logging.critical(x)
				pass

# save message function for the .save feature in the selfbot
async def save_msgs(message, filename, limit):
	async for msg in message.channel.history(limit=limit):
		try:
			check_file(filename)
			with open(filename, "a+", encoding="utf-8") as export_file:
				export_file.write(f"{msg.created_at} - {msg.author.id} / {msg.id} <{msg.author}> {msg.content}\n")
			print(f"{timestamp} - LOGGED - {msg.author.id} / {msg.id} <{msg.author}> {msg.content}")
		except Exception as x:
			logging.critical(x)
			pass

# validate if file exist, if not create it
def check_file(file):
	try:
		file = open(file, "r", encoding="utf-8")
	except IOError:
		file = open(file, "w", encoding="utf-8")

# react to one of your messages and it will delete all messages in that channel
@client.event
async def on_raw_reaction_add(payload):
	channel = await client.fetch_channel(payload.channel_id)
	author = await client.fetch_user(payload.user_id)
	if author == client.user:
		async for msg in channel.history(limit=99999):
			if msg.author == client.user:
				try:
					await msg.delete()
					print(f"{timestamp} - DELETE - Removed message {msg.content} ({msg.id})")
				except Exception as x:
					logging.critical(x)
					pass

if __name__ == "__main__":
	if not token: # Checks to see if the token variable is empty
		print("[!] Please insert a valid discord token.")
	else:
		client.run(token, bot=False)
