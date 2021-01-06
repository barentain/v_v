import discord
import asyncio

client = discord.Client()
token = "" # insert your token here :D

# on_ready event, prints out welcome message when initialized
@client.event
async def on_ready():
	print(f"\n[QwQ] Welcome, {client.user.name}#{client.user.discriminator}")

# clears open DMs of everyone you've msg'd
@client.event
async def on_message(message):
	# implemented from micah's selfbot | cleardms (https://github.com/girl/owo/blob/master/owo.py)
	if message.content == "melvinscat":
		for channel in client.private_channels:
			if isinstance(channel, discord.DMChannel):
				async for msg in channel.history(limit=9999):
					try:
						if msg.author == client.user:
							await msg.delete()
							print(msg)
					except:
						pass

# react to one of your messages and it will delete all msgs in that channel
@client.event
async def on_raw_reaction_add(payload):
	channel = await client.fetch_channel(payload.channel_id)
	if isinstance(channel, discord.DMChannel):
		async for msg in channel.history(limit=99999):
			if msg.author == client.user:
				try:
					await msg.delete()
					print(f"[{msg.guild.name}/{msg.channel.name}] Deleting '{msg.id}' + '{msg.content}' sent by you")
				except:
					pass

if __name__ == "__main__":
	if not token: # Checks to see if the token variable is empty
		print("[!] Please insert a valid discord token at line 5 in the code.")
	else:
		client.run(token, bot=False)