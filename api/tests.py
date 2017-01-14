import btr3baseball

# Some quick tests (temp)
vv = btr3baseball.ExpressionValidator()
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
