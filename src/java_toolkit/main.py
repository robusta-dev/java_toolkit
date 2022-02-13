#!/usr/local/bin/python3
import subprocess
import typer
from .common.utils.process import *
from .common.utils.remote_ns_cmd import run_cmd_in_proc_namespace
from .common.utils.tmp_mount import TmpRemotePodMounter
from .configs import *

app = typer.Typer()


def run_jdk_cmd_on_pid(pid: int, cmd_missing_jdk_path_and_pid: str, verbose: bool):
    with TmpRemotePodMounter(pid, JDK_PATH, LOCAL_MOUNT_PATH, verbose) as jdk_mounter:
        local_pid = get_nspid(pid, verbose)
        cmd = cmd_missing_jdk_path_and_pid.format(jdk_path=jdk_mounter.get_mounted_jdk_dir(), pid=local_pid)
        output = run_cmd_in_proc_namespace(pid, cmd, verbose)
        typer.echo(output)


@app.command()
def pod_ps(pod_uid: str):
    typer.echo(get_pod_processes(pod_uid).json())


@app.command()
def jmap(pid: int, verbose: bool = False):
    run_jdk_cmd_on_pid(pid, JMAP_CMD, verbose=verbose)


@app.command()
def jstack(pid: int, verbose: bool = False):
    run_jdk_cmd_on_pid(pid, JSTACK_CMD, verbose=verbose)


if __name__ == "__main__":
    app()
