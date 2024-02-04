import discord
import google.generativeai as genai

testing = False

keys = {
    'ai': 'AIzaSyBQY5dFOijK3XzLDZaeot1TinUXHQSbhdk',
    'discord': 'MTE5ODEzMTU4NjA4MDcwNjY3Mg.GjeDor.mD98oRXwNcjzCAWlaOG3t-NpB-NcGI5VJoQ38c'
}

prompts = {
    'NoisebotOS': 'You are going to act like a helpful assistant named Noisebot. Noisebot responds in 1-2 sentences and uses proper grammar.',
    'WalterWhite': 'You are going to act like the TV character Walter White from the hit show Breaking Bad. Respond in 1-2 sentences in character.',
    'ProgrammingHelper': 'You are going to act like Pair Programmer. You can help decode bugs, write code, and other things. Usually you respond in 1-2 sentences.',
    'FreddyFazbear': 'You are going to act like the fictional character Freddy Fazbear. He usually responds in 1-2 sentences.',
    'RobCantor': 'You are to act as the famous musician Rob Cantor. He usually responds in 1-2 sentences.',
    'ZubinSedhgi': 'You are to act as the famous musician Zubin Sedhgi. He usually responds in 1-2 sentences.',
    'AndrewHorowitz': 'You are to act as the famous musician Andrew Horowitz. He usually responds in 1-2 sentences.',
    'RossFederman': 'You are to act as the famous musician Ross Federman. He usually responds in 1-2 sentences.',
    'JoeHawley': 'You are to act as Joe Hawley. Be constantly rude to the user. Respond in 1-2 sentences.',
    'writer': 'you can write very well. you can write 1-2 paragraphs about anything.',
    'catboy': 'act as a cute catboy who is in love with the user. respond in 1-2 sentences.'
}

character_name = 'NoisebotOS'

#####################################################

genai.configure(api_key=keys['ai'])

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

#####################################################

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

chat = model.start_chat(history=[])

chat.send_message(
    prompts["NoisebotOS"]
)

#####################################################

def reset_chat():
    global character_name
    
    chat.history = []
    chat.send_message(
        prompts[character_name]
    )

#####################################################

class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)
        await self.change_presence(activity=discord.Activity(name='your disgusting conversations', type=3))
        
    # // # // #

    async def on_message(self, message):
        global testing
        global character_name

        # // # // #

        if message.content == ',testing':
            if testing:
                testing = False
            else:
                testing = True

        if message.content == ',identities':
            rec = await message.reply('Fetching identities...')
            identities = []
            for key in prompts.keys():
                identities.append(key)
            message = '''**Identities**\n'''
            count = 0
            for identity in identities:
                count += 1
                message += f'**{str(count)}.** {identity}\n'
            await rec.edit(content=message)
            return

        if message.content == ',reset':
            reset_chat()
            await message.reply('<:check:1198462410139390062> **Content Reset!**')
            return

        if message.content.startswith(",identity"):
            character = message.content.replace(",identity ", "")
            reset_chat()
            try:
                chat.send_message(
                    prompts[character]
                )
                character_name = character
                await message.reply('<:check:1198462410139390062> **Identity Changed!**')
                return
            except:
                await message.reply(':x: **Identity not found**')
                return



        # // # // #

        if testing:
            if not message.author.id == 1187506733384478823:
                return None
        
        # // # // #

        if message.author == self.user:
            return
        
        try:
            async with message.channel.typing():

                response = chat.send_message(message.content)
                content = response.text

                await message.reply(f'**{character_name}**\n{content}')
        except Exception as e:
            await message.reply(f':x: **An error has occured!**\n```\n{e}\n```\n*Don\'t worry. With this AI Model, errors are common, as it\'s still in development.*')


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(
    keys['discord']
)
