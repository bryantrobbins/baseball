from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas

point = Literal( "." )
fnumber = Combine( Word( "+-"+nums, nums ) + Optional( point + Optional( Word( nums ) ) ) )
plus  = Literal( "+" )
minus = Literal( "-" )
mult  = Literal( "*" )
div   = Literal( "/" )
lpar  = Literal( "(" ).suppress()
rpar  = Literal( ")" ).suppress()
addop  = plus | minus
multop = mult | div
expop = Literal( "^" )
        
expr = Forward()
atom = fnumber
factor = Forward()
factor << atom
term = factor + ZeroOrMore( ( multop + factor ))
expr << term + ZeroOrMore( ( addop + term ))
bnf = expr

s = "2.3*6"
results = bnf.parseString( s, parseAll=True)
print(results.dump())
