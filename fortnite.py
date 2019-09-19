import fortnitepy

client = fortnitepy.Client(
    email='',
    password='',
    net_cl='8371706',
)

print('fortnitepy-bot made by xMistt. credit to Terbau for creating the library.'.format(client))

@client.event
async def event_ready():
    print('Client ready as {0.user.display_name}'.format(client))

@client.event
async def event_party_invite(invitation):
    await invitation.accept()
    # if you want the bot to join with stuff on, put in here.

@client.event
async def event_friend_request(request):
    await request.accept()

@client.event
async def event_friend_message(message):
    print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))

    if message.content == "!purpleskull":

        variants = client.user.party.me.create_variants(
           clothing_color=1
        )

        await client.user.party.me.set_outfit(
            asset='CID_030_Athena_Commando_M_Halloween',
            variants=variants
        )

        await message.reply('Skin set to Purple Skull Trooper!')

    if "CID" in message.content:
        await client.user.party.me.set_outfit(
            asset=message.content
        )

        await message.reply('Skin set to' + message.content + '!')

    if "EID" in message.content:
        await client.user.party.me.set_emote(
            asset=message.content
        )

        await message.reply('Emote set to' + message.content + '!')

    if "BID" in message.content:
        await client.user.party.me.set_backbling(
            asset=message.content
        )

        await message.reply('Backbling set to' + message.content + '!')


client.run()
