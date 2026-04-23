import asyncio
import discord
from discord.ext import commands
import yt_dlp

# PUT YOUR DESIGNATED VOICE CHANNEL ID HERE
MUSIC_VOICE_CHANNEL_ID = 123456789012345678

# Optional: if ffmpeg is not in PATH, use the full path:
# FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFMPEG_PATH = "ffmpeg"

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "default_search": "auto",   # lets you do .play song name too
    "extract_flat": False,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


class YTDLSource:
    def __init__(self, data):
        self.data = data
        self.title = data.get("title", "Unknown title")
        self.webpage_url = data.get("webpage_url")
        self.stream_url = data["url"]

    @classmethod
    async def from_query(cls, query: str):
        loop = asyncio.get_running_loop()

        def extract():
            with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
                info = ydl.extract_info(query, download=False)

                # If a playlist/search result slips through, grab first entry
                if "entries" in info:
                    info = next((entry for entry in info["entries"] if entry), None)

                if not info:
                    raise ValueError("Could not extract audio info from that link/search.")

                return info

        data = await loop.run_in_executor(None, extract)
        return cls(data)


def setup(bot: commands.Bot):
    @bot.command()
    async def joinmusic(ctx):
        """Join the designated music voice channel."""
        channel = bot.get_channel(MUSIC_VOICE_CHANNEL_ID)

        if channel is None or not isinstance(channel, discord.VoiceChannel):
            await ctx.send("Music voice channel not found. Check the channel ID.")
            return

        if ctx.voice_client:
            if ctx.voice_client.channel.id == channel.id:
                await ctx.send(f"Already in **{channel.name}**.")
                return
            await ctx.voice_client.move_to(channel)
            await ctx.send(f"Moved to **{channel.name}**.")
            return

        await channel.connect()
        await ctx.send(f"Joined **{channel.name}**.")

    @bot.command()
    async def leave(ctx):
        """Leave voice."""
        if not ctx.voice_client:
            await ctx.send("I'm not in a voice channel.")
            return

        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")

    @bot.command()
    async def play(ctx, *, query: str):
        """
        Play from a YouTube link or search query
        Example:
        .play https://www.youtube.com/watch?v=...
        .play porter robinson shelter
        """
        channel = bot.get_channel(MUSIC_VOICE_CHANNEL_ID)

        if channel is None or not isinstance(channel, discord.VoiceChannel):
            await ctx.send("Music voice channel not found. Check the channel ID.")
            return

        # Connect/move bot into designated channel
        if ctx.voice_client is None:
            voice = await channel.connect()
        else:
            voice = ctx.voice_client
            if voice.channel.id != channel.id:
                await voice.move_to(channel)

        # Optional restriction: only allow users already in that same voice channel
        if not ctx.author.voice or ctx.author.voice.channel.id != channel.id:
            await ctx.send(f"You need to be in **{channel.name}** to use this command.")
            return

        try:
            source_info = await YTDLSource.from_query(query)
        except Exception as e:
            await ctx.send(f"Could not get audio: `{e}`")
            return

        if voice.is_playing() or voice.is_paused():
            voice.stop()

        audio_source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(
                source_info.stream_url,
                executable=FFMPEG_PATH,
                **FFMPEG_OPTIONS
            ),
            volume=0.5
        )

        voice.play(audio_source)

        await ctx.send(f"Now playing: **{source_info.title}**")

    @bot.command()
    async def stop(ctx):
        """Stop current audio."""
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send("Nothing is playing.")
            return

        ctx.voice_client.stop()
        await ctx.send("Stopped playback.")

    @bot.command()
    async def pause(ctx):
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send("Nothing is playing.")
            return

        ctx.voice_client.pause()
        await ctx.send("Paused.")

    @bot.command()
    async def resume(ctx):
        if not ctx.voice_client or not ctx.voice_client.is_paused():
            await ctx.send("Nothing is paused.")
            return

        ctx.voice_client.resume()
        await ctx.send("Resumed.")