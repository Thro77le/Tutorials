certoraRun \
    ../../02.Lesson_InvestigateViolations/MeetingScheduler/MeetingSchedulerFixed.sol:MeetingScheduler \
    --verify MeetingScheduler:../../02.Lesson_InvestigateViolations/MeetingScheduler/meetings.spec \
    --solc solc-0.8.7 \
    --send_only \
    --msg "$1"