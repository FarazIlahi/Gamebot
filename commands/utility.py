import discord
custom_roles = {}
def register_utility_commands(bot, deleted_messages):
    @bot.command()
    async def pfp(ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(f"{user.mention}'s profile picture: {user.avatar.url}")

    @bot.command()
    async def snipe(ctx):
        channel_id = ctx.channel.id
        if channel_id in deleted_messages:
            deleted_message = deleted_messages[channel_id]
            await ctx.send(
                f"Last deleted message by {deleted_message['author']}: "
                f"{deleted_message['content']}"
            )
        else:
            await ctx.send("No deleted messages to snipe")

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


        if(ctx.author.id in custom_roles):
            current_role = custom_roles[ctx.author.id]
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
                    positions={role: target_role.position - 1},
                    reason="Move custom color role under Color Roles"
                )
            except discord.Forbidden:
                await ctx.send("I don't have permission to move that role. Put my bot role above Color Roles.")
                return
            except discord.HTTPException as e:
                await ctx.send(f"Couldn't move the role: {e}")
                return
            custom_roles[ctx.author.id] = role
            await ctx.author.add_roles(role, reason = "Added color role to self")
            await ctx.send(f"Created role **{role_name}** with color `#{hexcode.upper()}` and assigned it to you.")
