# row = 1
# bandit = 1
# game = gamedata
# subj = 1
# subdata = data[data$id == id,]
# param = startParm
# N_BANDITS = 4
# games = 1
# trial = 0
# R = 0


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
			
			##
			# a 	   <- 1 + wins
			# b      <- 1 + bantrials - wins
			# xpoints 	<- matrix(data = 0, nrow = MAX_CHOICESB-1, ncol = N_BANDITS)
			# probability <- seq(from = 0 + (1/MAX_CHOICESB), to = (1-1/MAX_CHOICESB), by = 1/MAX_CHOICESB)
			# for (bandit in 1:N_BANDITS) {
			# 	xpoints[,bandit] <- qbeta(probability, a[bandit], b[bandit])
			# }
			# choices = matrix(data = 0, nrow = N_BANDITS, ncol = 1) 
			# for (row in 1:(MAX_CHOICESB-1)) {
			# 	idx          <- which(xpoints[row,] == max(xpoints[row,], na.rm = TRUE))
			# 	choices[idx] <- choices[idx] + 1
			# }
			# p = choices / (MAX_CHOICESB-1)
			# probs <- softmax(p, theta)
			## 
			probs <- getProbs(wins, bantrials, theta, lik)
			
			b = probs[choice]
			
			lik = lik + log(b)
			
			wins     [choice] <- wins     [choice] + R
			bantrials[choice] <- bantrials[choice] + 1
		}
	}
	return(-lik)
}
# 
# data <- data[data$id %in% c(5), ]
# subjects = unique(data$id)
# subdata = data[data$id == unique(subjects)[id],] 
# 	
# 
# STEP = 10
# thetastep = 1/STEP # step size, 0 <= theta
# startPabb <- c(1);   names(startParm) <- c("theta")
# lbb <- matrix(data = 0, nrow = 8, ncol = 3) # save log likelihood per game
# for (games in 1:length(unique(data$block_id[data$id == unique(subjects)[id]]))) {
# 	gamedata = subdata[subdata$block_id == unique(subdata$block_id)[games],]
# 	bestfit = 888888;
# 	bestfbb = 888888;
# 	for (theta in seq(0.005, 5, thetastep)) {
# 		startPabb <- c(theta)
# 		fit = bbanditsfunc(startParm, game = gamedata, N_BANDITS)
# 		if (fit < bestfit){
# 			bestfit <- fit
# 			lbb[games,1] <- round(bestfit, digits = 2)
# 			lbb[games,2] <- 0
# 			lbb[games,3] <- theta
# 		}
# 	}
# 	print(games)
# }
# print(id)
# print(games)
# lbb
