import asyncio
from collections import deque

import discord
from discord.ext import commands
import yt_dlp

FFMPEG_PATH = "C:\\Users\\faraz\\Documents\\Gamebot\\resources\\ffmpeg.exe"

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "auto",
    "extract_flat": False,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

INACTIVITY_TIMEOUT = 600  # 10 minutes


class YTDLSource:
    def __init__(self, data):
        self.title = data.get("title", "Unknown title")
        self.webpage_url = data.get("webpage_url")
        self.stream_url = data["url"]

    @classmethod
    async def from_query(cls, query: str):
        loop = asyncio.get_running_loop()

        def extract():
            with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
                info = ydl.extract_info(query, download=False)

                if "entries" in info:
                    info = next((entry for entry in info["entries"] if entry), None)

                if not info:
                    raise ValueError("Could not extract audio info from that link/search.")

                return info

        data = await loop.run_in_executor(None, extract)
        return cls(data)


class GuildMusicState:
    def __init__(self):
        self.queue = deque()
        self.current = None
        self.text_channel = None
        self.lock = asyncio.Lock()
        self.play_next_event = asyncio.Event()
        self.player_task = None
        self.inactivity_task = None

    def reset_idle_event(self):
        self.play_next_event.clear()


def register_music_commands(bot: commands.Bot):
    music_states: dict[int, GuildMusicState] = {}

    def get_state(guild_id: int) -> GuildMusicState:
        if guild_id not in music_states:
            music_states[guild_id] = GuildMusicState()
        return music_states[guild_id]

    async def ensure_user_in_voice(ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You’re not in a voice channel.")
            return None
        return ctx.author.voice.channel

    async def ensure_bot_in_user_channel(ctx):
        user_channel = await ensure_user_in_voice(ctx)
        if user_channel is None:
            return None, None

        voice = ctx.voice_client

        if voice is None:
            voice = await user_channel.connect()
        elif voice.channel.id != user_channel.id:
            await voice.move_to(user_channel)

        return voice, user_channel

    async def schedule_inactivity_disconnect(ctx, state: GuildMusicState):
        # cancel old timer if there is one
        if state.inactivity_task and not state.inactivity_task.done():
            state.inactivity_task.cancel()

        async def idle_disconnect():
            try:
                await asyncio.sleep(INACTIVITY_TIMEOUT)

                voice = ctx.voice_client
                if voice and not voice.is_playing() and not voice.is_paused() and len(state.queue) == 0:
                    await voice.disconnect()
                    if state.text_channel:
                        await state.text_channel.send("Left the voice channel due to inactivity.")
            except asyncio.CancelledError:
                pass

        state.inactivity_task = asyncio.create_task(idle_disconnect())

    async def player_loop(guild_id: int):
        state = get_state(guild_id)

        while True:
            try:
                # wait until there is something in queue
                while len(state.queue) == 0:
                    await asyncio.sleep(1)

                    # if bot disconnected and queue empty, kill loop
                    guild = bot.get_guild(guild_id)
                    if guild is None:
                        return

                    voice = guild.voice_client
                    if voice is None and len(state.queue) == 0:
                        state.player_task = None
                        return

                guild = bot.get_guild(guild_id)
                if guild is None:
                    state.player_task = None
                    return

                voice = guild.voice_client
                if voice is None:
                    state.player_task = None
                    return

                source_info = state.queue.popleft()
                state.current = source_info
                state.reset_idle_event()

                def after_playing(error):
                    if error:
                        print(f"Player error: {error}")
                    bot.loop.call_soon_threadsafe(state.play_next_event.set)

                audio_source = discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(
                        source_info.stream_url,
                        executable=FFMPEG_PATH,
                        **FFMPEG_OPTIONS
                    ),
                    volume=0.5
                )

                voice.play(audio_source, after=after_playing)

                if state.text_channel:
                    await state.text_channel.send(f"Now playing: **{source_info.title}**")

                await state.play_next_event.wait()
                state.play_next_event.clear()

                state.current = None

                if len(state.queue) == 0 and state.text_channel:
                    fake_ctx = type("FakeCtx", (), {"voice_client": guild.voice_client})()
                    await schedule_inactivity_disconnect(fake_ctx, state)

            except asyncio.CancelledError:
                state.player_task = None
                return
            except Exception as e:
                print(f"player_loop exception: {e}")
                state.current = None
                await asyncio.sleep(1)

    @bot.command()
    async def queue(ctx, *, query: str):
        """
        Add a track to the queue.
        If bot isn't connected, it joins the user's voice channel.
        If nothing is playing, playback starts automatically.
        """
        voice, user_channel = await ensure_bot_in_user_channel(ctx)
        if voice is None:
            return

        state = get_state(ctx.guild.id)
        state.text_channel = ctx.channel

        # if inactivity timer is running, cancel it since we are active again
        if state.inactivity_task and not state.inactivity_task.done():
            state.inactivity_task.cancel()

        try:
            source_info = await YTDLSource.from_query(query)
        except Exception as e:
            await ctx.send(f"Could not get audio: `{e}`")
            return

        state.queue.append(source_info)

        if voice.is_playing() or voice.is_paused() or state.current is not None:
            await ctx.send(f"Queued: **{source_info.title}**")
        else:
            await ctx.send(f"Queued: **{source_info.title}**")

        if state.player_task is None or state.player_task.done():
            state.player_task = asyncio.create_task(player_loop(ctx.guild.id))

    @bot.command()
    async def skip(ctx, amount: int = 1):
        """
        Skip current song plus optionally more tracks.
        .skip       -> skip current
        .skip 3     -> skip current + next 2 queued tracks
        """
        if amount < 1:
            await ctx.send("Skip amount must be at least 1.")
            return

        voice = ctx.voice_client
        if not voice or (not voice.is_playing() and not voice.is_paused()):
            await ctx.send("Nothing is playing.")
            return

        state = get_state(ctx.guild.id)

        # remove extra queued tracks beyond the current one
        tracks_to_remove = max(0, amount - 1)
        removed = 0
        while removed < tracks_to_remove and len(state.queue) > 0:
            state.queue.popleft()
            removed += 1

        voice.stop()

        if removed > 0:
            await ctx.send(f"Skipped current track and removed **{removed}** more from the queue.")
        else:
            await ctx.send("Skipped current track.")

    @bot.command()
    async def pause(ctx):
        voice = ctx.voice_client
        if not voice or not voice.is_playing():
            await ctx.send("Nothing is playing.")
            return

        voice.pause()
        await ctx.send("Paused.")

    @bot.command()
    async def resume(ctx):
        voice = ctx.voice_client
        if not voice or not voice.is_paused():
            await ctx.send("Nothing is paused.")
            return

        voice.resume()
        await ctx.send("Resumed.")

    @bot.command()
    async def stop(ctx):
        """
        Stop playback, clear queue, and disconnect bot.
        """
        voice = ctx.voice_client
        if not voice:
            await ctx.send("I’m not in a voice channel.")
            return

        state = get_state(ctx.guild.id)
        state.queue.clear()
        state.current = None

        if state.player_task and not state.player_task.done():
            state.player_task.cancel()
            state.player_task = None

        if state.inactivity_task and not state.inactivity_task.done():
            state.inactivity_task.cancel()

        if voice.is_playing() or voice.is_paused():
            voice.stop()

        await voice.disconnect()
        await ctx.send("Stopped playback, cleared queue, and left the voice channel.")

    @bot.command()
    async def q(ctx):
        """
        Show current queue.
        """
        state = get_state(ctx.guild.id)

        lines = []

        if state.current:
            lines.append(f"**Now playing:** {state.current.title}")
        else:
            lines.append("**Now playing:** Nothing")

        if len(state.queue) == 0:
            lines.append("**Up next:** Nothing queued")
        else:
            preview = list(state.queue)[:10]
            lines.append("**Up next:**")
            for i, track in enumerate(preview, start=1):
                lines.append(f"{i}. {track.title}")

            if len(state.queue) > 10:
                lines.append(f"...and {len(state.queue) - 10} more")

        await ctx.send("\n".join(lines))