certoraRun SpartaProtocolPool.sol:SpartaProtocolPool \
    --verify SpartaProtocolPool:Sparta.spec \
    --solc solc-0.8.4 \
    --optimistic_loop \
    --msg "$1"