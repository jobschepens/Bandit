# ---- plotfunctions ----

# predict and hist plots
colSeColMeans <- function(x, na.rm = TRUE) {
	if (na.rm) { 
		n <- colSums(!is.na(x)) 
		p <- colMeans(x, na.rm = T)
	} 
	else {
		n <- nrow(x) 
		p <- colMeans(x)
	}
	return(sqrt((1/n) * p * (1-p)))
}

plottrialsSE <- function(aggrPROB, BIC, group, lgnd, ylb, model = "predicted", 
						 col_se = array(data = 1, dim = c(100, 2*N_BANDITS))) {
	sp = .4 # % of the points
	colors = rainbow(n = 8, start=.7, end=.1)
	x <- seq(1,100)
	ylm = .5
	if (N_BANDITS == 8) {
		ylm = .35
	}
	xl <- seq(min(x),max(x), (max(x) - min(x))/1000)
	plot (xl, predict(loess(aggrPROB[,N_BANDITS + 1]~x, span = sp),xl), 
		  col=colors[1], lty = "solid", type="l", axes=F,  bty="n", xlab="", 
		  ylab = "", xlim=c(1,100), ylim=c(0,ylm), cex.lab=1.4,  lwd=1)
	lines(xl, predict(loess(aggrPROB[,N_BANDITS + 2]~x, span = sp),xl), 
		  col=colors[2], lty = "solid", lwd=1)
	lines(xl, predict(loess(aggrPROB[,N_BANDITS + 3]~x, span = sp),xl), 
		  col=colors[3], lty = "solid", lwd=1)
	lines(xl, predict(loess(aggrPROB[,N_BANDITS + 4]~x, span = sp),xl), 
		  col=colors[4], lty = "solid", lwd=1)
	if (N_BANDITS == 8) {
		l5 <- loess(aggrPROB[,N_BANDITS + 5]~x, span = sp)
		l6 <- loess(aggrPROB[,N_BANDITS + 6]~x, span = sp)
		l7 <- loess(aggrPROB[,N_BANDITS + 7]~x, span = sp)
		l8 <- loess(aggrPROB[,N_BANDITS + 8]~x, span = sp)
		lines(xl, predict(l5,xl), col=colors[5], lty = "solid", lwd=1)
		lines(xl, predict(l6,xl), col=colors[6], lty = "solid", lwd=1)
		lines(xl, predict(l7,xl), col=colors[7], lty = "solid", lwd=1)
		lines(xl, predict(l8,xl), col=colors[8], lty = "solid", lwd=1)
		lines(xl, predict(loess(aggrPROB[,N_BANDITS + 5] + col_se[,N_BANDITS + 5] ~x, 
								span = sp),xl),type="l",col=colors[5], lty = "dashed")
		lines(xl, predict(loess(aggrPROB[,N_BANDITS + 5] - col_se[,N_BANDITS + 5] ~x, 
								span = sp),xl),type="l",col=colors[5], lty = "dashed")
		lines(xl, predict(loess(aggrPROB[,N_BANDITS + 6] + col_se[,N_BANDITS + 6] ~x, 
								span = sp),xl),type="l",col=colors[6], lty = "dashed")
		lines(xl, predict(loess(aggrPROB[,N_BANDITS + 6] - col_se[,N_BANDITS + 6] ~x, 
								span = sp),xl),type="l",col=colors[6], lty = "dashed")
	}
	axis(1,  at=0:2*50, cex.axis=1.2, labels = c("0", "50", "100")) 
	axis(2,  at=0:2*.25,  las=2,  cex.axis=1.2)  
	if(ylb == T) {
		title(ylab = "Proportion of choices",  cex.lab=1.4)
		title(xlab = "Trial",  cex.lab=1.4)
	}
	title(group)
	grid(5, 10)
}

plottrials <- function(aggrPROB, BIC, group, lgnd, ylb, model = "predicted", 
					   col_se = array(data = 1, dim = c(100, 2*N_BANDITS))) {
	sp = .4 # % of the points
	colors = rainbow(n = 8, start=.7, end=.1)
	x <- seq(1,100)
	ylm = .5
	if (N_BANDITS == 8) {
		ylm = .35
	}
	xl <- seq(min(x),max(x), (max(x) - min(x))/1000)
	n1 <- loess(aggrPROB[,1]~x, span = sp)
	n2 <- loess(aggrPROB[,2]~x, span = sp)
	n3 <- loess(aggrPROB[,3]~x, span = sp)
	n4 <- loess(aggrPROB[,4]~x, span = sp)
	l1 <- loess(aggrPROB[,N_BANDITS + 1]~x, span = sp)
	l2 <- loess(aggrPROB[,N_BANDITS + 2]~x, span = sp)
	l3 <- loess(aggrPROB[,N_BANDITS + 3]~x, span = sp)
	l4 <- loess(aggrPROB[,N_BANDITS + 4]~x, span = sp)
	plot (xl, predict(n1,xl), col=colors[1], lty = "dashed", type="l", axes=F,  
		  bty="n", xlab="", ylab = "", xlim=c(1,100), ylim=c(0,ylm), 
		  cex.lab=1.4,  lwd=1)
	lines(xl, predict(n2,xl), col=colors[2], lty = "dashed")
	lines(xl, predict(n3,xl), col=colors[3], lty = "dashed")
	lines(xl, predict(n4,xl), col=colors[4], lty = "dashed")
	lines(xl, predict(l1,xl), col=colors[1], lty = "solid", lwd=1)
	lines(xl, predict(l2,xl), col=colors[2], lty = "solid", lwd=1)
	lines(xl, predict(l3,xl), col=colors[3], lty = "solid", lwd=1)
	lines(xl, predict(l4,xl), col=colors[4], lty = "solid", lwd=1)
	if (N_BANDITS == 8) {
		n5 <- loess(aggrPROB[,5]~x, span = sp)
		n6 <- loess(aggrPROB[,6]~x, span = sp)
		n7 <- loess(aggrPROB[,7]~x, span = sp)
		n8 <- loess(aggrPROB[,8]~x, span = sp)
		l5 <- loess(aggrPROB[,N_BANDITS + 5]~x, span = sp)
		l6 <- loess(aggrPROB[,N_BANDITS + 6]~x, span = sp)
		l7 <- loess(aggrPROB[,N_BANDITS + 7]~x, span = sp)
		l8 <- loess(aggrPROB[,N_BANDITS + 8]~x, span = sp)
		lines(xl, predict(n5,xl), col=colors[5], lty = "dashed")
		lines(xl, predict(n6,xl), col=colors[6], lty = "dashed")
		lines(xl, predict(n7,xl), col=colors[7], lty = "dashed")
		lines(xl, predict(n8,xl), col=colors[8], lty = "dashed")
		lines(xl, predict(l5,xl), col=colors[5], lty = "solid", lwd=1)
		lines(xl, predict(l6,xl), col=colors[6], lty = "solid", lwd=1)
		lines(xl, predict(l7,xl), col=colors[7], lty = "solid", lwd=1)
		lines(xl, predict(l8,xl), col=colors[8], lty = "solid", lwd=1)
	}
	if(lgnd == T) {
		legend("top", 
			   c(model, "observed"), 
			   lty = c("dashed","solid"), 
			   lwd = c(2.5,2.5))
	}
	axis(1,  at=0:2*50, cex.axis=1.2, labels = c("0", "50", "100")) 
	axis(2,  at=0:2*.25,  las=2,  cex.axis=1.2)  
	if(ylb == T) {
		title(ylab = "Proportion of choices",  cex.lab=1.4)
		title(xlab = "Trial",  cex.lab=1.4)
	}
	title(paste(group, sep = ""))
	grid(5, 10)
}


my_gg_plot <- function(data, cdata, var, xlab, color_choose, limits_choose, 
					   breaks_choose, labels_choose){
	data$temp <- data[,var]
	data <- data[is.na(data$temp)==FALSE,]
	ggplot(data, aes(temp, fill = age, colour = age, y = ..density..)) + 
		geom_histogram(aes(), alpha = .5, linetype = "blank", 
					   position = "identity", binwidth = 10) +
		scale_fill_discrete(name = "Age", breaks = c(24, 70), labels = c("YA", "OA")) +
		geom_vline(aes(xintercept=likBB_median.median, colour=age),
				   data=cdata, linetype="dashed", size=1, 
				   alpha = 1, show.legend = FALSE) +
		scale_y_continuous("", 
						   breaks = c(), #0, 1/100, 2/100),
						   labels = expression(), #"0",".01",".02"),
						   expand = c(0,0)) +
		scale_x_continuous(xlab, 
						   limits = limits_choose,
						   breaks = breaks_choose,
						   labels = labels_choose,
						   expand = c(0,0)) +
		theme_bw() + 
		theme(
			legend.position="none",
			panel.grid.minor = element_blank(), 
			panel.grid.major = element_blank(), 
			panel.background = element_blank(),
			panel.border = element_blank(), 
			axis.line = element_line())
}

my_gg_plot_no_legend <- function(data, cdata, var, xlab, color_choose, limits_choose,
								 breaks_choose, labels_choose){
	data$temp <- data[,var]
	data <- data[is.na(data$temp)==FALSE,]
	
	ggplot(data, aes(temp, fill = age, y = ..density..)) + 
		geom_histogram(aes(), alpha = .5, linetype = "blank", 
					   position = "identity", binwidth = 10) +
		geom_vline(aes(colour = age, xintercept=likBB_median.median),
				   data=cdata, linetype="dashed", size=1, 
				   alpha = 1, show.legend = FALSE) +
		# scale_fill_discrete(name = "Age") +
		scale_y_continuous("",
						   breaks = c(), #0, 1/100, 2/100),
						   labels = expression(), #"0",".01",".02"),
						   expand = c(0,0)) +
		scale_x_continuous(xlab,
						   limits = limits_choose,
						   breaks = breaks_choose,
						   labels = labels_choose,
						   expand = c(0,0)) +
		theme_bw() + 
		scale_fill_discrete(name = "Age", breaks = c(24, 70), labels = c("YA", "OA")) +
		theme(
			# legend.position="none",
			legend.position=c(0.27,0.8),
			panel.grid.minor = element_blank(), 
			panel.grid.major = element_blank(), 
			panel.background = element_blank(),
			panel.border = element_blank(), 
			axis.line = element_line())
}
