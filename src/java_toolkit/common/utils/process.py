#!/usr/local/bin/python3
import re
from typing import List
from .remote_ns_cmd import run_cmd_in_proc_namespace

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

ps_regex = re.compile(r"\s*(?P<pid>.*?)\s+(?P<cmd>.*?)\s+(?P<cmd_args>.*?)$")

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

def get_ns_processes(pid_in_ns: int, verbose: bool):
    cmd = "ps -Ao pid,comm,args | grep -v PID"
    processes = run_cmd_in_proc_namespace(pid_in_ns, cmd, verbose)
    processes = processes.split('\n')
    return_proc_list=[]
    for proc_line in processes:
        if not proc_line:
            continue
        match = ps_regex.match(proc_line)
        if not match:
            continue
        pid = int(match.group("pid"))
        exe = match.group("cmd")
        cmdline = match.group("cmd_args")
        if cmdline is None:
            cmdline = []
        else:
            cmdline = cmdline.split(' ')
        return_proc_list.append(Process(pid=pid, exe=exe, cmdline=cmdline))
    return ProcessList(processes=return_proc_list)



