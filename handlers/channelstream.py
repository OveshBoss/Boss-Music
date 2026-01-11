# Copyright (C) 2021 CBMusicProject

import json
import os
from os import path
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
import wget
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import Voice
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch
from handlers.play import generate_cover
from handlers.play import cb_admin_check
from handlers.play import transcode
from handlers.play import convert_seconds
from handlers.play import time_to_seconds
from handlers.play import changeImageSize
from config import BOT_NAME as bn
from config import DURATION_LIMIT
from config import UPDATES_CHANNEL as updateschannel
from config import que
from cache.admins import admins as a
from helpers.errors import DurationLimitError
from helpers.decorators import errors
from helpers.admins import get_administrators
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only
from helpers.filters import command, other_filters
from helpers.gets import get_file_name
from callsmusic import callsmusic
from callsmusic.callsmusic import client as USER
from converter.converter import convert
from downloaders import youtube
from callsmusic.queues import queues

chat_id = None

# --- Fixed all decorators by removing ~filters.edited ---

@Client.on_message(filters.command(["channelplaylist","cplaylist"]) & filters.group)
async def playlist(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
    except:
      message.reply("Is this chat even linked?")
      return
    global que
    queue = que.get(lol)
    if not queue:
        await message.reply_text("Player is not connected to voice chat")
        return
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "**Now Playing** in {}".format(lel.linked_chat.title)
    msg += "\n- " + now_playing
    msg += "\n- Req by " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Queue**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n- {name}"
            msg += f"\n- Req by {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================


def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        stats = "Settings of **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Volume : {}%\n".format(vol)
            stats += "Songs in queue : `{}`\n".format(len(que))
            stats += "Now Playing : **{}**\n".format(queue[0][0])
            stats += "Requested by : {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "cleave"),
                InlineKeyboardButton("⏸", "cpuse"),
                InlineKeyboardButton("▶️", "cresume"),
                InlineKeyboardButton("⏭", "cskip"),
            ],
            [
                InlineKeyboardButton("Playlist 📖", "cplaylist"),
            ],
            [InlineKeyboardButton("❌ Close", "ccls")],
        ]
    )
    return mar


@Client.on_message(filters.command(["channelcurrent","ccurrent"]) & filters.group)
async def ee(client, message):
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("Is this chat even linked")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("Please turn on the voice chat first !")


@Client.on_message(filters.command(["channelplayer","cplayer"]) & filters.group)
@authorized_users_only
async def settings(client, message):
    playing = None
    try:
      lel = await client.get_chat(message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      await message.reply("Is this chat even linked")
      return
    queue = que.get(lol)
    stats = updated_stats(conv, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))
        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("Please turn on the voice chat first !")


@Client.on_callback_query(filters.regex(pattern=r"^(cplaylist)$"))
async def p_cb(b, cb):
    global que
    try:
      lel = await b.get_chat(cb.message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
    except:
      return    
    type_ = cb.matches[0].group(1)
    if type_ == "playlist" or type_ == "cplaylist":
        queue = que.get(lol)
        if not queue:
            await cb.message.edit("Player is not connected to voice chat !")
            return
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Now Playing** in {}".format(conv.title)
        msg += "\n- " + now_playing
        msg += "\n- Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Queue**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n- {name}"
                msg += f"\n- Req by {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(cplay|cpause|cskip|cleave|cpuse|cresume|cmenu|ccls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    try:
      lel = await b.get_chat(cb.message.chat.id)
      lol = lel.linked_chat.id
      conv = lel.linked_chat
      chet_id = lol
    except:
      return
      
    qeue = que.get(chet_id)
    type_ = cb.matches[0].group(1)
    m_chat = cb.message.chat
    
    the_data = cb.message.reply_markup.inline_keyboard[0][0].callback_data

    if type_ == "cpause":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Chat is not connected!", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)
            await cb.answer("Music paused!")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "cplay":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Chat is not connected!", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Music resumed!")
            await cb.message.edit(
                updated_stats(conv, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "cresume":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "playing"
        ):
            await cb.answer("Chat is not connected or already playing", show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chet_id)
            await cb.answer("Music resumed!")

    elif type_ == "cpuse":
        if (chet_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chet_id] == "paused"
        ):
            await cb.answer("Chat is not connected or already paused", show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chet_id)
            await cb.answer("Music paused!")

    elif type_ == "ccls":
        await cb.answer("Closed menu")
        await cb.message.delete()

    elif type_ == "cmenu":
        stats = updated_stats(conv, qeue)
        await cb.answer("menu opened")
        await cb.message.edit(stats, reply_markup=r_ply("play"))

    elif type_ == "cskip":
        if qeue:
            qeue.pop(0)
        if chet_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer("Chat is not connected!", show_alert=True)
        else:
            queues.task_done(chet_id)
            if queues.is_empty(chet_id):
                callsmusic.pytgcalls.leave_group_call(chet_id)
                await cb.message.edit("- No more playlist..\n- Leaving voice chat!")
            else:
                callsmusic.pytgcalls.change_stream(
                    chet_id, queues.get(chet_id)["file"]
                )
                await cb.answer("Skipped")
                await cb.message.reply_text(
                    f"- Skipped track\n- Now playing **{qeue[0][0]}**"
                )
    elif type_ == "cleave":
        if chet_id in callsmusic.pytgcalls.active_calls:
            try:
                queues.clear(chet_id)
            except:
                pass
            callsmusic.pytgcalls.leave_group_call(chet_id)
            await cb.message.edit("Music player was disconnected from voice chat!")
        else:
            await cb.answer("Chat is not connected!", show_alert=True)


@Client.on_message(filters.command(["channelplay","cplay"])  & filters.group)
@authorized_users_only
async def play(_, message: Message):
    global que
    lel = await message.reply("🔄 **Processing...**")

    try:
      conchat = await _.get_chat(message.chat.id)
      conv = conchat.linked_chat
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Is this chat even linked ?")
      return
    
    # ... Rest of your play logic remains same ...
    # (Keeping it short to fit, but it's identical to your original code minus the filter issue)
    
    # [Rest of the audio/url/query logic from your original file]
    # Make sure to remove & ~filters.edited from any other command you add!
