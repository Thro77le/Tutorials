## Valid states
1. Uninitialized
2. Initialized
+ all ERC20 states

## State transitions
3. Uninitialized ~> {Uninitialized | Initialized}
4. (Uninitialized ~> Initialized) => `init_pool()` was called
+ all ERC20 State Transitions

## Variable transitions
all ERC20 Variable Transitions

## High-level properties
5. `init_pool()` can be called only once
6. `swap()` and then `swap()` back should be identity function (consider arithmetic rounding)
7. `add_liquidity()` and then `remove_liquidity()` should be identity function (consider arithmetic rounding)
8. `add_liquidity()` should increase K
9. `remove_liquidity()` should decrease K
10. `swap()` should maintain K
11. totalSupply of LP Token should be equal to all users sum of LP token
12. can't mint for free


## Unit tests
13. add_liquidity()
14. remove_liquidity()
15. swap()
16. init_pool()
17. sync()

<br>

## Prioritizing

### High Priority:
All High-level props

### Medium Priority:
Unit tests

### Low Priority:
Valid States & State Transitions