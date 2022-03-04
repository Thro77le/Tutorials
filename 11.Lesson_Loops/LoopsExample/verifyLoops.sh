certoraRun Loops.sol:Loops \
    --verify Loops:LoopsUnrolling.spec \
    --solc solc-0.8.11 \
    --optimistic_loop \
    --loop_iter 5 \
    --msg "$1"