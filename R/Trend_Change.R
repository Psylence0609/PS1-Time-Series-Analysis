linearRegressionTest <- function(c0, c, x){
  ## input: 
  ## c0: a linear regression model (output of lm)
  ## c: a linear regression model (output of lm)
  ## x: observation values
  ##
  ## output: the t-score value for linear model change
  ## reference: http://en.wikipedia.org/wiki/Student's_t-test
  n = length(x)
  SSR <- sum(c$residuals^2)
  SSRx <- sum((x-mean(x))^2)
  
  beta0 <- c0$coefficients[2] 
  beta <- c$coefficients[2]
  tscore_beta <- (beta-beta0)*sqrt(n-2)/sqrt(SSR/SSRx)
  
  tscore <- tscore_beta
  
  cat(paste("p value: " , pt(tscore, df=n-2), "\n=====\n"))
  
  return (pt(tscore, df=n-2))
}
locateRegimeChange <- function(a, initialWindowSize, incrementalWindowSize, plotScore=FALSE, pvalue_thr=0.01){
  ## input: 
  ## a: data has in the form of [X, Y] X, Y are vectors
  ## initialWindowSize: size of the first window to fit the model
  ## incrementalWindowSize: the size of sliding window (test window)
  ## plotScore: if TRUE it will plot the t-score value
  ## pvalue_thr: p-value threshold
  ##
  ## output: the index number at which the linear model changes
  
  len<-nrow(a)
  x0 <- a[ 1: initialWindowSize ,2] 
  y0 <- a[ 1: initialWindowSize ,1] 
  c0 <- lm(y0~x0)
  
  regime_change_point<- NULL
  while (initialWindowSize < len){
    x1 <- a[ (initialWindowSize + 1): min(initialWindowSize + incrementalWindowSize, len) ,2] 
    y1 <- a[ (initialWindowSize + 1): min(initialWindowSize + incrementalWindowSize, len) ,1] 
    
    c <- lm(y1~x1)
    
    #cat(paste("@ Point ", initialWindowSize, "\n"))
    #cat(paste("slope up to now: ", c0$coefficients[2], "\n"))
    #cat(paste("new slope: ", c$coefficients[2], "\n"))
    tscore <- linearRegressionTest(c0,c,x1)
    
    
    if(tscore < pvalue_thr){
      regime_change_point <- append(regime_change_point,initialWindowSize)
      initialWindowSize <- initialWindowSize + incrementalWindowSize
      x0 <- a[ 1: initialWindowSize ,2] 
      y0 <- a[ 1: initialWindowSize ,1] 
      c0 <- lm(y0~x0)
    }
    else{
      initialWindowSize <- initialWindowSize + incrementalWindowSize
      x0 <- a[ 1: initialWindowSize ,2] 
      y0 <- a[ 1: initialWindowSize ,1] 
      c0 <- lm(y0~x0)
    }
  }
  
  return (regime_change_point)
  
  
}

df <- read.csv(file='C:\\Users\\prane\\Desktop\\PS-1\\json_to_csv\\91302.csv')

list<-locateRegimeChange(df,48,48,FALSE,1e-5)
list
par(mar=c(1,1,1,1))
plot(df[,2],df[,1])
for(x in list){
  plot(df[x,2],df[x,1],pch=8,col="red")
}
  