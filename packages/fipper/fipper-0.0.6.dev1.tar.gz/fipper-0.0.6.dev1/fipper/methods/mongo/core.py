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


class MongoDB:
    def __init__(self: "fipper.Client"):
        self.mongo_async_ = AsyncIOMotorClient(self.mongo_db)
        self.mongo_sync_ = MongoClient(self.mongo_db)

    def mongo_async(self: "fipper.Client"):
        return self.mongo_async_.Fipper
    
    def mongo_sync(self: "fipper.Client"):
        return self.mongo_sync_.Fipper
