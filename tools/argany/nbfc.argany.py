#!/usr/bin/python3

import sys, argparse, importlib
from argany import *
sys.path.append('.')
sys.path.append('..')
sys.path.append('../..')
sys.path.append('../../..')
sys.path.append('../../../..')
module = importlib.import_module('nbfc')
argp = getattr(module, 'argp')
#from nbfc import argp


PROLOG = '''\
NBFC\_SERVICE 1 "MARCH 2021" Notebook FanControl
================================================

NAME
----

nbfc\_service - Notebook FanControl service

'''

EPILOG = '''
FILES
-----

*/var/run/nbfc_service.pid*
  File containing the PID of current running nbfc\_service.

*/var/run/nbfc_service.state.json*
  State file of nbfc\_service. Updated every *EcPollInterval* miliseconds See nbfc\_service.json(5) for further details.

*/etc/nbfc/nbfc.json*
  The system wide configuration file. See nbfc\_service.json(5) for further details.

*/etc/nbfc/configs/\*.json*
  Configuration files for various notebook models. See nbfc\_service.json(5) for further details.

BUGS
----

Bugs to https://github.com/braph/nbfc-dev

AUTHOR
------

Benjamin Abendroth (braph93@gmx.de)

SEE ALSO
--------

nbfc_service(1), nbfc\_service.json(5), ec_probe(1), fancontrol(1)'''

if __name__ == '__main__':
    p = Parser.from_ArgumentParser(argp)

    if sys.argv[1] == 'markdown':
        print(PROLOG)
        print(generate_markdown(p))
        print(EPILOG)
