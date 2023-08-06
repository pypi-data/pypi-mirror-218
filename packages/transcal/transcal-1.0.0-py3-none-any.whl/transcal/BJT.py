# The DC and AC Analysis of BJT Transistors

from .errors import *

class BJTAnalysis: 
   """ The DC and AC Analysis of BJT Transistors 
   
   This class provides common used BJT transistors configuration.
   The important point is that all transistors are 'npn' types. But, 
   can be derivated easily 'pnp' implementations. 
   
   ## Analysis type:
   ----------------
   + `'ac'` for alternative current
   + `'dc'` for direct current
   
   Another important point is that in AC analysis of transistors, 
   algorithms use 're' transistor model. These configuration:

   ## Configuration type:
   ----------------------
   + fixed-bias config. (ac, dc)
   + emitter-bias config. (ac, dc)
   + voltage-divider config. (ac, dc)
   + collector-feedback config. (ac, dc)
   + collector-dc-feedback config. (ac)
   + emitter-follower config. (ac, dc)
   + common-base config. (ac, dc)
   + miscellaneous-bias config. (dc)
   """   

   # Determine the analyzes.
   analyzes = ["ac", "dc"]              

   def __init__(self, 
                # 'analysis' argument represents type of analysis.
                analysis: str, 
                # 'Vbe' argument represents base-emitter voltage.
                Vbe: float = 0.7) -> None:
      # Determine parameters of this class.
      self.analysis = analysis
      self.Vbe = Vbe
      # Put in the ac and dc results in these two dictionary.
      self.dcs = {}
      self.acs = {}
      # Check 'analysis' and 'transistor' parameters.
      if self.analysis not in BJTAnalysis.analyzes:
         raise AnalysisError("Incosistent analysis type")

   def _save_dc_results_(self, Ib = None, Ic = None, Ie = None, 
                         Icsat = None, Vce = None, Vc = None, 
                         Ve = None, Vb = None, Vbc = None): 
      # Save results into dictionary.
      self.dcs["Ib (A)"], self.dcs["Ic (A)"] = Ib, Ic
      self.dcs["Ie (A)"], self.dcs["Icsat (A)"] = Ie, Icsat
      self.dcs["Vce (V)"], self.dcs["Vc (V)"] = Vce, Vc,
      self.dcs["Ve (V)"], self.dcs["Vb (V)"] = Ve, Vb
      self.dcs["Vbc (V)"], self.dcs["Vbe (V)"] = Vbc, self.Vbe

   def _save_ac_results_(self, re = None, Zi = None, Zo = None, 
                         Av = None, Ai = None, phase = None):
      # Save results into dictionary.
      self.acs["re (ohm)"], self.acs["Zi (ohm)"] = re, Zi
      self.acs["Zo (ohm)"], self.acs["Av"] = Zo, Av
      self.acs["Ai"], self.acs["Phase"] = Ai, phase

   def _Rth_(self, R1: float, R2: float):
      """ Rth is necassary for voltage-divider configuration. """
      return 1 / (1/R1 + 1/R2)
   
   def _Eth_(self, Vcc: float, R1: float, R2:float):
      """ Eth is necassary for voltage-divider configuration. """
      return Vcc * (R2 / (R1 + R2))
         
   def fixed_bias(self, Vcc: float, Rb: float, Rc:float, beta:float,
                  ro:float = None):
      """ The dc and ac analysis of fixed-bias configuration. 
      `Vcc` represents main voltage source and must be in terms of 
      'V'. `Rb` and `Rc` represents base and collector resistance 
      and must be in terms of 'ohm'. `beta` represents the ration of 
      collector current to base currant and is unitless. `ro` is 
      constant and just use it for ac analysis.

      ## Example 1
      >>> bjt = BJTAnalysis(analysis="dc", Vbe=0.7)
      >>> result = bjt.fixed_bias(Vcc=12, Rb=240000, Rc=2200, beta=50)
      >>> print(result)
      {'Ib': 4.708333333333334e-05, 
       'Ic': 0.0023541666666666667, 
       'Ie': 0.00240125, 
       'Icsat': 0.005454545454545455, 
       'Vce': 6.820833333333333, 
       'Vc': 12, 
       'Ve': 0, 
       'Vb': 0.7, 
       'Vbc': -11.3, 
       'Vbe': 0.7}
      
      ## Example 2
      >>> bjt = BJTAnalysis(analysis="ac")
      >>> result = bjt.fixed_bias(Vcc=12, Rb=470000, Rc=3000, 
                                  beta=100, ro=50000)
      >>> print(result)
      {'re': 10.70708840795584, 
      'Zi': 1068.2751988810212, 
      'Zo': 2830.1886792452833, 
      'Av': -264.32850569743385, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """
      # Check parameters.
      if (self.analysis == "ac" and ro == None):
         error = "Parameters of fixed-bias config. are conflict"
         raise FixedBiasError(error)
      # Both ac and dc analysis requires these.
      Ib = (Vcc - self.Vbe) / Rb # base current 
      Ie = (beta + 1) * Ib # emitter current
      # DC analysis:
      if self.analysis == "dc":
         Ic = beta * Ib # collector current
         Icsat = Vcc / Rc # saturation (max) current
         Vce = Vcc - (Ic * Rc) # q-point of transistor
         Vc = Vcc # collector voltage
         Ve = 0 # emitter voltage
         Vb = self.Vbe # base voltage
         Vbc = Vb - Vc # base-collector voltage
         # Save results into 'dcs'.
         self._save_dc_results_(Ib, Ic, Ie, Icsat, Vce, Vc, 
                                Ve, Vb, Vbc)
      # AC anaysis:
      if self.analysis == "ac":
         re = 0.026 / Ie
         Zi = 1.0 / (1.0/Rb + 1.0/(beta * re)) # input impedance
         Zo = 1.0 / (1.0/Rc + 1.0/ro) # output impedance
         Av = -1 * (1.0 / (1.0/Rc + 1.0/ro)) / re # voltage gain
         # Save results into 'acs'.
         self._save_ac_results_(re, Zi, Zo, Av, None, "Out of phase")
      
      return self.dcs if self.analysis == "dc" else self.acs
         
   def emitter_bias(self, Vcc: float, Rb: float, Rc: float, 
                    Re: float, beta: float, ro: float = None):
      """ The dc and ac analysis of emitter-bias configuration.
      `Vcc` represents main voltage source and must be in terms of
      'V'. `Rb`, `Rc` and `Re` parameter represents base, collector
      and emitter resistance in order and must be in terms of 'ohm'.
      `beta` represents the ration of collector current to base 
      currant and is unitless. `ro` is constant and just use it for 
      ac analysis.

      ## Example 1
      >>> bjt = BJTAnalysis(analysis="dc")
      >>> result = bjt.emitter_bias(Vcc=20, Rb=430000, Rc=2000, 
                                    Re=1000, beta=50)
      >>> print(result)
      {'Ib': 4.0124740124740125e-05, 
      'Ic': 0.0020062370062370063, 
      'Ie': 0.0020463617463617463, 
      'Icsat': 0.006666666666666667, 
      'Vce': 13.98128898128898, 
      'Vc': 16.027650727650727, 
      'Ve': 2.0463617463617463, 
      'Vb': 2.746361746361746, 
      'Vbc': -13.28128898128898, 
      'Vbe': 0.7}

      ## Example 2
      >>> bjt = BJTAnalysis(analysis="ac")
      >>> result = bjt.emitter_bias(Vcc=20, Rb=470000, Rc=2200, 
                                    Re=560, beta=120, ro=40000)
      >>> print(result)
      {'re': 5.987136556331092, 
      'Zi': 56433.06551078378, 
      'Zo': 2197.743642604834, 
      'Av': -4.116990327530924, 
      'Ai': None, 
      'Phase': 'In phase'}
      """ 
      # Check parameters.
      if (self.analysis == "ac" and ro == None):
         error = "Parameters of emitter-bias config. are conflict"
         raise EmitterBiasError(error)
      # Both dc and ac analysis requires these two value.
      Ib = (Vcc - self.Vbe) / (Rb + (beta + 1) * Re) # base current
      Ie = (beta + 1) * Ib # emitter current
      # DC analysis:
      if self.analysis == "dc":
         Ic = beta * Ib # collector current
         Icsat = Vcc / (Rc + Re) # saturation (max) current
         Vce = Vcc - Ic * (Rc + Re) # collector-emitter voltage
         Ve = Ie * Re # emitter voltage
         Vc = Vce + Ve # collector voltage
         Vb = self.Vbe + Ve # base voltage
         Vbc = Vb - Vc # base-collector voltage
         # Save the results into 'dcs'.
         self._save_dc_results_(Ib, Ic, Ie, Icsat, Vce, Vc, 
                                Ve, Vb, Vbc)
      # AC analysis:
      if self.analysis == "ac":
         re = 0.026 / Ie
         Zb1 = ((beta + 1) + (Rc/ro)) 
         Zb2 = (1 + (Rc + Re) / ro)
         Zb = beta * re + (Zb1 / Zb2) * Re
         Zi = 1 / (1/Rb + 1/Zb) # input impedance 
         Zo1 = beta * (ro + re)
         Zo2 = 1.0 + (beta * re) / Re
         Zo3 = ro + Zo1 / Zo2
         Zo = 1.0 / (1.0/Rc + 1.0/Zo3) # output impedance
         Av1 = (-1 * (beta * Rc) / Zb) 
         Av2 = (1 + (re/ro)) + (Rc/ro)
         Av3 = 1 + (Rc / ro)
         Av = (Av1 * Av2) / Av3 # voltage gain 
         # Save the results into 'acs'.
         self._save_ac_results_(re, Zi, Zo, Av, None, "In phase")
      
      return self.dcs if self.analysis == "dc" else self.acs

   def voltage_divider(self, Vcc:float, Rb1: float, Rb2: float, 
                       Rc: float, Re: float, beta: float, 
                       ro: float = None, bypass: str = None): 
      """ The dc and ac analysis of voltage-divider configuration.
      `Vcc` represents main voltage source and must be in terms of 
      'V'. `Rb1`, `Rb2`, `Rc` and `Re` represent upper base, lower
      base, collector and emitter resistances in order. These 
      resistance must be in terms 'ohm'. `beta` represents the ration
      of collector current to base currant and is unitless. `ro` is 
      constant and just use it for ac analysis. `bypass` represents
      wheter emitter terminal have bypassed or not. It can take two 
      argument which are `'bypassed'` or `'unbypassed'`.

      ## Example 1
      >>> bjt = BJTAnalysis(analysis="dc")
      >>> result = bjt.voltage_divider(Vcc=22, Rb1=39000, Rb2 = 3900,
                                       Rc=10000, Re=1500, beta=100)
      >>> print(result)
      {'Ib': 8.384637936089123e-06, 
      'Ic': 0.0008384637936089123, 
      'Ie': 0.0008468484315450014, 
      'Icsat': 0.0019130434782608696, 
      'Vce': 12.357666373497509, 
      'Vc': 13.62793902081501, 
      'Ve': 1.2702726473175021, 
      'Vb': 1.970272647317502, 
      'Vbc': -11.657666373497507, 
      'Vbe': 0.7}

      ## Example 2
      >>> bjt = BJTAnalysis(analysis="ac")
      >>> result = bjt.voltage_divider(Vcc=16, Rb1=90000, Rb2=10000, 
                                       Rc=2200, Re=680, beta=210, 
                                       ro=50000, bypass="bypassed")
      >>> print(result)
      {'re': 20.876671932596096, 
      'Zi': 2948.043326972088, 
      'Zo': 2107.27969348659, 
      'Av': -100.93944572632567, 
      'Ai': None, 
      'Phase': 'Out of phase'}

      ## Example 3
      >>> bjt = BJTAnalysis(analysis="ac")
      >>> result = bjt.voltage_divider(Vcc=16, Rb1=90000, Rb2=10000, 
                                       Rc=2200, Re=680, beta=210, 
                                       ro=50000, bypass="unbypassed")
      >>> print(result)
      {'re': 20.876671932596096, 
      'Zi': 8456.660452829594, 
      'Zo': 2196.6910805381563, 
      'Av': -3.1183317773113046, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """
      bypasses = ["bypassed", "unbypassed", None]
      # Check parameters.
      if (self.analysis == "ac" and ro == None) or \
         (self.analysis == "ac" and bypass == None) or \
         (bypass != None and bypass not in bypasses):
         error = "Parameters of voltage-divider config. are conflict"
         raise VoltageDividerError(error)
      # Both dc and ac analysis requires these values.
      rth = self._Rth_(Rb1, Rb2)
      eth = self._Eth_(Vcc, Rb1, Rb2)
      Ib = (eth - self.Vbe) / (rth + (beta + 1) * Re) # base current
      Ie = (beta + 1) * Ib # emitter current
      # DC analysis:
      if self.analysis == "dc":
         Ic = beta * Ib # collector current
         Icsat = Vcc / (Rc + Re) # saturation (max) current
         Vce = Vcc - Ic * (Rc + Re) # collector-emitter voltage
         Ve = Ie * Re # emitter voltage
         Vc = Vce + Ve # collector voltage
         Vb = self.Vbe + Ve # base voltage
         Vbc = Vb - Vc # base-collector voltage
         # Save the results into 'dcs'.
         self._save_dc_results_(Ib, Ic, Ie, Icsat, Vce, Vc, 
                                Ve, Vb, Vbc)
      # AC analysis:
      if self.analysis == "ac":
         re = 0.026 / Ie
         if bypass == "bypassed":
            Zi = 1 / (1/rth + 1/(beta * re)) # input impedance
            Zo = 1 / (1/Rc + 1/ro) # output impedance
            Av = -1 * (1 / (1/Rc + 1/ro)) / re
            # Save the results into 'acs'.
            self._save_ac_results_(re, Zi, Zo, Av, None, 
                                   "Out of phase")
         if bypass == "unbypassed":
            Zb1 = (beta + 1) + (Rc/ro)
            Zb2 = 1 + (Rc + Re) / ro
            Zb = beta * re + (Zb1 / Zb2) * Re
            Zi = 1.0 / (1.0/rth + 1.0/Zb) # input impedance
            Zo1 = beta * (ro + re)
            Zo2 = 1.0 + (beta * re) / Re
            Zo3 = ro + Zo1 / Zo2
            Zo = 1.0 / (1.0/Rc + 1.0/Zo3) # output impedance
            Av1 = (-1 * (beta * Rc) / Zb) * (1 + (re/ro)) + (Rc/ro)
            Av2 = 1 + (Rc / ro)
            Av = Av1 / Av2 # voltage gain
            # Save the results into 'acs'.
            self._save_ac_results_(re, Zi, Zo, Av, None, 
                                   "Out of phase")
      
      return self.dcs if self.analysis == "dc" else self.acs

   def collector_feedback(self, Vcc: float,  Rf: float, Rc: float, 
                          beta: float, Re: float = None,
                          ro: float = None): 
      """ The dc and ac analysis of collector-feedback configuration.
      `Vcc` represents main voltage source. `Rf`, `Rc`, `Re` represent
      base, collector and emitter resistances. These parameters must
      be in terms of 'ohm'. `beta` represents the ration of collector 
      current to base currant and is unitless. `ro` is constant and 
      just use it for ac analysis. Specially, `Re` parameter just is
      used for dc analysis.

      ## Example 1
      >>> bjt = BJTAnalysis(analysis="dc")
      >>> result = bjt.collector_feedback(Vcc=10, Rf=250000, Rc=4700, 
                                          Re=1200, beta=90)
      >>> print(result)
      {'Ib': 1.1907810499359796e-05, 
      'Ic': 0.0010717029449423816, 
      'Ie': 0.0010836107554417413, 
      'Icsat': 0.001694915254237288, 
      'Vce': 3.6769526248399487, 
      'Vc': 4.977285531370038, 
      'Ve': 1.3003329065300895, 
      'Vb': 2.0003329065300894, 
      'Vbc': -2.9769526248399485, 
      'Vbe': 0.7}

      ## Example 2
      >>> bjt = BJTAnalysis(analysis="ac")
      >>> result = bjt.collector_feedback(Vcc=9, Rf=180000, Rc=2700, 
                                          beta=200, ro=1e+10)
      >>> print(result)
      {'re': 11.221003416651678, 
      'Zi': 565.5822140464395, 
      'Zo': 2660.0978145552613, 
      'Av': -237.06416581317006, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """
      # Check parameters.
      if (self.analysis == "ac" and ro == None) or \
         (self.analysis == "dc" and Re == None):
         raise CollectorFeedbackError(
            "Parameters of collector-feedback config. are conflict"
         )
      # DC analysis:
      if self.analysis == "dc":
         # base current
         Ib = (Vcc - self.Vbe) / (Rf + beta * (Rc + Re)) 
         Ic = beta * Ib # collector current
         Ie = (beta + 1) * Ib # emitter current
         Icsat = Vcc / (Rc + Re) # saturation (max) current
         Vce = Vcc - Ic * (Rc + Re) # base-collector voltage
         Ve = Ie * Re # emitter voltage
         Vc = Vce + Ve # collector voltage
         Vb = self.Vbe + Ve # base voltage
         Vbc = Vb - Vc # base-collector voltage
         # Save the results into 'dcs' dictionary.
         self._save_dc_results_(Ib, Ic, Ie, Icsat, Vce, Vc, 
                                Ve, Vb, Vbc)
      # AC analysis:
      if self.analysis == "ac":
         Ib = (Vcc - self.Vbe) / (Rf + beta * Rc) # base current
         Ie = (beta + 1) * Ib # emitter current
         re = 0.026 / Ie
         Zi1 = 1 + (self._Rth_(Rc, ro) / Rf)
         Zi2 = (1 / (beta * re)) + (1 / Rf)
         Zi3 = self._Rth_(Rc, ro) / (beta * re * Rf)
         Zi4 = self._Rth_(Rc, ro) / (Rf * re)
         Zi = Zi1 / (Zi2 + Zi3 + Zi4) # input impedance
         Zo = 1.0 / (1.0/ro + 1.0/Rc + 1.0/Rf) # output impaedance
         Av1 = Rf / (self._Rth_(Rc, ro) + Rf)
         Av2 = self._Rth_(Rc, ro) / re
         Av = -1 * Av1 * Av2 # voltage gain
         # Save the results into 'acs' dictionary.
         self._save_ac_results_(re, Zi, Zo, Av, None, "Out of phase")

      return self.dcs if self.analysis == "dc" else self.acs

   def collector_dc_feedback(self, Vcc: float,  Rf1: float, 
                             Rf2: float, Rc: float, beta: float, 
                             Re: float = None, ro: float = None): 
      """ The dc and ac analysis of collector-dc-feedback config.
      `Vcc` represents main voltage source. `Rf1`, `Rf2`, `Rc`, `Re` 
      represent left base, right base, collector and emitter
      resistances and must be in terms of 'ohm'. These parameters 
      must be in terms of 'ohm'. `beta` represents the ration of 
      collector current to base currant and is unitless. `ro` is 
      constant and just use it for ac analysis. Specially, `Re` 
      parameter just is used for dc analysis.

      ## Example 1
      >>> bjt = BJTAnalysis(analysis="ac")
      >>> result = bjt.collector_dc_feedback(Vcc=12, Rf1=120000,
                                             Rf2=68000, Rc=3000, 
                                             beta=140, ro=30000)
      >>> print(result)
      {'re': 8.811899830540385, 
      'Zi': 1221.1122707618904, 
      'Zo': 2622.1079691516707, 
      'Av': -297.5644321402677, 
      'Ai': None, 
      'Phase': 'Out of phase'}
      """
      # Check parameters.
      if (self.analysis == "ac" and ro == None) or \
         (self.analysis == "dc" and Re == None):
         raise CollectorDCFeedbackError(
            "Parameters of collector-feedback config. are conflict"
         )
      # DC analysis:
      if self.analysis == "dc":
         error = "transistor do not support that analysis type"
         raise MissingTransistorAnalysisError(error)
      # AC analysis:
      if self.analysis == "ac":
         Ib = (Vcc - self.Vbe) / (Rf1 + (beta * Rc)) # base current
         Ie = (beta + 1) * Ib # emitter current
         re = 0.026 / Ie # re
         Zi = 1.0 / (1.0/Rf1 + 1.0/(beta * re)) # input impedance
         Zo = 1.0 / (1.0/Rc + 1.0/Rf2 + 1.0/ro) # output impedance
         Av = -1 * Zo / re # voltage gain
         # Save the results into 'acs' dictionary.
         self._save_ac_results_(re, Zi, Zo, Av, None, "Out of phase")

      return self.dcs if self.analysis == "dc" else self.acs

   def emitter_follower(self, Rb: float, Re: float, beta: float, 
                        Vee: float = None, Vcc: float = None, 
                        ro: float = None):
      """ THe dc and ac analysis of emitter-follower configuration.
      `Vcc` represents main voltage source for 'ac' analysis.
      `Vee` represents main voltage source for 'dc' analysis. `Rb`
      and `Re` represent base and emitter resistances and must be
      in terms of 'ohm'. `beta` represents the ration of collector
      current to base currant and is unitless. `ro` is constant and
      just use it for ac analysis.

      ## Example 1
      >>> bjt = BJTAnalysis(analysis="dc")
      >>> result = bjt.emitter_follower(Vee=20, Rb=240000, Re=2000,  
                                        beta=90)
      >>> print(result)
      {'Ib': 4.573459715639811e-05, 
      'Ic': 0.00411611374407583, 
      'Ie': 0.0041618483412322275, 
      'Icsat': None, 
      'Vce': 11.676303317535545, 
      'Vc': 40.0, 
      'Ve': 28.323696682464455, 
      'Vb': 29.023696682464454, 
      'Vbc': -10.976303317535546, 
      'Vbe': 0.7}

      ## Example 2
      >>> bjt = BJTAnalysis(analysis="ac")
      >>> result = bjt.emitter_follower(Vcc=12, Rb=220000, Re=3300, 
                                        beta=90, ro=1e+10)
      >>> print(result)
      {'re': 13.155499367888748, 
      'Zi': 127187.92970269317, 
      'Zo': 12.959836584149675, 
      'Av': 0.9960727754966983, 
      'Ai': None, 
      'Phase': 'In phase'}
      """ 
      # Check parameters.
      if (self.analysis == "dc" and Vee == None) or \
         (self.analysis == "ac" and Vcc == None) or \
         (self.analysis == "ac" and ro == None):
         raise EmitterFllowerError(
            "Parameters of emitter-follower config. are conflict"
         )
      # DC analysis:
      if self.analysis == "dc":
         Ib = (Vee - self.Vbe) / (Rb + (beta + 1) * Re) # base current
         Ie = (beta + 1) * Ib # emitter current
         Ic = beta * Ib # collector current
         Vce = Vee - (Ie * Re) # collector-emitter voltage
         Ve = (Ie * Re) + Vee # emitter voltage
         Vc = Vce + Ve # collector voltage
         Vb = self.Vbe + Ve # base voltage
         Vbc = Vb - Vc # base-collector voltage
         # Save the results into 'dcs' dictionary.
         self._save_dc_results_(Ib, Ic, Ie, None, Vce, 
                                Vc, Ve, Vb, Vbc)
      # AC analysis:
      if (self.analysis == "ac"):
         Ib = (Vcc - self.Vbe) / (Rb + (beta + 1) * Re) # base current
         Ie = (beta + 1) * Ib # emitter current
         re = 0.026 / Ie # re
         Zb1 = (beta + 1) * Re 
         Zb2 = 1 + (Re / ro)
         Zb = (beta * re) + (Zb1 / Zb2)
         Zi = 1 / (1/Rb + 1/Zb) # input impedance
         Zo1 = (beta * re) / (beta + 1)
         Zo = 1 / (1/ro + 1/Re + 1/Zo1) # output impedance
         Av1 = (beta + 1) * Re / Zb
         Av = Av1 / (1 + (Re/ro)) # voltage gain
         # Save the results into 'acs' dictionary.
         self._save_ac_results_(re, Zi, Zo, Av, None, "In phase")

      return self.dcs if self.analysis == "dc" else self.acs

   def common_base(self, Vcc: float, Vee: float, Rc: float, 
                     Re: float, beta: float = None, 
                     alpha: float = None): 
      """ The dc and ac analysis of common-base configuration.
      `Vee` and `Vcc` represent voltage sources. `Rc` and `Re`
      represent collector and emitter resistance in order and in 
      terms of 'ohm'. `beta` and `alpha` are constants and have 
      unitless.
      
      ## Example 1
      >>> bjt = BJTAnalysis(analysis="dc")
      >>> result = bjt.common_base(Vcc=10, Vee=4, Rc=2400, 
                                   Re=1200, beta=60)
      >>> print(result)
      {'Ib': 4.508196721311475e-05, 
      'Ic': 0.0027049180327868854, 
      'Ie': 0.00275, 
      'Icsat': None, 
      'Vce': 4.100000000000001, 
      'Vc': None, 
      'Ve': None, 
      'Vb': None, 
      'Vbc': -3.5081967213114753, 
      'Vbe': 0.7}

      ## Example 2
      >>> bjt = BJTAnalysis(analysis="ac")
      >>> result = bjt.common_base(Vcc=8, Vee=2, Rc=5000, 
                                   Re=1000, alpha=0.98)
      >>> print(result)
      {'re': 20.0, 
      'Zi': 19.6078431372549, 
      'Zo': 5000, 'Av': 245.0, 
      'Ai': None, 
      'Phase': 'In phase'}
      """
      # Check parameters.
      if (self.analysis == "dc" and beta == None) or \
         (self.analysis == "ac" and alpha == None):
         raise CommonBaseError( 
            "Parameters of common-base config. are conflict"
         )
      # Both variables are valid for two analyzes.
      Ie = (Vee - self.Vbe) / Re # emitter current
      # DC analysis:
      if self.analysis == "dc":
         Ib = Ie / (beta + 1) # base current
         Ic = beta * Ib # collector current
         Vce = Vee + Vcc - Ie * (Rc + Re) # collector-emitter voltage
         Vbc = -1 * (Vcc - Ic * Rc) # base-collector voltage
         # Save the results into 'dcs' dictionary.
         self._save_dc_results_(Ib, Ic, Ie, None, Vce, 
                                None, None, None, Vbc)
      # AC analysis:
      if (self.analysis == "ac"):
         re = 0.026 / Ie # re
         Zi = 1 / (1/Re + 1/re) # input impedance
         Zo = Rc # output impedance
         Av = alpha * Rc / re # voltage gain
         # Save the results into 'acs' dictionary.
         self._save_ac_results_(re, Zi, Zo, Av, None, "In phase")

      return self.dcs if self.analysis == "dc" else self.acs

   def miscellaneous_bias(self, Vcc: float, Rb: float, Rc: float, 
                          beta: float): 
      """ The dc analysis of miscellaneous-bias configuration.
      `Vcc` represents main voltage source. `Rb`, `Rc` represent
      base, collector and resistances. These parameters must be in 
      terms of 'ohm'. `beta` represents the ration of collector 
      current to base currant and is unitless. 

      ## Example 1
      >>> bjt = BJTAnalysis(analysis="dc")
      >>> result = bjt.miscellaneous_bias(Vcc=20, Rb=680000, 
                                          Rc=4700, beta=120)
      >>> print(result)
      {'Ib': 1.5514469453376205e-05, 
      'Ic': 0.0018617363344051445, 
      'Ie': 0.0018772508038585208, 
      'Icsat': None, 
      'Vce': 11.176921221864953, 
      'Vc': 11.176921221864953, 
      'Ve': 0, 
      'Vb': 0.7, 
      'Vbc': -10.476921221864954, 
      'Vbe': 0.7}
      """
      # DC analysis:
      if self.analysis == "dc":
         Ib = (Vcc - self.Vbe) / (Rb + beta * Rc) # base current 
         Ic = beta * Ib # collector current
         Ie = (beta + 1) * Ib # emitter current
         Vce = Vcc - (Ie * Rc) # collector-emitter voltage
         Ve = 0 # emitter voltage
         Vc = Vce + Ve # collector voltage
         Vb = self.Vbe + Ve # base voltage
         Vbc = Vb - Vc # base-collector voltage
         # Save the results into 'dcs' dictionary.
         self._save_dc_results_(Ib, Ic, Ie, None, Vce, 
                                Vc, Ve, Vb, Vbc)
      # AC analysis:
      if (self.analysis == "ac"):
         error = "transistor do not support ac analysis"
         raise MissingTransistorAnalysisError(error)
      
      return self.dcs if self.analysis == "dc" else self.acs


def two_port_system(Avnl: float, Zi: float, Zo: float, 
                    Rs: float, Rl:float) -> dict:
   """ Two Port System Analysis
   `Avnl` means not-null voltage gain and must be unitless. `Zi`,
   `Zo` represents input, output impedance and must be in terms of
   'ohm'. `Rs`, `Rl` represent source and load resistances and must
   be in terms of 'ohm'.

   ## Example 1 
   >>> results = two_port_system(Avnl=-480, Zi=4000, Zo=2000, 
                                 Rs=200, Rl=5600)
   >>> print(results)
   {'Avl': -353.6842105263158, # load-voltage gain
   'Avs': -336.84210526315786, # source-voltage gain
   'Ail': 252.6315789473684} # load-current gain
   """
   # Store the results into dictionary.
   results = {}
   # Load voltage gain:
   Avl = Rl / (Rl + Zo) * Avnl
   # Source voltage gain:
   Avs = Zi / (Zi + Rs) * Rl / (Rl + Zo) * Avnl
   # Input load current gain:
   Ail = -1 * Avl * Zi / Rl
   # Save the results.
   results["Avl"], results["Avs"], results["Ail"] = Avl, Avs, Ail

   return results

def cascaded(Zis: list, Zos: list, Avnls: list, Rs: float, 
             Rl: float) -> dict:
   """ Cascaded System Analysis
   `Avnls` mean not-null voltage gains and must be stored in list.
   `Zis`, `Zos` mean input and output impedances and each resistance
   must be in terms of 'ohm' and must be stored into list. `Rs`, `Rl`
   mean source and load resistance and must be in terms of 'ohm'. All
   variables must be given in order. 

   ## Example 1
   >>> results = cascaded(Avnls=[1, 240], # not-null voltage gains
                          Zis=[1e+4, 26], # input impedances
                          Zos=[12, 5100], # output impedances
                          Rs=1000, # source resistances
                          Rl=8200 # load resistance
                        )
   >>> print(results)
   {'Av1': 0.6842105263157895, # first stage voltage gain
   'Av2': 147.96992481203006, # second stage voltage gain
   'Avt': 101.24258013454688, # total voltage gains
   'Avs': 92.03870921322444, # source voltage gain
   'Ait': -123.46656113969132} # total current gains

   ## Example 2
   >>> results = cascaded(Avnls=[1, 250, 100],# not-null voltage gains
                          Zis=[500, 26, 100], # input impedances
                          Zos=[1000, 5100, 100], # output impedances
                          Rs=10000, # source resistance
                          Rl=820 # load resitance
                        )
   >>> print(results)
   {'Av1': 0.025341130604288498, # first stage voltage gain
   'Av2': 4.807692307692308, # second stage voltage gain
   'Av3': 89.13043478260869, # third stage voltage gain
   'Avt': 10.858971099245698, # total voltage gains
   'Avs': 0.5170938618688428, # source voltage gain
   'Ait': -6.621323841003474} # total current gains
   """
   # Check the parameters.
   if not len(Zis) == len(Zos) == len(Avnls):
      raise CascadedSystemError("all lists must be same lenght")
   # Store the results.
   results = {}
   # Calculate total voltage gain.
   total_voltage = 1
   # Caculates voltage gain.
   for index in range(len(Zis)-1):
      # voltage gain
      Av = Zis[index + 1] / (Zis[index + 1] + Zos[index])
      Av = Av * Avnls[index]
      # Each time, multiplies voltage gain with itself.
      total_voltage *= Av 
      vname = f"Av{index+1}" # voltage-gain name
      # Append voltage gain info.
      results[vname] = Av
   # Calculate the last stage voltage gain
   last_stage = Rl / (Rl + Zos[-1]) * Avnls[-1]
   total_voltage *= last_stage
   # Append the last stage voltage gain.
   results[f"Av{len(Zis)}"] = last_stage
   # Append the total voltage gain.
   results["Avt"] = total_voltage
   # Append the source voltage gain.
   results["Avs"] = Zis[0] / (Zis[0] + Rs) * total_voltage
   # Append the total current gain.
   results["Ait"] = -1 * total_voltage * Zis[0] / Rl

   return results

