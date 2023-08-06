#!/usr/bin/env python3

""" A place to put functions and such that don't fit else where
"""

import datetime
from pathlib import Path
import sys

import tomlkit

def load_settings(dev=False):
    if dev:
        settings_path = 'input/settings-dev.toml'
    else:
        settings_path = 'input/settings.toml'
    settings_path = program_path / settings_path
    try:
        with open (settings_path, 'r') as tomldata:
            data = tomldata.read()
        settings = tomlkit.loads(data)
        return settings
    except FileNotFoundError:
        sys.exit('Could not open "sou_meraki/input/settings.toml"')


def load_file(filename):
    """Opens a file for reading and formats the network data

    Args:
        filename (str): The filename to be opened

    Returns:
        list: The data found in the file
    """

    results = []
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            data = file.readlines()
        for each in data:
            if each.startswith("L_"):
                rdata = each.rstrip()
                rdata = rdata.split(",")
                results.append(rdata)
        return results
    except FileNotFoundError:
        sys.exit(f"Could not find file {filename}")


def validate_integer_in_range(end_range):
    """Prompts user to select a number within a defined range

    Args:
        end_range (int): The upper bound number that can be selected

    Returns:
        int: The selected number
    """

    while True:
        try:
            selected = int(
                input(
                    "\nEnter the number next to the name you would like to "
                    "use: "
                )
            )
            assert selected in range(0, end_range)
        except ValueError:
            print("\tThat is not an integer!\n")
        except AssertionError:
            print(f"\n\tYou must enter a number between 0 and {end_range-1}")
        else:
            break
    return selected


def format_radius():
    radius = settings['RADIUSSERVERS']
    accounting = settings['RADIUSACCOUNTING']
    radius_port = radius['port']
    radius_secret = radius['secret']
    accounting_port = accounting['port']
    accounting_secret = accounting['secret']

    radius_payload = []
    accounting_payload = []

    # Format Radius settings
    for server in radius['servers']:
        temp = {'host':server, 'port':radius_port, 'secret':radius_secret}
        radius_payload.append(temp)
    # Format Radius Accounting settings
    for server in accounting['servers']:
        temp = {'host':server, 'port':accounting_port, 'secret':accounting_secret}
        accounting_payload.append(temp)

    return radius_payload, accounting_payload


def get_networks_list(location):
    filepath = program_path / location
    
    with open(filepath, 'r') as netdata:
        networks = netdata.readlines()
    return networks


def writelines_to_file(location, text):
    location = program_path / location
    try:
        with open(location, 'w') as file_data:
            file_data.writelines(text)
    except FileNotFoundError:
        sys.exit(f'Could not open {location}')


def write_to_file(location, text):
    location = program_path / location
    try:
        with open(location, 'a') as file_data:
            file_data.write(text)
    except FileNotFoundError:
        sys.exit(f'Could not open {location}')


def logger(msg, destination='both'):
    console = True
    file = True
    if 'console' in destination:
        file = False
    if 'file' in destination:
        console = False
    if log_level.upper() == 'INFO' and msg.startswith('DEBUG'):
        console = False
        file = False
    if console:
        print(msg)
    if file:
        time_stamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        log_entry = time_stamp + ' ' + msg + '\n'
        write_to_file(log_path, log_entry)




# Returns the full path where this script was run
program_path = Path(__file__).parent
settings = load_settings()

# Setup logging
log_level = settings['LOGGING']['log_level']
log_path = program_path / settings['LOGGING']['log_path']
logger("INFO: Initializing ...", 'file')
logger(__file__)