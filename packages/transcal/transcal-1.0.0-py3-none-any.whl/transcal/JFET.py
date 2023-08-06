# The DC and AC Analysis of JFET Transistors

from math import *
from .errors import *

class JFETAnalysis: 
   """ The DC and AC Analysis of JFET Transistors 
   
   This class provides common used JFET transistors configuration.
   The important point is that all transistors are 'npn' types. But, 
   can be derivated easily 'pnp' implementations. 
   
   ## Analysis type:
   ----------------
   + `'ac'` for alternative current
   + `'dc'` for direct current
   
   Another important point is that in AC analysis of transistors, 
   algorithms use 'JFET small-signal' transistor model. 
   These configuration:

   ## Configuration type:
   ----------------------
   + fixed-bias config. (ac, dc)
   + self-bias config. (ac, dc)
   + voltage-divider config. (ac, dc)
   + source-follower config. (ac)
   """   

   # Determine the analyzes.
   analyzes = ["ac", "dc"]              

   def __init__(self, 
                # 'anaysis' argument represents type of analysis.
                analysis: str) -> None:
      # Determine parameters of this class.
      self.analysis = analysis
      # Put in the ac and dc results in these two dictionary.
      self.dcs = {}
      self.acs = {}
      # Check 'analysis' and 'transistor' parameters.
      if self.analysis not in JFETAnalysis.analyzes:
         raise AnalysisError("Incosistent analysis type")

   def _save_dc_results_(self, Id = None, Vds = None, Vgs = None,
                         Vs = None, Vd = None, Vg = None): 
      # Save results into dictionary.
      self.dcs["Id (A)"], self.dcs["Vds (V)"] = Id, Vds
      self.dcs["Vgs (V)"], self.dcs["Vs (V)"] = Vgs, Vs
      self.dcs["Vd (V)"], self.dcs["Vg (V)"]  = Vd, Vg

   def _save_ac_results_(self, gm = None, Zi = None, Zo = None, 
                         Av = None, Ai = None, phase = None):
      # Save results into dictionary.
      self.acs["gm (S)"], self.acs["Zi (ohm)"] = gm, Zi
      self.acs["Zo (ohm)"], self.acs["Av"] = Zo, Av
      self.acs["Ai"], self.acs["Phase"] = Ai, phase

   def _select_right_Id_(self, a: float, b: float, c: float):
      # Fİnd dicriminant and calculate two different roots.
      dicriminant = b ** 2 - 4 * a * c
      root1 = (-b + sqrt(dicriminant)) / (2 * a)
      root2 = (-b - sqrt(dicriminant)) / (2 * a)
      # Specially, in some configuration, can be found two roots and
      # requires selecting one.
      if (root1 >= 0 and root2 < 0): return root1
      if (root2 >= 0 and root1 < 0): return root2
      if (root1 >= 0 and root2 >= 0):
         if root1 >= root2: return root2
         else: return root1

   def _find_gm_factor_(self, Idss: float, Vp: float, Vgs: float):
      # Fİnd transconductance factor (gm).
      return 2 * Idss / abs(Vp) * (1 - Vgs / Vp)
   
   def _parallel_(self, R1: float, R2: float):
      # Fİnd resultant resistance for two parallel resistances.
      return 1 / (1/R1 + 1/R2)
   
   def fixed_bias(self, Vdd: float, Vgg: float, Rd: float, Idss: float,
                  Vp: float, Rg: float = None, rd: float = None):
      """ The DC and AC analysis of fixed-bias configuration.
      `Vdd` and `Vgg` represent drain and gate voltage source and 
      must be in terms of 'volt'. `Rd`, `Rg` represent drain and gate 
      resistance and must ne in terms of 'ohm'. `Idss`, `Vp` and `yos`
      are constants and must be in terms of 'A', 'V' and 'ohm' in 
      order. `Rg` and `rd` are required for 'ac' analysis.

      ## Example 1
      >>> jfet = JFETAnalysis("dc")
      >>> result = jfet.fixed_bias(Vdd=16, Vgg=2, Rd=2000, 
                                   Idss=0.01, Vp=-8)
      >>> print(result)
      {'Id': 0.005625, 
      'Vds': 4.75, 
      'Vgs': -2, 
      'Vs': 0, 
      'Vd': -2, 
      'Vg': -2}

      ## Example 2
      >>> jfet = JFETAnalysis("ac")
      >>> result = jfet.fixed_bias(Vdd=16, Vgg=2, Rd=2000, Idss=0.01,
                                   Vp=-8, Rg=1e+6, rd=25000)
      >>> print(result)
      {'gm': 0.001875, 
      'Zi': 1000000.0, 
      'Zo': 1851.8518518518517, 
      'Av': -3.472222222222222, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """
      # Check parameters.
      if (self.analysis == "ac" and Rg == None) or \
         (self.analysis == "ac" and rd == None):
         error = "Parameters of fixed-bias config. are conflict"
         raise FixedBiasError(error)
      # These variables are required for both analysis types.
      Vgs = -1 * Vgg # gate-source voltage
      # DC analysis:
      if (self.analysis == "dc"):
         Id = Idss * (1 - Vgs / Vp) * (1 - Vgs / Vp) # drain current
         Vds = Vdd - Id * Rd # drain-source voltage
         Vd = Vgs # drain voltage
         Vg = Vgs # gate voltage
         Vs = 0 # source voltage
         # Save the results.
         self._save_dc_results_(Id, Vds, Vgs, Vs, Vd, Vg)
      # AC analysis:
      if (self.analysis == "ac"):
         # Calculate the results.
         gm = self._find_gm_factor_(Idss, Vp, Vgs) # gm
         Zi = Rg # input impedance
         Zo = self._parallel_(Rd, rd) # output impedance
         Av = -1 * gm * Zo # voltage gain
         # Save the results.
         self._save_ac_results_(gm, Zi, Zo, Av, None, "Out of phase")
         
      return self.dcs if self.analysis == "dc" else self.acs
   
   def self_bias(self, Vdd: float, Rd: float, Rs: float, Idss: float,
                 Vp: float, Rg:float = None, rd: float = None):
      """ The AC and DC analysis of self-bias configuration. 
      `Vdd` represents drain voltage source and must be in terms of 
      'V'. `Rd`, `Rs`, `Rg` represent drain, source, gate resistances
      and must be in terms of 'ohm'. `Idss`, `Vp`, `yos` are constant
      and must be in terms of 'A', 'V', 'ohm' in order. `Rg` and `rd`
      are necassary just for 'ac' analysis.

      ## Example 1
      >>> jfet = JFETAnalysis("dc")
      >>> result = jfet.self_bias(Vdd=20, Rd=3300, Rs=1000, 
                                  Idss=0.008, Vp=-6)
      >>> print(result)
      {'Id': 0.002587624173546938, 
      'Vds': 8.873216053748168, 
      'Vgs': -2.5876241735469376, 
      'Vs': 2.5876241735469376, 
      'Vd': 11.460840227295105, 
      'Vg': 0}

      ## Example 2
      >>> jfet = JFETAnalysis("ac")
      >>> result = jfet.self_bias(Vdd=20, Rd=3300, Rs=1000, Vp=-6,
                                  Idss=0.008, Rg=1e+6, rd=50000)
      >>> print(result)
      {'gm': 0.0015166114784235833,
      'Zi': 1000000.0, 
      'Zo': 3216.3148238584104, 
      'Av': -1.9229984653065741, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """
      # Check parameters.
      if (self.analysis == "ac" and Rg == None) or \
         (self.analysis == "ac" and rd == None):
         error = "Parameters of self-bias config. are conflict"
         raise SelfBiasError(error)
      # These variables are required for both analysis types.
      a = Rs * Rs * Idss / Vp / Vp
      b = Idss * 2 * Rs / Vp - 1
      c = Idss
      # For quadritic equations, find discriminant.
      Id = self._select_right_Id_(a, b, c) # drain current
      Vgs = -1 * Id * Rs # gate-source voltage
      # DC analysis:
      if (self.analysis == "dc"):
         # Calculate the results.
         Vds = Vdd - Id * (Rs + Rd) # drain-source voltage
         Vs = Id * Rs # source voltage
         Vg = 0 # gate voltage
         Vd = Vds + Vs # drain voltage
         # Save the results.
         self._save_dc_results_(Id, Vds, Vgs, Vs, Vd, Vg)
      # AC analysis:
      if (self.analysis == "ac"):
         # Calculate the results.
         gm = self._find_gm_factor_(Idss, Vp, Vgs) # gm
         Zi = Rg # input impedance
         Zo1 = 1 + gm * Rs + Rs / rd
         Zo2 = 1 + gm * Rs + Rs / rd + Rd / rd
         Zo = Zo1 * Rd / Zo2 # output impedance
         Av1 = gm * Rd
         Av2 = 1 + gm * Rs + (Rd + Rs) / rd
         Av = -1 * Av1 / Av2 # voltage gain
         # Save the results.
         self._save_ac_results_(gm, Zi, Zo, Av, None, "Out of phase")
         
      return self.dcs if self.analysis == "dc" else self.acs  

   def voltage_divider(self, Vdd: float, Rg1: float, Rg2: float,     
                       Rd: float, Rs: float, Idss: float, 
                       Vp: float, rd: float = None):
      """ The DC and AC analysis of voltage-divider configuration.
      `Vdd` represent drain voltage source and must be in terms of
      'V'. `Rg1`, `Rg2`, `Rd`, `Rs` represent upper gate, lower 
      gate, drain, source resistances and must be in terms of 'ohm'.
      `Idss`, `Vp`, `rd` are constants and must be in terms of 'A', 
      'V', 'ohm' in order. `rd` is just necessary for ac analysis.

      ## Example 1
      >>> jfet = JFETAnalysis("dc")
      >>> result = jfet.voltage_divider(Vdd=16, Rg1=21*1e+5, 
                                        Rg2=27*1e+4, Rd=2400, Rs=1500, 
                                        Idss=0.008, Vp=-4)
      >>> print(result)
      {'Id': 0.0024163088350844407, 
      'Vds': 6.5763955431706815, 
      'Vgs': -1.8016784425000787, 
      'Vs': 3.624463252626661, 
      'Vd': 10.200858795797341, 
      'Vg': 1.8227848101265822}

      ## Example 2
      >>> jfet = JFETAnalysis("ac")
      >>> result = jfet.voltage_divider(Vdd=20, Rg1=82*1e+6, 
                                        Rg2=11*1e+6, Rd=2000, Rs=610, 
                                        Idss=0.012, Vp=-3, rd=5*1e+5)
      >>> print(result)
      {'gm': 0.00540336289667699, 
      'Zi': 9698924.731182795, 
      'Zo': 1992.0318725099598, 
      'Av': -10.763671108918304, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """       
      # Check parameters.
      if (self.analysis == "ac" and rd == None):
         error = "Parameters of voltage-divider config. are conflict"
         raise SelfBiasError(error)
      # These variables are required for both analysis types.
      Vg = (Rg2 * Vdd) / (Rg1 + Rg2) # gate voltage
      a = Rs * Rs * Idss / Vp / Vp
      b1 = (2 * Rs * Idss / Vp)
      b2 = (2 * Vg * Rs * Idss / Vp / Vp)
      b = b1 - b2 - 1
      c = Idss * (1 - 2 * Vg / Vp + Vg * Vg / Vp / Vp)
      # For quadritic equations, find discriminant.
      Id = self._select_right_Id_(a, b, c) # drain current
      Vgs = Vg - Id * Rs # gate-source voltage
      if (self.analysis == "dc"):
         # Calculate the results.
         Vds = Vdd - Id * (Rs + Rd) # drain-source voltage
         Vs = Id * Rs # source voltage
         Vd = Vdd - Id * Rd # drain voltage
         # Save the results.
         self._save_dc_results_(Id, Vds, Vgs, Vs, Vd, Vg)
      # AC analysis:
      if (self.analysis == "ac"):
         # Calculate the results.
         gm = self._find_gm_factor_(Idss, Vp, Vgs) # gm
         Zi = self._parallel_(Rg1, Rg2) # input impedance
         Zo = self._parallel_(Rd, rd) # output impedance
         Av = -1 * gm * Zo # voltage gain
         # Save the results.
         self._save_ac_results_(gm, Zi, Zo, Av, None, "Out of phase")
         
      return self.dcs if self.analysis == "dc" else self.acs  
   
   def common_gate(self, Vdd: float, Vss: float, Rd: float, Rs: float, 
                   Idss: float, Vp: float, rd: float = None):
      """ The DC and AC analysis of common-gate configuration.
      `Vdd`, `Vss` represent drain and source voltage and must be in 
      terms of 'V'. `Rd`, `Rs` represent drain and source resistances
      and must be in terms of 'ohm'. `Idss`, `Vp`, `rd` are constants
      and must be in terms of 'A', 'V', 'ohm' in order. `rd` is just
      used for ac analysis.

      ## Example 1
      >>> jfet = JFETAnalysis("dc")
      >>> result = jfet.common_gate(Vdd=12, Vss=0, Rd=1500, Rs=680, 
                                    Idss=0.012, Vp=-6)
      >>> print(result)
      {'Id': 0.003835265436559567, 
      'Vds': 3.6391213483001437, 
      'Vgs': -2.6079804968605056, 
      'Vs': 2.6079804968605056, 
      'Vd': 6.247101845160649, 
      'Vg': 0}

      ## Example 2
      >>> jfet = JFETAnalysis("ac")
      >>> result = jfet.common_gate(Vdd=15, Vss=0, Rd=3300, Rs=1500, 
                                    Idss=0.008, Vp=-2.8, rd=4*1e+4)
      >>> print(result)
      {'gm': 0.002172962193500108, 
      'Zi': 370.7663034739852, 
      'Zo': 3048.498845265589, 
      'Av': 6.700485208822499, 
      'Ai': None, 
      'Phase': 'In phase'}
      """
      # Check parameters.
      if (self.analysis == "ac" and rd == None):
         raise CommonGateError(
            "Parameters of common-gate config. are conflict"
         )
      # These variables are required for both analysis types.
      a = (Rs * Rs) * Idss / (Vp * Vp) 
      b1 = 2 * Rs * Idss / Vp
      b2 = -2 * Vss * Rs * Idss / Vp / Vp
      b = b1 + b2 - 1
      c = (1 - (2 * Vss / Vp) + (Vss * Vss / Vp / Vp)) * Idss
      # For quadritic equations, find discriminant.
      Id = self._select_right_Id_(a, b, c) # drain current
      Vgs = Vss - Id * Rs # gate-source voltage
      if (self.analysis == "dc"):
         # Calculate the results.
         Vds = Vdd + Vss - Id * (Rs + Rd) # drain-source voltage
         Vs = -Vss + Id * Rs # source voltage
         Vd = Vdd - Id * Rd # drain voltage
         Vg = 0 # gate voltage
         # Save the results.
         self._save_dc_results_(Id, Vds, Vgs, Vs, Vd, Vg)
      # AC analysis:
      if (self.analysis == "ac"):
         # Calculate the results.
         gm = self._find_gm_factor_(Idss, Vp, Vgs) # gm
         Zi1 = (rd + Rd) / (1 + gm * rd)
         Zi = self._parallel_(Rs, Zi1) # input impedance
         Zo = self._parallel_(Rd, rd) # output impedance
         Av1 = gm * Rd + Rd / rd
         Av2 = 1 + Rd / rd
         Av = Av1 / Av2 # voltage gain
         # Save the results.
         self._save_ac_results_(gm, Zi, Zo, Av, None, "In phase")
         
      return self.dcs if self.analysis == "dc" else self.acs 
   
   def source_follower(self, Vdd: float, Vgs: float, Rg: float, 
                       Rs: float, Idss: float, Vp: float, rd: float):
      """ The AC analysis of source-follower configuration. 
      `Vdd`, `Vgs` represent drain, gate-source voltage and must be
      in terms in 'V'. `Rg`, `Rs` represent gate, source resistances
      and must be in terms of 'ohm'. `Idss`, `Vp`, `rd` are constants
      and must be in terms of 'A', 'V', 'ohm' in order. `rd` is just
      used for ac analysis.
      
      ## Example 1
      >>> jfet = JFETAnalysis("ac")
      >>> result = jfet.source_follower(Vdd=9, Vgs=-2.86, Rg=1e+6, 
                                        Rs=2200, Idss=0.016, 
                                        Vp=-4, rd=4*1e+4)
      >>> print(result)
      {'gm': 0.0022800000000000003, 
      'Zi': 1000000.0, 
      'Zo': 362.37852083676495, 
      'Av': 0.8262230275078242, 
      'Ai': None, 
      'Phase': 'In phase'}
      """
      # DC analysis:
      if (self.analysis == "dc"):
         raise MissingTransistorAnalysisError(
            "transistor do not support dc analysis"
         )
      # AC analysis:
      if (self.analysis == "ac"):
         # Calculate the results.
         gm = self._find_gm_factor_(Idss, Vp, Vgs) # gm
         Zi = Rg # input impedance
         # output impedance
         Zo = self._parallel_(rd, self._parallel_(Rs, 1/gm))
         Av1 = gm * self._parallel_(rd, Rs)
         Av = Av1 / (1 + Av1) # voltage gain
         # Save the results.
         self._save_ac_results_(gm, Zi, Zo, Av, None, "In phase")
         
      return self.dcs if self.analysis == "dc" else self.acs 

