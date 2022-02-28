## Valid states
1. UNINITIALIZED:
```C++
definition meetingUninitialized(uint256 meetingId) returns bool =
    getStateById(meetingId) == 0 &&
    getStartTimeById(meetingId) == 0 &&
    getEndTimeById(meetingId) == 0 &&
    getNumOfParticipents(meetingId) == 0 &&
    getOrganizer(meetingId) == 0;
```
2. PENDING:
```C++
definition meetingPending(uint256 meetingId) returns bool =
    getStateById(meetingId) == 1 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) == 0 &&
    getOrganizer(meetingId) != 0;
```
3. STARTED:
```C++
definition meetingStarted(uint256 meetingId) returns bool =
    getStateById(meetingId) == 2 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) >= 0 &&
    getOrganizer(meetingId) != 0;
```
4. ENDED:
```C++
definition meetingEnded(uint256 meetingId) returns bool =
    getStateById(meetingId) == 3 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) >= 0 &&
    getOrganizer(meetingId) != 0;
```
5. CANCELLED:
```C++
definition meetingCancelled(uint256 meetingId) returns bool =
    getStateById(meetingId) == 4 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) == 0 &&
    getOrganizer(meetingId) != 0;
```

## State transitions
6. UNINITIALIZED ~> UNINITIALIZED | PENDING
7. (UNINITIALIZED ~> PENDING) => `scheduleMeeting()` called
8. PENDING ~> PENDING | STARTED | CANCELED
9. (PENDING ~> STARTED) => `startMeeting()` called
10. (PENDING ~> CANCELED) => `cancelMeeting()` called
11. STARTED ~> STARTED | ENDED
12. (STARTED ~> ENDED) => `endMeeting()` called
13. ENDED ~> ENDED
14. CANCELED ~> CANCELED

## Variable transitions
15. numOfParticipants can only increase in STARTED state
16. organizer cant change in state != UNINITIALIZED
17. startTime cant change in state != UNINITIALIZED
18. endTime cant change in state != UNINITIALIZED

## High-level properties
(None, the code is mostly about state transition)
## Unit tests
(None, the code is mostly about state transition)
<br>

## Prioritizing


### High Priority:

- Property 16: if this prop doesn't hold, organizer can be changed and DoS meetings via canceling them in pending state

- Property 17 & 18: if this prop doesn't hold, anyone can end a meeting and delay opening it

### Medium Priority:

- All **Valid State** and  **State transition** should hold

### Low Priority:

- Property 15: counts num of participants which is not crucial for system to work properly