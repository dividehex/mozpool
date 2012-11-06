# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import with_statement
import sys
from mozpool.bmm import relay

def relay_script():
    # Basic commandline interface for testing the relay module.
    def usage():
        print "Usage: %s [powercycle|status|turnon|turnoff] <hostname> <bank> <relay>" % sys.argv[0]
        sys.exit(1)
    if len(sys.argv) != 5:
        usage()
    cmd, hostname, bnk, rly = sys.argv[1:5]
    bnk, rly = int(bnk), int(rly)
    if cmd == 'powercycle':
        if relay.powercycle(hostname, bnk, rly, timeout=60):
            print "OK"
        else:
            print "FAILED"
            sys.exit(1)
    elif cmd == 'status':
        status = relay.get_status(hostname, bnk, rly, timeout=60)
        if status is None:
            print "FAILED"
            sys.exit(1)
        print "bank %d, relay %d status: %s" % (bnk, rly, 'on' if status else 'off')
    elif cmd == 'turnon' or cmd == 'turnoff':
        status = (cmd == 'turnon')
        if relay.set_status(hostname, bnk, rly, status, timeout=60):
            print "OK"
        else:
            print "FAILED"
            sys.exit(1)
    else:
        usage()
    sys.exit(0)
