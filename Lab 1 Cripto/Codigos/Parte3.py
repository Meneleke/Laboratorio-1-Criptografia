from scapy.all import *
from termcolor import colored

# Function to extract the hidden character from the data payload
def extract_hidden_character(packet):
    if ICMP in packet and packet[ICMP].type == 8:
        data_payload = packet[Raw].load
        hidden_character = data_payload[8:9].decode('utf-8')
        return hidden_character
    return None

# Function to handle intercepted packets and collect characters
def packet_handler(packet):
    hidden_character = extract_hidden_character(packet)
    if hidden_character:
        intercepted_characters.append(hidden_character)

# Sniff ICMP packets and call the packet_handler for each packet
intercepted_characters = []

# Instruct the user to press "Ctrl+C" to stop the interception
print("Press Ctrl+C to stop intercepting...")

try:
    sniff(filter="icmp and icmp[0] == 8", prn=packet_handler)
except KeyboardInterrupt:
    pass

# Combine intercepted characters into a string
intercepted_string = ''.join(intercepted_characters)

# Perform Caesar cipher decryption and analyze likelihood
def caesar_cipher(text, shift):
    decrypted_text = ''
    for char in text:
        if char.isalpha():
            shift_amount = 3  # Common shift value for Caesar ciphers (Spanish/English)
            decrypted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

best_decryption = ''
best_score = 0

for shift in range(26):
    decrypted_message = caesar_cipher(intercepted_string, shift)
    
    # You can use language analysis tools to score the likelihood of a clear message
    # In this example, we'll simply count the number of common English and Spanish words
    common_words = ["the", "and", "que", "de", "el", "la", "en", "un"]
    score = sum(decrypted_message.lower().count(word) for word in common_words)
    
    if score > best_score:
        best_score = score
        best_decryption = decrypted_message

# Print all Caesar cipher decrypted messages and highlight the best one in green
for shift in range(26):
    decrypted_message = caesar_cipher(intercepted_string, shift)
    if decrypted_message == best_decryption:
        print(colored(decrypted_message, 'green'))
    else:
        print(decrypted_message)
