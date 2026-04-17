import discord
from database.repositories.users_repo import upsert_user, get_all_users
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

        if message.content and message.content[0] == bot.command_prefix:
            await bot.process_commands(message)
            return

        user_message = str(message.content)
        response = responses.handle_response(user_message)
        if response:
            await message.channel.send(response)


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
        print(f"Inserted/updated user: {member.name} ({member.id})")
        print("Current users table:")
        for row in get_all_users():
            print(row)
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
                f"man gtfo of here\nWe didnt want you here anyways {member.name}"
            )