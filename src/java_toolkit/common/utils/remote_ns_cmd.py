import subprocess
import typer


def run_command(cmd: str, verbose: bool):
    if verbose:
        typer.echo(f"Running {cmd}")
    output = subprocess.check_output(
        cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    if verbose:
        typer.echo(f"output recieved: \n{output.decode()}")
    return output.decode()

def run_cmd_in_proc_namespace(pid, command_to_run, verbose):
    NSENTER_CMD = "nsenter -t {} -p -m {}"
    nsenter_cmd_formatted = NSENTER_CMD.format(pid, command_to_run)
    return run_command(nsenter_cmd_formatted, verbose)