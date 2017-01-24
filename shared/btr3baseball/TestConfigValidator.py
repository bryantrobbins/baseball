from __future__ import print_function
from ConfigValidator import ConfigValidator
import unittest
import json

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

config = json.loads(strConfig)
vv = ConfigValidator(config)
vv.validateConfig()
