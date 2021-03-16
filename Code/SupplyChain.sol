pragma solidity ^0.5.5;
pragma experimental ABIEncoderV2; // needed to return struct in a function

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/drafts/Counters.sol";

contract WineRegistry is ERC721Full {

    constructor() ERC721Full("Winenot", "VINO") public { }

    using Counters for Counters.Counter;
    Counters.Counter token_ids;

    struct Winenot {
        string name; // wine name
        uint vintage; // year of manufacture
        string origin; // country
        string producer; // producer of the wine
        uint appraisal_value; // price of the wine
        address ownership; // ETH address of the current owner (possessor) of the wine
        string possessor; // current owner of the wine
    }

    // connect token ID (uint) to the wine info held in the struct Winenot
    mapping(uint => Winenot) public rare_wines;

    // connect token ID (uint) to a dynamic array which contains a histrical chain of ownership
    mapping(uint => string[]) public owner_chains;

    // modifier to prohibit non-tokenholders from engaging in an unauthorized token transfer
    modifier onlyPossessor(uint token_id){
        require(msg.sender == rare_wines[token_id].ownership, "Only a tokenholder is authorized to run this function.");
        _;
    }

    // modifier to confirm that the wine (token) exists
    modifier checkExistenceOfToken(uint token_id) {
        require(_exists(token_id), "Wine not registered!");
        _;
    }



    /// functions about a token
    // function to create a new token
    function registerWine(address owner, string memory name, uint vintage, string memory origin, string memory producer, 
                                uint initial_value, string memory possessor, string memory token_uri
    ) public returns(uint) {
        require(msg.sender == owner); // only the current owner of the wine can create a token

        // create a token with and allocate an ID
        token_ids.increment();
        uint token_id = token_ids.current();
        _mint(owner, token_id);
        _setTokenURI(token_id, token_uri);

        // using the two mappings, tie the token to the information of the wine
        rare_wines[token_id] = Winenot(name, vintage, origin, producer, initial_value, owner, possessor);
        owner_chains[token_id].push(possessor);

        return token_id;
    }


    // function to check the latest status of a token at a given time
    function getWineInfo(uint token_id) public view checkExistenceOfToken(token_id) returns(Winenot memory, string[] memory){
        return (rare_wines[token_id], owner_chains[token_id]);
    }


    // function to get the length of the dynamic array containing all the past owners
    // it is used in the python file to print all the owners using for loop
    // because the number of owners increases as transfers compile, the length of the array also increases
    function getLength(uint token_id) public view returns(uint){
        return owner_chains[token_id].length;
    }



    /// functions about entities involved in a supply chain
    /// they are required to register themselves before engaging in transfers of a token
    using Counters for Counters.Counter;
    Counters.Counter entity_ids;

    struct Entity {
        string name;
        address entity_address;
    }

    // each entity is to be assigned its own ID (uint). Tie the ID to the information of the entity
    mapping(uint => Entity) entities;

    // event to log all transfers of a token with the names of an assigner and assignee and the time of transactions
    event ChangeToken(uint256 token_num, string transferor, string transferee, uint time);

    // just like the wine token issuance, assign an ID to each entity and tie it to the entity information
    function registerEntity(string memory _name, address _entity_address) public returns(uint){
        entity_ids.increment();
        uint entity_id = entity_ids.current();
        entities[entity_id] = Entity(_name, _entity_address);
        return entity_id;
    }


    // function to check the entity information
    function getEntityInfo(uint entity_id) public view returns (Entity memory){
        return entities[entity_id];
    }



    /// function to transfer a token
    // by the modifiers, assure the existence of the token and the ownership of the token by an entity calling this function
    function transferOwnership(uint token_id, uint new_owner_id, bool qualityCheck, bool tamperProof) public checkExistenceOfToken(token_id) onlyPossessor(token_id) {
        require(qualityCheck == true && tamperProof == true);
        // before transferring a token, preserve the old owner name so as to log it in the event
        string memory _transferor = rare_wines[token_id].possessor;
        // change the ownership information held in the struct Winenot to that of the new owner
        rare_wines[token_id].ownership = entities[new_owner_id].entity_address;
        rare_wines[token_id].possessor = entities[new_owner_id].name;
        // add the new owner to the chain of ownership held in the dynamic array (string[])
        owner_chains[token_id].push(entities[new_owner_id].name);
        // log the transfer transaction to the event ChangeToken
        emit ChangeToken(token_id, _transferor, entities[new_owner_id].name, now);
    }



    /// function to reevcaluate the value of wine
    event Appraisal(uint token_id, uint appraisal_value, string report_uri);

    function newAppraisal(uint token_id, uint new_value, string memory report_uri) public checkExistenceOfToken(token_id) returns(uint) {
        rare_wines[token_id].appraisal_value = new_value;
        emit Appraisal(token_id, new_value, report_uri);
        return rare_wines[token_id].appraisal_value;
    }
    



    /// function for the purpose of frontend
    event Copyright(uint cid, address owner_address, string uri);
    
    function copyrightWork(string memory reference_uri) public {
        token_ids.increment();
        uint cid = token_ids.current();
        emit Copyright(cid, msg.sender, reference_uri);
    }

}