import sys
import pytoml

try:
    with open("pyproject.toml") as f:
        pyproject_data = pytoml.load(f)
except FileNotFoundError:
    pyproject_data = {}
except Exception as e:
    sys.exit(e)
else:
    import importlib

    try:
        backend = importlib.import_module(
            pyproject_data["build-system"]["build-backend"]
        )
    except KeyError:
        import setuptools.build_meta

        backend = setuptools.build_meta
    except ImportError:
        backend = None

if "requires" in pyproject_data.get("build-system"):
    print(*pyproject_data["build-system"]["requires"], sep="\n")

if backend is not None:
    try:
        print(*backend.get_requires_for_build_wheel(), sep="\n")
    except Exception as e:
        sys.exit(e)
