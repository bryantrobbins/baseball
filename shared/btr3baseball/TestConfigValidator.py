from __future__ import print_function
from ConfigValidator import (
    ConfigValidator,
    UnknownDatasetException,
    UnknownSelectRowsOperatorException
)
import unittest
import json

class TestConfigValidator(unittest.TestCase):

    def helper_testString(self, strConfig):
      cv = ConfigValidator(strConfig)
      cv.validateConfig()
      return cv
    
    def helper_testString_Exception(self, ex, exc):
        with self.assertRaises(exc):
            self.helper_testString(ex)

    def testHappy(self):
        strConfig = '''
        {
          "dataset": "Lahman_Batting",
          "transformations": [
            {
              "type": "columnSelect",
              "columns": [
                "HR",
                "yearID",
                "playerID"
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
              "column": "2HR",
              "expression": "2*$('HR')"
            },
            {
              "type": "columnDefine",
              "column": "myString",
              "expression": "'BRYAN'"
            },
            {
              "type": "rowSum",
              "columns": [
                "playerID",
                "yearID",
                "myString"
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
        self.assertEqual(5, len(cv.cols))

    def testBadDataset(self):
        strConfig= '''
        {
          "dataset": "BAD"
        }
        '''
        cv = self.helper_testString_Exception(strConfig, UnknownDatasetException)

    def testBadRowSelectOp(self):
        strConfig = '''
        {
          "dataset": "Lahman_Batting",
          "transformations": [
            {
              "type": "rowSelect",
              "column": "yearID",
              "operator": "bad",
              "criteria": "2000"
            }
          ] 
        }
        '''
        cv = self.helper_testString_Exception(strConfig, UnknownSelectRowsOperatorException)

if __name__ == '__main__':
    unittest.main()

