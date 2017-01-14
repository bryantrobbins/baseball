from ExpressionValidator import ExpressionValidator
import unittest

vv = ExpressionValidator()
ee = [
    "2 * COL('HR')",
    "2",
		"'BRYAN'",
		"hi(2) * HR",
		"hi(2,3,4)",
		"-hi(2,3,4)",
		"-hi((2),log(-col('HR')),4)",
		"hi(2)^-5^6",
		"(hi(2))^-5",
]

for ex in ee:
    result = vv.parseExpression(ex)
    print('{} => {}'.format(ex, result))
