# check\_temp.py #
Another simple Nagios plugin to check the temperature with lm-sensors.
This one is written in Python and can be used to monitor any adapter the user
specifies with the -a option.

## Usage ##
    usage: check_temp.py [-h] -w N -c N -a string

    optional arguments:
        -h, --help  show this help message and exit
        -w N        warning temperature
        -c N        critical temperature
        -a string   the adapter to monitor (for example: acpitz-virtual-0)

## License ##
check\_temp.py is relased under GNU GPL.
