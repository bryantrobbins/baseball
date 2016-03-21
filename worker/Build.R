## r-baseball
# Data and functions for analyzing Baseball statistics
# Author: Bryan Robbins <bryantrobbins@gmail.com>
#

cran <- "http://cran.rstudio.com/"
libloc <- "."
plist <- c("devtools", "roxygen2")
install.packages(plist, repos=cran, lib=libloc)

library(devtools, lib=libloc)
devtools::load_all(pkg = "baseball")

# All Lahman tables from CSV
Lahman.AllstarFull <- read.csv('extract/lahman/AllstarFull.csv')
Lahman.Appearances <- read.csv('extract/lahman/Appearances.csv')
Lahman.AwardsManagers <- read.csv('extract/lahman/AwardsManagers.csv')
Lahman.AwardsPlayers <- read.csv('extract/lahman/AwardsPlayers.csv')
Lahman.AwardsShareManagers <- read.csv('extract/lahman/AwardsShareManagers.csv')
Lahman.AwardsSharePlayers <- read.csv('extract/lahman/AwardsSharePlayers.csv')
Lahman.Batting <- read.csv('extract/lahman/Batting.csv')
Lahman.BattingPost <- read.csv('extract/lahman/BattingPost.csv')
Lahman.CollegePlaying <- read.csv('extract/lahman/CollegePlaying.csv')
Lahman.Fielding <- read.csv('extract/lahman/Fielding.csv')
Lahman.FieldingOF <- read.csv('extract/lahman/FieldingOF.csv')
Lahman.FieldingPost <- read.csv('extract/lahman/FieldingPost.csv')
Lahman.HallOfFame <- read.csv('extract/lahman/HallOfFame.csv')
Lahman.Managers <- read.csv('extract/lahman/Managers.csv')
Lahman.ManagersHalf <- read.csv('extract/lahman/ManagersHalf.csv')
Lahman.Master <- read.csv('extract/lahman/Master.csv')
Lahman.Pitching <- read.csv('extract/lahman/Pitching.csv')
Lahman.PitchingPost <- read.csv('extract/lahman/PitchingPost.csv')
Lahman.Salaries <- read.csv('extract/lahman/Salaries.csv')
Lahman.Schools <- read.csv('extract/lahman/Schools.csv')
Lahman.SeriesPost <- read.csv('extract/lahman/SeriesPost.csv')
Lahman.Teams <- read.csv('extract/lahman/Teams.csv')
Lahman.TeamsFranchises <- read.csv('extract/lahman/TeamsFranchises.csv')
Lahman.TeamsHalf <- read.csv('extract/lahman/TeamsHalf.csv')

# Game Logs from Retrosheet
RetroGL.RegularSeason <- read.csv('extract/gamelogs/gl_regular.csv')
RetroGL.PostSeason <- read.csv('extract/gamelogs/gl_post.csv')
RetroGL.AllStar <- read.csv('extract/gamelogs/gl_allstar.csv')

# Export as RData files
devtools::use_data(Lahman.AllstarFull,
                   Lahman.Appearances,
                   Lahman.AwardsManagers,
                   Lahman.AwardsPlayers,
                   Lahman.AwardsShareManagers,
                   Lahman.AwardsSharePlayers,
                   Lahman.Batting,
                   Lahman.BattingPost,
                   Lahman.CollegePlaying,
                   Lahman.Fielding,
                   Lahman.FieldingOF,
                   Lahman.FieldingPost,
                   Lahman.HallOfFame,
                   Lahman.Managers,
                   Lahman.ManagersHalf,
                   Lahman.Master,
                   Lahman.Pitching,
                   Lahman.PitchingPost,
                   Lahman.Salaries,
                   Lahman.Schools,
                   Lahman.SeriesPost,
                   Lahman.Teams,
                   Lahman.TeamsFranchises,
                   Lahman.TeamsHalf,
                   RetroGL.AllStar,
                   RetroGL.PostSeason,
                   RetroGL.RegularSeason,
                   pkg = "baseball")

devtools::build(pkg = "baseball")
