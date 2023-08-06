from dataclasses import dataclass
from typing import Optional, Set, List, Any
from dbt.adapters.base.impl import AdapterConfig
from dbt.adapters.sql import SQLAdapter

from dbt.adapters.cratedb import CrateDBAdapterConnectionManager
from .relation import CrateDBAdapterRelation
from .column import CrateDBColumn

import dbt.exceptions
import dbt.utils

from dbt.adapters.base.relation import BaseRelation

LIST_RELATIONS_MACRO_NAME = "list_relations_without_caching"
LIST_SCHEMAS_MACRO_NAME = "list_schemas"
RENAME_RELATION_MACRO_NAME = "rename_relation"
RENAME_VIEW_RELATION_MACRO_NAME = "rename_view_relation"


@dataclass
class CrateDBConfig(AdapterConfig):
    unlogged: Optional[bool] = None


class CrateDBAdapter(SQLAdapter):
    Relation = CrateDBAdapterRelation
    ConnectionManager = CrateDBAdapterConnectionManager
    Column = CrateDBColumn

    AdapterSpecificConfigs = CrateDBConfig

    @classmethod
    def date_function(cls):
        return 'now()'

    @classmethod
    def is_cancelable(cls) -> bool:
        return False

    def _get_catalog_schemas(self, manifest):
        schemas = super()._get_catalog_schemas(manifest)
        try:
            return schemas.flatten()
        except dbt.exceptions.DbtRuntimeError as exc:
            dbt.exceptions.Exception(
                'Cross-db references not allowed in adapter {}: Got {}'.format(
                        self.type(), exc.msg
                )
            )

    def list_schemas(self, database: str = "") -> List[str]:
        results = self.execute_macro(LIST_SCHEMAS_MACRO_NAME)
        return [row[0] for row in results]

    def list_relations_without_caching(
        self,
        schema_relation: BaseRelation,
    ) -> List[BaseRelation]:
        kwargs = {"schema_relation": schema_relation}
        results = self.execute_macro(LIST_RELATIONS_MACRO_NAME, kwargs=kwargs)

        relations = []
        quote_policy = {"database": True, "schema": True, "identifier": True}
        for _database, name, _schema, _type in results:
            try:
                _type = self.Relation.get_relation_type(_type)
            except ValueError:
                _type = self.Relation.External
            relations.append(
                self.Relation.create(
                    database=_database,
                    schema=_schema,
                    identifier=name,
                    quote_policy=quote_policy,
                    type=_type,
                )
            )
        return relations

    def rename_relation(self, from_relation, to_relation):
        self.cache_renamed(from_relation, to_relation)

        kwargs = {"from_relation": from_relation, "to_relation": to_relation}
        try:
            self.execute_macro(RENAME_RELATION_MACRO_NAME, kwargs=kwargs)
        except dbt.exceptions.DbtDatabaseError as exc:
            self.execute_macro(RENAME_VIEW_RELATION_MACRO_NAME, kwargs=kwargs)
        except Exception as exc:
            raise exc
