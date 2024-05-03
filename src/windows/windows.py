import ctypes
import os
from datetime import datetime


class SYSTEMTIME(ctypes.Structure):
    """Struct for holding system time."""

    _fields_ = [
        ("wYear", ctypes.c_int16),
        ("wMonth", ctypes.c_int16),
        ("wDayOfWeek", ctypes.c_int16),
        ("wDay", ctypes.c_int16),
        ("wHour", ctypes.c_int16),
        ("wMinute", ctypes.c_int16),
        ("wSecond", ctypes.c_int16),
        ("wMilliseconds", ctypes.c_int16),
    ]


def get_current_time() -> datetime:
    """Gets the current system time from the kernel.

    Note: Have to use this method, since time in python for windows does not get
        updated during the running instance

    Returns: (datetime) current system time
    """
    system_time_format = "%d-%m-%Y %H:%M:%S"
    st = SYSTEMTIME()
    lpSystemTime = ctypes.pointer(st)
    ctypes.windll.kernel32.GetLocalTime(lpSystemTime)
    current_time = "{}-{}-{} {}:{}:{}".format(
        st.wDay, st.wMonth, st.wYear, st.wHour, st.wMinute, st.wSecond
    )
    current_time_obj = datetime.strptime(current_time, system_time_format)

    return current_time_obj


def change_time_zone(timezone: str):
    """Changes the timezone of the system.

    Args:
        timezone: name of the timezone to change to.
            For timezone names, refer to this:
            https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-vista/cc749073(v=ws.10)?redirectedfrom=MSDN
    """
    os.system('tzutil /s "{}"'.format(timezone))
    print("Timezone set to [{}]".format(timezone))
