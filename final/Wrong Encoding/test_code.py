import unittest
import utils

class testCode(unittest.TestCase):
  """
  Note: This function sets several test cases to verify 
  the expected performance of the "test_manipulate_string" function
  """
  def test_manipulate_string(self): 
    self.assertEqual(utils.manipulate_string("\".H.E.I.Z.G.R.U.P.P.E\""), 
                                             "HEIZGRUPPE")
    self.assertEqual(utils.manipulate_string("\".T.E.M.P.E.R.A.T.U.R.E...1.F...2.2.5\""), 
                                             "TEMPERATURE.1F.225")
    self.assertEqual(utils.manipulate_string(".H.E.I.Z.G.R.U.P.P.E"), 
                                             "HEIZGRUPPE")
    self.assertEqual(utils.manipulate_string("H.E.I.Z.G.R.U.P.P.E."), 
                                             "HEIZGRUPPE")
    self.assertEqual(utils.manipulate_string("\"This text is using \"quotes\".\""), 
                                             "This text is using \"quotes\".")
    self.assertEqual(utils.manipulate_string("T.h.i.s. is a special test case"),
                                             "T.h.i.s. is a special test case")
    self.assertEqual(utils.manipulate_string("................"), 
                                             "........")
    self.assertEqual(utils.manipulate_string(""), "")
    self.assertEqual(utils.manipulate_string("\"\""), "")

if __name__ == "__main__":
  unittest.main()