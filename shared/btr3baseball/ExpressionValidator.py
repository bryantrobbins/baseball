from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas,ParseException

point = Literal( "." )
fnumber = Combine( Word( "+-"+nums, nums ) + Optional( point + Optional( Word( nums ) ) ) )
quote = Literal("'").suppress()
comma = Literal(",")
ident = Word(alphas)
plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )
lpar  = Literal( "(" )
rpar  = Literal( ")" )
num_const = fnumber
str_const = quote + ident + quote
addop  = plus | minus
multop = mult | div
expop = Literal( "^" )

expr = Forward()
col = ident
func = ident + lpar + Optional( expr + ZeroOrMore( (comma + expr) ) ) + rpar
atom = Optional('-') + ( num_const | func | col )
parfactor = ( atom | lpar + atom + rpar )
factor = Forward()
factor << ( parfactor + ZeroOrMore(expop + parfactor) )
term = factor + ZeroOrMore( ( multop + factor ))
expr << (term + ZeroOrMore( ( addop + term ))  | str_const)

class ExpressionValidator:
    def __init__(self):
        self.grammar = expr

    def parseExpression(self, strEx):
        try:
            results = self.grammar.parseString(strEx, parseAll=True).dump()
            return ExpressionValidatorResult(expression = strEx, tokens = results)
        except ParseException as e:
            return ExpressionValidatorResult(expression = strEx, exception = e)

class ExpressionValidatorResult:
    def __init__(self, expression = None, tokens = None, exception = None):
        self.expression = expression
        self.tokens = tokens
        if exception != None:
            self.message = str(exception)
            self.location = exception.loc
    def __str__(self):
        if self.tokens != None:
            return self.tokens.__str__()
        if self.message != None:
            return 'In expression "{}": {}'.format(self.expression, self.message)

