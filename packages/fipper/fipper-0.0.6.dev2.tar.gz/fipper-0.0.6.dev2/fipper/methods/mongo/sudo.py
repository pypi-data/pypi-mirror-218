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

from fipper.filters import SUDOERS


class Sudoers:
    async def add_sudo(self: "fipper.Client", user, nama):
        sudoersdb = self.mongo_async.sudoers
        cek = await sudoersdb.find_one({"user_id": self.me.id, "user": user})
        if cek:
            await sudoersdb.update_one(
                {"user_id": self.me.id},
                {
                    "$set": {
                        "user": user,
                        "nama": nama,
                    }
                },
            )
        else:
            await sudoersdb.insert_one({"user_id": self.me.id, "user": user, "nama": nama})


    async def del_sudo(self: "fipper.Client", user):
        sudoersdb = self.mongo_async.sudoers
        await sudoersdb.delete_one({"user_id": self.me.id, "user": user})


    async def get_all_sudo(self: "fipper.Client"):
        sudoersdb = self.mongo_async.sudoers
        r = [jo async for jo in sudoersdb.find({"user_id": self.me.id})]
        if r:
            return r
        else:
            return False

    def sudo(self: "fipper.Client"):
        global SUDOERS
        
        sudoersdb = self.mongo_sync.sudoers
        sudoers = sudoersdb.find_one({"user_id": self.me.id})
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x['user'])
            print(f"Sudoers {self.me.first_name} Loaded.")