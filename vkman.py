#!/opt/venvs/yubikey-manager/bin/python
"""Wrapper script to use the Yubikey Manager CLI utility with a Vivokey applet

NOTE: Yubico's bundled Python3 interpreter must be used in the hashbang above,
      as it includes the correct search path to the Yubico modules.

Usage examples:

./vkman.py -r 0 info
./vkman.py -r ACR122U oath accounts list
./vkman.py -r identiv oath accounts code
./vkman.py -r utrust oath accounts code GitHub:
"""

### Modules
import sys
from enum import Enum



# Import the bit we want to stick the Vivokey AID in ahead of time and fix it up
import yubikit.core

class VivokeyFixedUpAID(bytes, Enum):
  OTP = yubikit.core.AID.OTP.value
  MANAGEMENT = yubikit.core.AID.MANAGEMENT.value
  OPENPGP = yubikit.core.AID.OPENPGP.value
  OATH = bytes.fromhex("a0000007470061fc54d5")
  PIV = yubikit.core.AID.PIV.value
  FIDO = yubikit.core.AID.FIDO.value
  HSMAUTH = yubikit.core.AID.HSMAUTH.value

yubikit.core.AID = VivokeyFixedUpAID

# Remove the OATH reset command that's unsupported by the Vivokey applet
import ykman.cli.oath
del(ykman.cli.oath.oath.commands["reset"])

# Import the yubikey-manager's main
from ykman.cli.__main__ import *

# Only keep the commands supported by the Vivokey applet
cli.commands = {cmd: cli.commands[cmd] for cmd in ("info", "oath")}

# Make sure -r / --reader was passed, because apparently NFC won't work without
# an explicit reader
if not "-r" in sys.argv and not "--reader" in sys.argv:
  print('Please pass a reader name with -r or --reader', file = sys.stderr)
  print(file = sys.stderr)
  print('A case-insensitive partial match is sufficient, e.g. "utrust" for ',
	file = sys.stderr)
  print('"Identiv uTrust 3700 F CL Reader [uTrust 3700 F CL Reader] '
	'(55072290205) 00 00"', file = sys.stderr)
  print(file = sys.stderr)
  print('Use "pcsc_scan -r" to view the names of connected readers',
	file = sys.stderr)
  exit(-1)

# Run the fixed-up yubikey-manager
main()
