""" 'transcal' Transistor Calculations with Python

Transistors are so important electronic components. I has range 
usage area. A analysis of transistor requires a lot of calculation. 
For example, in dc analysis, base, collect or emiiter currents, 
voltages between terminals can be more complex and confusing for 
beginning. So, I've written the most used transistors type 
(self-bias, voltage-divider, common-gate etc) analyzes in dc and
ac states.

Resource: Electronic Devices and Circuit Theory by Robert L. 
BOYLESTAD and Louis NASHELSKY
"""

__author__ = "Can Gulmez (ahmetcangulmez02@gmail.com)"
__version__ = "1.0.0"
__licence__ = "MIT License"

from .BJT import BJTAnalysis
from .BJT import two_port_system
from .BJT import cascaded
from .JFET import JFETAnalysis
from .MOSFET import MOSFETAnalysis

