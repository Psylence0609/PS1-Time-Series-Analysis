library(trendsegmentR)
x <- as.vector(read.csv(file='C:\\Users\\prane\\Desktop\\PS-1\\json_to_csv\\91316.csv'))

y<-x[,1]
n<-length(y)
y<-y+rnorm(n)
y
tsfit<-trendsegment(x=y,bal=0)
tsfit

plot(x,type="b",ylim=range(x,tsfit$est))
lines(tsfit$est,col=2,lwd=2)