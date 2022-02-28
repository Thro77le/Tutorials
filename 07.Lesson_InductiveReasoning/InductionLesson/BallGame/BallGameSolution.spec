
methods {
	ballAt() returns uint256 envfree
	pass() envfree
}

invariant neverReachPlayer4()
	ballAt() != 3 && ballAt() != 4

// rule invariant_as_a_rule_init() {
// 	assert ballAt() != 3 && ballAt() != 4;
// }

rule invariant_as_a_rule_step() {
	require ballAt() != 3 && ballAt() != 4;
	pass();
	assert ballAt() != 3 && ballAt() != 4;
}
