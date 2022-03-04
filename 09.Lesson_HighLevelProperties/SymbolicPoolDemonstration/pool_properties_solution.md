## Valid states
all ERC20 states

## State transitions
all ERC20 State Transitions

## Variable transitions
1. Fee must be within sane bounds at all times (0-1%)
+ all ERC20 Variable Transitions


## High-level properties
2. Pool balance increased by fee when flashloan called
3. Flashloan should revert when assets not returned
4. User can withdraw his assets


## Unit tests
13. calcPremium()
14. withdraw()
15. deposit()
16. sharesToAmount()

<br>

## Prioritizing

### High Priority:
1, 2, 3, 4 + Variable Transitions

### Medium Priority:
Unit tests

### Low Priority:
Valid States & State Transitions