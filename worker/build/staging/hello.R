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

addCustomCol <- function(d, colName, sexpr, ...) {
  sexpr_u = sexpr
  for ( v in colnames(d)) {
    vx = sprintf("x$%s", v)
    sexpr_u = gsub(v, vx, c(sexpr_u))[1]
  }
  e = parse(text = sexpr_u)
	res <- ddply(d, 'id', function(x) {
		cc <- eval(e)
  	data.frame(x, computed = cc)
	})
	return(rename(res, c("computed"=colName)))
}

# Select rows
subA <- selectRows(baseball, 'year', 'gt', '2000')

# Select columns
subB <- selectColumns(subA, 'id', 'team', 'year', 'hr')

# Define new columns
subC <- addCustomCol(subB, 'custom', '(2*(hr))')

# Group rows
subD <- groupRowsSum(subC, 'custom', 'year', 'team')
head(subD)

# Produce Leaderboard CSV

# Produce Histogram

# Produce Bivariate Plot

