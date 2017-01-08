cat('Installing packages\n')
cran <- "http://cran.rstudio.com/"
libloc <- "/tmp/rpackages"
plist <- c("dplyr", "ggplot2", "gridExtra", "svglite") 
install.packages(plist, repos=cran, lib=libloc)
cat('DONE\n')
