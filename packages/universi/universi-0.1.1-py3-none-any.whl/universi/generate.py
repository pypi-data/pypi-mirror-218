import ast
import importlib
import inspect
import os
import shutil
from copy import deepcopy
from enum import Enum
from pathlib import Path
from types import GenericAlias
from typing import Any, TypeAlias, get_args, get_origin

from pydantic import BaseConfig, BaseModel
from pydantic.fields import ModelField
from typing_extensions import assert_never

from universi.structure.common import Sentinel
from universi.structure.schemas import (
    OldSchemaDidntHaveField,
    OldSchemaFieldWas,
    OldSchemaHadField,
)
from universi.structure.versions import Version, Versions

FieldNameT: TypeAlias = str
# NOTE: Can't use chdir anymore
CURRENT_DIR = Path().resolve().absolute()
print(CURRENT_DIR)


def regenerate_dir_to_all_versions(dir: Path, versions: Versions):
    schemas = {
        k: (v, get_fields_for_model(v))
        for k, v in deepcopy(versions.versioned_schemas).items()
    }

    for version in versions.versions:
        # NOTE: You'll have to use relative imports

        generate_versioned_directory(dir, schemas, version.date.replace("-", "_"))
        apply_schema_migrations(version, schemas)


def apply_schema_migrations(
    version: Version,
    schemas: dict[
        str,
        tuple[type[BaseModel], dict[FieldNameT, tuple[type[BaseModel], ModelField]]],
    ],
):
    for version_change in version.version_changes:
        for alter_schema_instruction in version_change.alter_schema_instructions:
            schema = alter_schema_instruction.schema
            schema_path = schema.__module__ + schema.__name__
            schema_field_info_bundle = schemas.get(schema_path)
            if schema_field_info_bundle is not None:
                field_name_to_field_model = schema_field_info_bundle[1]
                for field_change in alter_schema_instruction.changes:
                    match field_change:
                        case OldSchemaDidntHaveField(field_name):
                            # TODO: Check that the user doesn't pop it and change it at the same time

                            field_name_to_field_model.pop(field_change.field_name)
                        case OldSchemaFieldWas(
                            field_name,
                            old_field_type,
                            old_field_info,
                        ):
                            field_info = field_name_to_field_model[
                                field_change.field_name
                            ][1].field_info
                            for attr_name in old_field_info.__dataclass_fields__:
                                attr_value = getattr(old_field_info, attr_name)
                                if attr_value is not Sentinel:
                                    setattr(field_info, attr_name, attr_value)
                                    field_info._universi_field_names.add(attr_name)
                        case OldSchemaHadField(
                            field_name,
                            old_field_type,
                            old_field_info,
                        ):
                            field_name_to_field_model[field_change.field_name] = (
                                schema,
                                ModelField(
                                    name=field_name,
                                    type_=old_field_type,
                                    field_info=old_field_info,
                                    class_validators=None,
                                    model_config=BaseConfig,
                                ),
                            )
                        case _:
                            assert_never(field_change)


def generate_versioned_directory(
    dir: Path,
    schemas: dict[
        str,
        tuple[type[BaseModel], dict[FieldNameT, tuple[type[BaseModel], ModelField]]],
    ],
    version: str,
):
    version_dir = dir.with_name(dir.name + "_v" + str(version))
    version_dir.mkdir(exist_ok=True)
    for subroot, dirnames, filenames in os.walk(dir):
        # NOTE: subroot is already relative to root. What're doing is meaningless
        original_subroot = Path(subroot)
        versioned_subroot = version_dir / original_subroot.relative_to(dir)
        if "__pycache__" in dirnames:
            dirnames.remove("__pycache__")
        for dirname in dirnames:
            (versioned_subroot / dirname).mkdir(exist_ok=True)
        for filename in filenames:
            original_file = (original_subroot / filename).absolute()
            versioned_file = (versioned_subroot / filename).absolute()
            print(original_file)

            if filename.endswith(".py") and filename != "__init__.py":
                module_path = ".".join(
                    original_file.relative_to(CURRENT_DIR).with_suffix("").parts,
                )
                module = importlib.import_module(module_path)
                new_module_text = modify_module(module, schemas)
                versioned_file.write_text(new_module_text)
            else:
                shutil.copyfile(original_file, versioned_file)


def get_fields_for_model(model) -> dict[FieldNameT, tuple[type[BaseModel], ModelField]]:
    actual_fields: dict[FieldNameT, tuple[type[BaseModel], ModelField]] = {}
    for cls in model.__mro__:
        if cls is BaseModel:
            break
        if not issubclass(cls, BaseModel):
            continue
        for field_name, field in cls.__fields__.items():
            if field_name not in actual_fields and field_name in cls.__annotations__:
                actual_fields[field_name] = (cls, field)
    return actual_fields


def modify_module(
    module,
    modified_schemas: dict[
        str,
        tuple[type[BaseModel], dict[str, tuple[type[BaseModel], ModelField]]],
    ],
) -> str:
    parsed_file = ast.parse(inspect.getsource(module))
    body = ast.Module(
        [ast.ImportFrom(module="universi", names=[ast.alias(name="Field")], level=0)]
        + [
            modify_cls(n, modified_schemas[module_name][1])
            if isinstance(n, ast.ClassDef)
            and (module_name := module.__name__ + n.name) in modified_schemas
            else n
            for n in parsed_file.body
        ],
        [],
    )

    return ast.unparse(body)


def modify_cls(
    n: ast.ClassDef,
    actual_fields: dict[str, tuple[type[BaseModel], ModelField]],
) -> ast.ClassDef:
    body = [
        ast.AnnAssign(
            target=ast.Name(id=name, ctx=ast.Store()),
            annotation=ast.Name(id=custom_repr(field[1].annotation), ctx=ast.Load()),
            value=ast.Call(
                func=ast.Name(id="Field", ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(
                        arg=attr,
                        value=ast.Constant(
                            value=repr(getattr(field[1].field_info, attr)),
                        ),
                    )
                    # TODO: We need to raise an exception if field_info doesn't have _universi_field_names
                    # to prevent weird bugs when the user uses a mix of our Field and pydantic Field
                    for attr in getattr(
                        field[1].field_info,
                        "_universi_field_names",
                        (),
                    )
                ],
            ),
            simple=1,
        )
        for name, field in actual_fields.items()
    ]
    old_body = [n for n in n.body if not isinstance(n, ast.AnnAssign)]
    n.body = body + old_body
    return n


# Heavily inspired by Samuel Colvin's devtools


def custom_repr(value: Any) -> Any:
    if isinstance(value, list | tuple | set | frozenset):
        return value.__class__(map(custom_repr, value))
    if isinstance(value, dict):
        return value.__class__(
            (custom_repr(k), custom_repr(v)) for k, v in value.items()
        )
    if isinstance(value, GenericAlias):
        return f"{custom_repr(get_origin(value))}[{', '.join(custom_repr(a) for a in get_args(value))}]"
    if isinstance(value, type):
        return value.__name__
    if isinstance(value, Enum):
        return PlainRepr(f"{value.__class__.__name__}.{value.name}")
    else:
        return PlainRepr(repr(value))


class PlainRepr(str):
    """
    String class where repr doesn't include quotes.
    """

    def __repr__(self) -> str:
        return str(self)
