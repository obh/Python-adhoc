import numpy as np
from collections import namedtuple


class BayesianBandit:
    """
    Thompson Sampling

    Parameters
    ----------
    K : int
        total number of arms
    
    prior_params : list of float length 2 tuple, default None, (optional)
        each element of the list is a tuple, where each tuple
        contains the alpha and beta parameter that represents the prior
        beta distribution for each arm. If not supplied
        it will assume that all arms's prior starts with an uniform distribution
        
    Attributes
    ----------
    trials, success : int 1d ndarray, shape [K,]
        stores the trials and success for each arm,
        e.g. trial = [ 1, 1 ] and success = [ 0, 1 ] means 
        that both arm has been pulled once and arm 1 has generated
        the reward (clicked)
    """
    
    def __init__(self, K, prior_params=None):
        if prior_params:
            priors = namedtuple("priors", ["alpha", "beta"])
            prior = [priors(*p) for p in prior_params]
            self.alphas = np.array([p.alpha for p in prior])
            self.betas = np.array([p.beta  for p in prior])
        else:
            self.alphas = np.ones(K)
            self.betas = np.ones(K)

        self.trials = np.zeros(K, dtype=np.int)
        self.success = np.zeros(K, dtype=np.int)

    def get_recommendation(self):        
        """
        for all arms, construct their beta distribution and
        draw a random sample from it, then return the arm
        with the maximum value random sample 
        """
        print(self.alphas)
        print(self.success)
        print(self.betas)
        print(self.trials - self.success)
        theta = np.random.beta(self.alphas + self.success, 
                               self.betas + self.trials - self.success)
        theta = np.random.beta(self.alphas , 
                               self.betas)
        print(theta)
        print("-------")
        return np.argmax(theta)

    def update_result(self, arm, converted):
        """
        override the trials and success array, the success array
        will only be updated if it has generated a reward
        """
        self.trials[arm] += 1
        if converted:
            self.success[arm] += 1
            
        return self

def experiment(T, ctr, prior_params=None):
    """
    run the experiment for Thompson Sampling,
    pass in ctr, the fixed ctr for each arm
    or K, the total number of arms to run the experiment,
    if K is supplied then it will be randomly generated
    
    Parameters
    ----------
    T : int
        number of simulation in an experiment

    ctr : float sequence, len = K (total number of arms)
        the empirical click through rate for each arm
        
    prior_params : list of float length 2 tuple, default None, (optional)
        each element of the list is a tuple, where each tuple
        contains the alpha and beta parameter that represents the prior
        beta distribution for each arm. If not supplied
        it will assume that all arms's prior starts with an uniform distribution
    
    Returns
    -------
    ctr : float sequence, len = K
        the supplied or the randomly generated ctr
    
    trials, success : int 2d ndarray, shape [T, K]
        trials and success recorded for each turn of the experiment
        
    alphas, betas : float 1d ndarray, shape [K,]
        the alpha and beta parameters for each arm
    """
    K = len(ctr)
    trials = np.zeros((T, K), dtype=np.int)
    success = np.zeros((T, K), dtype=np.int)

    bayes_bandit = BayesianBandit(K, prior_params)
    for t in range(T):
        arm = bayes_bandit.get_recommendation()
        converted = np.random.rand() < ctr[arm]
        #bayes_bandit.update_result(arm, converted)
        # what if we do not update the result? 
        bayes_bandit.update_result(arm, False)
        trials[t] = bayes_bandit.trials
        success[t] = bayes_bandit.success

    return ctr, trials, success, bayes_bandit.alphas, bayes_bandit.betas

# number of simulation in an experiment
T = 10000

# the empirical click through rate for each arm
ctr = 0.25, 0.35

ctr, trials, success, alphas, betas = experiment(T=T, ctr=ctr, prior_params=[(60, 40), (40,60)])
print(trials)
