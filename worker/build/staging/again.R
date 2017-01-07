.libPaths( "." )
suppressMessages(library(dplyr))
suppressMessages(library(ggplot2))
suppressMessages(library(gridExtra))

sumRows <- function(d, ... ) {
  by_vars <- group_by_(d, ...)
  summed_groups <- summarise_if(by_vars, .predicate = function(x) is.numeric(x), funs("sum"))
  return(ungroup(summed_groups))
}

generateLeaderboard <- function(d, sortCol, sortDir, keyCols) {
  sortExpr = sprintf("%s(%s)", sortDir, sortCol)
  allCols = c(keyCols, sortCol)
  leaders <- arrange_(d, sortExpr)
  leaders <- selectWithKeys(leaders, keyCols, sortCol)
  leaders <- filter(leaders, row_number() <= 10L)
  p <- tableGrob(leaders)
  gp <- grid.arrange(p)
  ggsave(filename="output.svg", gp)
}

selectWithKeys <- function(d, keyCols, ...) {
  allCols = c(keyCols, c(...))
  return(select(d, one_of(allCols)))
}

# Load data into a dataframe
lahman_Batting <- read.csv("lahman/Batting.csv")
keyCols <- c('playerID', 'stint', 'yearID')

# Select columns
lahman_Batting <- selectWithKeys(lahman_Batting, keyCols, 'HR', 'lgID')

# Select rows
lahman_Batting <- filter(lahman_Batting, yearID >= 2000)

# Define new columns
lahman_Batting <- mutate(lahman_Batting, custom = (2*(HR)))

# Group rows
lahman_Batting <- sumRows(lahman_Batting, 'playerID', 'yearID', 'lgID')
keyCols <- c('playerID', 'yearID', 'lgID')

# Produce leaderboard
generateLeaderboard(lahman_Batting, "HR", "desc", keyCols)
