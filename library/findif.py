#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import os
import netaddr
import subprocess

def list_interfaces():
    '''Get a list of available network interfaces by looking at
    the contents of /sys/class/net.'''
    for name in os.listdir('/sys/class/net'):
        path = os.path.join('/sys/class/net', name)
        if not os.path.isdir(path):
            continue

        yield name

def get_addresses_for(name):
    '''Call "ip addr show <iface>" for the given interface name, and then
    parse ipv4 and ipv6 addresses out of the result.'''
    out = subprocess.check_output(['ip', 'addr', 'show', name])
    ipv6_addrs = []
    ipv4_addrs = []
    for line in out.splitlines():
        words = line.strip().split()
        if words[0] == "inet":
            ipv4_addrs.append(words[1].split('/')[0])
        elif words[0] == "inet6":
            ipv6_addrs.append(words[1].split('/')[0])

    return {'ipv6': ipv6_addrs, 'ipv4': ipv4_addrs}

def main():
    module = AnsibleModule(
        argument_spec=dict(
            address=dict(required=True),
        ),
        supports_check_mode=True,
    )

    target = module.params['address']

    if netaddr.valid_ipv6(target):
        is_ipv6 = True
    elif netaddr.valid_ipv4(target):
        is_ipv6 = False
    else:
        module.fail_json(msg='%s is not a valid ip address' % target)

    results = {}
    for iface in list_interfaces():
        addrs = get_addresses_for(iface)
        if (
                (is_ipv6 and target in addrs['ipv6']) or
                (not is_ipv6 and target in addrs['ipv4'])
        ):
            results['found'] = True
            results['interface'] = iface
            results['addresses'] = addrs
            break
    else:
        results['found'] = False


    module.exit_json(changed=False,
                     results=results)


if __name__ == '__main__':
    main()
