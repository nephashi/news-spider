import platform

def get_line_break():
    if platform.system() == "Windows":
        return '\r\n'
    elif platform.system() == "Linux":
        return '\n'
    else:
        return '\r'