import troposphere.rds as rds

from ..common import *
from ..shared import (
    get_endvalue,
    auto_get_props,
    add_obj,
)


def RDS_DB(key):
    for n, v in getattr(cfg, key).items():
        mapname = f"{key}{n}"

        if not v["IBOX_ENABLED"]:
            continue

        # trick to keep current in use resname and obj.title
        resname = v.get("IBOX_RESNAME", mapname)

        # resources
        r_DB = rds.DBInstance(resname)
        auto_get_props(r_DB, mapname=mapname)
        # trick - when providing DBSnapshotIdentifier
        # or SourceDBInstanceIdentifier some props must not exists
        add_obj([
            r_DB,
        ])
