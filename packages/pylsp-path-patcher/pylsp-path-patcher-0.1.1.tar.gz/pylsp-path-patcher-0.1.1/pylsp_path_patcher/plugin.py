import logging
import os
import shlex
import pathlib
import subprocess
from functools import lru_cache

from pylsp import hookimpl
from pylsp._utils import find_parents
from pylsp.config import config as config_module
from pylsp.config.source import ConfigSource

PROJECT_CONFIGS = [".flake8", "setup.cfg", "tox.ini", "pyproject.toml"]
log = logging.getLogger(__name__)


class PathPatcherConfig(ConfigSource):
    def __init__(self, *args, config, **kwargs):
        super().__init__(*args, **kwargs)
        self._config = config

    def user_config(self):
        return {}

    @lru_cache(maxsize=32)
    def project_config(self, document_path):
        files = find_parents(self.root_path, document_path, PROJECT_CONFIGS)
        in_project = 1 if len(files) > 0 else 0
        project_path = str(
            pathlib.Path((files or [document_path])[0]).parent.absolute()
        )
        log.debug(f"project_config({document_path=}): {project_path=}")
        package_path = (
            subprocess.run(
                shlex.split(
                    f"""bash -c '
set -e
VENV_PREFIX=$(([[ {in_project} > 0 ]] && poetry env info --path 2>/dev/null) || \
	([[ {in_project} > 0 ]] && pipenv --venv 2>/dev/null) || \
	(pyenv prefix 2>/dev/null) || \
	echo $VIRTUAL_ENV)
if [[ -n $VENV_PREFIX ]]; then
	$VENV_PREFIX/bin/python -c "import site; print(site.getsitepackages()[0])"
fi'"""
                ),
                cwd=project_path,
                env=os.environ | {"PYENV_VERSION": ""},
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )
        log.debug(f"project_config({document_path=}): {package_path=}")
        plugins = {}
        if package_path:
            plugins["pylint"] = {
                "args": [
                    # a workaround for not being filtered by `pylsp._utils.merge_dicts`
                    # https://github.com/python-lsp/python-lsp-server/blob/363d864b694d39bed6fdecf6d392e5b1261b83a7/pylsp/_utils.py#L137
                    # and that can work with the pylint plugin
                    # https://github.com/python-lsp/python-lsp-server/blob/363d864b694d39bed6fdecf6d392e5b1261b83a7/pylsp/plugins/pylint_lint.py#L194
                    f"--init-hook \"import sys; sys.path += ['{package_path}', '{project_path}']\""
                ]
            }
            plugins["jedi"] = {"extra_paths": [package_path, project_path]}

            mypy_args = (
                self._config._settings.get("plugins", {})
                .get("pylsp_path_patcher", {})
                .get("mypy_args", [])
            )
            if "--python-executable" not in mypy_args:
                python_bin_path = str(
                    (pathlib.Path(package_path) / ".." / ".." / ".." / "bin").resolve()
                    / "python"
                )
                mypy_args += [
                    "--python-executable",
                    python_bin_path,
                ]
            mypy_args += [True]

            plugins["pylsp_mypy"] = {"overrides": mypy_args}
        return {"plugins": plugins}


def patch_config(config):
    config._config_sources["path_patcher"] = PathPatcherConfig(
        config._root_path, config=config
    )


class PatchedConfig(config_module.Config):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        patch_config(self)


@hookimpl
def pylsp_initialize(config: config_module.Config, workspace):
    log.debug("pylsp-path-patcher initialized.")
    config_module.Config = PatchedConfig
    config_module.DEFAULT_CONFIG_SOURCES.append("path_patcher")
    server = workspace._endpoint._dispatcher
    # patch the already created `Config`s
    patch_config(config)
    for name, _workspace in server.workspaces.items():
        patch_config(_workspace)
