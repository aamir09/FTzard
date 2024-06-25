import pandas as pd
from upath import UPath

from dagster import (
    Field,
    InitResourceContext,
    InputContext,
    OutputContext,
    StringSource,
    UPathIOManager,
    io_manager,
    input_manager,
    InputManager,
)


import joblib
import sys

class FixedPathIOManager(UPathIOManager):
    extension: str = ".joblib"

    def _get_path(self, context) -> str:
        context.log.info(context.resource_config)
        context.log.info(type(context))
        if 'file_name' in context.resource_config: # input manager and output with filename
            return UPath(f"{context.resource_config['base_path']}/{context.resource_config['file_name']}")
        else:
            return UPath(f"{context.resource_config['base_path']}/{context.name}{FixedPathIOManager.extension}")
    
    def dump_to_path(self, context: OutputContext, obj, path: UPath):
        context.log.info("dump in fixedpathio")
        context.log.info(context.resource_config)
        with path.open("wb") as file:
            joblib.dump(obj, file)

    def load_from_path(self, context: InputContext, path: UPath) -> pd.DataFrame:
        context.log.info("load in fixedpathio")
        context.log.info(context.resource_config)
        with path.open("rb") as file:
            return joblib.load(file)

    def load_input(self, context):
        context.log.info(f"FPIOxxxxxxxxxxxxx\n {context} AND {context.upstream_output}")
        source_asset = False
        asset_mode = False
        if context.has_asset_key: # this io manager is being used in an asset op
            asset_mode = True
            context.log.info("asset_mode=True")
            context.log.info(context.upstream_output.asset_key.path[0])
            if context.upstream_output.asset_key.path[0][0:7]=='source_':
                source_asset = True
        if (source_asset and asset_mode) or (context.upstream_output is None and 'file_name' in context.resource_config):   # input manager
            # remove because dagstermill processes dont seem to have a context
            # context.log.info(f"{context.metadata}<>{context.name}<>{context.resource_config}")
            # if context.upstream_output is None and 'file_name' in context.resource_config: # input manager
            context.log.info("xxxxxxxxxxx Input Manager Path")
            path = self._get_path(context)
        else:
            context.log.info("xxxxxxxxxxx Upstrem Output Path")
            path = self._get_path(context.upstream_output)

        with path.open("rb") as file:
            return joblib.load(file)




class PandasCSVIOManager(UPathIOManager):
    extension: str = ".csv"

    def _get_path(self, context) -> str:
        context.log.info(f"resource_config={context.resource_config}")
        context.log.info(f"type{type(context)}")
        if 'file_name' in context.resource_config: # input manager and output with filename
            return UPath(f"{context.resource_config['base_path']}/{context.resource_config['file_name']}")
        else:
            return UPath(f"{context.resource_config['base_path']}/{context.name}{type(self).extension}")

    def dump_to_path(self, context: OutputContext, obj: pd.DataFrame, path: UPath):
        context.log.info(context.asset_key)
        with path.open("wb") as file:
            obj.to_csv(file)

    def load_from_path(self, context: InputContext, path: UPath) -> pd.DataFrame:
        with path.open("rb") as file:
            return pd.read_csv(file)

    def load_input(self, context):
        context.log.info(f"CSVxxxxxxxxxxxxx\n {context} AND {context.upstream_output}")
        context.log.info(dir(InitResourceContext))
        # remove because dagstermill processes dont seem to have a context
        # context.log.info(f"{context.metadata}<>{context.name}<>{context.resource_config}")
        source_asset = False
        asset_mode = False
        if context.has_asset_key: # this io manager is being used in an asset op
            asset_mode = True
            context.log.info("asset_mode=True")
            context.log.info(context.asset_key)
            context.log.info(context.upstream_output.asset_key)
            context.log.info(context.upstream_output.asset_key.path[0])
            if context.upstream_output.asset_key.path[0][0:7]=='source_':
                source_asset = True
        #if (source_asset and asset_mode) or (context.upstream_output is None and 'file_name' in context.resource_config): # input manager
        if (context.upstream_output is None and 'file_name' in context.resource_config): # input manager
            context.log.info(f"xxxxxxxxxxx Input Manager Path {asset_mode}")
            path = self._get_path(context)
        else:
            context.log.info("xxxxxxxxxxx Upstrem Output Path {asset_mode}")
            bla = context.upstream_output
            context.log.info(dir(bla))
            if asset_mode:
                context.log.info(f"Asset keys {context.asset_key} Upstream {bla.asset_key}")
            path = self._get_path(context.upstream_output)
        #path = self._get_path(context)
        with path.open("rb") as file:
            return pd.read_csv(file)

@io_manager(config_schema=
    {
        "base_path": Field(str, is_required=False),
        "file_name": Field(str, is_required=False)
    }
)
def pandas_csv_io_manager(
    init_context: InitResourceContext,
) -> PandasCSVIOManager:
    assert init_context.instance is not None  # to please mypy
    init_context.log.info(f":::{init_context.resource_config}")
    base_path = UPath(
        init_context.resource_config.get(
            "base_path", init_context.instance.storage_directory()
        )
    )
    return PandasCSVIOManager(base_path=base_path)


@io_manager(config_schema=
    {
        "base_path": Field(str, is_required=False),
        "file_name": Field(str, is_required=False)
    }
)
def joblib_io_manager(
    init_context: InitResourceContext,
) -> FixedPathIOManager:
    assert init_context.instance is not None  # to please mypy
    base_path = UPath(
        init_context.resource_config.get(
            "base_path", init_context.instance.storage_directory()
        )
    )
    return FixedPathIOManager(base_path=base_path)