from contextlib import contextmanager

from crate import client
from crate.client.exceptions import Error, DatabaseError, InterfaceError
from crate.client.converter import DataType

from typing import List, Optional, Tuple, Any, Iterable, Dict, Union

import dbt.exceptions
from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager
from dbt.contracts.connection import AdapterResponse
from dbt.events import AdapterLogger

from dataclasses import dataclass

logger = AdapterLogger("Cratedb")


@dataclass
class CrateDBAdapterCredentials(Credentials):
    database: str = "crate"
    host: Optional[str | List[str]] = "http://localhost:4200/"
    username: Optional[str] = "crate"
    password: Optional[str] = None
    ca_cert: Optional[str] = None
    verify_ssl_cert: Optional[bool] = False
    cert_file: Optional[str] = None
    key_file: Optional[str] = None
    timeout: Optional[int] = 60  # Timeout in Seconds
    error_trace: Optional[bool] = False
    backoff_factor: Optional[float] = 0.1
    socket_keepalive: Optional[bool] = False
    socket_tcp_keepidle: Optional[int] = None
    socket_tcp_keepintvl: Optional[int] = None
    socket_tcp_keepcnt: Optional[int] = None
    schema: Optional[str] = "doc"
    retries: int = 1

    _ALIASES = {
        'pass': 'password'
    }

    @property
    def type(self):
        return 'cratedb'

    @property
    def unique_field(self):
        return self.host

    def _connection_keys(self):
        return (
            'host',
            'user',
            'schema'
        )

    def auth_args(self):
        result = {}

        if self.ca_cert:
            result['ca_cert'] = self.ca_cert
        if self.verify_ssl_cert is not None:
            result['verify_ssl_cert'] = self.verify_ssl_cert
        if self.cert_file:
            result['cert_file'] = self.cert_file
        if self.key_file:
            result['key_file'] = self.key_file
        if self.timeout:
            result['timeout'] = self.timeout
        if self.error_trace is not None:
            result['error_trace'] = self.error_trace
        if self.backoff_factor:
            result['backoff_factor'] = self.backoff_factor
        if self.socket_keepalive:
            if self.socket_tcp_keepidle:
                result['socket_tcp_keepidle'] = self.socket_tcp_keepidle
            if self.socket_tcp_keepintvl:
                result['socket_tcp_keepintvl'] = self.socket_tcp_keepintvl
            if self.socket_tcp_keepcnt:
                result['socket_tcp_keepcnt'] = self.socket_tcp_keepcnt

        return result


class CrateDBAdapterConnectionManager(SQLConnectionManager):
    TYPE = 'cratedb'

    @contextmanager
    def exception_handler(self, sql):
        try:
            yield

        except DatabaseError as e:
            logger.debug('CrateDB error: {}'.format(str(e)))
            try:
                self.rollback_if_open()
            except Error:
                logger.debug("Failed to release connection!")
                pass

            raise dbt.exceptions.DbtDatabaseError(str(e).strip()) from e

        except Exception as e:
            logger.debug("Error running SQL: {}", sql)
            logger.debug("Rolling back transaction.")
            self.rollback_if_open()
            if isinstance(e, dbt.exceptions.DbtRuntimeError):
                # during a sql query, an internal to dbt exception was raised.
                # this sounds a lot like a signal handler and probably has
                # useful information, so raise it without modification.
                raise

            raise dbt.exceptions.DbtRuntimeError(e) from e

    @classmethod
    def open(cls, connection):
        if connection.state == 'open':
            logger.debug('Connection is already open, skipping open.')
            return connection

        creds = connection.credentials

        def connect():
            handle = client.connect(
                creds.host,
                username=creds.username,
                password=creds.password,
                schema=creds.schema,
                **creds.auth_args()
            )
            return handle

        retryable_exceptions = [
            client.exceptions.OperationalError,
            client.exceptions.InternalError,
            client.exceptions.DatabaseError
        ]

        def exponential_backoff(attempt: int):
            return attempt * attempt

        return cls.retry_connection(
            connection,
            connect=connect,
            logger=logger,
            retry_limit=creds.retries,
            retry_timeout=exponential_backoff,
            retryable_exceptions=retryable_exceptions
        )

    def cancel(self, connection):
        connection_name = connection.name
        try:
            pid = connection.handle.get_backend_pid()  # TODO: Investigate if this is the right way to get the pid in crate
        except InterfaceError as exc:
            # if the connection is already closed, not much to cancel!
            if 'already closed' in str(exc):
                logger.debug(
                    f'Connection {connection_name} was already closed'
                )
                return
            raise

        sql = "KILL {})".format(pid)

        logger.debug("Cancelling query '{}' ({})".format(connection_name, pid))

        _, cursor = self.add_query(sql)
        res = cursor.fetchone()

        logger.debug("Cancel query '{}': {}".format(connection_name, res))

    @classmethod
    def get_response(cls, cursor) -> AdapterResponse:
        rows = cursor.rowcount

        return AdapterResponse(
            _message="{} {}".format(rows, "row" if rows == 1 else "rows"),
            rows_affected=rows
        )

    @classmethod
    def data_type_code_to_name(cls, type_code: Union[int, str]) -> str:
        type_name = "UNKNOWN"

        for t in list(DataType):
            if t.value == type_code:
                type_name = t.name
                break

        return type_name
