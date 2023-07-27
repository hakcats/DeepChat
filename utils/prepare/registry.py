import json
import pkgutil
from importlib import import_module, reload

import chat_core
from chat_core.core.common.metrics_registry import _registry_path as m_registry_path, _REGISTRY as M_REGISTRY
from chat_core.core.common.registry import _registry_path as c_registry_path, _REGISTRY as C_REGISTRY

if __name__ == '__main__':
    C_REGISTRY.clear()
    M_REGISTRY.clear()

    for _, pkg_name, _ in pkgutil.walk_packages(chat_core.__path__, chat_core.__name__ + '.'):
        if pkg_name not in ('chat_core.core.common.registry', 'chat_core.core.common.metrics_registry'):
            reload(import_module(pkg_name))

    with c_registry_path.open('w', encoding='utf-8') as f:
        json.dump(dict(sorted(C_REGISTRY.items())), f, indent=2)

    with m_registry_path.open('w', encoding='utf-8') as f:
        json.dump(dict(sorted(M_REGISTRY.items())), f, indent=2)
