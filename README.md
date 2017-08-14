This is just prototype of a module-based solution to [a stackoverflow
question](https://stackoverflow.com/questions/45659201/).  Given an ip
address, it returns information about the interface that owns that
address.

You would use it like:

    ansible-playbook playbook.yml -e target_address=192.168.122.1

Assuming that your system has an interface with address
`192.168.122.1`, your output would look something like:

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

