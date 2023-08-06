import threading
from TheSilent.elf import *

def elf():
    import TheSilent.elf

if __name__ == "__main__":
    elf_thread = threading.Thread(target=elf).start()

