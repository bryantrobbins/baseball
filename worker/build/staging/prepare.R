cat('Installing packages\n')
cran <- "http://cran.rstudio.com/"
libloc <- "."
plist <- c("plyr")
install.packages(plist, repos=cran, lib=libloc)
cat('DONE\n')
