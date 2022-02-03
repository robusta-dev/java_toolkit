#!/usr/local/bin/python3
import subprocess
import typer
from .utils.process import get_pod_processes, get_ns_processes
from .utils.remote_ns_cmd import run_cmd_in_proc_namespace
from .utils.tmp_mount import TmpRemotePodMounter
from .configs import *
from os.path import join

app = typer.Typer()

@app.command()
def pod_ps(pod_uid: str):
    app.echo(get_pod_processes(pod_uid).json())

@app.command()
def pod_ns_ps(pid: str, verbose: bool = True):
    app.echo(get_ns_processes(pid, verbose).json())

@app.command()
def jmap(pid: int, verbose: bool = True):
    with TmpRemotePodMounter(pid, JDK_PATH, LOCAL_MOUNT_PATH, verbose) as jdk_mounter:
        jstack_cmd = JMAP_CMD.format(jdk_mounter.get_mounted_jdk_dir(), 1)
        run_cmd_in_proc_namespace(pid, jstack_cmd, verbose)


@app.command()
def jstack(pid: int, verbose: bool = True):
    with TmpRemotePodMounter(pid, JDK_PATH, LOCAL_MOUNT_PATH, verbose) as jdk_mounter:
        jstack_cmd = JSTACK_CMD.format(jdk_mounter.get_mounted_jdk_dir(), 1)
        run_cmd_in_proc_namespace(pid, jstack_cmd, verbose)

if __name__ == "__main__":
    app()
