import os
import pwd
import subprocess
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from distutils import log
from pathlib import Path


HERE = Path(os.path.abspath(os.path.dirname(__file__)))

USERNAME = pwd.getpwuid(os.getuid()).pw_name
IS_ROOT = USERNAME == 'root'

RW__ = 0o600
RRR = 0o444
RWRR = 0o644
RWRWRW = 0o666
RXRXRX = 0o555
RWXRXRX = 0o755

BSSENV_ENVIRONMENTS = \
    Path('/var/bssenv/environments') if IS_ROOT else Path('~/.local/share/bssenv/environments').expanduser()
BSSENV_ENVIRONMENTS_LOCK = Path(f'{BSSENV_ENVIRONMENTS}.lock')

BSSENV_BASH_COMPLETION = \
    Path('/etc/bash_completion.d/bssenv.autocomplete') if IS_ROOT else Path('~/.bash_completion').expanduser()


def ensure_files_exist(*files: Path, mode: int) -> None:
    for file in files:
        file.touch(mode=mode, exist_ok=True)
        file.chmod(mode=mode)


def install_bssenv_completions(package_completion_file: Path, completion_file: Path) -> None:
    if not package_completion_file.exists():
        return
    in_section = False
    content = []
    for line in completion_file.read_text().splitlines():
        if line == '# -- bssenv -->':
            in_section = True
            continue
        elif in_section and line == '# ------------<':
            in_section = False
            continue
        elif in_section:
            continue
        else:
            content.append(line)
    content = [
        *content,
        '# -- bssenv -->',
        *(package_completion_file.read_text().splitlines()),
        '# ------------<'
    ]
    with completion_file.open(mode="w") as f:
        f.write('\n'.join(content))


def pre_build_py(step):
    """-- Pre build_py steps --"""

    pass


def post_build_py(step):
    """-- Post build_py steps --"""

    build_lib = Path(step.build_lib)
    data_dir = build_lib / 'comarch' / 'bss' / 'bssenv' / 'data'
    config_dir = data_dir / 'config'

    version = step.distribution.get_version()
    who_am_i = 'root' if IS_ROOT else 'non_root'

    package_completion_file = build_lib / 'comarch/bss/bssenv/data/scripts/sys/bssenv.autocomplete'

    log.info('_______________________________________________________________')
    log.info('Installation metadata:')
    log.info(f'BSSENV VERSION: {version}')
    log.info(f'INSTALLATION TYPE: {who_am_i}')
    log.info('_______________________________________________________________')

    # save bssenv version
    bssenv_version = config_dir / 'bssenv_version'
    if bssenv_version.exists():
        bssenv_version.unlink()
    bssenv_version.write_text(version)

    # save installation type (root/non-root)
    installation_type = config_dir / 'install_type'
    if installation_type.exists():
        installation_type.unlink()
    installation_type.write_text(who_am_i)

    # save environments path
    bssenv_environments = config_dir / 'bssenv_environments'
    bssenv_environments.write_text(str(BSSENV_ENVIRONMENTS))

    # install package dependencies
    python_site_packages_dir = data_dir / 'python_site_packages'
    requirements_txt = python_site_packages_dir / 'requirements.txt'
    if requirements_txt.exists():
        log.info('Install dependencies to custom python site packages directory:')
        log.info(str(python_site_packages_dir))
        subprocess.run(
            [
                'python3', '-m', 'pip', 'install',
                '--extra-index-url', 'http://devops-telco.krakow.comarch:8080/simple',
                '--trusted-host', 'devops-telco.krakow.comarch',
                f'--target={python_site_packages_dir}',
                '-r', requirements_txt
            ],
            check=True)
        subprocess.run(['ls', '-alh', str(python_site_packages_dir)], check=True)

    # Prepare paths
    if IS_ROOT:
        BSSENV_BASH_COMPLETION.parent.mkdir(mode=RWXRXRX, parents=False, exist_ok=True)
        BSSENV_BASH_COMPLETION.parent.chmod(mode=RWXRXRX)
        ensure_files_exist(BSSENV_BASH_COMPLETION, mode=RWRR)
        BSSENV_ENVIRONMENTS.parent.mkdir(mode=RWXRXRX, parents=False, exist_ok=True)
        BSSENV_ENVIRONMENTS.parent.chmod(mode=RWXRXRX)
        (BSSENV_ENVIRONMENTS.parent / 'env').mkdir(mode=RWXRXRX, parents=False, exist_ok=True)
        (BSSENV_ENVIRONMENTS.parent / 'env').chmod(mode=RWXRXRX)
        ensure_files_exist(BSSENV_ENVIRONMENTS, BSSENV_ENVIRONMENTS_LOCK, mode=RWRWRW)
    else:
        ensure_files_exist(BSSENV_BASH_COMPLETION, mode=RW__)
        BSSENV_ENVIRONMENTS.parent.mkdir(parents=True, exist_ok=True)
        (BSSENV_ENVIRONMENTS.parent / 'env').mkdir(parents=True, exist_ok=True)
        ensure_files_exist(BSSENV_ENVIRONMENTS, BSSENV_ENVIRONMENTS_LOCK, mode=RW__)

    log.info('_______________________________________________________________')
    log.info('Installation paths:')
    log.info(f'BSSENV_BASH_COMPLETION: {BSSENV_BASH_COMPLETION}')
    log.info(f'BSSENV_ENVIRONMENTS: {BSSENV_ENVIRONMENTS}')
    log.info('_______________________________________________________________')

    # Install bssenv bash completions
    install_bssenv_completions(package_completion_file, BSSENV_BASH_COMPLETION)


class build_py(_build_py):

    def run(self):
        """Call pre build_py, build_py and post build_py steps"""

        self.execute(pre_build_py, args=[self], msg=pre_build_py.__doc__)
        _build_py.run(self)
        self.execute(post_build_py, args=[self], msg=post_build_py.__doc__)


setup(cmdclass={'build_py': build_py})
