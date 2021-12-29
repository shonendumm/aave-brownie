// copied this interface file from the tutorial's github (as instructed)

pragma solidity ^0.4.19;

interface IWeth {
  function allowance(address owner, address spender) external view returns (uint256 remaining);
  function approve(address spender, uint256 value) external returns (bool success);
  function balanceOf(address owner) external view returns (uint256 balance);
  function decimals() external view returns (uint8 decimalPlaces);
  function name() external view returns (string memory tokenName);
  function symbol() external view returns (string memory tokenSymbol);
  function totalSupply() external view returns (uint256 totalTokensIssued);
  function transfer(address to, uint256 value) external returns (bool success);
  function transferFrom(address from, address to, uint256 value) external returns (bool success);
  function deposit() external;
  function withdraw(uint wad) external;
}

// Compare to WETH token contract code at kovan: 0xd0a1e359811322d97991e03f863a0c30c2cf029c


// pragma solidity ^0.4.18;

// contract WETH9_ {
//     string public name     = "Wrapped Ether";
//     string public symbol   = "WETH";
//     uint8  public decimals = 18;

//     event  Approval(address indexed src, address indexed guy, uint wad);
//     event  Transfer(address indexed src, address indexed dst, uint wad);
//     event  Deposit(address indexed dst, uint wad);
//     event  Withdrawal(address indexed src, uint wad);

//     mapping (address => uint)                       public  balanceOf;
//     mapping (address => mapping (address => uint))  public  allowance;

//     function() public payable {
//         deposit();
//     }
//     function deposit() public payable {
//         balanceOf[msg.sender] += msg.value;
//         Deposit(msg.sender, msg.value);
//     }
//     function withdraw(uint wad) public {
//         require(balanceOf[msg.sender] >= wad);
//         balanceOf[msg.sender] -= wad;
//         msg.sender.transfer(wad);
//         Withdrawal(msg.sender, wad);
//     }

//     function totalSupply() public view returns (uint) {
//         return this.balance;
//     }

//     function approve(address guy, uint wad) public returns (bool) {
//         allowance[msg.sender][guy] = wad;
//         Approval(msg.sender, guy, wad);
//         return true;
//     }

//     function transfer(address dst, uint wad) public returns (bool) {
//         return transferFrom(msg.sender, dst, wad);
//     }

//     function transferFrom(address src, address dst, uint wad)
//         public
//         returns (bool)
//     {
//         require(balanceOf[src] >= wad);

//         if (src != msg.sender && allowance[src][msg.sender] != uint(-1)) {
//             require(allowance[src][msg.sender] >= wad);
//             allowance[src][msg.sender] -= wad;
//         }

//         balanceOf[src] -= wad;
//         balanceOf[dst] += wad;

//         Transfer(src, dst, wad);

//         return true;
//     }
// }


