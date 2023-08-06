from dbt.adapters.base.relation import BaseRelation

from dataclasses import dataclass


@dataclass(frozen=True, eq=False, repr=False)
class CrateDBAdapterRelation(BaseRelation):

    def render(self) -> str:
        return f"{self.schema}.{self.identifier}"
