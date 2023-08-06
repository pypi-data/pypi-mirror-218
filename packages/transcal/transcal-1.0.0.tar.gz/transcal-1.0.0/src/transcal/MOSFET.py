# The DC and AC Analysis of E-MOSFET Transistors

from .errors import *
from math import *

class MOSFETAnalysis:
   """ The DC and AC Analysis of E-MOSFET Transistors 
   
   This class provides common used E-MOSFET transistors configuration.
   The important point is that all transistors are 'npn' types. But, 
   can be derivated easily 'pnp' implementations. 
   
   ## Analysis type:
   ----------------
   + `'ac'` for alternative current
   + `'dc'` for direct current
   
   Another important point is that this class do not provide D-MOSFET
   analyzes. Because D-MOSFET analyzes are same JFET. So, in here, 
   you can find E-MOSFET anayzes only.

   ## Configuration type:
   ----------------------
   + drain-feedback config. (ac, dc)
   + voltage-divider config. (ac, dc)
   """

   # Determine the analyzes
   analyzes = ["ac", # alternative current
               "dc" # direct current
            ] 

   def __init__(self, 
                # 'analysis' argument represents type of analysis.
                analysis: str, 
                ) -> None:
      # Detemine the parameters.
      self.analysis = analysis
      # Check 'analysis' and 'mosfet' arguments.
      if self.analysis not in MOSFETAnalysis.analyzes:
         raise AnalysisError("Inconsistent analysis type")
      # Put in ac and dc results into these two directory.
      self.dcs = {}
      self.acs = {}

   def _save_dc_results_(self, k = None, Id = None, Vds = None, 
                         Vgs = None): 
      # Save results into dictionary.
      self.dcs["k (A/V^2)"], self.dcs["Id (A)"] = k, Id
      self.dcs["Vds (V)"], self.dcs["Vgs (V)"] = Vds, Vgs

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

   def drain_feedback(self, Vdd: float, Rg: float, Rd: float, 
                      Idon: float, Vgson: float, Vgsth: float, 
                      rd: float = None):
      """ The DC and AC Analysis of Drain-Feedback (Feedback-Biasing)
      `Vdd` represents drain voltage and must be in terms of 'V'. `Rg`
      , `Rd` preresent gate and drain resistances and must be in terms
      of 'ohm'. `Idon`, `Vgson`, `Vgsth` represent Id(on), Vgs(on), 
      Vgs(th) and must be in terms of 'A', 'V', 'V' in order. `rd` is
      required for 'ac' analysis and must be in terms of 'ohm'.
      
      ## Example 1
      >>> mosfet = MOSFETAnalysis("dc")
      >>> result = mosfet.drain_feedback(Vdd=12, Rg=1*1e+7, Rd=2000, 
                                         Idon=0.006, Vgson=8, Vgsth=3)
      >>> print(result)
      {'k': 0.00024, 
      'Id': 0.002794004340996671, 
      'Vds': 6.411991318006658, 
      'Vgs': 6.411991318006658}

      ## Example 2
      >>> mosfet = MOSFETAnalysis("ac")
      >>> result = mosfet.drain_feedback(Vdd=12, Rg=1e+7, Rd=2000, 
                                         Idon=0.006, Vgson=8, 
                                         Vgsth=3, rd=5*1e+4)
      >>> print(result)
      {'gm': 0.0016377558326431958, 
      'Zi': 2410374.668587459, 
      'Zo': 1922.7071716977505, 
      'Av': -3.1489248849128932, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """
      # Check parameters.
      if (self.analysis == "ac" and rd == None):
         error = "Parameters of drain feedback config. are conflict"
         raise DrainFeedbackError(error)
      # These variables are required for both analysis types.
      k = Idon / ((Vgson - Vgsth) * (Vgson - Vgsth))
      a = Rd * Rd * k
      b = 2 * k * Rd * (Vgsth - Vdd) - 1
      c = k * (Vgsth -Vdd) * (Vgsth - Vdd)
      # Can be used dicriminant for finding right 'Id'.
      Id = self._select_right_Id_(a, b, c) # drain current
      Vgs = Vdd - Id * Rd # gate-source voltage
      # DC analysis:
      if (self.analysis == "dc"):
         Vds = Vgs # drain-source voltage
         # Save the results.
         self._save_dc_results_(k, Id, Vds, Vgs)
      # AC analysis:
      if (self.analysis == "ac"):
         gm = 2 * k * (Vgs - Vgsth) # gm factor
         Zi1 = Rg + self._parallel_(rd, Rd)
         Zi2 = 1 + gm * self._parallel_(rd, Rd)
         Zi = Zi1 / Zi2; # input impedance
         # output impedance
         Zo = self._parallel_(Rg, self._parallel_(rd, Rd))
         Av = -1 * gm * Zo # voltage gain
         # Save the results.
         self._save_ac_results_(gm, Zi, Zo, Av, None, "Out of phase")
         
      return self.dcs if self.analysis == "dc" else self.acs

   def voltage_divider(self, Vdd: float, Rg1: float, Rg2: float, 
                       Rd: float, Rs: float, Idon: float, Vgson: float
                       , Vgsth: float, rd: float = None):
      """ The DC and AC Analysis of Voltage-Divider COnfiguration
      `Vdd` represent drain voltage source and must be in terms of
      'V'. `Rg1`, `Rg2`, `Rd`, `Rs` represent upper gate, lower 
      gate, drain, source resistances and must be in terms of 'ohm'.
      `Idon`, `Vgson`, `Vgsth` represent Id(on), Vgs(on), Vgs(th) and
      must be in terms of 'A', 'V', 'V' in order. `rd` is required 
      just for ac analysis.

      ## Example 1
      >>> mosfet = MOSFETAnalysis("dc")
      >>> result = mosfet.voltage_divider(Vdd=40, Rg1=22*1e+6, 
                                 Rg2=18*1e+6, Rd=3000, Rs=820, 
                                 Idon=0.003, Vgson=10, Vgsth=5)
      >>> print(result)
      {'k': 0.00012, 
      'Id': 0.006724565430189656, 
      'Vds': 14.312160056675516, 
      'Vgs': 12.485856347244482}

      ## Example 2
      >>> mosfet = MOSFETAnalysis("ac")
      >>> result = mosfet.voltage_divider(Vdd=24, Rg1=1e+7, 
                           Rg2=6.8*1e+6, Rd=2200, Rs=750, Idon=0.005, 
                           Vgson=6, Vgsth=3, rd=1e+6)
      >>> print(result)
      {'gm': 0.003321981658367837, 
      'Zi': 4047619.047619048, 
      'Zo': 2195.170624625823, 
      'Av': -7.292316551994853, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """
      # Check parameters.
      if (self.analysis == "ac" and rd == None):
         error = "Parameters of voltage-divider config. are conflict"
         raise VoltageDividerError(error)
      # These variables are required for both analysis types.
      k = Idon / ((Vgson - Vgsth) * (Vgson - Vgsth))
      Vg = Rg2 * Vdd / (Rg1 + Rg2) # gate voltage
      a = Rs * Rs * k
      b = -2 * k * Rs * (Vg - Vgsth) - 1
      c = k * (Vgsth - Vg) * (Vgsth - Vg)
      # Can be used dicriminant for finding right 'Id'.
      Id = self._select_right_Id_(a, b, c) # drain current
      Vgs = Vg - Id * Rs # gate-source voltage
      # DC analysis:
      if (self.analysis == "dc"):
         Vds = Vdd - Id * (Rd + Rs) # drain-source voltage
         # Save the results.
         self._save_dc_results_(k, Id, Vds, Vgs)
      # AC analysis:
      if (self.analysis == "ac"):
         gm = 2 * k * (Vgs - Vgsth) # gm factor
         Zi = self._parallel_(Rg1, Rg2) # input impedance
         Zo = self._parallel_(rd, Rd) # output impedance
         Av = -1 * gm * Zo # voltage gain
         # Save the results.
         self._save_ac_results_(gm, Zi, Zo, Av, None, "Out of phase")
         
      return self.dcs if self.analysis == "dc" else self.acs
