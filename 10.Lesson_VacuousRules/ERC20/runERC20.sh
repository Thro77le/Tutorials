certoraRun ERC20Bug1.sol:ERC20 --verify ERC20:Sanity.spec \
    --solc solc-0.8.0 \
    --optimistic_loop \
    --msg "$1"