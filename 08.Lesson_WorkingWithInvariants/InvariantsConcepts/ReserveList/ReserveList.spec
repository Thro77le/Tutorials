methods {
    getTokenAtIndex(uint256 index) returns (address) envfree
    getIdOfToken(address token) returns (uint256) envfree
    getReserveCount() returns (uint256) envfree
    addReserve(address token, address stableToken, address varToken, uint256 fee) envfree
    removeReserve(address token) envfree
}


// Both lists are correlated - If we use the id of a token in reserves to retrieve a token in underlyingList, we get the same token.
invariant dataStructuresAreCorrelated(uint256 id)
    getTokenAtIndex(id) != 0 => getIdOfToken(getTokenAtIndex(id)) == id

// There should not be a token saved at an index greater or equal to reserve counter.
//@note it will fail because the code doesn't guarantee this property
invariant noReserveWithIndexAboveCounter(address token)
    getIdOfToken(token) < getReserveCount() || (getReserveCount() == 0 && token == 0)

// Id of assets is injective (i.e. different tokens should have distinct ids).
invariant injectivenessOfAssetIds(address token1, address token2)
    (token1 != token2 && getTokenAtIndex(getIdOfToken(token1)) == token1 && getTokenAtIndex(getIdOfToken(token2)) == token2) => (getIdOfToken(token1) != getIdOfToken(token2))


// Independency of tokens in list - removing one token from the list doesn't affect other tokens.
rule independencyOfTokens() {
    env e;
    address token;
    require token != 0;
    require getTokenAtIndex(getIdOfToken(token)) == token;

    address other_token;
    require other_token != 0;
    require getTokenAtIndex(getIdOfToken(other_token)) == other_token;
    require token != other_token;
    uint256 other_token_id = getIdOfToken(other_token);

    removeReserve(token);

    assert other_token_id == getIdOfToken(other_token);
    assert getTokenAtIndex(getIdOfToken(other_token)) == other_token, "Other Token still exists";
}

// Each non-view function changes reservesCount by 1.
rule reservesCountMovesByOne(method f) {
    calldataarg arg;
    env e;
    uint256 countBefore = getReserveCount();
    require f.selector == addReserve(address,address,address,uint256).selector || f.selector == removeReserve(address).selector;

    f(e, arg);

    uint256 countAfter = getReserveCount();

    assert countAfter - countBefore == 1 || countBefore - countAfter == 1;
    // if (f.selector == addReserve(address,address,address,uint256).selector) {
    //     assert countBefore + 1 == countAfter, "Add Reserve didnt increment";
    // } else if (f.selector == removeReserve(address).selector) {
    //     assert countBefore - 1 == countAfter, "Remove Reserve didnt increment";
    // }
    // assert true; // last statement of a rule must be an assert command
}
