certoraRun Popsicle.sol:PopsicleFinance \
    --verify PopsicleFinance:Popsicle.spec \
    --solc solc-0.8.4 \
    --optimistic_loop \
    --msg "$1"