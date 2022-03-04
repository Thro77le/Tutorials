## Valid states
None

## State transitions
None

## Variable transitions
1. balance is changed => transfer/transferFrom/min/burn called
2. TransferFrom decrease allowance
3. mint() called <=> increase supply
4. burn() called <=> decrease supply

## High-level properties
5. Transfer/TransferFrom doesn't inflate/deflate supply
6. `totalSupply` == sum of `balance[user]` for all user

## Unit tests
7. transfer()
8. transferFrom()
9. increase_allowance()
10. decrease_allowance()
11. mint()
12. approve()

<br>

## Prioritizing

### High Priority:
All High-level props
+ 3, 4, 1

### Medium Priority:
All Unit Test props
+ 2

### Low Priority:
