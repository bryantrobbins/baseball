.libPaths( "." )
library(plyr)

selectRows <- function(d, colName, cond, val) {
	condStr = switch(cond,
    eq = '==',
    neq = '!=',
    geq = '>=',
    leq = '<=',
		gt = '>',
	  lt = '<'
  )
  sexpr = sprintf("%s %s %s", colName, condStr, val)
	e = parse(text = sexpr)
	return(subset(baseball, eval(e)))
}

selectColumns <- function(d, ... ) {
  args = c(...)
	return(d[args])
}

groupRowsSum <- function(d, colName, ...) {
  groupCols = c(...)
  newCol = sprintf("%s.sum", colName)
	res <- ddply(d, groupCols, function(x) {
  	data.frame(grouped = sum(x[colName]))
	})
	return(rename(res, c("grouped"=newCol)))
}

# Select rows
subA <- selectRows(baseball, 'year', 'gt', '2000')

# Select columns
subB <- selectColumns(subA, 'id', 'team', 'year', 'hr')

# Group rows
subC <- groupRowsSum(subB, 'hr', 'year', 'team')
head(subC)
