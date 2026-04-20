from random import random

import discord
from bot import bot
import bot.roasts as roasts
from database.repositories.roles_repo import get_all_custom_color_roles_creator, get_role, upsert_role



def register_fun_commands(bot):
    @bot.command()
    async def roast(ctx, user: discord.Member = None):
        user = user or ctx.author
        msg = await ctx.send("thinking...")
        roast_message = roasts.get_roast(user)
        await msg.edit(content=roast_message)

    @bot.command()
    async def colorrole(ctx, hexcode: str, *, role_name: str):
        hexcode = hexcode.lstrip('#')
        if(len(hexcode) != 6 or not all(c in '0123456789abcdefABCDEF' for c in hexcode)):
            await ctx.send("Invalid hex code. Please provide a 6-digit hex code.")
            return
            
        try:
            color_value = int(hexcode, 16)
        except ValueError:
            await ctx.send("That is not a valid hex code.")
            return
            
        color = discord.Color(color_value)


        if(str(ctx.author.id) in get_all_custom_color_roles_creator()):
            print("User already has a custom color role. Updating existing role.")
            current_role = ctx.guild.get_role(int(get_role(str(ctx.author.id))))
            upsert_role(current_role, created_by_user_id=ctx.author.id, is_color_role=True)
            await current_role.edit(name=role_name, color=color, reason = "Updated color role")
            await ctx.send(f"Updated role **{role_name}** with color `#{hexcode.upper()}` for you.")
        else:
                
            role = await ctx.guild.create_role(
                name = role_name,
                color = color,
                hoist=False,
                mentionable=False,
                reason = f"Color role created by {ctx.author}"
            )
            target_role = discord.utils.get(ctx.guild.roles, name="Color Roles")
            if target_role is None:
                await ctx.send("Target role 'Color Roles' not found. Please create it to manage color roles.")
                return
            try:
                await ctx.guild.edit_role_positions(
                    positions={role: target_role.position},
                    reason="Move custom color role under Color Roles"
                )
            except discord.Forbidden:
                await ctx.send("I don't have permission to move that role. Put my bot role above Color Roles.")
                return
            except discord.HTTPException as e:
                await ctx.send(f"Couldn't move the role: {e}")
                return
            upsert_role(role, created_by_user_id=ctx.author.id, is_color_role=True)
            await ctx.author.add_roles(role, reason = "Added color role to self")
            await ctx.send(f"Created role **{role_name}** with color `#{hexcode.upper()}` and assigned it to you.")



    @bot.command()
    async def ship(ctx, user1: discord.Member, user2: discord.Member):
        percent = random.randint(0, 100)
        await ctx.send(f"{user1.mention} :hearts: {user2.mention} = {percent}% compatibility")


    @bot.command()
    async def iq(ctx, user: discord.Member = None):
        user = user or ctx.author
        iq = random.randint(50, 160)
        await ctx.send(f"{user.mention} has an IQ of {iq} ")