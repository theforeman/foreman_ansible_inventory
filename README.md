foreman_ansible_inventory
=========================

This script can be used as an ansible dynamic inventory[1].
The connection parameters are set up via a configuration
file *foreman.ini* that resides in the same dir as the
inventory script.

The data returned from Foreman for each host is stored in a foreman
hash so they're available as *host_vars*.

The hostgroup of each host is created as ansible group with
a foreman prefix, all lowercase and problematic parameters removed. So
e.g. the foreman hostgroup

    myapp / webtier / datacenter1

would turn into the ansible group:

    foreman_myapp_webtier_datacenter1

Furthermore groups can be created on the fly using the
*group_patterns* variable in *foreman.ini* so that you can build up
hierarchies using parameters on the hostgroup.

Lets assume you have a host that is built using this nested hostgroup:

    myapp / webtier / datacenter1

and each of the hostgroups defines a parameters respectively:

    myapp: app_param = myapp
    webtier: tier_param = webtier
	datacenter1: dc_param = datacenter1

then *group_patterns* like:

    [ansible]
	group_patterns = ["{app_param}-{tier_param}-{dc_param}",
                      "{app_param}-{tier_param}",
                      "{app_param}"]

would put the host into the additional anisble groups:

    - myapp-webtier-datacenter1
    - myapp-webtier
    - myapp

by reursively resolving the hostgroups, getting the parameter keys and
values performing doing a Python *string.format()* like replacement on
it.

[1]: http://docs.ansible.com/intro_dynamic_inventory.html
