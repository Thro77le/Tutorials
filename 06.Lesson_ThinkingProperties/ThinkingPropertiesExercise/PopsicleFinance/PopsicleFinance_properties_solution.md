## Valid states
(None, no clear states in the system)

## State transitions
(None, no clear states in the system)

## Variable transitions
1. totalFeesEarnedPerShare is non-decreasing
2. accounts[id].feesCollectedPerShare is non-decreasing

## High-level properties
User balance = ETH + LP_Token + LP_Token_Reward
3. User balance = const when deposit + withdraw/collectFees are called && totalFees didn't increment
4. User balance non-decreasing


## Unit tests
5. deposit:
    delta totalSupply = delta ETH balance
    user ETH balance decrease by X, user Token supply increase by X
6. withdraw:
    delta totalSupply = delta ETH balance
    user ETH balance increase by X, user Token supply decrease by X
7. collectFees:
    total supply is non-decreasing
    user's fees counter is updated to latest counter
    user's rewards is zeroed


<br>

## Prioritizing


### High Priority:
Properties that lead to loss or blockage of deposited funds are HIGH

3, 4, 5, 6

### Medium Priority:
Properties that lead to loss or blockage of additional rewards are MEDIUM

1, 2, 7

### Low Priority:
None