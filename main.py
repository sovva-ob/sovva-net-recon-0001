import subprocess
import socket
import ipaddress

def ping_host(target):
    try:
        result = subprocess.run(["ping", "-n", "1", "-w", "250", target], capture_output=True)
    except OSError:
        print("error: unable to execute ping")
        return None    

    if result.returncode == 0:
        return True
    else:
        return False

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip, port))
    sock.close

    if result == 0:
        return True
    else:
        return False

# active_hosts = []

target_ip = input("enter target ip ")
try:
    ipaddress.IPv4Address(target_ip)
except ipaddress.AddressValueError:
    print("error: invalid ip address")
    exit()

try:
    start_port = int(input("enter starting port: "))
    port_range = int(input("enter upward range of ports to scan: "))
except ValueError:
    print("error: ports must be numbers")
    exit()


if start_port < 1 or start_port > 65535:
    print("error: invalid starting port")
    exit()

if port_range < 1 or start_port + port_range - 1 > 65535:
    print("error: invalid port range")
    exit()

reachable = ping_host(target_ip)

if reachable is True:
    print("target is reachable")
else:
    print("target is unreachable")

open_ports = []

for port in range(start_port, start_port + port_range):
    result = scan_port(target_ip, port)
    #print(port, result)

    if result is True:
        open_ports.append(port)

print("\nscan results: ")
if len(open_ports) == 0:
    print("no open ports found")
else:
    for port in open_ports:
        print(f"port {port}: OPEN")


print("total open ports:", len(open_ports))