library(hadron)

Nt <- 10
Ns <- 16
HH <- seq(0.002000, 0.005750, by = 0.000250)
II <- seq(0, 2, by = 1)

boot.R <- 500
therm <- 1000
boot.l <- 500

################################

data_path <- function(Ns, hh, ii){
  return(paste0("/home/negro/projects/reconfinement/R_reconfinement/01_data/L", Ns,"/data/dati_", sprintf("%.6f", hh), "_", ii, ".dat"))
}

output_path <- "/home/negro/projects/reconfinement/R_reconfinement/02_output/"
################################

L2 <- list()
L4 <- list()

for(hh_i in seq_along(HH)){
  data <- NULL
  for (ii in II) { 
    tmp <- as.matrix(read.table(paste0(data_path(Ns, HH[hh_i], ii)), skip = 1 + therm))
    data <- if (is.null(data)) tmp else rbind(data, tmp)
  }
  
  L2[[length(L2) + 1]] <- data[,3]^2
  L4[[length(L4) + 1]] <- data[,3]^4
}

L2 <- matrix(unlist(L2), ncol = length(L2), nrow = length(L2[[1]]))
L4 <- matrix(unlist(L4), ncol = length(L4), nrow = length(L4[[1]]))

newcf <- cf_orig(cf=L2)
cf_L2 <- cf_meta(newcf, nrObs=1, Time=length(HH), symmetrised=FALSE, nrStypes = 0)

newcf <- cf_orig(cf=L4)
cf_L4 <- cf_meta(newcf, nrObs=1, Time=length(HH), symmetrised=FALSE, nrStypes = 0)

rm(data)
rm(L2)
rm(L4)

seed <- 12345

cf_L2 <- bootstrap.cf(cf_L2, boot.R = boot.R, boot.l = boot.l, seed = seed, sim = "fixed", endcorr = TRUE)
cf_L4 <- bootstrap.cf(cf_L4, boot.R = boot.R, boot.l = boot.l, seed = seed, sim = "fixed", endcorr = TRUE)


U <- cf_L4$cf0/cf_L2$cf0^2
U_t <-  cf_L4$cf.tsboot$t/cf_L2$cf.tsboot$t^2

d_U <- apply(U_t, 2, sd)

write.table(data.frame(Ns = Ns, h = HH, U = U, d_U = d_U),
            file = paste0(output_path, "/L", Ns, "/U.txt"), sep = "\t", row.names = FALSE, col.names = FALSE, quote = FALSE, append = TRUE)

    
pdf(paste0(output_path, "/L", Ns, "/U.pdf"))
plotwitherror(HH, U, d_U, xlab = "h", ylab = "U")
dev.off()