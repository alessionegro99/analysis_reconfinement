library(hadron)

Nt <- 10
Ns <- 64
HH <- seq(0.002000, 0.005750, by = 0.000250)
II <- seq(0, 2, by = 1)

h_pre <- HH[1]

boot.R <- 500
therm <- 1000

#######################################

data_path <- function(Ns, hh, ii){
  return(paste0("/home/negro/projects/reconfinement/R_reconfinement/01_data/L", Ns,"/data/dati_", sprintf("%.6f", hh), "_", ii, ".dat"))
}

output_path <- "/home/negro/projects/reconfinement/R_reconfinement/02_output/"

## skipping the header
data <- as.matrix(read.table(paste0(data_path(Ns, h_pre, II[1])), skip = 1))
#######################################

message("thermalization...")
## MC history plot
pdf(paste0(output_path, "plots/L", Ns,"/thermalization_", sprintf("%.6f", h_pre), ".pdf"))

ReL <- data[,3]
G_0 <- data[,5]
G_min <- data[,6]

plot(x = c(1:length(G_0)), y = G_0, xlab = "n_configs", ylab = "G_0", main = paste0("G_0, h = ", sprintf("%.6f", h_pre)))

myacf <- computeacf(G_0)
plot(myacf, main = paste0("Autocorrelation function G_0 for h = ", sprintf("%.6f", h_pre)))
summary(myacf)
cat("\n")

plot(x = c(1:length(G_min)), y = G_min, xlab = "n_configs", ylab = "G_min", main = paste0("G_min, h = ",sprintf("%.6f", h_pre)))

myacf <- computeacf(G_min)
plot(myacf, main = paste0("Autocorrelation function G_min for h = ", sprintf("%.6f", h_pre)))
summary(myacf)
cat("\n")

plot(x = c(1:length(ReL)), y = ReL, xlab = "n_configs", ylab = "ReL", main = paste0("ReL, h = ",sprintf("%.6f", h_pre)), xlim = c(0,10000))

myacf <- computeacf(ReL)
plot(myacf, main = paste0("Autocorrelation function ReL for h = ", sprintf("%.6f", h_pre)))
summary(myacf)
cat("\n")

hist(ReL, 50, main = paste0("Distribution of ReL for h = ", sprintf("%.6f", h_pre)))

dev.off()

data <- NULL
for (ii in II) { 
  tmp <- as.matrix(read.table(paste0(data_path(Ns, h_pre, ii)), skip = 1 + therm))
  data <- if (is.null(data)) tmp else rbind(data, tmp)
}

message("bootstrap analysis...")
## bootstrap analysis
pdf(paste0(output_path, "plots/L", Ns,"/bootstrap_analysis_h_", sprintf("%.6f", h_pre),".pdf"))

G <- data[,c(3, 5, 6)]

Time <- ncol(G)

G <- cf_orig(cf = G)
G <- cf_meta(G, nrObs = 1, Time = Time)

suppressMessages(bootstrap.analysis(G$cf[, 1], boot.R = boot.R, boot.l = 2, pl = TRUE))
suppressMessages(bootstrap.analysis(G$cf[, 2], boot.R = boot.R, boot.l = 2, pl = TRUE))
suppressMessages(bootstrap.analysis(G$cf[, 3], boot.R = boot.R, boot.l = 2, pl = TRUE))

dev.off()

## combined histogram

data1 <- as.matrix(read.table(paste0(data_path(16, HH[11], II[1])), skip = 1))
ReL1 <- data1[,3]

data2 <- as.matrix(read.table(paste0(data_path(32, HH[11], II[1])), skip = 1))
ReL2 <- data2[,3]

data3 <- as.matrix(read.table(paste0(data_path(48, HH[11], II[1])), skip = 1))
ReL3 <- data3[,3]

data4 <- as.matrix(read.table(paste0(data_path(64, HH[11], II[1])), skip = 1))
ReL4 <- data4[,3]

pdf(paste0(output_path, "plots/hist_L_h_0.0045_combined.pdf"))

par(mfrow=c(2,2))

hist(ReL1, 75, col="lightgrey", main = paste0("L = 16, h = ", HH[11]))
hist(ReL2, 50,  col="lightblue", main = paste0("L = 32, h = ", HH[11]))
hist(ReL3, 50,  col="lightgreen", main = paste0("L = 48, h = ", HH[11]))
hist(ReL4, 50, col="lightyellow", main = paste0("L = 64, h = ", HH[11]))

par(mfrow=c(1,1))
dev.off()