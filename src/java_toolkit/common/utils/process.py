#!/usr/local/bin/python3
import re
from typing import List
from src.java_toolkit.common.utils.remote_ns_cmd import run_command

import psutil
import typer
from pydantic import BaseModel

kube_regex = re.compile(r"\d+:.+:/kubepods/[^/]+/pod([^/]+)/([0-9a-f]{64})")
docker_regex = re.compile(r"\d+:.+:/docker/pod([^/]+)/([0-9a-f]{64})")
other_regex = re.compile(r"\d+:.+:/docker/.*/pod([^/]+)/([0-9a-f]{64})")
other_regex2 = re.compile(r"\d+:.+:/kubepods/.*/pod([^/]+)/([0-9a-f]{64})")
other_regex3 = re.compile(
    r"\d+:.+:/kubepods\.slice/kubepods-[^/]+\.slice/kubepods-[^/]+-pod([^/]+)\.slice/docker-([0-9a-f]{64})"
)

app = typer.Typer()


# TODO: split to pod and python subcommands


class Process(BaseModel):
    pid: int
    exe: str
    cmdline: List[str]


class ProcessList(BaseModel):
    processes: List[Process]


def get_process_details(pid: int):
    # see https://man7.org/linux/man-pages/man7/cgroups.7.html
    try:
        path = "/proc/%d/cgroup" % (pid,)
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                match = (
                        kube_regex.match(line)
                        or docker_regex.match(line)
                        or other_regex.match(line)
                        or other_regex2.match(line)
                        or other_regex3.match(line)
                )
                if match is not None:
                    # pod, container
                    return match.group(1).replace("_", "-"), match.group(2)
    except Exception as e:
        print("exception:", e)
    return None, None


def get_pod_processes(pod_uid: str) -> ProcessList:
    processes = []
    for pid in psutil.pids():
        this_pod_uid, container_uid = get_process_details(pid)
        if this_pod_uid is not None and this_pod_uid.lower() == pod_uid.lower():
            proc = psutil.Process(pid)
            processes.append(Process(pid=pid, exe=proc.exe(), cmdline=proc.cmdline()))
    return ProcessList(processes=processes)

def get_pid_info(pid: int) -> Process:
    proc = psutil.Process(pid)
    return Process(pid=pid, exe=proc.exe(), cmdline=proc.cmdline())

def get_nspid(pid_in_ns: int, verbose: bool):
    cmd = f"cat /proc/{pid_in_ns}/status"
    status_output = run_command(cmd, verbose)
    nspid_regex = re.compile(r".+NSpid:\s+(?P<pid>.*?)\s+(?P<nspid>.*?)\s+", re.DOTALL)
    match = nspid_regex.match(status_output)
    if not match:
        raise Exception(f"No match found for pid {pid_in_ns}")
    return int(match.group("nspid"))



