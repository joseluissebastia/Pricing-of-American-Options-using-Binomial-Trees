# Pricing of American Options using Binomial Trees
## Description
binomial_pricing.py provides a simple script in order to price American option on dividend paying stocks.
Binomial trees are often used for option pricing because they offer a simple yet flexible framework for modeling the evolution of an underlying asset's price over time. 

American options are similar to European options, but with the difference that they can be exercised at any point in time before expiration. <br />
The payoff for an american option at expiration is given in the following table:

|Option|Payoff|
|------|------|
|Call  | $(S_{T} - K)^{+}$|
|Put   | $(K - S_{T})^{+}$|

 where: <br />
 $S_{T}$: price of the underlying at expiration <br />
 K: Strike price <br />


 binomial_pricing.py includes an *AmericanOption* class that must be provided with the following parameters in order:
 1. Option Type:
 - call 
 - put
2. Starting Price
3. Strike Price
4. Time left to maturity in years
5. annual volatility (between 0 and 1) 
6. annual risk free rate 
7. dividends (list of tuples where the first element of the tuple is the amount paid, the second element is the time left until it's paid in years.)

In order to price the option, the *binomial_tree_pricing* method must be used. The method takes in as an input the amount of steps to be used in the binomial tree.

## Example
Suppose we have a contract with the following specifications:
1. Option Type: call 
3. Starting Price: 100
3. Strike Price:100
4. Time left to maturity in years: 1
5. annual volatility (between 0 and 1): 0.25 (25%)
6. annual risk free rate: 0.04 (4%)
7. dividens: [\(2,0.75\)]  (a dividend of $2 in 0.75 years time)

and we want the binomial tree to consist of 1000 steps

```
option = AmericanOption("call",100,100,1,0.25,0.04,[(2,0.75)])
option.contract_specification()
option.binomial_tree_pricing(1000)
```

This gives us the following output

```
Contract Specifications
-----------------------------------------------------------------------
Option type:                    call
Initial price:                  100
Strike price:                   100
Time to maturity (in years):    1
Annual volatility:              0.25
Annual risk free rate:          0.04
Dividends:                      [(2, 0.75)]

Estimated contract value: 11.064426299681479
```

## Requirements
numpy >= 1.25.2
