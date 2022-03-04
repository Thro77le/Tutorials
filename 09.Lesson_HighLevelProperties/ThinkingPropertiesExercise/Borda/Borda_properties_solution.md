## Valid states
1. UnregisteredVoter
2. UnregisteredContender
3. RegisteredVoterCanVote
4. RegisteredVoterCannotVote
5. RegisteredContender

## State transitions
6. (UnregisteredContender ~> RegisteredContender) => registerContender() called
7. (UnregisteredVoter ~> RegisteredVoterCanVote) => registerVoter() called
8. (RegisteredVoterCanVote ~> RegisteredVoterCannotVote) => vote() called
9. UnregisteredContender ~> {UnregisteredContender | RegisteredContender}
10. UnregisteredVoter ~> {UnregisteredVoter | RegisteredVoterCanVote}
11. RegisteredVoterCanVote ~> {RegisteredVoterCanVote | RegisteredVoterCannotVote}

## Variable transitions
12. `pointsOfWinner` is non-decreasing
13. `pointsOfWinner` increased => vote() called
14. `_blackList.length` is non-decreasing
15. `_blackList.length` increased => vote() called
16. `winner` changed => vote() called
17. Contenders points is non-decreasing
18. Age cannot change
19. Vote attempts is non-decreasing and max 3.

## High-level properties
20. Registered voter/contender cannot be unregistered
21. Blacklisted voter cannot be unblacklisted.
22. Invariant: `winner` has `pointsOfWinner` points at all times
23. Once voted is true cannot be false in the future.

## Unit tests
24. vote()
25. registerVoter()
26. registerContender()

<br>

## Prioritizing

### High Priority:
All High-level props
+ 17, 19

### Medium Priority:
All Unit Test props
+ 12, 13, 14, 15, 16, 18

### Low Priority:
Valid States and State Transitions
