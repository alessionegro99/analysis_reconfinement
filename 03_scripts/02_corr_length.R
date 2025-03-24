library(hadron)

Nt <- 10
Ns <- 64
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

G_0 <- list()
G_min <- list()

for(hh_i in seq_along(HH)){
  data <- NULL
  for (ii in II) { 
    tmp <- as.matrix(read.table(paste0(data_path(Ns, HH[hh_i], ii)), skip = 1 + therm))
    data <- if (is.null(data)) tmp else rbind(data, tmp)
  }
  
  G_0[[length(G_0) + 1]] <- data[,5]
  G_min[[length(G_min) + 1]] <- data[,6]
}

G_0 <- matrix(unlist(G_0), ncol = length(G_0), nrow = length(G_0[[1]]))
G_min <- matrix(unlist(G_min), ncol = length(G_min), nrow = length(G_min[[1]]))

newcf <- cf_orig(cf=G_0)
cf_G_0 <- cf_meta(newcf, nrObs=1, Time=length(HH), symmetrised=FALSE, nrStypes = 0)

newcf <- cf_orig(cf=G_min)
cf_G_min <- cf_meta(newcf, nrObs=1, Time=length(HH), symmetrised=FALSE, nrStypes = 0)

rm(data)
rm(G_0)
rm(G_min)

seed <- 12345

cf_G_0 <- bootstrap.cf(cf_G_0, boot.R = boot.R, boot.l = boot.l, seed = seed, sim = "fixed", endcorr = TRUE)
cf_G_min <- bootstrap.cf(cf_G_min, boot.R = boot.R, boot.l = boot.l, seed = seed, sim = "fixed", endcorr = TRUE)

xi_L <- sqrt((cf_G_0$cf0 - cf_G_min$cf0)/(cf_G_min$cf0*4*sin(pi/Ns)*sin(pi/Ns)))/Ns
xi_L_t <- sqrt((cf_G_0$cf.tsboot$t - cf_G_min$cf.tsboot$t)/(cf_G_min$cf.tsboot$t*4*sin(pi/Ns)*sin(pi/Ns)))/Ns

d_xi_L <- apply(xi_L_t, 2, sd)

pdf(paste0(output_path, "/L", Ns,"/G0_Gmin_xiL.pdf"))
plotwitherror(HH, cf_G_0$cf0, cf_G_0$tsboot.se, xlab = "h", ylab = expression(G[0]))
plotwitherror(HH, cf_G_min$cf0, cf_G_min$tsboot.se, rep = FALSE, xlab = "h", ylab = expression(G[min]))
plotwitherror(HH, xi_L, d_xi_L, rep = FALSE, xlab = "h", ylab = expression(xi/L))
dev.off()

write.table(data.frame(Ns = Ns, h = HH, xi_L = xi_L, d_xi_L = d_xi_L),
            file = paste0(output_path, "/L", Ns, "/xi_L.txt"), sep = "\t", row.names = FALSE, col.names = FALSE, quote = FALSE, append = TRUE)
