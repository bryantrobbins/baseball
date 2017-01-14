from ExpressionValidator import ExpressionValidator

vv = ExpressionValidator()
ee = [
    "2 * COL('HR')",
    "2",
		"'BRYAN'",
		"hi(2)",
		"hi(2,3,4)",
		"-hi(2,3,4)",
]

for ex in ee:
    result = vv.parseExpression(ex)
    print('{} => {}'.format(ex, result))
