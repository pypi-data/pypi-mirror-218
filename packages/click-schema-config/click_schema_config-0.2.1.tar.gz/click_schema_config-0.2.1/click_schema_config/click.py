__all__ = ["schema_from_inis"]

from typing import Any, Protocol
from click.decorators import FC
from .types import FileLike

import builtins

import click
from .read_config import read_configs


class Decorator(Protocol):
    def __call__(self, func: FC) -> FC:
        ...


def schema_from_inis(
    files: list[FileLike] | FileLike = ["config.default.ini", "config.ini"],
    insecure_eval: bool = False,
    **kwargs: Any,
) -> Decorator:
    """Decorate a click command to load options from a config file.

    Parameters
    ----------
    filenames : list[FileLike] | files, optional
        List of files (either open file-pointers or filenames) to load, by default ["config.default.ini", "config.ini"]
    insecure_eval : bool, optional
        Whether or not to allow arbitrary code execution, by default False
    **kwargs : Any
        Passed to click.option
    """

    if isinstance(files, str):
        files = [files]

    config = read_configs(files)

    def decorator(func: FC) -> FC:
        # We use reverse-order so that the options are added in the order they appear in the file
        for section in reversed(config.values()):
            for d in reversed(section.values()):
                type_evalled = d.type
                if type_evalled is not None:
                    if insecure_eval:
                        try:
                            type_evalled = eval(type_evalled)
                        except Exception:
                            type_evalled = None
                    else:
                        type_evalled = getattr(builtins, type_evalled, None)

                func = click.option(
                    f"--{d.option_name}"
                    if type_evalled is not bool
                    else f"--{d.option_name}/--no-{d.option_name}",
                    d.programmatic_name,
                    **(
                        dict(
                            type=type_evalled,
                            default=d.value,
                            required=d.required,
                            help=f"\n{d.description or ''}".replace("\n", "\b\n"),
                            show_default=True,
                        )
                        | kwargs
                    ),
                )(func)

        return func

    return decorator
