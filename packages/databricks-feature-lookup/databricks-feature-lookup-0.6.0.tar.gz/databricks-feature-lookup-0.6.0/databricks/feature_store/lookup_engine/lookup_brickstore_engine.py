from databricks.feature_store.entities.online_feature_table import OnlineFeatureTable
from databricks.feature_store.lookup_engine.lookup_mysql_engine import LookupMySqlEngine


class LookupBrickstoreEngine(LookupMySqlEngine):
    def __init__(
        self, online_feature_table: OnlineFeatureTable, ro_user: str, ro_password: str
    ):
        super().__init__(online_feature_table, ro_user, ro_password)

    def _get_database_and_table_name(self, online_table_name):
        name_components = online_table_name.split(".")
        # expect 3L names for Brickstore
        if len(name_components) != 3:
            raise ValueError(
                f"Online table name {online_table_name} is misformatted and must be in 3L format for Brickstore"
            )
        # database and table name are 2nd and 3rd entry, respectively due to presence of catalog name
        return (name_components[1], name_components[2])

    @property
    def engine_url(self):
        return f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"
