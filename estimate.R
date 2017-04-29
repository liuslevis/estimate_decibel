dat <- read.csv('data/4sec.input.csv')
lm <- lm(decibel ~ log(x,10) - 1, dat)
summary(lm)