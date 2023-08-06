#!/usr/bin/env python3

"""This module handles the interface between the controller and the Meraki Dashboard
"""

import os
import sys

import meraki

from sou_meraki import misc


def create_dashboard(settings):
    misc.logger('DEBUG: Function "create_dashboard" has been called', 'file')
    """Instantiate an instance of the Meraki dashboard

    Args:
        settings (dict): A dictionary pulled from the settings.toml file

    Returns:
        dashboard object
    """

    # Make sure API KEY is available
    if settings['API_KEY']:
        api_key = settings['API_KEY']
    elif settings['API_KEY_ENVIRONMENT_VARIABLE'] in os.environ:
        api_key = os.environ.get(settings['API_KEY_ENVIRONMENT_VARIABLE'])
    else:
        return 401

    # Instantiate an instance of the Meraki dashboard
    dashboard = meraki.DashboardAPI(
            api_key=api_key,
            output_log=settings['OUTPUT_LOG'], 
            print_console=settings['PRINT_TO_CONSOLE'], 
            suppress_logging=settings['SUPPRESS_LOGGING'],
            log_file_prefix=settings['LOG_FILE_PREFIX'],
            log_path=settings['LOG_PATH']
        )

    # Run test to make sure dashboard is initialized
    try:
        dashboard.organizations.getOrganizations()
    except meraki.exceptions.APIKeyError:
        return 401
    except meraki.exceptions.APIError:
        return 503
    else:
        return dashboard


def select_organization(dashboard):
    misc.logger('DEBUG: Function "select_organization" has been called', 'file')
    """Lists all organizations and prompts the user to select one

    Args:
        dashboard (obj): The Meraki dashboard instance

    Returns:
        str: the selected organization ID
        str: the selected organization name
    """
    try:
        organizations = dashboard.organizations.getOrganizations()
    except meraki.exceptions.APIError:
        sys.exit("Check network connection and/or DNS settings.")
    organizations.sort(key=lambda x: x["name"])
    counter = 0
    print("\nSelect organization:")
    for organization in organizations:
        name = organization["name"]
        print(f"{counter} - {name}")
        counter += 1
    selected = misc.validate_integer_in_range(counter)
    return (
        organizations[int(selected)]["id"],
        organizations[int(selected)]["name"]
    )


def select_network(dashboard, org, lines_to_display=25):
    misc.logger('DEBUG: Function "select_network" has been called', 'file')
    """Lists the organization networks and prompts user to select one

    Args:
        dashboard (obj): The Meraki dashboard instance
        org (str): The selected organization ID
        lines_to_display (int): The number of lines before pausing

    Returns:
        list: the selected network ID and network name
    """

    networks = dashboard.organizations.getOrganizationNetworks(org)
    # Prompt search for network name to filter for shorter list.
    search_name = input(
        "Enter search string or leave blank for all networks: "
    )
    net_list = []
    while not net_list:
        if search_name == "":
            # Return all networks for blank search string.
            net_list = networks
        else:
            # Return networks matching search_name.
            for net in networks:
                if search_name.lower() in net["name"].lower():
                    net_list.append(net)
        # Validate at least 1 network is returned and prompt for new search
        # string if empty.
        if net_list == []:
            print(f"No networks found matching {search_name}.")
            search_name = input(
                "Enter search string or leave blank for all networks: "
            )
    net_list.sort(key=lambda x: x["name"])
    counter = 0
    print("\nNetworks:")
    for net in net_list:
        net_name = net["name"]
        print(f"{counter} - {net_name}")
        counter += 1
        if counter % lines_to_display == 0:
            user_response = input(
                "\nPress Enter to continue, or q + Enter to quit search: "
            )
            if "q" in user_response:
                break
    selected = misc.validate_integer_in_range(counter)
    return ([net_list[int(selected)]["id"], net_list[int(selected)]["name"]])


def get_network_list(dashboard, organization_id, filepath):
    misc.logger('DEBUG: Function "get_network_list" has been called', 'file')
    response = dashboard.organizations.getOrganizationNetworks(
    organization_id, total_pages='all')
    wireless_count = 0
    no_wireless = 0
    wireless = []
    for network in response:
        if 'wireless' in network['productTypes']:
            write_info = (network['id'] + ',' + network['name']) + '\n'
            wireless.append(write_info)
            wireless_count += 1
        else:
            no_wireless += 1
    misc.writelines_to_file(filepath, wireless)
    misc.logger('', 'console')
    misc.logger(f"INFO: There are {wireless_count} sites with some type of wireless device")
    misc.logger(f"INFO: There were {no_wireless} sites with no wireless")
    misc.logger(f'INFO: Network IDs and names were written to {filepath}')


def get_ssids(dashboard, network_id):
    misc.logger('DEBUG: Function "get_ssids" has been called', 'file')
    response = dashboard.wireless.getNetworkWirelessSsids(network_id)
    return response


def wheres_ssid(dashboard, networks, write_path, search_ssid):
    misc.logger('DEBUG: Function "wheres_ssid" has been called', 'file')
    found_count = not_found_count = 0 
    ssid_sites = []
    for network in networks:
        site = network.split(',')
        site_id = site[0]
        site_name = site[1].strip('\n')
        ssids = get_ssids(dashboard, site_id)
        found_ssid = False
        for ssid in ssids:
            if ssid['name'] == search_ssid:
                found_ssid = True
                newline = f"{site_id},{site_name},{ssid['name']},{ssid['number']}\n"
                ssid_sites.append(newline)
                misc.logger(f'INFO: Found SSID {search_ssid} for "{site_name}"')
                found_count += 1
        if not found_ssid:
            misc.logger(f'INFO: SSID {search_ssid} was not found for "{site_name}"')
            not_found_count += 1
    misc.writelines_to_file(write_path, ssid_sites)
    misc.logger(f"INFO: Sites with SSID {search_ssid}, found {found_count}")
    misc.logger(f"INFO: Sites without SSID {search_ssid}, found {not_found_count}")


def update_radius_servers(dashboard, networks, radius, accounting):
    misc.logger('DEBUG: Function "update_radius_servers" has been called', 'file')
    counter = 0
    for network in networks:
        site = network.split(',')
        net_id = site[0]
        net_name = site[1]
        ssid_num = site[3].strip('\n')
        misc.logger(f'INFO: Updating radius settings for {net_name} and SSID number {ssid_num}')
        dashboard.wireless.updateNetworkWirelessSsid(
            networkId=net_id,
            number=ssid_num, 
            radiusServers=radius,
            radiusAccountingServers=accounting
        )
        counter += 1
    misc.logger(f'INFO: Updated radius settings on {counter} SSIDs')

