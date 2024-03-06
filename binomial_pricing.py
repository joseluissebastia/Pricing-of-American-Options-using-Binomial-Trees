import numpy as np
import matplotlib.pyplot as plt
import sys

class AmericanOption():
    def __init__(self, option_type, S0, K, T, volatility, risk_free_rate, dividends=None):
        """
        Parameters
        ----------
            option_type      (str): "call" or "put"
            S0             (float): initial price
            K              (float): strike price
            T              (float): time to maturity in years
            volatility     (float): annual volatility of underlying
            risk_free_rate (float): annual risk free rate
            dividends       (list): list of dividends paid out. Each element of the list is a tuple. The first element of the tuple is the amount paid, the second element is the time left until it's paid in years. Example: [(2,0.15),(1,0.3)] consists of two dividends, the first one pays $2 in 0.15 years, the second one pays $1 in 0.3 years.
        """
        if option_type != "call" and option_type != "put":
            print('Error!\nPlease make sure option_type="call" or option_type="put"')
            sys.exit()

        if volatility < 0 or volatility > 1:
            print("Error!\nPlease make sure 0 <= volatility <= 1")
            sys.exit()
        

        self.option_type    = option_type
        self.S0             = S0
        self.K              = K
        self.T              = T
        self.volatility     = volatility
        self.risk_free_rate = risk_free_rate
        self.dividends       = dividends


    def contract_specification(self) -> None:
        """
        Display contract specifications
        """
        print("\nContract Specifications")
        print("-----------------------------------------------------------------------")
        print(f"Option type:                    {self.option_type}")
        print(f"Initial price:                  {self.S0}")
        print(f"Strike price:                   {self.K}")
        print(f"Time to maturity (in years):    {self.T}")
        print(f"Annual volatility:              {self.volatility}")
        print(f"Annual risk free rate:          {self.risk_free_rate}")
        print(f"Dividends:                      {self.dividends}")

    
    def present_value(self, value):
        """
        Calculate the present value of future cashflows 

        Paramters
        ---------
            value (list of floats): values to be discounted 

        Returns
        --------
            pv    (list of floats): present value 
        """
        pv = np.array(value)*np.exp(-self.risk_free_rate*self.T)
        return pv
    

    def vanilla_payoff(self, expiration_prices):
        """
        Given the price of the underlying at maturity, calculate the payoff of the vanilla option

        Parameters
        ----------
            expiration_prices (list of floats): price of the underlying at maturity

        Returns
        ----------
            payoff            (list of floats): payoff 
        """

        if self.option_type == "call":
            payoff = np.maximum(expiration_prices - self.K, 0)
        
        #if self.option_type == "put"
        else:
            payoff = np.maximum(self.K - expiration_prices, 0)

        return payoff
    

    def binomial_tree_pricing(self,steps):
        """
        Calculates the value of an American option using Binomial Trees

        Parameters
        ----------
            steps             (int): number of steps

        Returns
        ----------
            estimated_value (float): estimated value for the options contract
        """
        u = np.exp(self.volatility*np.sqrt(self.T/steps))
        d = 1/u

        p = (np.exp(self.risk_free_rate*self.T/steps) - d)/(u-d)
        
        paid_dividends = np.zeros(steps + 1)
        date_of_steps = np.linspace(0, self.T, steps+1)
        if self.dividends != None:
            for dividend in self.dividends:
                pay = np.where(date_of_steps > dividend[1], 1, 0)
                paid_dividends += dividend[0]*pay


        tree = [[None] * (steps+1) for _ in range(steps+1)] #Initialize list full of none's
        for j in range(steps,-1,-1):
            for i in range(j,-1,-1):
                #Please note that the the second index on our tree is inverted to the usual notation, with the branch with the lowest price having the highest index and the branch with the highest price having the lowest index.
                price = self.S0*np.power(d,i)*np.power(u,j-i) - paid_dividends[j]
                intrinsic_value = self.vanilla_payoff(price)
                continuation_value = 0

                if j != steps:
                    continuation_value = (tree[j+1][i]['option_value']*p + tree[j+1][i+1]['option_value']*(1-p))*np.exp(-self.risk_free_rate*(self.T/steps))

                tree[j][i] = {'option_value': np.maximum(continuation_value, intrinsic_value), 'price': price}


        estimated_value = tree[0][0]['option_value']
        print(f"\nEstimated contract value: {estimated_value}")
        return estimated_value
                

if __name__ == "__main__":
    option = AmericanOption("call",100,100,1,0.25,0.04,[(2,0.75)])
    option.contract_specification()
    option.binomial_tree_pricing(1000)