library(EnvCpt)
x <- as.vector(read.csv(file='C:\\Users\\prane\\Desktop\\PS-1\\json_to_csv\\91302.csv'))
#df <- structure(c(288L, 259L, 265L, 293L, 271L, 278L, 300L, 286L, 278L, 
#275L, 282L, 285L, 290L, 296L, 296L, 279L, 270L, 292L, 283L, 289L, 
#                  280L, 269L, 289L, 290L, 287L, 271L, 280L, 299L, 278L, 287L, 293L, 
#                  286L, 297L, 281L, 285L, 305L, 288L, 295L, 277L, 292L, 286L, 281L, 
#287L, 302L, 292L, 297L, 292L, 279L, 281L, 291L), .Tsp = c(1961, 
#2010, 1), class = "ts")
out=envcpt(as.numeric(x[,1]))
out$summary

plot(out,type='aic')
out$trendar2cpt