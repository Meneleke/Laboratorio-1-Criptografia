import sys
from scapy.all import *
import random

# Ensure a command line argument is provided
if len(sys.argv) != 2:
    print("Usage: python icmp_sender.py <string>")
    sys.exit(1)

# Extract the string from the command line argument
input_string = sys.argv[1]

# Initialize sequence number, identifier, and IP ID
seq_num = 1
identifier = 1

# Send one packet per character in the string
for char in input_string:
    # Generate a random IP ID within the specified range
    ip_id = random.randint(0xe000, 0xefff)
    
    # Create the ICMP packet
    icmp_packet = IP(dst="8.8.8.8", id=ip_id) / ICMP(type=8, code=0, id=identifier, seq=seq_num)
    
    # Generate the timestamp in little-endian ("<Q") format
    timestamp = struct.pack("<Q", int(time.time()))
    
    # Create the data payload with 56 bytes (timestamp + character + padding)
    padding = bytes([0x00] * 7 + list(range(0x10, 0x38)))
    data_payload = timestamp + char.encode('utf-8') + padding
    
    # Set the ICMP data payload
    icmp_packet = icmp_packet / Raw(load=data_payload)
    
    # Calculate and set the correct ICMP checksum
    icmp_packet[ICMP].sum = 0
    
    icmp_packet.show()
    
    send(icmp_packet)
    
    # Increment the sequence number
    seq_num = (seq_num % 3) + 1
    
    # Increment the identifier after every 3 packets
    if seq_num == 1:
        identifier += 1
