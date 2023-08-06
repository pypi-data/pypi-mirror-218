import re
from TheSilent.clear import clear

CYAN = "\033[1;36m"

# attempts to view source code of file
def source_code_viewer(file, keyword=""):
    clear()

    count = 0

    with open(file, "rb") as f:
        data = f.read()

    strings = re.findall("[\w\.]{4,}", data.decode(errors="ignore"))
    for string in strings:
        print(CYAN + string)

    print(CYAN + "\ndone")
