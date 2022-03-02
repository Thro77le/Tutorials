methods {
    // ERC20 methods
	totalSupply() returns (uint256) envfree
    balanceOf(address) returns (uint256) envfree
    transfer(address, uint256) returns (bool)
    allowance(address, address) returns (uint256) envfree
    approve(address, uint256) returns (bool)
    transferFrom(address, address, uint256) returns (bool)
    increase_allowance(address to_user, uint inc_amount)
    decrease_allowance(address from_user, uint dec_amount)

    // Spartan methods
    init_pool()
    add_liquidity() returns uint
    remove_liquidity(uint LP_tokens)
    swap(address from_token)
    sync()
    token0Amount() returns uint envfree
    token1Amount() returns uint envfree
    K() returns uint envfree
    token0() returns address envfree
    token1() returns address envfree
    owner() returns address envfree
}

// Valid state
definition validAMM() returns bool = K() == token0Amount() * token1Amount();

// High level
// total funds == sum of users funds
// WILL FAIL because init_pool() can be called more than once
invariant totalFunds_GE_single_user_funds()
    forall address user. totalSupply() >= balanceOf(user)

ghost sum_of_all_funds() returns uint256 {
    init_state axiom sum_of_all_funds() == 0;
}

hook Sstore balances[KEY address user] uint256 new_balance
    (uint256 old_balance) STORAGE {
        havoc sum_of_all_funds assuming sum_of_all_funds@new() == sum_of_all_funds@old() + new_balance - old_balance;
    }

invariant totalFunds_GE_to_sum_of_all_funds()
    totalSupply() == sum_of_all_funds()


// High level - SHOULD FAIL because of bug
// Init pool can be called only once
//@note: is it better to check this property as written below or is it better to check: `(K=0 ~> K!=0) => init_pool() called`
rule initPoolCanBeCalledOnlyOnce() {
    env e;
    require validAMM();
    requireInvariant totalFunds_GE_to_sum_of_all_funds();

    init_pool(e);
    init_pool@withrevert(e);

    assert lastReverted, "Second init should revert";
}

// rule cantMintForFree(method f) {
//     calldataarg arg;
//     env e;
//     require e.msg.sender != 0;
//     require validAMM();
//     requireInvariant totalFunds_GE_to_sum_of_all_funds();

//     uint256 KBefore = K();
//     uint256 balanceBefore = balanceOf(e.msg.sender);

//     add_liquidity(e);

//     uint256 KAfter = K();
//     uint256 balanceAfter = balanceOf(e.msg.sender);

//     assert KBefore == KAfter, "K value is not maintained";
//     assert balanceBefore == balanceAfter, "User LP Token balance changed";
// }

// THIS WILL FAIL FOR PRECISION REASONS
// rule addAndRemoveShouldBeIdentityFunction(method f) {
//     calldataarg arg;
//     env e;
//     require e.msg.sender != 0;
//     require validAMM();
//     requireInvariant totalFunds_GE_to_sum_of_all_funds();

//     uint256 KBefore = K();

//     // User has to start with 0 LP tokens
//     // because otherwise it is possible to swap back too much
//     uint256 balanceBefore = balanceOf(e.msg.sender);
//     require balanceBefore == 0;

//     uint256 amount = add_liquidity(e);
//     remove_liquidity(e, amount);

//     uint256 KAfter = K();
//     uint256 balanceAfter = balanceOf(e.msg.sender);

//     assert KBefore == KAfter, "K value is not maintained";
//     assert balanceBefore == balanceAfter, "User LP Token balance changed";
// }

// rule swapAndSwapBackShouldBeIdentityFunction(method f) {
//     calldataarg arg;
//     env e;
//     require e.msg.sender != 0;
//     require validAMM();

//     uint256 amount0Before = token0Amount();
//     uint256 amount1Before = token1Amount();
//     uint256 KBefore = K();

//     // User has to start with 0 LP tokens
//     // because otherwise it is possible to swap back too much
//     uint256 balanceBefore = balanceOf(e.msg.sender);
//     require balanceBefore == 0;

//     swap(e, token0());
//     swap(e, token1());

//     uint256 amount0After = token0Amount();
//     uint256 amount1After = token1Amount();
//     uint256 KAfter = K();
//     uint256 balanceAfter = balanceOf(e.msg.sender);

//     assert amount0Before == amount0After, "Token0 Pool balance changed";
//     assert amount1Before == amount1After, "Token1 Pool balance changed";
//     assert KBefore == KAfter, "K value is not maintained";
//     assert balanceBefore == balanceAfter, "User LP Token balance changed";
// }

// High level
rule swapShouldMaintainAMMInvariant(method f) {
    calldataarg arg;
    env e;
    require e.msg.sender != 0;
    require validAMM();
    requireInvariant totalFunds_GE_to_sum_of_all_funds();

    uint256 amount0Before = token0Amount();
    uint256 amount1Before = token1Amount();
    uint256 KBefore = K();

    swap(e, arg);

    uint256 amount0After = token0Amount();
    uint256 amount1After = token1Amount();
    uint256 KAfter = K();

    assert KBefore == KAfter, "K value is not maintained";
}
