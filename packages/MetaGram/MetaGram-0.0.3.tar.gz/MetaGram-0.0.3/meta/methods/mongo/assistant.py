# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import asyncio
from datetime import datetime, timedelta
from typing import Union

import meta
from meta import Client
from meta.errors import (ChatAdminRequired,
                             UserAlreadyParticipant,
                             UserNotParticipant)
from meta.types import InlineKeyboardMarkup

from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import (AlreadyJoinedError,
                                  NoActiveGroupCall,
                                  TelegramServerError,
                                  NoMtProtoClientSet)
from pytgcalls.types import (JoinedGroupCallParticipant,
                             LeftGroupCallParticipant, Update)
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded


from .bit_rate import BitRate


autoend = {}
counter = {}
AUTO_END_TIME = 3

class AssistantErr(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)



class Ubot:
    def set_ubot(self: "meta.Client", api_id, api_hash, session_string):
        ubotdb = self.mongo_sync.ubot
        user = ubotdb.find_one({"user_id": self.me.id})
        if user:
            ubotdb.update_one(
                {"user_id": self.me.id},
                {
                    "$set": {
                        "api_id": api_id,
                        "api_hash": api_hash,
                        "session_string": session_string,
                    }
                },
            )
        else:
            ubotdb.insert_one(
                {
                    "user_id": self.me.id,
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "session_string": session_string,
                }
            )


    def del_ubot(self: "meta.Client"):
        ubotdb = self.mongo_sync.ubot
        return ubotdb.delete_one({"user_id": self.me.id})


    def get_ubot(self: "meta.Client"):
        ubotdb = self.mongo_sync.ubot
        ubot = ubotdb.find_one({"user_id": self.me.id})
        if ubot:
            for x in ubot:
                name = x["user_id"]
                api_id = x["api_id"]
                api_hash = x["api_hash"]
                string = x["session_string"]
            return name, api_id, api_hash, string
        else:
            return False


class Assistant:
    def set_assistant(self: "meta.Client", calls):
        asstdb = self.mongo_sync.assistant
        user = asstdb.find_one({"user_id": self.me.id})
        if user:
            asstdb.update_one(
                {"user_id": self.me.id},
                {"$set": {"calls": calls}},
            )
        else:
            asstdb.insert_one(
                {
                    "user_id": self.me.id,
                    "calls": calls
                }
            )

    def del_assistant(self: "meta.Client"):
        asstdb = self.mongo_sync.assistant
        return asstdb.delete_one({"user_id": self.me.id})


    def get_assistant(self: "meta.Client") -> PyTgCalls:
        asstdb = self.mongo_sync.assistant
        asst = asstdb.find_one({"user_id": self.me.id})
        if not asst:
            raise NoMtProtoClientSet
        else:
            return asst['calls']


class MetaCall(PyTgCalls, Assistant, Ubot, BitRate):
    def __init__(self):
        name, app_id, app_hash, string = self.get_ubot()
        self.userbot = Client(
            name=name,
            api_id=app_id,
            api_hash=app_hash,
            session_name=str(string),
        )
        self.calls = PyTgCalls(
            self.userbot,
            cache_duration=100,
        )
        self.set_assistant(self.calls)

    async def pause_stream(self, chat_id: int):
        assistant = self.get_assistant()
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = self.get_assistant()
        await assistant.resume_stream(chat_id)

    async def mute_stream(self, chat_id: int):
        assistant = self.get_assistant()
        await assistant.mute_stream(chat_id)

    async def unmute_stream(self, chat_id: int):
        assistant = self.get_assistant()
        await assistant.unmute_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = self.get_assistant()
        try:
            await assistant.leave_group_call(chat_id)
        except:
            pass

    async def stream_call(self, chat_id, link):
        assistant = self.get_assistant()
        await assistant.join_group_call(
            chat_id,
            AudioVideoPiped(link),
            stream_type=StreamType().pulse_stream,
        )
        await asyncio.sleep(2)
        await assistant.leave_group_call(chat_id)

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
    ):
        assistant = self.get_assistant()
        audio_stream_quality = await self.get_audio_bitrate(chat_id)
        video_stream_quality = await self.get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(
                link, audio_parameters=audio_stream_quality
            )
        )
        try:
            await assistant.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
        except NoActiveGroupCall:
            try:
                await self.join_assistant(original_chat_id, chat_id)
            except Exception as e:
                raise e
            try:
                await assistant.join_group_call(
                    chat_id,
                    stream,
                    stream_type=StreamType().pulse_stream,
                )
            except Exception as e:
                raise AssistantErr(
                    "**No Active Voice Chat Found**\n\nPlease make sure group's voice chat is enabled. If already enabled, please end it and start fresh voice chat again and if the problem continues, try /restart"
                )
        except AlreadyJoinedError:
            raise AssistantErr(
                "**Assistant Already in Voice Chat**\n\nSystems have detected that assistant is already there in the voice chat, this issue generally comes when you play 2 queries together.\n\nIf assistant is not present in voice chat, please end voice chat and start fresh voice chat again and if the  problem continues, try /restart"
            )
        except TelegramServerError:
            raise AssistantErr(
                "**Telegram Server Error**\n\nTelegram is having some internal server problems, Please try playing again.\n\n If this problem keeps coming everytime, please end your voice chat and start fresh voice chat again."
            )

    async def start(self):
        print("Starting PyTgCalls Client\n")
        assistant = self.get_assistant()
        await assistant.start()

    async def decorators(self):
        assistant = self.get_assistant()
        @assistant.on_kicked()
        @assistant.on_closed_voice_chat()
        @assistant.on_left()
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @assistant.on_stream_end()
        async def stream_end_handler1(client, update: Update):
            if not isinstance(update, StreamAudioEnded):
                return
            await self.change_stream(client, update.chat_id)

        @assistant.on_participants_change()
        async def participants_change_handler(client, update: Update):
            if not isinstance(
                update, JoinedGroupCallParticipant
            ) and not isinstance(update, LeftGroupCallParticipant):
                return
            chat_id = update.chat_id
            users = counter.get(chat_id)
            if not users:
                try:
                    got = len(await client.get_participants(chat_id))
                except:
                    return
                counter[chat_id] = got
                if got == 1:
                    autoend[chat_id] = datetime.now() + timedelta(
                        minutes=AUTO_END_TIME
                    )
                    return
                autoend[chat_id] = {}
            else:
                final = (
                    users + 1
                    if isinstance(update, JoinedGroupCallParticipant)
                    else users - 1
                )
                counter[chat_id] = final
                if final == 1:
                    autoend[chat_id] = datetime.now() + timedelta(
                        minutes=AUTO_END_TIME
                    )
                    return
                autoend[chat_id] = {}
