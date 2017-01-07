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
	return(subset(d, eval(e)))
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
  cols = c(...)
  for (v in cols) {
    vx = sprintf("x$%s", v)
    sexpr_u = gsub(v, vx, c(sexpr_u))[1]
  }
  e = parse(text = sexpr_u)
	res <- ddply(d, 'playerID', function(x) {
		cc <- eval(e)
  	data.frame(x, computed = cc)
	})
  head(res)
	return(rename(res, c("computed"=colName)))
}

# Load data into a dataframe
lahman_Batting= read.csv("lahman/Batting.csv")
head(lahman_Batting)

# Select columns
lahman_Batting <- selectColumns(lahman_Batting, 'playerID', 'yearID', 'teamID', 'HR')

# Select rows
lahman_Batting <- selectRows(lahman_Batting, 'yearID', 'eq', '2000')

# Define new columns
lahman_Batting <- addCustomCol(lahman_Batting, 'custom', '(2*(HR))', 'HR')
head(lahman_Batting)

# Group rows
#subD <- groupRowsSum(subC, 'custom', 'year', 'team')
#head(subD)

# Produce Leaderboard CSV

# Produce Histogram

# Produce Bivariate Plot

