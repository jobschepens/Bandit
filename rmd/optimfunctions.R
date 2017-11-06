# ---- optimfunctions ----

# predict and hist plots
getParams <- function(data, bbanditsfunc) {
	subjects = unique(data$id)
	
	fi_bb <- matrix(data = 0, 
		nrow = length(unique(subjects)), 
		ncol = 6)
	fi_bb[,6] = subjects
	
	for (id in 1:length(unique(subjects))) {  
		print(paste("id  ", id))
		subdata <- data[data$id == unique(subjects)[id],]

		bb.lik <- matrix(data = NA, nrow = 8, ncol = MAXITERBB) 
		bb.tht <- matrix(data = NA, nrow = 8, ncol = MAXITERBB) 

		for (games in 1:length(unique(data$block_id[data$id == unique(subjects)[id]]))) {
			print(paste("game", games))
			gamedata = subdata[subdata$block_id == unique(subdata$block_id)[games],]
			
			if (MAXITERBB > 0 ) {
				for (iter in 1:MAXITERBB) {
					startParm <- runif(length(BB.LB)) * (BB.UB - BB.LB) + BB.LB 
					names(startParm) <- c("theta")
					out <- optim(startParm, bbanditsfunc, game = gamedata, 
								 N_BANDITS = N_BANDITS, 
								 method = "L-BFGS-B", lower = BB.LB, upper = BB.UB)
					whle = 0
					while (out$value == 0 & whle < WHLEBB) {
						# subst BB.UB with 1 to a bit focus less on randomness?
						startParm <- runif(length(BB.LB)) * (1 - BB.LB) + BB.LB 
						names(startParm) <- c("theta")
						out <- optim(startParm, bbanditsfunc, game = gamedata, 
									 N_BANDITS = N_BANDITS, 
									 method = "L-BFGS-B", lower = BB.LB, upper = BB.UB)
						whle = whle + 1
						# print(paste("whle", whle, "tht", round(startParm, digits = 1)))
					}
					if(out$value == 0 | out$value > 300) {
						out$value = NA
						print(paste("OUT VALUE IS IMPOSSIBLE", id, games, sep = " "))
					}
					print(paste("BB ", 
								round(out$value, digits = 1), 
								round(out$par[1], digits = 1)))
					bb.lik[games,iter] <- out$value
					bb.tht[games,iter] <- out$par[1]
				}
			}
		}
		if (MAXITERBB > 0 ) {
			fi_bb[id,1] <- median(apply(bb.lik,1,min), na.rm = T)
			fi_bb[id,2] <- median(apply(bb.tht,1,min), na.rm = T)
			fi_bb[id,3] <- median(apply(bb.tht,1,min), na.rm = T)
		}
	}
	
	fi_bb[,4] <- 2 * fi_bb[,1] + 2 * log(100) # BIC: deviance + #parameters * log(N)
	fi_bb[,5] <- 2 * fi_bb[,1] + 2 * 2        # AIC: deviance + #parameters * 2
	fi_bb
}

getPredictions <- function(data, fi_bb) {
	subjects = unique(fi_bb[,6])

	basescheme = as.data.frame(sort(unique(data$ev)));
	colnames(basescheme)[1] <- "ev"
	
	# 3D array subjects, trials, 8 (q values per trial and choices)
	pr_bb <- array(data = NA, dim = c(length(subjects)*8, 100, 2*N_BANDITS)) 
	for (id in 1:length(unique(subjects))){
		thetaBB <- fi_bb[id,2];
		subdata = data[data$id == unique(subjects)[id],]
		for (games in 1:length(unique(data$block_id[data$id == unique(subjects)[id]]))) {
			gamedata = subdata[subdata$block_id == unique(subdata$block_id)[games],]
			scheme <- getScheme(gamedata, N_BANDITS, basescheme) 
			bantrials <- matrix(data = 0, nrow = 1, ncol = N_BANDITS) 
			wins      <- matrix(data = 0, nrow = 1, ncol = N_BANDITS) 
			
			for (trial in c(0:99)) {
				choice <- gamedata$bandit_real_id[gamedata$trial_number == trial]
				R      <- gamedata$payoff        [gamedata$trial_number == trial]
				ev     <- gamedata$ev            [gamedata$trial_number == trial]
				
				# BB
				probs <- getProbs(wins, bantrials, thetaBB)
				orderedprobs = probs[order(scheme$evorder, decreasing = FALSE)]
				ind <- which(sort(unique(gamedata$ev)) == ev)
				pr_bb[(id - 1) * 8 + games, trial + 1, 1:N_BANDITS] <- orderedprobs
				pr_bb[(id - 1) * 8 + games, trial + 1, N_BANDITS + ind] <- 1
				wins     [choice] <- wins     [choice] + R
				bantrials[choice] <- bantrials[choice] + 1
			}
		}
	}  
	# print(colMeans(pr_bb, dims = 1, na.rm = T))
	pr_bb
}
