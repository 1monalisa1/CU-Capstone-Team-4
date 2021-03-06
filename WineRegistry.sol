pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/drafts/Counters.sol";

contract WineRegistry is ERC721Full {

    constructor() ERC721Full("Winenot", "VINO") public { }

    using Counters for Counters.Counter;
    Counters.Counter token_ids;

    struct Winenot {
        string name;
        string producer;
        uint appraisal_value;
        string origin;
        uint vintage;
    }

    mapping(uint => Winenot) public rare_wines;

    event Appraisal(uint token_id, uint appraisal_value, string report_uri);

    function registerWineBottle(address owner, string memory name, string memory producer, uint initial_value, string memory origin, uint vintage, string memory token_uri) public returns(uint) {
        token_ids.increment();
        uint token_id = token_ids.current();

        _mint(owner, token_id);
        _setTokenURI(token_id, token_uri);

        rare_wines[token_id] = Winenot(name, producer, initial_value, origin, vintage);

        return token_id;
    }

    function newAppraisal(uint token_id, uint new_value, string memory report_uri) public returns(uint) {
        rare_wines[token_id].appraisal_value = new_value;

        emit Appraisal(token_id, new_value, report_uri);

        return rare_wines[token_id].appraisal_value;
    }
}
