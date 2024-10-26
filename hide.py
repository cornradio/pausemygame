import ctypes
from ctypes import wintypes

# 定义 Windows API 函数和常量
user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.py_object), ctypes.py_object]
EnumWindows.restype = wintypes.BOOL

GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
GetWindowThreadProcessId.restype = wintypes.DWORD

OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
OpenProcess.restype = wintypes.HANDLE

QueryFullProcessImageName = kernel32.QueryFullProcessImageNameW
QueryFullProcessImageName.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
QueryFullProcessImageName.restype = wintypes.BOOL

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL

ShowWindow = user32.ShowWindow
ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
ShowWindow.restype = wintypes.BOOL

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
SW_MINIMIZE = 6
SW_RESTORE = 9
SW_SHOW = 5
SW_SHOWDEFAULT = 10

def get_window_by_exe(exe_name):
    """获取指定 exe 名称的窗口句柄和 PID"""
    def callback(hwnd, handles):
        pid = wintypes.DWORD()
        GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        # 打开进程以获取进程名
        process_handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid.value)
        if process_handle:
            image_name = (ctypes.c_wchar * 260)()
            size = wintypes.DWORD(260)
            if QueryFullProcessImageName(process_handle, 0, image_name, ctypes.byref(size)):
                # 检查文件名是否匹配
                if image_name.value.split("\\")[-1].lower() == exe_name.lower():
                    CloseHandle(process_handle)
                    handles.append((hwnd, pid.value))
                    return False  # 找到后停止枚举
            CloseHandle(process_handle)
        return True  # 继续枚举

    handles = []
    EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.py_object)(callback), handles)
    return handles[0] if handles else None

def hide_by_exe(exe_name):
    """最小化指定 exe 名称的窗口"""
    handle_info = get_window_by_exe(exe_name)
    if handle_info:
        hwnd, _ = handle_info
        ShowWindow(hwnd, SW_MINIMIZE)
        print(f"Window of '{exe_name}' minimized successfully.")
    else:
        print(f"No window for process '{exe_name}' found.")

def pop_by_exe(exe_name): # pop函数仍然不可用 , 效果没有
    """还原指定 exe 名称的窗口"""
    handle_info = get_window_by_exe(exe_name)
    if handle_info:
        hwnd, _ = handle_info
        # 尝试使用 SW_RESTORE、SW_SHOW、SW_SHOWDEFAULT 等组合
        ShowWindow(hwnd, SW_RESTORE)
        ShowWindow(hwnd, SW_SHOW)
        ShowWindow(hwnd, SW_SHOWDEFAULT)
        print(f"Window of '{exe_name}' restored successfully.")
    else:
        print(f"No window for process '{exe_name}' found.")


# 测试函数
# if __name__ == "__main__":
    # 示例：最小化 GitHubDesktop.exe 窗口
    # hide_by_exe("GitHubDesktop.exe")
    # 示例：还原 GitHubDesktop.exe 窗口
    # pop_by_exe("GitHubDesktop.exe")
