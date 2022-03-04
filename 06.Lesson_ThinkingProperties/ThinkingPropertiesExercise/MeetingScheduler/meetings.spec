methods {
    getMeetingId(uint256) returns (uint8) envfree
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

definition meetingUninitialized(uint256 meetingId) returns bool =
    getStateById(meetingId) == 0 &&
    getStartTimeById(meetingId) == 0 &&
    getEndTimeById(meetingId) == 0 &&
    getNumOfParticipents(meetingId) == 0 &&
    getOrganizer(meetingId) == 0;

definition meetingPending(uint256 meetingId) returns bool =
    getStateById(meetingId) == 1 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) == 0 &&
    getOrganizer(meetingId) != 0;

definition meetingStarted(uint256 meetingId) returns bool =
    getStateById(meetingId) == 2 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) >= 0 &&
    getOrganizer(meetingId) != 0;

definition meetingEnded(uint256 meetingId) returns bool =
    getStateById(meetingId) == 3 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) >= 0 &&
    getOrganizer(meetingId) != 0;

definition meetingCancelled(uint256 meetingId) returns bool =
    getStateById(meetingId) == 4 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) == 0 &&
    getOrganizer(meetingId) != 0;

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

rule numOfParticipantsNonDecreasingInStartedState(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require meetingStarted(meetingId);
	uint256 numOfParticipantsBefore = getNumOfParticipents(meetingId);

	f(e, args);

    uint256 numOfParticipantsAfter = getNumOfParticipents(meetingId);

	assert numOfParticipantsBefore <= numOfParticipantsAfter, "the number of participants decreased as a result of a function call";
}

rule organizerCantChangeOnceSet(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require meetingStarted(meetingId) || meetingStarted(meetingId) || meetingEnded(meetingId) || meetingCancelled(meetingId);
	uint256 organizerBefore = getOrganizer(meetingId);

	f(e, args);

    uint256 organizerAfter = getOrganizer(meetingId);

	assert organizerBefore == organizerAfter, "Organizer can't change once set";
}

rule startTimeCantChangeOnceSet(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require meetingStarted(meetingId) || meetingStarted(meetingId) || meetingEnded(meetingId) || meetingCancelled(meetingId);
	uint256 startTimeBefore = getStartTimeById(meetingId);

	f(e, args);

    uint256 startTimeAfter = getStartTimeById(meetingId);

	assert startTimeBefore == startTimeAfter, "startTime can't change once set";
}

rule endTimeCantChangeOnceSet(method f, uint256 meetingId) {
	env e;
	calldataarg args;
    require meetingStarted(meetingId) || meetingStarted(meetingId) || meetingEnded(meetingId) || meetingCancelled(meetingId);
	uint256 endTimeBefore = getEndTimeById(meetingId);

	f(e, args);

    uint256 endTimeAfter = getEndTimeById(meetingId);

	assert endTimeBefore == endTimeAfter, "endTime can't change once set";
}

rule startBeforeEnd(method f, uint256 meetingId, uint256 startTime, uint256 endTime) {
	env e;

    scheduleMeeting(e, meetingId, startTime, endTime);

    uint256 scheduledStartTime = getStartTimeById(meetingId);
    uint256 scheduledEndTime = getEndTimeById(meetingId);

	assert scheduledStartTime < scheduledEndTime, "the created meeting's start time is not before its end time";
}
