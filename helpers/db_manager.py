import os

import aiosqlite

from database.models import Zone, Connection, Link

DATABASE_PATH = f"{os.path.realpath(os.path.dirname(__file__))}/../database/database.db"

async def get_blacklisted_users() -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT user_id, strftime('%s', created_at) FROM blacklist"
        ) as cursor:
            result = await cursor.fetchall()
            return result


async def is_blacklisted(user_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT * FROM blacklist WHERE user_id=?", (user_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result is not None


async def add_user_to_blacklist(user_id: int) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO blacklist(user_id) VALUES (?)", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def remove_user_from_blacklist(user_id: int) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM blacklist WHERE user_id=?", (user_id,))
        await db.commit()
        rows = await db.execute("SELECT COUNT(*) FROM blacklist")
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def add_warn(user_id: int, server_id: int, moderator_id: int, reason: str) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await db.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await db.commit()
            return warn_id


async def remove_warn(warn_id: int, user_id: int, server_id: int) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await db.commit()
        rows = await db.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0


async def get_warnings(user_id: int, server_id: int) -> list:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        rows = await db.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list

async def add_details_to_zone(
        zone: Zone
        ) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO zones(name,continent,type,url_name,friendly_name,name_in_who,url,above_45,key_required,firepot_port,shaman_port,druid_port,wizard_port,level_of_monsters,zem_value,succor_evac,zone_spawn_timer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(
            zone.name,
            zone.continent,
            zone.type,
            zone.url_name,
            zone.friendly_name,
            zone.name_in_who,
            zone.url,
            zone.above_45,
            zone.key_required,
            zone.firepot_port,
            zone.shaman_port,
            zone.druid_port,
            zone.wizard_port,
            zone.level_of_monsters,
            zone.zem_value,
            zone.succor_evac,
            zone.zone_spawn_timer,
            ),
        )
        await db.commit()

async def add_zone_connection(
        connection: Connection
        ) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO connections(zone, connected_to, ocean_connection, one_way_connection) VALUES (?, ?, ?, ?)",(
            connection.zone,
            connection.connected_to,
            connection.ocean_connection,
            connection.one_way_connection,
            ),
        )
        await db.commit()

async def add_zone_link(
        link: Link
        ) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("INSERT INTO links(zone, value, type, url) VALUES (?, ?, ?, ?)",(
            link.zone,
            link.value,
            link.type,
            link.url,
            ),
        )
        await db.commit()