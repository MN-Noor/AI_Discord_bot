

import discord
import os

token = os.environ['TOKEN_ID']


class MyClient(discord.Client):

  async def on_ready(self):
    print('Logged on as', self.user)

  async def on_message(self, message):
    from assistant import create_assignment
    # Don't respond to ourselves
    if message.author == self.user:
      return

    if message.content.startswith('!create assignment '):
      query = message.content[len('!create assignment '):]
      response = create_assignment(query)
      if len(response) > 1995:
        response = response[:1995] + '...'
      await message.channel.send(response)

    elif message.content == 'ping':
      await message.channel.send('pong')
    else:
      await message.channel.send(
          'open your eyes and type correctly Unknown command')


def main():
  import discord
  intents = discord.Intents.default()
  intents.message_content = True
  client = MyClient(intents=intents)
  client.run(token)


if __name__ == '__main__':
  main()
