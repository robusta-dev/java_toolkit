import subprocess
import typer


def run_command(cmd: str, verbose: bool):
    if verbose:
        typer.echo(f"Running {cmd}")
    proc = subprocess.Popen(
        cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    (output, err) = proc.communicate()

    proc.stdout.close()
    return_code = proc.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    if verbose:
        typer.echo(output)
    return output, err

def run_cmd_in_proc_namespace(pid, command_to_run, verbose):
    NSENTER_CMD = "nsenter -t {} -p -m {}"
    nsenter_cmd_formatted = NSENTER_CMD.format(pid, command_to_run)
    return run_command(nsenter_cmd_formatted, verbose)