// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.19;

import "forge-std/Test.sol";
import "../src/SCContract.sol";

contract SCTest is Test
{
    SC public sc;
    address client_address = address(0x1);
    address seller_address;

    event transferProduct(address indexed holder, address indexed new_holder);

    function setUp() public
    {
        sc = new SC();
        sc.startAgreement(1, client_address, "screw", 1000, "hash");
        vm.deal(client_address, 1 ether);
    }


    function testFulfilmentOnContractStart() public view
    {
        (bool client, bool seller) = sc.getContractFulfilment(1);
        assertEq(client, false);
        assertEq(seller, false);
    }

    function testGetSCData() public view
    {
        (address seller, address holder, address nextHolder , address client,
        string memory product, uint quantity) = sc.getAgreementData(1);

        assertEq(seller, address(this));
        assertEq(holder, address(this));
        assertEq(nextHolder, address(0));
        assertEq(client, client_address);
        assertEq(product, "screw");
        assertEq(quantity, 1000);
    } 

    function testVerifiyContract() public view
    {
        assertEq(sc.verifyContract(1, "hsah"), false);
        assertEq(sc.verifyContract(1, "hash"), true);
    }

    function testInitialTrail() public view
    {
        assertEq(sc.getTrailHistory(1)[0], address(this));
    }

    function testNextDestination() public
    {
        vm.expectEmit(true, true, false, false);
        emit transferProduct(address(this), client_address);

        sc.nextDestination(1, client_address);
        (, , address nextHolder, , , ) = sc.getAgreementData(1);
        assertEq(nextHolder, client_address);
    }
    
    function testNextDestinationNotByHolder() public
    {
        vm.startPrank(address(0x2));
            vm.expectRevert("You are not the holder of the product!");
            sc.nextDestination(1, client_address);
        vm.stopPrank();
    }

    function testReceiveProduct() public
    {
        sc.nextDestination(1, client_address);
        vm.startPrank(client_address);
            sc.receiveProduct(1);
        vm.stopPrank();

        assertEq(sc.getTrailHistory(1)[0], address(this));
        assertEq(sc.getTrailHistory(1)[1], client_address);

        (, address holder, address nextHolder, , , ) = sc.getAgreementData(1);
        assertEq(holder, client_address);
        assertEq(nextHolder, address(0));

        (, bool seller) = sc.getContractFulfilment(1);
        assertEq(seller, true);
   
    }

       function testReceiveProductNotByHolder() public
    {
        sc.nextDestination(1, client_address);
        vm.startPrank(address(0x2));
            vm.expectRevert("You are not the next holder of the product!");
            sc.receiveProduct(1);
        vm.stopPrank();
    }

    function testEndAgreement() public
    {
        sc.nextDestination(1, client_address);
        vm.startPrank(client_address);
            sc.receiveProduct(1);
        vm.stopPrank();

        (, bool seller) = sc.getContractFulfilment(1);
        assertEq(seller, true);

        vm.startPrank(client_address);
            sc.endAgreement{value: 1 ether}(1);
        vm.stopPrank();

        (bool client,) = sc.getContractFulfilment(1);
        assertEq(client, true);
    }

    function testEndAgreementNotByClient() public
    {
        sc.nextDestination(1, client_address);
        vm.startPrank(client_address);
            sc.receiveProduct(1);
        vm.stopPrank();

        vm.expectRevert("Only the client can end the agreement");
        sc.endAgreement{value: 1 ether}(1);
    }

    receive() external payable {}
    fallback() external payable {}
}