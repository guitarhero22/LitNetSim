pragma solidity ^0.4.25;

contract DAPP {

    // User struct
    struct User { 
        uint id; //user ID
        uint bal; //users's balance, not important
        string name; //username

        uint[] neighbours; //neighbours in PCN
        mapping (uint => uint) account; //balances in accounts
    }

    //State Variables 
    uint[] public userIds; //list of registered users
    int[1001] public _path; //for debugging
    string public answer = ""; //for debugging
    mapping (uint => User) public users; //mapping from user ids to structs
    mapping (uint => bool) public visited; //for bfs

    //contract constructor 
    constructor() public {
        _path[0] = -1;
        _path[1000] = 0;
    }

    //to check if a transaction was successfull
    function getSuccessfulTransactions() public view  returns (int){
        return _path[1000];
    }

    //to register a User to PCN
    function registerUser(uint id, string memory uname) public {
        if(userExists(id)) {
            //if user ID is taken
            revert("User already registered");
        }

        //add user to list
        userIds.push(id);

        //create a new struct instance for the user
        User memory user;
        user.id = id;
        user.bal = 0;
        user.name = uname;
        users[id] = user;

        //initialization
        visited[id] = false;
    }

    //to add an edges in the PCN
    function createAcc(uint id1, uint id2, uint balance) public {
        if(!userExists(id1) || !userExists(id2)){
            //when one of the users don't exist
            revert("One of the users does not exist");
        }

        //add the edge
        addNeighbour(id1, id2, balance/2);
        addNeighbour(id2, id1, balance/2);
    }

    //to close an existing account
    function closeAccount(uint id1, uint id2) public {
        if(!userExists(id1) || !userExists(id2)) {
            //one of the users does not exist
            revert("One of the users does not exist");
        }

        if(!accountExists(id1, id2)){
            //account does not exist
            revert("Account not open");
        }

        uint i = 0;
        for(i=0; i < users[id1].neighbours.length; ++i) {
            if(users[id1].neighbours[i] == id2) break;
        }

        //Finally delete accounts from both user structs
        if(i < users[id1].neighbours.length && users[id1].neighbours[i] == id2){
            users[id1].bal -= users[id1].account[id2];
            delete users[id1].neighbours[i];
            users[id1].neighbours.length --;
        }else{
            revert("This should not happen");
        }
        
        for(i=0; i < users[id2].neighbours.length; ++i) {
            if(users[id2].neighbours[i] == id1) break;
        }

        if(i < users[id2].neighbours.length && users[id2].neighbours[i] == id1){
            users[id2].bal -= users[id2].account[id1];
            delete users[id2].neighbours[i];
            users[id2].neighbours.length --;
        }else{
            revert("This should not happen");
        }

    }

    //to send amount throught the PCN
    function sendAmount(uint from , uint to) public {
        uint amount = 1; //hardcoded as per problem statement
        uint[] memory pth = new uint[](userIds.length); //for storing the path
        uint[] memory Q = new uint[](userIds.length); //Queue for BFS
        int[] memory P = new int[](userIds.length); //parents in bfs run for obtaining the path
        uint[5] memory data = [0, 0, 0, to, amount]; //some data for the algorithm

        //BFS algorithm
        uint id = 0;
        for(id = 0; id < userIds.length; ++id){
            visited[userIds[id]] = false;
        }
        visited[from] = true;
        Q[data[2]++] = from;
        P[data[2]-1] = -1;

        while(data[1] < data[2]) {
            //while the queue is not empty, visit the next node in Queue
            if(exploreNode(Q, P, data)){
                break;
            }
        }

        if(preparePath(pth, Q, P, data)){
            //path found
            answer = "good";
        }else{
            //path not found
            answer = "bad";
        }

        //for debugging and checking the correctness of BFS
        putPathInGlobal(pth, data);

        //finally transfer the amount through the path found
        if(!transferAmount(pth, data[0], amount)){
            revert("Invalid Transaction");
        }

        //update the number of successful transactions
        _path[1000] += 1;

        return;
    }

    //helper to check if account exists    
    function accountExists(uint id1, uint id2) public view returns (bool) {
        uint i = 0;
        bool found = false;
        for(i = 0; i < users[id1].neighbours.length; ++i){
            if(users[id1].neighbours[i] == id2) {
                found = true;
                break;
            }
        }

        if(!found) return false;

        found = false;
        for(i=0; i < users[id2].neighbours.length; ++i){
            if(users[id2].neighbours[i] == id1) {
                found = true;
                break;
            }
        }

        return found;
    }

    //helper to see the list of registered users
    function showUsers() public view returns (uint[] memory) {
        return userIds;
    }

    //helper to check if userExists
    function userExists(uint id) internal view returns (bool) {
        for(uint i = 0; i < userIds.length; ++i) {
            if(userIds[i] == id) return true;
        }
        return false;
    }

    //credit amount to a an account
    function credit(uint id1, uint id2, uint amount) public {
        if(!userExists(id1) || !userExists(id2)){
            revert("One of the users does not exist");
        }

        if(!accountExists(id1, id2)) {
            revert("Account does not exist");
        }

        users[id1].account[id2] += amount / 2;
        users[id1].bal += amount / 2;

        users[id2].account[id1] += (amount - amount/2);
        users[id2].bal += (amount - amount/2);
        return;
    }

    //helper to check a user's neighbours
    function showUserNeighbours(uint id) public view returns (uint[] memory) {
        if(!userExists(id)){
            revert("User does not exist");
        }
        return users[id].neighbours;
    }

    //add account to a user's struct / add neighbour in PCN
    function addNeighbour(uint uid, uint acc, uint balance) internal {
        User storage u = users[uid];

        uint i = 0;
        for(i = 0; i < u.neighbours.length; ++i) {
            if(u.neighbours[i] == acc) return;
        }
        u.neighbours.push(acc);
        u.account[acc] = balance;
    }

    //Proof of Concept for BFS in solidity
    function shortestPath(uint from, uint to) public returns (bool){
        
        uint[] memory pth = new uint[](userIds.length);
        uint[] memory Q = new uint[](userIds.length);
        int[] memory P = new int[](userIds.length);
        uint[5] memory data = [0, 0, 0, to, 0];

        uint id = 0;
        for(id = 0; id < userIds.length; ++id){
            visited[userIds[id]] = false;
        }
        visited[from] = true;
        Q[data[2]++] = from;
        P[data[2]-1] = -1;

        while(data[1] < data[2]) {
            if(exploreNode(Q, P, data)){
                break;
            }
        }

        if(preparePath(pth, Q, P, data)){
            answer = "good";
        }else{
            answer = "bad";
        }
        putPathInGlobal(pth, data);
        return true;
    }

    //helper function to visit each node during BFS
    function exploreNode(uint[] memory Q, int[] memory P, uint[5] memory data) internal returns (bool) {
        if(Q[data[1]] == data[3]) return true;

        uint cur = Q[data[1]++];
        uint i = 0;
        for(i = 0; i < users[cur].neighbours.length; ++i){
            //only add to queue if the full amount can be sent through this edge
            if(!visited[users[cur].neighbours[i]] && users[cur].account[users[cur].neighbours[i]] >= data[4]){
                visited[users[cur].neighbours[i]]=true;
                Q[data[2]++] = users[cur].neighbours[i];
                P[data[2]-1] = int(data[1]-1);
            }
        }

        return false;
    }

    //to prepare path from the Queue and list of parents
    function preparePath(uint[] memory path, uint[] memory Q, int[] memory P, uint[5] memory data) internal pure returns (bool) {
        if(data[1] >= Q.length) return false;
        if(data[1] >= data[2]) return false;

        int node = int(data[1]);
        while(node >= 0){
            path[data[0]++] = Q[uint(node)];
            node = P[uint(node)];
        }

        return true;
    }

    //to transfer an amount through a given path in the PCN
    function transferAmount(uint[] memory path, uint pathlength, uint amount) internal returns (bool){
        if(pathlength < 1) return false;

        uint i = 0;
        bool check = true;
        for(i = 0; i < pathlength - 1; ++i){
            if(users[path[i + 1]].account[path[i]] < amount) check = false;
        }

        if(!check) return false;

        users[path[0]].bal += amount;
        users[path[pathlength - 1]].bal -= amount;

        for(i = 0; i < pathlength - 1; ++i){
            users[path[i]].account[path[i+1]] += amount;
            users[path[i+1]].account[path[i]] -= amount;
        }

        return true;
    }

    //helper function to view what path was chosen for the last transfer
    function path_() public view returns (int[] memory) {
        uint sz = 0;
        while(sz < _path.length && _path[sz] >= 0) sz++;

        int[] memory ret = new int[](sz);
        for(sz = 0; sz < ret.length; ++sz){
            ret[sz] = _path[sz];
        }
        return ret;
    }

    //helper function to make the last path found publicly available for debugging
    function putPathInGlobal(uint[] memory path, uint[5] memory data) internal {
        uint i = 0;
        for(i = 0; i < data[0]; ++i){
            _path[i] = int(path[i]);
        }
        _path[i] = -1;
    }
}