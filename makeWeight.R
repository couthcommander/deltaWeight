gendat <- function(id) {
  n <- sample(20, 1)
  date <- sort(as.Date(sample(365, n), origin='2014-01-01'))
  base <- rnorm(1, 200, 60)
  weight <- round(rnorm(n, base, sqrt(base)))
  count <- seq(n)
  data.frame(id, date, weight, count)
}

set.seed(10)
x <- do.call(rbind, lapply(seq(10), gendat))
write.csv(x, 'weightFile.csv', row.names=FALSE, quote=FALSE)
