# ---- bbanditsfunc ----

bbanditsfunc <- function(param, game, N_BANDITS) {
	theta = param[1]
	lik <- 0 
	bantrials <- matrix(data = 0, nrow = 1, ncol = N_BANDITS) 
	wins      <- matrix(data = 0, nrow = 1, ncol = N_BANDITS) 
	
	if ((theta < 0.005) | (theta > 30)) {
		LL <- -999999	
	} 
	else {
		for (trial in c(0:99)) {
			choice <- game$bandit_real_id[game$trial_number == trial]
			R      <- game$payoff        [game$trial_number == trial]
			probs <- getProbs(wins, bantrials, theta, lik)
			b = probs[choice]
			if (is.nan(b)) 						{b <- 1 / MIN_GRAIN}
		    if (b <= (1 / MIN_GRAIN)) 			{b <- 1 / MIN_GRAIN}
		    if (b >= (MIN_GRAIN - 1)/MIN_GRAIN) {b <- 1}
			lik = lik + log(b)
			wins     [choice] <- wins     [choice] + R
			bantrials[choice] <- bantrials[choice] + 1
		}
	}
	return(-lik)
}