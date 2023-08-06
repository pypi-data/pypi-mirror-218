""" shimport:

Module importing so dynamic, it's probably crazy.

Some features include:
    * lazy imports
    * import hooks
    * module "registries",
    * namespaces and namespace-filtering
    * fluent style

Examples:
    ```
    import shimport
    namespace = (
        shimport
        .wrapper('my.module_name')
        .prune(
            filter_types=[typing.FunctionType,],
            defined_in_module=True,)
    )
    for name, fxn in namespace.items():
        ...
    ```
"""
from importlib import import_module  # noqa

from . import module

wrap = wrapper = namespace = module.wrapper  # noqa
lazy = lazy_import = module.lazy  # noqa
