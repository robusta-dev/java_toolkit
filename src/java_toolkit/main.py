#!/usr/local/bin/python3
import subprocess
import typer
from .utils.pod_ps import get_pod_processes
from .configs import *
from os.path import join

app = typer.Typer()


def run_command(cmd: str, verbose: bool):
    if verbose:
        typer.echo(f"running {cmd}")
    output = subprocess.Popen(
        cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    output.wait()
    if verbose:
        typer.echo(output.decode())


class JDKMounter(object):
    mnt_path =""
    verbose = False

    def __init__(self, pid: str, verbose: bool):
        self.verbose = verbose
        self.mnt_path = DST_MOUNT_PATH.format(pid)

    def __enter__(self):
        mkdir_cmd = MKDIR_POD_CMD.format(self.mnt_path)
        run_command(mkdir_cmd, self.verbose)
        return self

    def get_mounted_jdk_dir(self):
            return join(LOCAL_MOUNT_PATH, JDK_NAME )

    def __exit__(self, exc_type, exc_val, exc_tb):
        rm_dir_cmd = RMDIR_POD_CMD.format(self.mnt_path)
        run_command(rm_dir_cmd, self.verbose)

def run_cmd_in_proc_namespace(pid, command_to_run, verbose):
    nsenter_cmd_formatted = NSENTER_CMD.format(pid, command_to_run)
    run_command(nsenter_cmd_formatted, verbose)

@app.command()
def pod_ps(pod_uid: str):
    typer.echo(get_pod_processes(pod_uid).json())

@app.command()
def find_pid(pod_uid: str, cmdline: str, exe: str):
    for proc in get_pod_processes(pod_uid).processes:
        if cmdline in " ".join(proc.cmdline) and exe in proc.exe:
            typer.echo(proc.pid)

@app.command()
def jmap(pid: int, verbose: bool = False):
    with JDKMounter(pid, verbose) as jdk_mounter:
        jstack_cmd = JMAP_CMD.format(jdk_mounter.get_mounted_jdk_dir(), 1)
        run_cmd_in_proc_namespace(pid, jstack_cmd, verbose)


@app.command()
def jstack(pid: int, verbose: bool = False):
    with JDKMounter(pid, verbose) as jdk_mounter:
        jstack_cmd = JSTACK_CMD.format(jdk_mounter.get_mounted_jdk_dir(), 1)
        run_cmd_in_proc_namespace(pid, jstack_cmd, verbose)

if __name__ == "__main__":
    app()
