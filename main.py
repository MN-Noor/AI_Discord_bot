# app_id:1159521914524549210

# public_key:ed37d610ecbaf842b644a35bcbb218bcf545fde1d5e2c687cd0e597497525f47

import discord
import os

token = os.environ['TOKEN_ID']


class MyClient(discord.Client):

  async def on_ready(self):
    print('Logged on as', self.user)

  async def on_message(self, message):
    from assistant import create_assignment
    from explain import topic_explanation
    from learningpath import roadmap
    from codechecker import check_code

    # Check if the bot is mentioned
    if self.user in message.mentions:
      response = "Sorry, I can't assist you."
      if message.content.startswith('!create assignment '):
        query = message.content[len('!create assignment '):]
        response = create_assignment(query)
      elif message.content.startswith('!explain '):
        query = message.content[len('!explain '):]
        response = topic_explanation(query)
      elif message.content.startswith('!roadmap '):
        query = message.content[len('!roadmap '):]
        response = roadmap(query)
      elif message.content.startswith('!code help'):
        query = message.content[len('!code help'):]
        response = check_code(query)
      elif message.content == 'ping':
        await message.channel.send('pong')
        return  # Return early if it's just a ping

      if len(response) > 1995:
        await message.channel.send(response[:1995])
        await message.channel.send(response[1995:])
      else:
        await message.channel.send(response)

  # Add other methods as needed


def main():
  intents = discord.Intents.default()
  intents.message_content = True
  client = MyClient(intents=intents)
  client.run(token)


if __name__ == '__main__':
  main()
