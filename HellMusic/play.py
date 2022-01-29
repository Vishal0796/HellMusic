import os
import re
import asyncio
from pyrogram import Client
from HellMusic.queues import QUEUE, add_to_queue
from Config import bot, call_py, HNDLR, contact_filter, GRPPLAY
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query):
   try:
      search = VideosSearch(query, limit=1)
      for r in search.result()["result"]:
         ytid = r['id']
         if len(r['title']) > 34:
            songname = r['title'][:35] + "..."
         else:
            songname = r['title']
         url = f"https://www.youtube.com/watch?v={ytid}"
      return [songname, url]
   except Exception as e:
      print(e)
      return 0

# YTDL
# https://github.com/pytgcalls/pytgcalls/blob/dev/example/youtube_dl/youtube_dl_example.py
async def ytdl(link):
   proc = await asyncio.create_subprocess_exec(
       'youtube-dl',
       '-g',
       '-f',
       # CHANGE THIS BASED ON WHAT YOU WANT
       'bestaudio',
       f'{link}',
       stdout=asyncio.subprocess.PIPE,
       stderr=asyncio.subprocess.PIPE,
   )
   stdout, stderr = await proc.communicate()
   if stdout:
      return 1, stdout.decode().split('\n')[0]
   else:
      return 0, stderr.decode()


@Client.on_message(filters.command(['play', '/play'], prefixes=f"{HNDLR}"))
async def play(client, m: Message):
 if GRPPLAY or (m.from_user and m.from_user.is_contact) or m.outgoing:
   replied = m.reply_to_message
   chat_id = m.chat.id
   if replied:
      if replied.audio or replied.voice:
         huehue = await replied.reply("`Downloading`")
         dl = await replied.download()
         link = replied.link
         if replied.audio:
            if replied.audio.title:
               songname = replied.audio.title[:35] + "..."
            else:
               if replied.audio.file_name:
                  songname = replied.audio.file_name[:35] + "..."
               else:
                  songname = "Audio"
         elif replied.voice:
            songname = "Voice Note"
         if chat_id in QUEUE:
            pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
            await huehue.edit(f"Queued at **#{pos}**")
         else:
            await call_py.join_group_call(
               chat_id,
               AudioPiped(
                  dl,
               ),
               stream_type=StreamType().pulse_stream,
            )
            add_to_queue(chat_id, songname, dl, link, "Audio", 0)
            await huehue.edit(f"**Started Playing Audio ▶** \n**🎧 SONG** : [{songname}]({link}) \n**💬 CHAT** : `{chat_id}`", disable_web_page_preview=True)
      else:
         if len(m.command) < 2:
            await m.reply("`Reply to an Audio File or give something to Search`")
         else:
            huehue = await m.reply("`Searching...`")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search==0:
               await huehue.edit("`Found Nothing for the Given Query`")
            else:
               songname = search[0]
               url = search[1]
               hm, ytlink = await ytdl(url)
               if hm==0:
                  await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
               else:
                  if chat_id in QUEUE:
                     pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                     await huehue.edit(f"Queued at **#{pos}**")
                  else:
                     try:
                        await call_py.join_group_call(
                           chat_id,
                           AudioPiped(
                              ytlink,
                           ),
                           stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.edit(f"**Started Playing Audio ▶** \n**🎧 SONG** : [{songname}]({url}) \n**💬 CHAT** : `{chat_id}`", disable_web_page_preview=True)
                     except Exception as ep:
                        await huehue.edit(f"`{ep}`")
            
   else:
         if len(m.command) < 2:
            await m.reply("`Reply to an Audio File or give something to Search`")
         else:
            huehue = await m.reply("`Searching...`")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search==0:
               await huehue.edit("`Found Nothing for the Given Query`")
            else:
               songname = search[0]
               url = search[1]
               hm, ytlink = await ytdl(url)
               if hm==0:
                  await huehue.edit(f"**YTDL ERROR ⚠️** \n\n`{ytlink}`")
               else:
                  if chat_id in QUEUE:
                     pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                     await huehue.edit(f"Queued at **#{pos}**")
                  else:
                     try:
                        await call_py.join_group_call(
                           chat_id,
                           AudioPiped(
                              ytlink,
                           ),
                           stream_type=StreamType().pulse_stream,
                        )
                        add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.edit(f"**Started Playing Audio ▶** \n**🎧 SONG** : [{songname}]({url}) \n**💬 CHAT** : `{chat_id}`", disable_web_page_preview=True)
                     except Exception as ep:
                        await huehue.edit(f"`{ep}`")