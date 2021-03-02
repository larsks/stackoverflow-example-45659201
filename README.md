This is just prototype of a module-based solution to [a stackoverflow
question](https://stackoverflow.com/questions/45659201/).  Given an ip
address, it returns information about the interface that owns that
address.

You would use it in a playbook like this:

```
- hosts: localhost
  tasks:
    - assert:
        that: target_address is defined
        msg: "You must defined 'target_address'"

    - findif:
        address: '{{ target_address }}'
      register: result

    - debug:
        var: result
```

Assuming the above is in `playbook.yml`, running `ansible-playbook`
like this:

```
ansible-playbook playbook.yml -e target_address=192.168.122.1
```

Might result in output like this (assuming your system has an
interface with address `192.168.122.1`):

```
TASK [findif] ******************************************************************
ok: [localhost]

TASK [debug] *******************************************************************
ok: [localhost] => {
    "result": {
        "changed": false,
        "results": {
            "addresses": {
                "ipv4": [
                    "192.168.122.1"
                ],
                "ipv6": []
            },
            "found": true,
            "interface": "virbr0"
        }
    }
}
```
