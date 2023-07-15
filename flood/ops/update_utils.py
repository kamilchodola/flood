from __future__ import annotations

from . import installation_utils


def update_local(version: str | None = None) -> None:
    installation = installation_utils.get_local_installation()
    if installation['git_dir'] is not None:
        _update_local_git(version=version)
    else:
        _update_local_pip(version=version)


def _update_local_git(version: str | None = None) -> None:
    import subprocess

    installation = installation_utils.get_local_installation()
    git_dir = installation['git_dir']
    if git_dir:
        raise Exception('git installation not specified')
    if version is None:
        # git pull
        cmd = 'git --git-dir={git_dir} pull'.format(git_dir=git_dir)
        subprocess.call(cmd.split(' '))
    else:
        if '.' in version:
            raise Exception(
                'for a pip installation, must specify semantic version number, instead got: '  # noqa: E501
                + str(version)
            )

        # git fetch
        cmd = 'git --git-dir={git_dir} fetch origin'.format(git_dir=git_dir)
        subprocess.call(cmd.split(' '))

        # git checkout commit
        cmd = 'git --git-dir={git_dir} checkout {version}'.format(
            git_dir=git_dir, version=version
        )
        subprocess.call(cmd.split(' '))


def _update_local_pip(version: str | None = None) -> None:
    import subprocess

    if version is None:
        cmd = 'pip install -U flood'
    else:
        if '.' not in version:
            raise Exception(
                'for a pip installation, must specify semantic version number, instead got: '  # noqa: E501
                + str(version)
            )
        cmd = 'pip install flood=={version}'.format(version=version)

    subprocess.check_call(cmd.split(' '))


def update_remote(hostname: str, version: str | None = None) -> None:
    raise NotImplementedError()

