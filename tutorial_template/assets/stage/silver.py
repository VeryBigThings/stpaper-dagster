import os
import pandas as pd
from dagster import (
    AssetIn,
    asset,
)
from ..common import get_ingestion_assets, config


@asset(
    metadata={"path": os.path.join(config["silver_path_prefix"], "customers")},
    io_manager_key="parquet_io_manager",
    group_name="silver",
    description="Collect unique customers",
    ins=get_ingestion_assets(
        asset_keys=[
            "production_tblPurchaseOrder",
            "production_tlkpCustomer",
            "production_tblBillofLadingHeader",
        ],
        per_asset_params=["key", "metadata"],
        asset_direction_class=AssetIn,
    ),
)
def customers(
    production_tblPurchaseOrder: pd.DataFrame,
    production_tlkpCustomer: pd.DataFrame,
    production_tblBillofLadingHeader: pd.DataFrame,
):
    m1 = pd.merge(production_tblPurchaseOrder, production_tlkpCustomer, on="Customer")
    m2 = pd.merge(m1, production_tblBillofLadingHeader, on="Customer")
    return m2[["Customer"]].drop_duplicates()