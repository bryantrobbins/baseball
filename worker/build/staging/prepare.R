cat('Installing packages\n')
cran <- "http://cran.rstudio.com/"
libloc <- "."
#plist <- c("dplyr", "ggplot2", "gridExtra") 
plist <- c("svglite") 
install.packages(plist, repos=cran, lib=libloc)
cat('DONE\n')
