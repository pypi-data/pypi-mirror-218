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

import fipper

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient


class MongoDB(object):
    def __init__(self: "fipper.Client", name: str):
        self.mongo_async_ = AsyncIOMotorClient(name)
        self.mongo_sync_ = MongoClient(name)

    def mongo_async(self: "fipper.Client"):
        return self.mongo_async_.Fipper
    
    def mongo_sync(self: "fipper.Client"):
        return self.mongo_sync_.Fipper
