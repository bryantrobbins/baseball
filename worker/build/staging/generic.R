library(jsonlite)
library(plyr)
query <- fromJSON('config.json')

tableName <- query$table
load(paste(tableName,'Rdata', sep = '.'))
my.table <- eval(parse(text = tableName))

filterv <- rep(TRUE, nrow(my.table))
if ('filter' %in% names(query$metadata)) {
	filters <- query$metadata$filter
	for (i in 1:length(filters)){
		if(!is.na(filters[i,1])) {
			filterv <- filterv & grepl(filters[i,1], my.table[[query$metadata$colName[i]]]) 
		}
		if (!is.na(filters[i,2])) {
			filterv <- filterv & my.table[[query$metadata$colName[i]]] > filters[i,2]
		}
		if (!is.na(filters[i,3])) {
			filterv <- filterv & my.table[[query$metadata$colName[i]]] < filters[i,3]	
		}
	}
}

out.tab <- my.table[query$metadata$colName][which(filterv),]

if ('fields' %in% names(query$export)) {
	decr <- query$export$fields[[1]]$value[2] == 'desc' 
	out.tab <- out.tab[order(out.tab[[query$export$fields[[1]]$value[1]]], decreasing = decr),]
}

#fix POS variable
if('POS' %in% colnames(out.tab)) {
	ref.v <- c('P' = 1, 'C' = 2, '1B' = 3, '2B' = 4, '3B' = 5, 'SS' = 6, 'LF' = 7, 'CF' = 8, 'RF' = 9, 'OF' = 10, 'DH' = 11)
	out.tab$POS <- names(ref.v)[out.tab$POS]
}
write.csv(out.tab, file = 'output.csv')
