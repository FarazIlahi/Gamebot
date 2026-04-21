import discord
from database.repositories.edited_messages_repo import insert_edited_messages
from database.repositories.messages_repo import upsert_messages
from database.repositories.users_repo import upsert_user
from database.repositories.guilds_repo import upsert_guild
import bot.responses as responses

async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        if response:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def register_events(bot, deleted_messages):
    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        if not message.content and not message.attachments:
            return
    
        if message.content and message.content[0] == bot.command_prefix:
            await bot.process_commands(message)
            return

        upsert_messages(message)

        user_message = str(message.content)
        response = responses.handle_response(user_message)
        if response:
            await message.channel.send(response)

    @bot.event
    async def on_message_edit(before, after):
        if after.author.bot:
            return

        # skip if content didn’t actually change
        if before.content == after.content:
            return

        insert_edited_messages(before, after)
        upsert_messages(after)



    @bot.event
    async def on_message_delete(message):
        deleted_messages[message.channel.id] = {
            'content': message.content,
            'author': message.author.name,
            'timestamp': message.created_at
        }

    @bot.event
    async def on_member_join(member):
        upsert_user(member)
        if member.guild.system_channel:
            await member.guild.system_channel.send("yo wsg new guy")  
            try:
                await member.add_roles(discord.utils.get(member.guild.roles, name='base aura'))
            except Exception as e:
                print(e)


    @bot.event
    async def on_member_remove(member):
        if member.guild.system_channel:
            await member.guild.system_channel.send(
                f"{member.display_name} is gone.\nman gtfo of here."
            )


    @bot.event
    async def on_guild_join(guild):
        upsert_guild(guild)