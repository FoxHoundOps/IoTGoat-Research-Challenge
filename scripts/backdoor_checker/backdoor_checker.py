import sys
import xml.etree.ElementTree as ET
from pwn import *


def clear_data(sock):
    """
    Clear any existing data from the socket.

    Args:
        sock (pwnlib.tubes.remote.remote): The socket object.
    """
    while True:
        try:
            data = sock.recvline(timeout=0.1).decode().strip()
            if not data:
                break
        except:
            break


def check_backdoor(xml_file):
    """
    Check for potential backdoors on ports with unknown service names.

    Args:
        xml_file (str): Path to the XML file containing Nmap scan results.
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Iterate through each host and port in the XML file
    for host in root.findall('host'):
        address = host.find('address')
        if address is None:
            continue

        address = address.get('addr')
        for port in host.findall('ports/port'):
            portid = port.get('portid')
            state = port.find('state').get('state')
            service = port.find('service').get('name')

            # Check if the service is unknown and the port is open
            if service == 'unknown' and state == 'open':
                print(f'Checking port {portid} for potential backdoor...')

                try:
                    # Connect to the port using netcat with a shorter timeout
                    nc = remote(address, portid, timeout=2)
                    print(f'[DEBUG] Connected to {address}:{portid}')

                    # Clear any existing data from the socket
                    clear_data(nc)

                    # Issue the 'id' command
                    nc.sendline('id')
                    print(f'[DEBUG] Sent "id" command')

                    # Receive the response with a timeout
                    response = nc.recvline(timeout=2).decode().strip()
                    print(f'[DEBUG] Received response: {response}')

                    if 'uid=' in response:
                        print(f'Backdoor detected on port {portid}! Response: {response}')
                    else:
                        print(f'No backdoor detected on port {portid}')

                    nc.close()

                except Exception as e:
                    print(f'Error connecting to port {portid}: {str(e)}')


if __name__ == '__main__':
    # Check if the XML file path is provided as a command-line argument
    if len(sys.argv) != 2:
        print('Usage: python3 backdoor_checker.py <xml_file>')
        sys.exit(1)

    xml_file = sys.argv[1]

    # Call the check_backdoor function with the provided XML file
    check_backdoor(xml_file)
