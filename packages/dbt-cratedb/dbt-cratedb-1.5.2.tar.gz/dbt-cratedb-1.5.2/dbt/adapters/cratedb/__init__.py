# these are mostly just exports, #noqa them so flake8 will be happy
from dbt.adapters.cratedb.connections import CrateDBAdapterConnectionManager
from dbt.adapters.cratedb.connections import CrateDBAdapterCredentials
from dbt.adapters.cratedb.relation import CrateDBAdapterRelation  # noqa: F401
from dbt.adapters.cratedb.column import CrateDBColumn  # noqa
from dbt.adapters.cratedb.impl import CrateDBAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import cratedb

Plugin = AdapterPlugin(
    adapter=CrateDBAdapter,   # type: ignore
    credentials=CrateDBAdapterCredentials,
    include_path=cratedb.PACKAGE_PATH
)