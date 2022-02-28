## Valid states
1. EventUninitialized = all values 0
2. EventCreated = owner, ticketPRice != 0
3. OfferUninitialized = all values 0
4. OfferCreated = all values != 0

## State transitions
5. EventUninitialized => EventUninitialized | EventCreated
6. (EventUninitialized ~> EventCreated) => createEvent() called
7. OfferUninitialized => OfferUninitialized | OfferCreated
8. (OfferUninitialized ~> OfferCreated) => offerTicket() called

## Variable transitions
9. numEvent is non-decreasing
10. eventsMap[id].ticketsRemaining is non-increasing (if Event created)

## High-level properties
11. Contract ETH balance is 0 at all times

## Unit tests
12. buyNewTicket():
    balances are updated correctly between buyer, eventowner and system owner
    remainign tickets is decreased by 1
    buyer is in atendee mapping

13. offerTicket():
    deadline is in the future
    balances are updated correctly between seller and system owner
    buyer is not present in atendee mapping
    offer is created

14. buyOfferedTicket():
    deadline is respected
    balances are updated correctly between buyer, seller and system owner
    atendees are updated correctly, buer is there, seller is not there


<br>

## Prioritizing


### High Priority:
Properties that are related to moving funds are HIGH

11, 12, 13, 14

### Medium Priority:
Properties that lead to DoS or ticket stealing are MEDIUM

9, 10

### Low Priority:
State validity and transitions

1,2,3,4,5,6,7,8