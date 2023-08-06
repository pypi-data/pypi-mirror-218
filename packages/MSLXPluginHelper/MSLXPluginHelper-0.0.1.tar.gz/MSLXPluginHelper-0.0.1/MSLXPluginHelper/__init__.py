import os, pkgutil
print("已调用Plugins/__init__.py")
__all__ = list(module for _, module, _ in pkgutil.iter_modules([os.path.dirname(__file__)]))
print(f"当前__all__变量:{__all__}")
name = "MSLXPluginHelper"