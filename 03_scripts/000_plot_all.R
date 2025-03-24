library(hadron)

Nt <- 10
NSS <- c(16, 32, 48, 64, 80, 96)
CC <- c("blue", "purple", "orange", "darkgreen", "darkred", "")
HH <- seq(0.002000, 0.005750, by = 0.000250)

boot.R <- 500
therm <- 1000
boot.l <- 300

rawdata_path <- function(Ns, hh, ii) {
  return(paste0("/home/negro/projects/EST/data/corr_length/L", Ns, "/data/dati_", sprintf("%.6f", hh), "_", ii, ".dat"))
}

plot_path <- function(str) {
  return(paste0("/home/negro/projects/EST/analysis/corr_length/", str))
}

output_file <- paste0(plot_path("general"), "/Ns_h_xi_dxi.txt")

pdf(paste0(plot_path("general"), "/FSS_xi2L2.pdf"))
for (Nss in seq_along(NSS)) {
  Ns <- NSS[Nss]
  print(Ns)
  
  G <- readRDS(paste0(plot_path("special"), "/L", Ns, "/", "data/G.rds"))
  
  G_0 <- c()
  dG_0 <- c()
  G_min <- c()
  dG_min <- c()
  
  xiL <- c()
  dxiL <- c()
  
  for (hh_i in seq_along(HH)) {
    G_0 <- c(G_0, G[[hh_i]]$cf.tsboot$t0[1])
    G_min <- c(G_min, G[[hh_i]]$cf.tsboot$t0[2])
    
    dG_0 <- c(dG_0, G[[hh_i]]$tsboot.se[1])
    dG_min <- c(dG_min, G[[hh_i]]$tsboot.se[2])
    
    xiL <- c(xiL, sqrt((G[[hh_i]]$cf.tsboot$t0[1] - G[[hh_i]]$cf.tsboot$t0[2])/(G[[hh_i]]$cf.tsboot$t0[2]*4*sin(pi/Ns)*sin(pi/Ns)))/Ns)
    xiLt <- sqrt((G[[hh_i]]$cf.tsboot$t[,1] - G[[hh_i]]$cf.tsboot$t[,2])/(G[[hh_i]]$cf.tsboot$t[,2]*4*sin(pi/Ns)*sin(pi/Ns)))/Ns
    dxiL <- c(dxiL,sd(xiLt))
    
    
    write.table(data.frame(Ns = Ns, h = HH[hh_i], xiL = xiL[hh_i], dxiL = dxiL[hh_i]),
                file = output_file, sep = "\t", row.names = FALSE, col.names = FALSE, quote = FALSE, append = TRUE)
    
  }
  if (Nss == 1) {
    par(mgp = c(2.5, 0.5, 0))  # Set margin parameters before plotting
    plotwitherror(HH, xiL, dxiL, 
                  xlab = "h", 
                  ylab = "", 
                  col = CC[Nss],
                  main = "Curve intersection", pch = 0, xlim = c(HH[1], HH[length(HH)]), ylim = c(0.5, 2.2), lwd = 0.1, cex = 1.2, las = 1)
    mtext(expression(xi/L), side = 2, line = 2, las = 1)
    grid()
  }
  else plotwitherror(HH, xiL, dxiL, rep = TRUE, col = CC[Nss], pch = 0, lwd = 0.5, cex = 1.2)
}

legend("topright",  # Position of the legend
       legend = paste0("N_s = ",c(NSS)),  # Labels
       col = CC,  # Match colors
       pch = 0,  # Point symbol
       bg = "white",
       cex = 1.2)  # Background color
dev.off()