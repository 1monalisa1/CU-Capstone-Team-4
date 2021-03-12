pragma solidity ^0.5.5;
pragma experimental ABIEncoderV2;

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
        address ownership;
        string possessor;
    }

    mapping(uint => Winenot) public rare_wines;

    mapping(uint => string[]) public owner_chains;

    modifier onlyPossessor(uint token_id){
        require(msg.sender == rare_wines[token_id].ownership, "Only a tokenholder is authorized to run this function.");
        _;
    }

    modifier checkExistenceOfToken(uint token_id) {
        require(_exists(token_id), "Wine not registered!");
        _;
    }

    modifier checkExistenceOfEntity(uint entity_id) {
        require(_exists(entity_id), "Entity not registered!");
        _;
    }

    event Appraisal(uint token_id, uint appraisal_value, string report_uri);

    function registerWineBottle(address owner, string memory name, string memory producer, uint initial_value, string memory possessor, string memory token_uri) public returns(uint) {
        require(msg.sender == owner);
        token_ids.increment();
        uint token_id = token_ids.current();
        _mint(owner, token_id);
        _setTokenURI(token_id, token_uri);

        rare_wines[token_id] = Winenot(name, producer, initial_value, owner, possessor);
        owner_chains[token_id].push(producer);
        return token_id;
    }

    function getWineInfo(uint token_id) public view checkExistenceOfToken(token_id) returns(Winenot memory, string[] memory){
        return (rare_wines[token_id], owner_chains[token_id]);
    }

    function newAppraisal(uint token_id, uint new_value, string memory report_uri) public checkExistenceOfToken(token_id) returns(uint) {
        rare_wines[token_id].appraisal_value = new_value;
        emit Appraisal(token_id, new_value, report_uri);
        return rare_wines[token_id].appraisal_value;
    }

    // About Entities in a Chain
    using Counters for Counters.Counter;
    Counters.Counter entity_ids;

    struct Entity {
        string name;
        address entity_address;
    }

    mapping(uint => Entity) entities;

    function registerEntity(string memory _name, address _entity_address) public returns(uint){
        entity_ids.increment();
        uint entity_id = entity_ids.current();
        entities[entity_id] = Entity(_name, _entity_address);
        // entities[entity_id].name = _name;
        // entities[entity_id].entity_address = _entity_address;
        return entity_id;
    }

    function getEntityInfo(uint entity_id) public view returns (Entity memory){
        return entities[entity_id];
    }

    function transferOwnership(uint token_id, uint new_owner_id) public checkExistenceOfToken(token_id) onlyPossessor(token_id) checkExistenceOfEntity(new_owner_id) {
        // require(msg.sender == rare_wines[token_id].ownership);
        rare_wines[token_id].ownership = entities[new_owner_id].entity_address;
        rare_wines[token_id].possessor = entities[new_owner_id].name;
        owner_chains[token_id].push(entities[new_owner_id].name);
    }

    // // event Approval(address indexed _owner, address indexed _approved, uint256 indexed _tokenId);
    // event Approval(address indexed _owner, address indexed _newowner, uint256 indexed_tokenId);

    // function approval() public {
    //     emit Approval(msg.sender, );
    // }

    // function revokeAuthentication(uint token_id, bool qualityCheck, bool tamperProof) public returns(bool) {
    //     if (qualityCheck == true && tamperProof == true) {
    //     return rare_wines[token_id].Authenticated = true;
    // }
    
}