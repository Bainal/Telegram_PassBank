import os
import platform


def set_terminal_title(title):
    system = platform.system()
    if system == "Linux" or system == "Darwin":  # Linux и macOS
        print(f"\033]0;{title}\007", end="", flush=True)
    elif system == "Windows":
        os.system(f"title {title}")
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")
