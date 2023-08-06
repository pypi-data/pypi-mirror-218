#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import meta
from meta import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~meta.types.InlineQueryResultCachedAudio`
    - :obj:`~meta.types.InlineQueryResultCachedDocument`
    - :obj:`~meta.types.InlineQueryResultCachedAnimation`
    - :obj:`~meta.types.InlineQueryResultCachedPhoto`
    - :obj:`~meta.types.InlineQueryResultCachedSticker`
    - :obj:`~meta.types.InlineQueryResultCachedVideo`
    - :obj:`~meta.types.InlineQueryResultCachedVoice`
    - :obj:`~meta.types.InlineQueryResultArticle`
    - :obj:`~meta.types.InlineQueryResultAudio`
    - :obj:`~meta.types.InlineQueryResultContact`
    - :obj:`~meta.types.InlineQueryResultDocument`
    - :obj:`~meta.types.InlineQueryResultAnimation`
    - :obj:`~meta.types.InlineQueryResultLocation`
    - :obj:`~meta.types.InlineQueryResultPhoto`
    - :obj:`~meta.types.InlineQueryResultVenue`
    - :obj:`~meta.types.InlineQueryResultVideo`
    - :obj:`~meta.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "meta.Client"):
        pass
