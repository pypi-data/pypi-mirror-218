#!/usr/bin/env python3

"""This module controls the interaction between the user and the model data/view
"""

# Add function to pull user agent info and log it

import os
import sys

from sou_meraki import model, view, misc

settings = misc.load_settings()
org_id = settings['DEFAULT_ORG_ID']
network_id = ''

misc.logger("INFO: Creating A New Instance of the Meraki Dashboard API")

dashboard = model.create_dashboard(settings['MERAKI'])
if dashboard == 401:
    view.display_error("API KEY not found")
    sys.exit()
elif dashboard == 503:
    view.display_error("Unable to connect. Check network and DNS settings")
    sys.exit()
else:
    misc.logger("INFO: A Meraki Dashboard API session has been establised")


def one():
    global org_id
    org_id, org_name = model.select_organization(dashboard)
    misc.logger('', 'console')
    misc.logger(f'INFO: Organization "{org_name}" ID {org_id} has been selected')
    input("Press Enter to Continue\n")
    view.clear_screen()


def two():
    global network_id
    network = model.select_network(dashboard, org_id)
    misc.logger('', 'console')
    misc.logger(f'INFO: Network "{network[1]}" ID "{network[0]}" has been selected')
    network_id = network[0]
    input("Press Enter to Continue\n")
    view.clear_screen()


def three():
    menu_dict = [
        {'function': three_one, 'description': 'Generate a report of all sites of type wireless'},
        {'function': three_two, 'description': 'Generate a report of all sites with a particular SSID'},
        {'function': three_three, 'description': 'Replace radius servers'},
        {'function': menu, 'description': 'Return to previous menu'},
        {'function': four, 'description': 'Exit'}
    ]
    menu_items = dict(enumerate(menu_dict, start=1))

    while True:
        view.display_menu(menu_items)
        selection = int(
            input("\nPlease enter your selection number: "))
        selected_value = menu_items[selection]
        selected_value['function']()


def three_one():
    model.get_network_list(dashboard, org_id, settings['WIRELESS_NETWORKS']['output_file'])
    input("Press Enter to Continue\n")
    view.clear_screen()


def three_two():
    networks = misc.get_networks_list(settings['WIRELESS_SSID']['input_file'])
    model.wheres_ssid(dashboard, networks, 
    settings['WIRELESS_SSID']['output_file'],settings['WIRELESS_SSID']['ssid'])
    input("Press Enter to Continue\n")
    view.clear_screen()


def three_three():
    networks = misc.get_networks_list(settings['RADIUS']['input_file'])
    radius, accounting = misc.format_radius()
    model.update_radius_servers(dashboard, networks, radius, accounting)
    input("Press Enter to Continue\n")
    view.clear_screen()


def four():
    view.clear_screen()
    print("Goodbye")
    sys.exit()

def menu():
    menu_dict = [
        {'function': one, 'description': 'Select an organization'},
        {'function': two, 'description': 'Select a network'},
        {'function': three, 'description': 'Wireless options'},
        {'function': four, 'description': 'Exit'}
    ]
    menu_items = dict(enumerate(menu_dict, start=1))
 
    while True:
        view.display_menu(menu_items)
        try:
            selection = int(input("\nPlease enter your selection number: "))
            if selection not in range(1,5):
                print('\nEntry not in range, please try again: ')
                input("Press Enter to Continue\n")
                continue
            else:
                selected_value = menu_items[selection]
                selected_value['function']()
        except ValueError:
            print('\nEntry needs to be an integer, please try again: ')
            input("Press Enter to Continue\n")
            continue
