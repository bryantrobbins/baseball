from ExpressionValidator import ExpressionValidator
import unittest

vv = ExpressionValidator()
#ee = [
#    "2 * $('HR')",
#    "2",
#		"'BRYAN'",
#		"hi(2) * $('HR')",
#		"hi(2,3,4)",
#		"-hi(2,3,4)",
#		"-hi((2),log(-$('HR')),4)",
#		"hi(2)^-5^6",
#		"(hi(2))^-5",
#]

ee = [
"2",
"3.14",
"'Hey'",
"-2",
"2*3",
"2*3 + 5*4",
"2*3*4",
"5^2",
"hi(2)",
"hi(2,3)",
"$('HR')",
"2 * $('HR')",
"2 * 3 * $('HR')",
"(2 + 5) * 3",
] 

for ex in ee:
    result = vv.parseExpression(ex)
    print('{} => {}'.format(ex, result))
