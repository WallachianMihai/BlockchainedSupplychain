//SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

contract SC
{
    event transferProduct(address indexed holder, address indexed new_holder, uint256 indexed agreement_id);

    struct Fulfilment
    {
        bool client;
        bool seller;
    }

    struct Agreement
    {
        address seller;
        address client;
        address holder;
        address nextHolder;
        bytes product;
        uint quantity;
        Fulfilment fulfilment;
        address[] trail;
        bytes contractHash;
    }

    mapping(uint256 => Agreement) private agreements;

    function startAgreement(uint256 agreement_id, address account, string calldata product, uint quantity, string calldata contract_hash) external
    {
        agreements[agreement_id] = Agreement({
            seller: msg.sender,
            holder: msg.sender, 
            client: account, 
            nextHolder: address(0),
            product: bytes(product),
            quantity: quantity,
            fulfilment: Fulfilment(false, false),
            contractHash: bytes(contract_hash),
            trail: new address[](0)
            });
        agreements[agreement_id].trail.push(msg.sender);
    }

    function verifyContract(uint256 agreement_id, string calldata hash) external view returns(bool)
    {
        return keccak256(abi.encodePacked(agreements[agreement_id].contractHash)) == keccak256(abi.encodePacked(bytes(hash)));
    }

    function nextDestination(uint256 agreement_id, address account) external
    {
        require(agreements[agreement_id].fulfilment.client != true, "This contract is fulfiled!");
        require(msg.sender == agreements[agreement_id].holder, "You are not the holder of the product!");

        agreements[agreement_id].nextHolder = account;
        emit transferProduct(msg.sender, account, agreement_id);
    }

    function receiveProduct(uint256 agreement_id) external
    {
        require(agreements[agreement_id].fulfilment.client != true, "This contract is fulfiled!");
        require(msg.sender == agreements[agreement_id].nextHolder, "You are not the next holder of the product!");
        
        if(agreements[agreement_id].client == msg.sender)
        {
            agreements[agreement_id].fulfilment.seller = true;
        }

        agreements[agreement_id].holder = msg.sender;
        agreements[agreement_id].trail.push(msg.sender);
        agreements[agreement_id].nextHolder = address(0);
    }

    function endAgreement(uint256 agreement_id) external payable
    {
        require(agreements[agreement_id].fulfilment.seller == true, "The seller did not fulfil his obligations!");
        require(msg.value == 1 ether, "The payment amount does not match");
        require(msg.sender == agreements[agreement_id].client, "Only the client can end the agreement");
    
        payable(agreements[agreement_id].seller).transfer(msg.value);
        agreements[agreement_id].fulfilment.client = true;
    }

    function getTrailHistory(uint256 agreement_id) view external returns(address[] memory)
    {
        return agreements[agreement_id].trail;
    }

    function getAgreementData(uint256 agreement_id) view external returns(address, address, address,
                                                                          address, string memory, uint)
    {
        return (agreements[agreement_id].seller, agreements[agreement_id].holder,
                agreements[agreement_id].nextHolder, agreements[agreement_id].client, string(agreements[agreement_id].product),
                agreements[agreement_id].quantity);
    }

    function getContractFulfilment(uint256 agreement_id) view external returns(bool, bool)
    {
        return (agreements[agreement_id].fulfilment.client, agreements[agreement_id].fulfilment.seller);
    }
}