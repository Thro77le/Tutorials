methods {
    getPointsOfContender(address) returns(uint256) envfree
    hasVoted(address) returns(bool) envfree
    getWinner() returns(address, uint256) envfree
    getFullVoterDetails(address) returns(uint8, bool, bool, uint256, bool) envfree
    getFullContenderDetails(address) returns(uint8, bool, uint256) envfree
    registerVoter(uint8) returns (bool)
    registerContender(uint8) returns (bool)
    vote(address, address, address) returns(bool)
}

function isVoterRegistered(address voter) returns bool {
    uint256 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return registered;
}

function didVoterVote(address voter) returns bool {
    uint256 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return voted;
}

function isContenderRegistered(address contender) returns bool {
    uint8 age; bool registered; uint256 points;
    age, registered, points = getFullContenderDetails(contender);
    return registered;
}

function isBlocked(address voter) returns bool {
    uint256 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return blocked;
}

function getContenderPoints(address contender) returns uint256 {
    uint8 age; bool registered; uint256 points;
    age, registered, points = getFullContenderDetails(contender);
    return points;
}

definition unRegisteredVoter(address voter) returns bool = !isVoterRegistered(voter);
definition registeredYetVotedVoter(address voter) returns bool = isVoterRegistered(voter) && !didVoterVote(voter);
definition legitRegisteredVotedVoter(address voter) returns bool = isVoterRegistered(voter) && didVoterVote(voter) && !isBlocked(voter);
definition blockedVoter(address voter) returns bool = isBlocked(voter);




// Checks that a voter's "registered" mark is changed correctly -
// If it's false after a function call, it was false before
// If it's true after a function call, it either started as true or changed from false to true via registerVoter()
rule registeredCannotChangeOnceSet(method f, address voter) {
    env e;
    calldataarg args;
    bool voterRegBefore = isVoterRegistered(voter);

    f(e, args);

    bool voterRegAfter = isVoterRegistered(voter);

    assert (!voterRegAfter => !voterRegBefore, "voter changed state from registered to not registered after a function call");
    assert (voterRegAfter =>
        ((!voterRegBefore && f.selector == registerVoter(uint8).selector) || voterRegBefore),
            "voter was registered from an unregistered state, by other function then registerVoter()");
}

// Checks that each voted contender receieves the correct amount of points after each vote
rule correctPointsIncreaseToContenders(address first, address second, address third) {
    env e;
    uint256 firstPointsBefore = getPointsOfContender(first);
    uint256 secondPointsBefore = getPointsOfContender(second);
    uint256 thirdPointsBefore = getPointsOfContender(third);

    vote(e, first, second, third);

    uint256 firstPointsAfter = getPointsOfContender(first);
    uint256 secondPointsAfter = getPointsOfContender(second);
    uint256 thirdPointsAfter = getPointsOfContender(third);

    assert (firstPointsAfter - firstPointsBefore == 3, "first choice receieved other amount than 3 points");
    assert (secondPointsAfter - secondPointsBefore == 2, "second choice receieved other amount than 2 points");
    assert (thirdPointsAfter - thirdPointsBefore == 1, "third choice receieved other amount than 1 points");

}

// Checks that a blocked voter cannot get unlisted
rule onceBlockedNotOut(method f, address voter) {
    env e;
    calldataarg args;
    bool blocked_before = isBlocked(voter);
    bool registeredBefore = isVoterRegistered(voter);
    require blocked_before => registeredBefore;

    f(e, args);

    bool blocked_after = isBlocked(voter);

    assert blocked_before => blocked_after, "the specified user got out of the blocked users' list";
}

// Checks that a contender's point count is non-decreasing
rule contendersPointsNondecreasing(method f, address contender) {
    env e;
    calldataarg args;
    bool registeredBefore = isContenderRegistered(contender);
    uint256 pointsBefore = getContenderPoints(contender);
    require pointsBefore > 0 => registeredBefore;

    f(e,args);

    uint256 pointsAfter = getContenderPoints(contender);

    assert (pointsAfter >= pointsBefore);
}
