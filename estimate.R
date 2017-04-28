dat <- read.csv('data/87sec.input.csv')
lm <- lm(decibel ~ log(x,10), dat)
summary(lm)