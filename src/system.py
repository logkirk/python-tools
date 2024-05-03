from datetime import datetime
from time import sleep

import psutil


def kill_process_by_name(proc_name, timeout=10):
    """Kills the specified process immediately.

    Args:
        proc_name (str): name of the process to kill
        timeout (int): max amount of time in seconds to wait for the process to be
            killed
    """
    start_time = datetime.now()
    while True:
        if (datetime.now() - start_time).total_seconds() > timeout:
            raise TimeoutError(
                'Timed out trying to kill process "{}".'.format(proc_name)
            )

        for proc in psutil.process_iter():
            if proc.name() == proc_name:
                proc.kill()

        # Wait a bit and make sure the process is killed
        sleep(0.1)
        if not is_process_running(proc_name):
            return


def is_process_running(proc_name):
    """Determines whether the given process is currently running.

    Args:
        proc_name (str): name of the process

    Returns:
        True if the process is running else False
    """
    for proc in psutil.process_iter():
        if proc.name() == proc_name:
            return True
    return False


def wait_for_process_closed(proc_name, timeout=10):
    """Waits for the process to be closed.

    Args:
        proc_name (str): process to wait for
        timeout (int): maximum seconds to wait

    Raises:
        TimeoutError if process is not closed before timeout
    """
    start_time = datetime.now()
    while is_process_running(proc_name):
        if (datetime.now() - start_time).total_seconds() > timeout:
            raise TimeoutError(
                "Timed out waiting for process '{}' to close.".format(proc_name)
            )
