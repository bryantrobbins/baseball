from __future__ import print_function
from ConfigValidator import ConfigValidator
import unittest
import json

class TestConfigValidator(unittest.TestCase):

    def createSimpleValidator(self, strConfig):
        return ConfigValidator()

    def helper_testString(self, strConfig):
      cv = self.createSimpleValidator(strConfig)
      cv.validateConfig()
      return cv
    
    def testHappy(self):
        strConfig = '''
        {
          "dataset": "Lahman_Batting",
          "transformations": [
            {
              "type": "columnSelect",
              "columns": [
                "HR",
                "lgID"
              ]
            },
            {
              "type": "rowSelect",
              "column": "yearID",
              "operator": "ge",
              "criteria": "2000"
            },
            {
              "type": "columnDefine",
              "column": "custom",
              "expression": "2*(HR)"
            },
            {
              "type": "rowSum",
              "columns": [
                "playerID",
                "yearID",
                "lgID"
              ]
            }
          ],
          "output": {
            "type": "leaderboard",
            "column": "HR",
            "direction": "desc"
          }
        }
        '''
        cv = self.helper_testString(strConfig)
        self.assertEqual(23, len(cv.cols))

    def testBadDataset(self):
        strConfig= '''
        {
          "dataset": "BAD"
        }
        '''
        cv = self.helper_testString(strConfig)

if __name__ == '__main__':
    unittest.main()




