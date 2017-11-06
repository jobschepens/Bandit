# ---- optimfunctions ----

softmax <- function(Q, theta) {
	e = exp(Q / theta)
	# e = exp(theta * Q)
	# e = exp(((3^theta)-1) * Q)
	# e = exp((((trial + 1)/100)^theta) * Q)
	probs = e / sum(e)
	probs
}
getScheme <- function(game, N_BANDITS, basescheme) {
	# trial numbers of first time choice for each bandit
	oc        <- match(unique(game$bandit_real_id), game$bandit_real_id) 
	newscheme <- as.data.frame(cbind(game$ev[oc],   game$bandit_real_id[oc]))
	scheme    <- merge(basescheme, newscheme, by.x = "ev", by.y = "V1", all.x = T)
	scheme    <- scheme[order(scheme[,1], decreasing = FALSE),]
	scheme$evorder <- 1:N_BANDITS
	scheme    <- scheme[order(scheme[,2], decreasing = FALSE),]
	scheme$V2[is.na(scheme$V2)] <- c(1:N_BANDITS)[(scheme$V2 %in% 1:N_BANDITS) == F]
	return(scheme)
}
getProbs <- function (wins, bantrials, theta, lik = 0) {
	a 	   <- 1 + wins
	b      <- 1 + bantrials - wins
	xpoints 	<- matrix(data = 0, nrow = MAX_CHOICESB-1, ncol = N_BANDITS)
	probability <- seq(from = 0 + (1/MAX_CHOICESB), 
					   to = (1-1/MAX_CHOICESB), by = 1/MAX_CHOICESB)
	for (bandit in 1:N_BANDITS) {
		xpoints[,bandit] <- qbeta(probability, a[bandit], b[bandit])
	}
	choices = matrix(data = 0, nrow = N_BANDITS, ncol = 1) 
	for (row in 1:(MAX_CHOICESB-1)) {
		idx          <- which(xpoints[row,] == max(xpoints[row,], na.rm = TRUE))
		choices[idx] <- choices[idx] + 1
	}
	p = choices / (MAX_CHOICESB-1)
	probs <- softmax(p, theta)
	
	# probs <- c(.25, .25, .25, NA)
	# probs <- c(.25, .25, .25, .0001)
	# probs <- c(.25, .25, .25, .25)
	if (sum(is.nan(probs)) > 0 | sum(is.na(probs)) > 0) { 
		# print("aap")
		# print(cat("lik:", lik, "alpha:", alpha, "theta:", theta, "tr:", trial,
		# 		  "QQ:",    round(Q       , digits = 2),
		# 		  "probs:", round(t(probs), digits = 2),
		# 		  " wins: ", wins, " trials: ", bantrials, "click: ", choice,
		# 		  collapse = " "))
		## throw error
	}
	probs[is.nan(probs)]            <- 1 / MIN_GRAIN
	probs[is.na(probs)]             <- 1 / MIN_GRAIN 
	probs[probs <= (1 / MIN_GRAIN)] <- 1 / MIN_GRAIN
	# probs[probs >= .999]            <- 1
	probs
}
getBaseline <- function(game, N_BANDITS) { 
	# game = gamedata
	lik = 0
	probs <- table(game$bandit_real_id)/100
	for (trial in c(0:99)) {
		choice <- game$bandit_real_id[game$trial_number == trial]
		R      <- game$payoff        [game$trial_number == trial]
		b 	   <- probs[choice]
	    if (is.nan(b)) {
	    	b <- 1 / MIN_GRAIN 
	    }
	    if (b <= (1 / MIN_GRAIN)) {
	    	b <- 1 / MIN_GRAIN 
	    }
	    if (b >= (MIN_GRAIN - 1)/MIN_GRAIN) {
	    	b <- 1
	    }		
		lik    <- lik + log(b)
		# print(paste(choice, log(b)))
	}
	lik
	return(-lik)
}