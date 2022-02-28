methods {
	getCurrentManager(uint256 fundId) returns (address) envfree
	getPendingManager(uint256 fundId) returns (address) envfree
	isActiveManager(address a) returns (bool) envfree
}



rule uniqueManagerAsRule(uint256 fundId1, uint256 fundId2, method f) {
	// assume different IDs
	require fundId1 != fundId2;
	//Note: Assume that current manager exists in isActiveManger mapping
	//Note: Both ways because I wanted to exclude address 0 (which has special meaning in the code)
	//Note: It successfully catches bug in ManagerBug1.sol
	//Note: Also I think it is little bit better than rule from APrtilSolution because it allows calling f() on empty funds
	require (getCurrentManager(fundId1) != 0) <=> isActiveManager(getCurrentManager(fundId1));
	require (getCurrentManager(fundId2) != 0) <=> isActiveManager(getCurrentManager(fundId2));
	// assume different managers
	require getCurrentManager(fundId1) != getCurrentManager(fundId2);

	// hint: add additional variables just to look at the current state
	// bool active1 = isActiveManager(getCurrentManager(fundId1));

	env e;
	calldataarg args;
	f(e,args);

	// verify that the managers are still different
	assert getCurrentManager(fundId1) != getCurrentManager(fundId2), "managers not different";
	//Note: the following 2 asserts catch bug in ManagerBug2.sol
	assert (getCurrentManager(fundId1) != 0) <=> isActiveManager(getCurrentManager(fundId1));
	assert (getCurrentManager(fundId2) != 0) <=> isActiveManager(getCurrentManager(fundId2));
}


// /* A version of uniqueManagerAsRule as an invariant */
//Note: this invariant should fail with uninitialized funds
// invariant uniqueManagerAsInvariant(uint256 fundId1, uint256 fundId2)
// 	fundId1 != fundId2 => getCurrentManager(fundId1) != getCurrentManager(fundId2)
