methods {
    deposit()
    withdraw(uint amount)
    OwnerDoItsJobAndEarnsFeesToItsClients()
    assetsOf(address user) returns uint  envfree
    transfer(address recipient, uint256 amount) returns bool
    transferFrom(address sender, address recipient, uint256 amount) returns (bool)
    balanceOf(address account) returns (uint256) envfree
    approve(address spender, uint256 amount) returns bool
    increase_allowance(address to_user, uint inc_amount)
    decrease_allowance(address from_user, uint dec_amount)
    usersSharesAccumulator(address user) returns uint envfree
    totalSharesAccumulator() returns uint envfree
}

//@note: this will fail on 3 functions. These fails uncover bug that leads to Popsicle Finance Hack
rule sharesAccumulatorShouldBeUpdatedOnLPTokenBalanceChange(method f) {
    calldataarg arg;
    env e;
    address user;
    require user != 0;
    uint256 balanceBefore = balanceOf(user);

    f(e, arg);

    uint256 balanceAfter = balanceOf(user);
    uint256 userSharesAccumulatorAfter = usersSharesAccumulator(user);
    uint256 totalSharesAccumulator = totalSharesAccumulator();

    assert balanceAfter != balanceBefore => userSharesAccumulatorAfter == totalSharesAccumulator;
}

rule totalFeesEarnedPerShareNotDecreasing(method f) {
    calldataarg arg;
    env e;
    uint256 totalSharesAccumulatorBefore = totalSharesAccumulator();

    f(e, arg);

    uint256 totalSharesAccumulatorAfter = totalSharesAccumulator();

    assert totalSharesAccumulatorBefore <= totalSharesAccumulatorAfter;
}

rule userFeesEarnedPerShareNotDecreasing(method f) {
    calldataarg arg;
    env e;
    address user;
    require user != 0;
    uint256 userSharesAccumulatorBefore = usersSharesAccumulator(user);

    f(e, arg);

    uint256 userSharesAccumulatorAfter = usersSharesAccumulator(user);

    assert userSharesAccumulatorBefore <= userSharesAccumulatorAfter;
}


rule depositUnitTest() {
    env e;
    address user = e.msg.sender;
    require user != 0;
    uint256 balanceBefore = balanceOf(user);

    deposit(e);

    uint256 balanceAfter = balanceOf(user);
    assert balanceAfter - balanceBefore == e.msg.value, "Balance didnt increment";

    uint256 totalSharesAccumulatorAfter = totalSharesAccumulator();
    uint256 userSharesAccumulatorAfter = usersSharesAccumulator(user);
    assert userSharesAccumulatorAfter == totalSharesAccumulatorAfter, "Deposit should update sharesAccumulator";
}

rule withdrawUnitTest() {
    env e;
    uint256 amount;
    address user = e.msg.sender;

    require user != 0;
    uint256 balanceBefore = balanceOf(user);

    withdraw(e, amount);

    uint256 balanceAfter = balanceOf(user);
    assert balanceBefore - balanceAfter == amount, "Balance didnt increment";
}