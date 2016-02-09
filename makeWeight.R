gendat <- function(id) {
  n <- sample(20, 1)
  date <- sort(as.Date(sample(365, n), origin='2014-01-01'))
  base <- rnorm(1, 190, 60)
  weight <- round(rnorm(n, base, sqrt(base)))
  data.frame(PatientID=id, Date=date, Value=weight)
}

set.seed(10)
x <- do.call(rbind, lapply(seq(10), gendat))
x <- cbind(ValueID=seq(nrow(x)), x)
write.csv(x, 'Data1.csv', row.names=FALSE, quote=FALSE)

strata <- data.frame(PatientID=seq(10))
grps <- c('small','medium','large')
strata[,'StrataID'] <- cut(tapply(x[,'Value'], x[,'PatientID'], mean), c(0,160,220,Inf), labels=grps)
write.csv(strata, 'StrataIDs.csv', row.names=FALSE, quote=FALSE)

bounds <- data.frame(StrataID=grps, LowerBound=c(90,145,200), UpperBound=c(170,235,300))
write.csv(bounds, 'StrataExternalBounds.csv', row.names=FALSE, quote=FALSE)
