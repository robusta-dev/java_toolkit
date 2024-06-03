from src.java_toolkit.common.utils.remote_ns_cmd import run_command
from os import path

class TmpRemotePodMounter(object):

    def __init__(self, pid: str, src_dir: str, local_mnt_path: str, verbose: bool):
        self.verbose = verbose
        self.src_dir = src_dir
        self.local_mnt_path = local_mnt_path
        self.remote_mnt_path = f"/proc/{pid}/cwd{local_mnt_path}"

    def __enter__(self):
        mkdir_cmd = f"mkdir -p '{self.remote_mnt_path}'"
        run_command(mkdir_cmd, self.verbose)
        cp_cmd= f"cp -R '{self.src_dir}' '{self.remote_mnt_path}'"
        run_command(cp_cmd, self.verbose)
        return self

    def get_mounted_jdk_dir(self):
        return path.join(self.local_mnt_path, path.basename(self.src_dir) )

    def __exit__(self, exc_type, exc_val, exc_tb):
        rm_dir_cmd = f"rm -R '{self.remote_mnt_path}'"
        run_command(rm_dir_cmd, self.verbose)