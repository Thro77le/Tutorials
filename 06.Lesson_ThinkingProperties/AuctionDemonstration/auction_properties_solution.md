# Valid states:
1. AuctionNotCreated/AuctionDeleted - all fields 0
2. AuctionCreated - `winner != 0 && payment > 0 && bid_expiry > 0 && end_time >0`

# State Transitions:
1. UNINIT => UNINIT | STARTED

   (UNINIT ~> STARTED) => method=newAuction()

2. STARTED => STARTED | UNINIT

    (STARTED ~> UNINIT) => method=close()


# Variable transitions:
1. prize cant increase
2. prize is strictly decreasing in STARTED state when bid()
3. bid_expiry cant decrease
4. bid_expiry is strictly increasing +h in STARTED state when bid()

# Unit test
1. bid()
    - doesn't change state
    - moves funds amount=payment
    - sets sender as winner
    - delays bid_expiry by 1 hr
    - decreases prize

2. close()
    - changes state to UNINIT
    - moves funds amount=prize

3. mint()
    - increases total supply and user balance

4. transferTo()
    - total funds doesn't change


# High-level
1. Auction cant be deleted otherwise than via calling close() when time is right
2. Supply is const or non-decreasing when calling close()