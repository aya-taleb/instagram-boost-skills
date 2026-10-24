"""Load a skill's script as a module by path, so tests work with python3 -I."""
import importlib.util
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load(skill, script):
    path = os.path.join(ROOT, "skills", skill, "scripts", script)
    name = "%s_%s" % (skill.replace("-", "_"), script[:-3])
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
