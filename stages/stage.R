s <- paste(readLines(file("stdin"), warn=FALSE), collapse=" ")
cat(trimws(s), " -> R", sep="")
