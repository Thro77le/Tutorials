methods {
    ticketDepot(uint64)
    createEvent(uint64, uint16) returns (uint16)
    buyNewTicket(uint16, address) returns (uint16)
    offerTicket(uint16, uint16, uint64, address, uint16)
    buyOfferedTicket(uint16, uint16, address)
    certora_getContractEthBalance() returns (uint256) envfree
    numEvents() returns (uint16) envfree
    getEventOwner(uint16) returns (address) envfree
    getEventTicketPrice(uint16) returns (uint64) envfree
    getEventTicketsRemaining(uint16) returns (uint16) envfree
}

definition eventUninitialized(uint256 eventId) returns bool =
    getEventOwner(meetingId) == 0 &&
    getEventTicketPrice(meetingId) == 0 &&
    getEventTicketsRemaining(meetingId) == 0;

definition eventCreated(uint256 eventId) returns bool =
    getEventOwner(meetingId) != 0 &&
    getEventTicketPrice(meetingId) > 0 &&
    getEventTicketsRemaining(meetingId) > 0;

definition eventSoldOut(uint256 eventId) returns bool =
    getEventOwner(meetingId) != 0 &&
    getEventTicketPrice(meetingId) > 0 &&
    getEventTicketsRemaining(meetingId) == 0;



invariant zero_eth_balance(env e)
    certora_getContractEthBalance() == 0

rule numEventNonDecreasing(method f) {
	env e;
	calldataarg args;
    uint16 numEventsBefore = numEvents();

	f(e, args);

    uint16 numEventsAfter = numEvents();
	assert numEventsBefore <= numEventsAfter, "the number of events decreased as a result of a function call";
}

rule ticketsRemainingNonIncreasing(method f, uint256 eventId) {
	env e;
	calldataarg args;
    require eventCreated(eventId);
	uint256 ticketsRemainingBefore = getEventTicketsRemaining(eventId);

	f(e, args);

    uint256 ticketsRemainingAfter = getEventTicketsRemaining(meetingId);

	assert ticketsRemainingBefore >= ticketsRemainingAfter, "TicketsRemaining can't decrease";
}

rule eventStateTransition(method f, uint256 eventId) {
	env e;
	calldataarg args;
    require eventUninitialized(eventId);

	f(e, args);

    require eventCreated(eventId);

	assert f.selector == createEvent(uint64,uint16).selector, "EventCreated() should be called";
}

rule eventStateTransition(method f, uint256 eventId) {
	env e;
	calldataarg args;
    require eventUninitialized(eventId);

	f(e, args);

    require eventCreated(eventId);

	assert f.selector == createEvent(uint64,uint16).selector, "createEvent() should be called for this state transition";
}

rule eventStateTransition2(method f, uint256 eventId) {
	env e;
	calldataarg args;
    require eventCreated(eventId);

	f(e, args);

    require eventSoldOut(eventId);

	assert f.selector == buyNewTicket(uint16,address).selector, "buyNewTicket() should be called for this state transition";
}
