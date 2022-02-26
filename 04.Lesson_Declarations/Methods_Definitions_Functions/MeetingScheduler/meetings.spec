methods {
    getStateById(uint256) returns (uint8) envfree
    getStartTimeById(uint256) returns (uint256) envfree
    getEndTimeById(uint256) returns (uint256) envfree
    getNumOfParticipents(uint256) returns (uint256) envfree
    getOrganizer(uint256) returns (address) envfree
    scheduleMeeting(uint256, uint256, uint256)
    startMeeting(uint256)
    cancelMeeting(uint256)
    endMeeting(uint256)
    joinMeeting(uint256) envfree
}

definition is_uninitialized(uint8 state) returns bool = state == 0;
definition is_pending(uint8 state) returns bool = state == 1;
definition is_started(uint8 state) returns bool = state == 2;
definition is_ended(uint8 state) returns bool = state == 3;
definition is_cancelled(uint8 state) returns bool = state == 4;

	/*  Representing enums

    enums are supported by the Certora Verification Language (CVL),
    according to thier low level representation - uint8.
    in our case:
        -UNINITIALIZED = 0
        -PENDING = 1
        -STARTED = 2
        -ENDED = 3
        -CANCELLED = 4
    So for exmple if we write 'state == 0' we mean 'state == UNINITIALIZED'
    or 'state % 2 == 1' we mean 'state == PENDING || state == ENDED'.

    We will learn more about supported data structures in future lessons.
    For now, follow the above explanation to pass this exercise.
 */


// Checks that when a meeting is created, the planned end time is greater than the start time
rule startBeforeEnd(method f, uint256 meetingId, uint256 startTime, uint256 endTime) {
	env e;

    scheduleMeeting(e, meetingId, startTime, endTime);

    uint256 scheduledStartTime = getStartTimeById(meetingId);
    uint256 scheduledEndTime = getEndTimeById(meetingId);

	assert scheduledStartTime < scheduledEndTime, "the created meeting's start time is not before its end time";
}


// Checks that a meeting can only be started within the defined range [startTime, endTime]
rule startOnTime(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);

	f(e, args); // call only non reverting paths to any function on any arguments.

	uint8 stateAfter = getStateById(meetingId);
    uint256 startTimeAfter = getStartTimeById(meetingId);
    uint256 endTimeAfter = getEndTimeById(meetingId);

	assert (is_pending(stateBefore) && is_started(stateAfter)) => startTimeAfter <= e.block.timestamp, "started a meeting before the designated starting time.";
	assert (is_pending(stateBefore) && is_started(stateAfter)) => endTimeAfter > e.block.timestamp, "started a meeting after the designated end time.";

}


// Checks that state transition from STARTED to ENDED can only happen if endMeeting() was called
// @note read again the comment at the top regarding f.selector
rule checkStartedToStateTransition(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);

	f(e, args);

    uint8 stateAfter = getStateById(meetingId);

	assert (is_started(stateBefore) => (is_started(stateAfter) || is_ended(stateAfter))), "the status of the meeting changed from STARTED to an invalid state";
	assert ((is_started(stateBefore) && is_ended(stateAfter)) => f.selector == endMeeting(uint256).selector), "the status of the meeting changed from STARTED to ENDED through a function other then endMeeting()";
}


// Checks that state transition from PENDING to STARTED or CANCELLED can only happen if
// startMeeting() or cancelMeeting() were called, respectively
// @note read again the comment at the top regarding f.selector
rule checkPendingToCancelledOrStarted(method f, uint256 meetingId) {
	env e;
	calldataarg args;
	uint8 stateBefore = getStateById(meetingId);

	f(e, args);

    uint8 stateAfter = getStateById(meetingId);

	assert (is_pending(stateBefore) => (is_pending(stateAfter) || is_started(stateAfter) || is_cancelled(stateAfter))), "invalidation of the state machine";
	assert ((is_pending(stateBefore) && is_started(stateAfter)) => f.selector == startMeeting(uint256).selector), "the status of the meeting changed from PENDING to STARTED through a function other then startMeeting()";
	assert ((is_pending(stateBefore) && is_cancelled(stateAfter)) => f.selector == cancelMeeting(uint256).selector), "the status of the meeting changed from PENDING to CANCELLED through a function other then cancelMeeting()";
}


// Checks that the number of participants in a meeting cannot be decreased
rule monotonousIncreasingNumOfParticipants(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require getStateById(meetingId) == 0 => getNumOfParticipents(meetingId) == 0;
	uint256 numOfParticipantsBefore = getNumOfParticipents(meetingId);

	f(e, args);

    uint256 numOfParticipantsAfter = getNumOfParticipents(meetingId);

	assert numOfParticipantsBefore <= numOfParticipantsAfter, "the number of participants decreased as a result of a function call";
}
