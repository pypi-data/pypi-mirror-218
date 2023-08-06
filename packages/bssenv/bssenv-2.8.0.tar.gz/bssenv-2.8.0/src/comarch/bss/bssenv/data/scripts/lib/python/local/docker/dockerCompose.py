import os
from typing import Optional, List, Union
from pathlib import Path
from ..os import exec2


def get_container_config_hash(*container_names: str) -> Union[str, List[str]]:
    if len(container_names) > 0:
        hash = exec2(
            ['docker', 'inspect', '-f', '{{index .Config.Labels "com.docker.compose.config-hash"}}', *container_names])
        if hash.returncode != 0:
            raise Exception(
                f"Can't get config hash for containers: {container_names}\n"
                f"exit code: {hash.returncode}\n"
                f"stdout: {hash.stdout}\n"
                f"stderr: {hash.stderr}")
        # INFO: at the moment of writing this docker was returning results in the same order as order of
        # input arguments. So there is no need of postprocessing
        return hash.stdout.strip() if len(container_names) == 1 else hash.stdout.strip().splitlines()


def get_service_config_hash(*service_keys: str, composefile_path: Optional[Path] = None) -> Union[str, List[str]]:
    if len(service_keys) > 0:
        hash = exec2(
            ['docker-compose', '--log-level', 'ERROR'] +
            (['-f', str(composefile_path)] if composefile_path is not None else []) +
            ['config', f"--hash={','.join(service_keys)}"],
            env=os.environ)
        if hash.returncode != 0:
            raise Exception(
                f"Can't get config hash for services: {service_keys}\n"
                f"exit code: {hash.returncode}\n"
                f"stdout: {hash.stdout}\n"
                f"stderr: {hash.stderr}")
        if len(service_keys) == 1:
            return hash.stdout.strip().split()[1]
        else:
            # Unfortunately docker-compoe is not returning results in the same order as order of input arguments
            services_and_hashes = {_: __ for _, __ in [_.split() for _ in hash.stdout.strip().splitlines()]}
            hashes = []
            for service_key in service_keys:
                hashes.append(services_and_hashes[service_key])
            return hashes
