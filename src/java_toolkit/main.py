#!/usr/local/bin/python3
import subprocess
import typer
from java_toolkit.common.utils.process import *
from java_toolkit.common.utils.remote_ns_cmd import run_cmd_in_proc_namespace
from java_toolkit.common.utils.tmp_mount import TmpRemotePodMounter
from java_toolkit.configs import *

app = typer.Typer()


def run_jattach_command(pid: int, cmd_missing_jdk_path_and_pid: str, verbose: bool):
    cmd = cmd_missing_jdk_path_and_pid.format(jdk_path=JDK_PATH, pid=pid)
    output = run_command(cmd, verbose)
    typer.echo(output)


@app.command()
def pod_ps(pod_uid: str):
    typer.echo(get_pod_processes(pod_uid).json())


@app.command()
def jmap(pid: int, verbose: bool = False):
    run_jattach_command(pid, JMAP_CMD, verbose=verbose)


@app.command()
def jstack(pid: int, verbose: bool = False):
    run_jattach_command(pid, JSTACK_CMD, verbose=verbose)


if __name__ == "__main__":
    app()
