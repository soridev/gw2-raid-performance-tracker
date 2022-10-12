import psycopg2
import psycopg2.extras
from typing import List, Dict
from EliteInsider.config_helper import ConfigHelper


class EICustomFilters:
    def __init__(self):

        self.conn = psycopg2.connect(
            host=ConfigHelper().get_config_item("postgres-db", "server"),
            port=ConfigHelper().get_config_item("postgres-db", "port"),
            user=ConfigHelper().get_config_item("postgres-db", "user"),
            password=ConfigHelper().get_config_item("postgres-db", "password"),
            database=ConfigHelper().get_config_item("postgres-db", "database_name"),
        )

    def get_fullclear_stats(self, guild_name: str) -> List[Dict]:
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            sql = """
                select
                    qualifying_date,
                    encounter_name,
                    cm,
                    cast(min(kill_duration_seconds) as decimal(16,2)) as "kd_sec"
                from
                    public.raid_kill_times rkt
                where
                    success
                    and kill_duration_seconds > 10
                    and log_id in (
                    select
                        log_id
                    from
                        (
                        select
                            rkt.log_id,
                            rkt.qualifying_date ,
                            rkt.encounter_name ,
                            count(gm.account_name) as "GUILD_COUNT"
                        from
                            public.raid_kill_times rkt
                        inner join public.player_info p on
                            rkt.log_id = p.log_id
                        left outer join public.guild_members gm on
                            p.account_name = gm.account_name
                        where gm.guild_name = %s
                        group by 1,2,3 )as lwgm
                    where
                        "GUILD_COUNT" >= 6)
                group by qualifying_date, encounter_name, cm
                order by
                    qualifying_date asc
            """

            cursor.execute(sql, [guild_name])
            result = []

            for row in cursor.fetchall():
                result.append(dict(row))

            return result

        except Exception as err:
            raise err

    def get_log_count(self, user_id=None):
        try:
            cursor = self.conn.cursor()
            sql = """SELECT COUNT(*) FROM PUBLIC.RAID_KILL_TIMES"""
            extension = " WHERE UPLOADED_BY = %s"

            if user_id:
                cursor.execute(sql + extension, [user_id])
                return cursor.fetchall()[0][0]
            else:
                cursor.execute(sql)
                return cursor.fetchall()[0][0]

        except Exception as err:
            raise err
            