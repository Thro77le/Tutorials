# format: <relative/path/to/solidity/file>:<contrac_name> --verify <contract_name>:<relative/path/to/spec/file>

certoraRun ../BankLesson1/Bank.sol:Bank --verify Bank:../BankLesson1/TotalGreaterThanUser.spec \
  --solc solc-0.7.5 \
  --msg "My first Certora shell script"
