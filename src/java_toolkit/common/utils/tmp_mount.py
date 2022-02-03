from .remote_ns_cmd import run_command
from os.path import join, basename

class TmpRemotePodMounter(object):
    remote_mnt_path =""
    local_mnt_path =""
    src_dir =""
    verbose = False
    MKDIR_POD_CMD="mkdir -p {}"
    RMDIR_POD_CMD="rm -R {}"
    COPY_CMD="cp -R {} {}"
    ROOT_PROC_NS="/proc/{}/cwd",

    def __init__(self, pid: str, src_dir: str, local_mnt_path: str, verbose: bool):
        self.verbose = verbose
        self.src_dir = src_dir
        self.local_mnt_path = local_mnt_path
        self.remote_mnt_path = join(self.ROOT_PROC_NS.format(pid), local_mnt_path)

    def __enter__(self):
        mkdir_cmd = self.MKDIR_POD_CMD.format(self.remote_mnt_path)
        run_command(mkdir_cmd, self.verbose)
        cp_cmd=self.COPY_CMD.format(self.src_dir, self.remote_mnt_path)
        run_command(cp_cmd, self.verbose)
        return self

    def get_mounted_jdk_dir(self):
            return join(self.local_mnt_path, basename(self.src_dir) )

    def __exit__(self, exc_type, exc_val, exc_tb):
        rm_dir_cmd = self.RMDIR_POD_CMD.format(self.remote_mnt_path)
        run_command(rm_dir_cmd, self.verbose)