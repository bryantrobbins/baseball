from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,\
    ZeroOrMore,Forward,nums,alphas

point = Literal( "." )
fnumber = Combine( Word( "+-"+nums, nums ) + Optional( point + Optional( Word( nums ) ) ) + Optional( Word( "+-"+nums, nums ) ) )
#ident = Word(alphas)
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
atom = (Optional("-") + ( fnumber | ident + lpar + expr + rpar ) | ( lpar + expr.suppress() + rpar )) 
factor = Forward()
factor << atom + ZeroOrMore( ( expop + factor ))
term = factor + ZeroOrMore( ( multop + factor ))
expr << term + ZeroOrMore( ( addop + term ))
bnf = expr

s = "2+f"
results = bnf.parseString( s )
print(results)
