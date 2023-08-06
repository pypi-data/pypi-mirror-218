# Errors 

class AnalysisError(Exception):
   """ Raise error, if type of analysis is invalid. """

class MissingTransistorAnalysisError(Exception):
   """ Raise error, if given analysis is missing. """

class FixedBiasError(Exception):
   """ Raise error, if parameters of fixed-bias config is conflict. 
   """

class EmitterBiasError(Exception):
   """ Raise error, if parameters of fixed-bias config is conflict. 
   """

class SelfBiasError(Exception):
   """ Raise error, if parameters of self-bias config is conflict. 
   """

class VoltageDividerError(Exception):
   """ Raise error, if parameters of voltage-divider config 
      is conflict. """
   
class CollectorFeedbackError(Exception):
   """ Raise error, if parameters of collector-feedback config 
      is conflict. """
   
class CollectorDCFeedbackError(Exception):
   """ Raise error, if parameters of collector-dc-feedback config 
      is conflict. """
   
class EmitterFllowerError(Exception):
   """ Raise error, if parameters of emitter-fllower config 
      is conflict. """
   
class DrainFeedbackError(Exception):
   """ Raise error, if parameters of drain-feedback config are 
   conflict. """
   
class CommonBaseError(Exception):
   """ Raise error, if parameters of common-base config is conflict. 
   """

class CommonGateError(Exception):
   """ Raise error, if parameters of common-gate config is conflict. 
   """

class TwoPortSystemError(Exception):
   """ Raise error, if parameters of two port system are conflict. """

class MOSFETTypeError(Exception):
   """ Raise error, if parameters of MOSFET are conflict. """

class CascadedSystemError(Exception):
   """ Raise error, if parmeters of cascaded system are conflict. """