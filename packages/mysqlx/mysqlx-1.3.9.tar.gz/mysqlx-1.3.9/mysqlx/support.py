import re
import threading
from enum import Enum
from typing import Sequence
from jinja2 import Template
from functools import lru_cache
from logging import basicConfig, INFO, getLogger
from .constant import NAMED_REGEX, DYNAMIC_REGEX

DB_LOCK = threading.RLock()
logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def get_batch_args(*args):
    return args[0] if isinstance(args, tuple) and len(args) == 1 and isinstance(args[0], Sequence) else args


def try_commit(db_ctx):
    if db_ctx.transactions == 0:
        logger.debug('Commit transaction...')
        try:
            db_ctx.connection.commit()
            logger.debug('Commit ok.')
        except Exception:
            logger.warning('Commit failed, try rollback...')
            db_ctx.connection.rollback()
            logger.warning('Rollback ok.')
            raise


def simple_sql(sql: str, *args, **kwargs):
    return get_named_sql_args(sql, **kwargs) if kwargs else (sql, args)


def dynamic_sql(sql: str, *args, **kwargs):
    if kwargs:
        if _is_dynamic_sql(sql):
            sql = Template(sql).render(**kwargs)
        return get_named_sql_args(sql, **kwargs)

    return sql, args


def is_dynamic_sql(sql: str):
    return re.search(DYNAMIC_REGEX, sql)


@lru_cache(maxsize=128)
def _is_dynamic_sql(sql: str):
    return True if is_dynamic_sql(sql) else False


def get_named_sql_args(sql: str, **kwargs):
    args = get_named_args(sql, **kwargs)
    return get_named_sql(sql), args


@lru_cache(maxsize=256)
def get_named_sql(sql: str):
    return re.sub(NAMED_REGEX, '?', sql)


def get_named_args(sql: str, **kwargs):
    return [kwargs[r[1:]] for r in re.findall(NAMED_REGEX, sql)]


class DBCtx(threading.local):
    """
    Thread local object that holds connection info.
    """

    def __init__(self, connect, use_mysql_connector):
        self.connect = connect
        self.connection = None
        self.transactions = 0
        self.prepared = True
        if use_mysql_connector:
            self.get_cursor = lambda: self.connection.cursor(prepared=self.prepared)
            self.log = lambda action: logger.debug('%s connection <%s>...' % (action, hex(id(self.connection._cnx))))
        else:
            self.get_cursor = lambda: self.connection.cursor()
            self.log = lambda action: logger.debug('%s connection <%s>...' % (action, hex(id(self.connection))))

    def is_not_init(self):
        return self.connection is None

    def init(self):
        self.transactions = 0
        self.connection = self.connect()
        self.log('Use')

    def release(self):
        if self.connection:
            self.log('Release')
            self.connection.close()
            self.connection = None

    def cursor(self):
        """
        Return cursor
        """
        # logger.debug('Cursor prepared: %s' % self.prepared)
        return self.get_cursor()

    def statement(self, sql: str):
        """
        Return statement
        """
        return self.connection.statement(sql)


class ConnectionCtx(object):
    """
    ConnectionCtx object that can open and close connection context. ConnectionCtx object can be nested and only the most
    outer connection has effect.
    with connection():
        pass
        with connection():
            pass
    """

    def __init__(self, db_ctx):
        self.db_ctx = db_ctx

    def __enter__(self):
        self.should_cleanup = False
        if self.db_ctx.is_not_init():
            self.db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        if self.should_cleanup:
            self.db_ctx.release()


class TransactionCtx(object):
    """
    TransactionCtx object that can handle transactions.
    with TransactionCtx():
        pass
    """

    def __init__(self, db_ctx):
        self.db_ctx = db_ctx

    def __enter__(self):
        self.should_close_conn = False
        if self.db_ctx.is_not_init():
            # needs open a connection first:
            self.db_ctx.init()
            self.should_close_conn = True
        self.db_ctx.transactions += 1
        logger.debug('Begin transaction...' if self.db_ctx.transactions == 1 else 'Join current transaction...')
        return self

    def __exit__(self, exctype, excvalue, traceback):
        self.db_ctx.transactions -= 1
        try:
            if self.db_ctx.transactions == 0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                self.db_ctx.release()

    def commit(self):
        try_commit(self.db_ctx)

    def rollback(self):
        logger.warning('Rollback transaction...')
        self.db_ctx.connection.rollback()
        logger.debug('Rollback ok.')


class DBError(Exception):
    pass


class MapperError(DBError):
    pass


class MultiColumnsError(DBError):
    pass


class Dict(dict):
    """
    Simple dict but support access as x.y style.
    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    """

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class SqlModel:
    from typing import List
    def __init__(self, sql: str, action: str, namespace: str, dynamic=False, includes: List[str] = None):
        self.sql = sql
        self.action = action
        self.namespace = namespace
        self.dynamic = dynamic
        self.includes = includes
        self.mapping = True if dynamic else ':' in sql
        self.placeholder = False if self.mapping else '?' in sql


class SqlAction(Enum):
    CALL = 'call'
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'
    SELECT = 'select'


def sql_log(function: str, sql: str, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.db.%s' \n\t\tsql: %s \n\t\targs: %s \n\t\tkwargs: %s" % (function, sql.strip(), args, kwargs))


def page_log(function: str, sql: str, page_num, page_size, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.db.%s', page_num: %d, page_size: %d \n\t\tsql: %s \n\t\targs: %s \n\t\tkwargs: %s" % (
        function, page_num, page_size, sql.strip(), args, kwargs))


def insert_log(function: str, table: str, **kwargs):
    logger.debug("Exec func 'mysqlx.db.%s' \n\t\t Table: '%s', kwargs: %s" % (function, table, kwargs))


def do_sql_log(function: str, sql: str, *args):
    logger.debug("Exec func 'mysqlx.db.%s' \n\t\t sql: %s \n\t\t args: %s" % (function, sql, args))


def do_page_log(function: str, sql: str, page_num, page_size, *args):
    logger.debug(
        "Exec func 'mysqlx.db.%s', page_num: %d, page_size: %d \n\t\t sql: %s \n\t\t args: %s" % (function, page_num, page_size, sql.strip(), args))


def sql_id_log(function: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.dbx.%s', sql_id: %s, args: %s, kwargs: %s" % (function, sql_id.strip(), args, kwargs))


def page_sql_id_log(function: str, sql_id: str, page_num, page_size, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.dbx.%s', page_num: %d, page_size: %d, sql_id: %s, args: %s, kwargs: %s" % (
        function, page_num, page_size, sql_id.strip(), args, kwargs))


def orm_by_page_log(function, page_num, page_size, class_name, where, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s', page_num: %d, page_size: %d \n\t\t Class: '%s', where: %s, args: %s, kwargs: %s" % (
        function, page_num, page_size, class_name, where, args, kwargs))


def orm_page_log(function, page_num, page_size, class_name, *fields, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s', page_num: %d, page_size: %d \n\t\t Class: '%s', fields: %s, kwargs: %s" % (
        function, page_num, page_size, class_name, fields, kwargs))


def orm_insert_log(function, class_name, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', kwargs: %s" % (function, class_name, kwargs))


def orm_delete_by_id_log(function, class_name, _id, update_by):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', id: %d, update_by: %s" % (function, class_name, _id, update_by))


def orm_by_log(function, class_name, where, *args, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', where: %s, args: %s, kwargs: %s" % (function, class_name, where, args, kwargs))


def orm_inst_log(function, class_name):
    logger.debug("Exec func 'mysqlx.orm.Model.%s', Class: '%s'" % (function, class_name))


def orm_logical_delete_by_ids_log(function, class_name, ids, update_by, batch_size):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', ids: %s, update_by: %s, batch_size: %s" % (function, class_name, ids, update_by, batch_size))


def orm_count_log(function, class_name, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', kwargs: %s" % (function, class_name, kwargs))


def orm_find_log(function, class_name, *fields, **kwargs):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', fields: %s, kwargs: %s" % (function, class_name, fields, kwargs))


def orm_find_by_id_log(function, class_name, _id, *fields):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', id: %d, fields: %s" % (function, class_name, _id, fields))


def orm_find_by_ids_log(function, class_name, ids, *fields):
    logger.debug("Exec func 'mysqlx.orm.Model.%s' \n\t\t Class: '%s', ids: %s, fields: %s" % (function, class_name, ids, fields))

