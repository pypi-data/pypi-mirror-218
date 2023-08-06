import os
from typing import Any
import psycopg2, psycopg2.extras

from baumanecbank_common.abstract import AbstractBbClass
from baumanecbank_common.log import Log

PG_HOST     = 'PG_HOST'
PG_PORT     = 'PG_PORT'
PG_USER     = 'PG_USER'
PG_PASSWORD = 'PG_PASSWORD'
PG_DATABASE = 'PG_DATABASE'
TZ          = 'TZ'

PURCHASE = 'purchase'

class PgTelegramTokenManyOrMissing(Exception):
    pass

class PgCon(AbstractBbClass):
    def __init__(self, appname: str) -> None:
        super().__init__(appname)
        self.host     = os.environ.get(PG_HOST,     'localhost')
        self.port     = os.environ.get(PG_PORT,     '5432')
        self.user     = os.environ.get(PG_USER,     'postgres')
        self.password = os.environ.get(PG_PASSWORD, 'postgres')
        self.dbname   = os.environ.get(PG_DATABASE, 'postgres')

        self.connection = psycopg2.connect(
            host     = self.host,
            port     = self.port,
            user     = self.user,
            password = self.password,
            dbname   = self.dbname
        )
        self.connection.autocommit = True

        with self.connection.cursor() as cursor:
            cursor.execute(f"SET timezone TO '{os.environ.get(TZ, 'Europe/Moscow')}'")
    
    def _get_exactly_one_or_none(self, sql: str) -> Any|None:
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            if cursor.rowcount == 0:
                return None
            return cursor.fetchone()[0]

    def get_telegram_token(self) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT token FROM telegram_tokens WHERE app = '{self.appname}'")
            if cursor.rowcount != 1:
                raise PgTelegramTokenManyOrMissing(f"App {self.appname} has none or more than one telegram token")
            return cursor.fetchone()[0]
    
    def write_event(self, message: str, chat_id: str|int = None) -> None:
        chat_id_val = f"'{chat_id}'" if chat_id is not None else 'NULL'
        with self.connection.cursor() as cursor:
            cursor.execute((
                "INSERT INTO events"
                " (chat_id, message, app)"
                " VALUES"
                f" ({chat_id_val}, '{message}', '{self.appname}')"
            ))
    
    def get_admin_groups(self) -> list[str]:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT chat_id FROM admin_groups")
            if cursor.rowcount == 0:
                return []
            return [ x[0] for x in cursor.fetchall()]
    
    def check_if_government_group(self, chat_id: int|str) -> bool:
        repl = self._get_exactly_one_or_none(
            f"SELECT True FROM government_groups WHERE chat_id = '{chat_id}'"
        )
        if repl is None:
            return False
        return repl
    
    def check_if_market_group(self, chat_id: int|str) -> bool:
        repl = self._get_exactly_one_or_none(
            f"SELECT True FROM market_groups WHERE chat_id = '{chat_id}'"
        )
        if repl is None:
            return False
        return repl
    
    def check_if_bank_group(self, chat_id: int|str) -> bool:
        repl = self._get_exactly_one_or_none(
            f"SELECT True FROM bank_groups WHERE chat_id = '{chat_id}'"
        )
        if repl is None:
            return False
        return repl

    def get_card_code_id_or_none_by_uuid(self, uuid: str) -> int|None:
        return self._get_exactly_one_or_none(
            f"SELECT id FROM avaliable_card_codes WHERE uuid = '{uuid}'"
        )
    
    def check_if_squad_valid(self, squad: str) -> bool:
        repl = self._get_exactly_one_or_none(
            f"SELECT True FROM valid_squads WHERE squad = '{squad}'"
        )
        if repl is None:
            return False
        return repl

    def create_client(self, card_code_id: int|str, name: str, squad: int|str) -> None|Exception:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute((
                    "INSERT INTO clients"
                    " (card_code_id, name, squad)"
                    " VALUES"
                    f" ({card_code_id}, '{name}', '{squad}')"
                ))
                Log.info(f"Created client {card_code_id=} {name=} {squad=}")
                return None
        except Exception as e:
            return e
    
    def check_if_client_exists_by_chat_id(self, chat_id: str|int) -> bool:
        repl = self._get_exactly_one_or_none(
            f"select true from active_clients_card_codes_balances where chat_id = '{chat_id}'"
        )
        if repl is None:
            return False
        return repl
    
    def check_if_client_exists_by_uuid(self, uuid: str|int) -> bool:
        repl = self._get_exactly_one_or_none(
            f"select true from active_clients_card_codes_balances where uuid = '{uuid}'"
        )
        if repl is None:
            return False
        return repl

    def get_client_by_uuid(self, uuid: str|int) -> Any|None:
        with self.connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            cursor.execute((
                "SELECT * "
                "FROM active_clients_card_codes_balances "
                f"WHERE uuid = '{uuid}'"
            ))
            if cursor.rowcount == 0:
                return None
            return cursor.fetchone()

    def get_client_by_chat_id(self, chat_id: str|int) -> Any|None:
        with self.connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            cursor.execute((
                "SELECT * "
                "FROM active_clients_card_codes_balances "
                f"WHERE chat_id = '{chat_id}'"
            ))
            if cursor.rowcount == 0:
                return None
            return cursor.fetchone()
    
    def check_if_account_exists_by_chat_id(self, chat_id: str|int) -> bool:
        repl = self._get_exactly_one_or_none(
            f"select true from active_accounts_card_codes_balances where client_chat_id = '{chat_id}'"
        )
        if repl is None:
            return False
        return repl
    
    def check_if_account_exists_by_uuid(self, uuid: str|int) -> bool:
        repl = self._get_exactly_one_or_none(
            f"select true from active_accounts_card_codes_balances where uuid = '{uuid}'"
        )
        if repl is None:
            return False
        return repl

    def get_account_by_uuid(self, uuid: str|int) -> Any|None:
        with self.connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            cursor.execute((
                "SELECT * "
                "FROM active_accounts_card_codes_balances "
                f"WHERE uuid = '{uuid}'"
            ))
            if cursor.rowcount == 0:
                return None
            return cursor.fetchone()

    def get_account_by_chat_id(self, chat_id: str|int) -> Any|None:
        with self.connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            cursor.execute((
                "SELECT * "
                "FROM active_accounts_card_codes_balances "
                f"WHERE client_chat_id = '{chat_id}'"
            ))
            if cursor.rowcount == 0:
                return None
            return cursor.fetchone()
    
    def check_if_firm_exists_by_uuid(self, uuid: str|int) -> bool:
        repl = self._get_exactly_one_or_none(
            f"select true from active_firms_card_codes_balances where uuid = '{uuid}'"
        )
        if repl is None:
            return False
        return repl

    def get_firm_by_uuid(self, uuid: str|int) -> Any|None:
        with self.connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            cursor.execute((
                "SELECT * "
                "FROM active_firms_card_codes_balances "
                f"WHERE uuid = '{uuid}'"
            ))
            if cursor.rowcount == 0:
                return None
            return cursor.fetchone()
    
    def update_client_chat_id_username(self, id: int|str, chat_id: int|str, username: str) -> None|Exception:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute((
                    "UPDATE clients "
                    f"SET chat_id  = '{chat_id}', "
                    f"    username = '{username}' "
                    f"WHERE id = {id}"
                ))
                Log.info(f"UPDATE client {id=} {chat_id=} {username=}")
                return None
        except Exception as e:
            return e
    
    def get_client_operations_by_chat_id(self, chat_id: int|str) -> list[Any]:
        with self.connection.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cursor:
            cursor.execute((
                "SELECT * "
                "FROM client_operations "
                f"WHERE client_chat_id = '{chat_id}'"
            ))
            return cursor.fetchall()
    
    def create_purchase(self, card_code_id: int|str, amount: float) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute((
                "INSERT INTO transactions"
                " (source_card_code_id, amount, type)"
                " VALUES"
                f" ({card_code_id}, {amount}, '{PURCHASE}')"
            ))
            Log.info(f"INSERT transaction {PURCHASE} {card_code_id=} {amount=}")