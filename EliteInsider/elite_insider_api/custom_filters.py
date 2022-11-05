import psycopg2
import psycopg2.extras
from typing import List, Dict
from config_helper import ConfigHelper


class EICustomFilters:
    def __init__(self):

        self.conn = psycopg2.connect(
            host=ConfigHelper().get_config_item("postgres-db", "server"),
            port=ConfigHelper().get_config_item("postgres-db", "port"),
            user=ConfigHelper().get_config_item("postgres-db", "user"),
            password=ConfigHelper().get_config_item("postgres-db", "password"),
            database=ConfigHelper().get_config_item("postgres-db", "database_name"),
        )

    def get_fullclear_stats(self, guild_name: str, week: int=None) -> List[Dict]:
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            last_fc_filter = """(select max(yearweek) from public.guild_logs where guild_name = %s)"""
            specific_week_filter = """%s"""

            sql = """
                select
                    qualifying_date,
                    encounter_name,
                    cm,
                    start_time ,
                    end_time, 
                    kill_duration_seconds 
                from
                    public.raid_kill_times rkt
                where
                    success
                    and kill_duration_seconds > 10
                    and log_id in (select log_id from public.guild_logs gl where guild_name = %s)
                    and cast(CONCAT(date_part('isoyear', qualifying_date), TO_CHAR(date_part('week', qualifying_date), 'fm00')) as int) = 
                    {filter_clause}
                order by
                    start_time asc
            """

            arguments = []

            if week:
                sql = sql.format(filter_clause=specific_week_filter)
                arguments = [guild_name, week]
            else:
                sql = sql.format(filter_clause=last_fc_filter)
                arguments = [guild_name, guild_name]

            cursor.execute(sql, arguments)
            result = []

            for row in cursor.fetchall():
                result.append(dict(row))

            return result

        except Exception as err:
            raise err


    def get_wing_stats(self, guild_name: str, week: int=None) -> List[Dict]:
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            last_fc_filter = """(select max(yearweek) from public.guild_logs where guild_name = %s)"""
            specific_week_filter = """%s"""

            sql = """
                select
                    min(start_time) as start_time,
                    max(end_time) as end_time, 
                    rkt.qualifying_date,
                    re.raid_wing,
                    re.wing_name
                from
                    public.raid_kill_times rkt
                    inner join public.raid_encounters re ON replace(rkt.encounter_name::text, ' CM'::text, ''::text) = re.encounter_name::text
                where
                    success
                    and kill_duration_seconds > 10
                    and log_id in (select log_id from public.guild_logs gl where guild_name = %s)
                    and cast(CONCAT(date_part('isoyear', qualifying_date), TO_CHAR(date_part('week', qualifying_date), 'fm00')) as int) = 
                    {filter_clause}
                group by 
                    rkt.qualifying_date,
                    re.raid_wing,
                    re.wing_name
                order by
                    start_time asc
            """

            arguments = []

            if week:
                sql = sql.format(filter_clause=specific_week_filter)
                arguments = [guild_name, week]
            else:
                sql = sql.format(filter_clause=last_fc_filter)
                arguments = [guild_name, guild_name]

            cursor.execute(sql, arguments)
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

    def get_users_guilds(self, account_name):
        try:
            cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            sql = """
                select 
                    guild_name 
                from
                    public.guild_members 
                    where 
                        account_name = %s"""

            arguments = [account_name]
            cursor.execute(sql, arguments)

            result = []

            for row in cursor.fetchall():
                result.append(dict(row))

            return result

        except Exception as err:
            raise err

