pragma solidity ^0.4.25;

contract DAPP {
    struct User {
        uint id; 
        uint bal;
        string name;

        uint[] neighbours;
        mapping (uint => int) account;
    }

    mapping (uint => User) users;
    mapping (uint => bool) visited;
    uint[] userIds;
    int[1000] public _path; //for debugging
    string public answer = ""; // for debugging

    constructor() public {
        _path[0] = -1;
    }

    function userExists(uint id) internal view returns (bool) {
        for(uint i = 0; i < userIds.length; ++i) {
            if(userIds[i] == id) return true;
        }
        return false;
    }

    function registerUser(uint id, string uname) public {
        if(userExists(id)) {
            revert("User already registered");
        }

        userIds.push(id);

        User memory user;
        user.id=id;
        user.bal = 0;
        user.name = uname;
        users[id] = user;

        visited[id] = false;
    }

    function createAcc(uint id1, uint id2) public {
        if(!userExists(id1) || !userExists(id2)){
            revert("One of the users does not exist");
        }

        addNeighbour(id1, id2);
        addNeighbour(id2, id1);
    }

    function addNeighbour(uint uid, uint acc) internal {
        User storage u = users[uid];

        uint i = 0;
        for(i = 0; i < u.neighbours.length; ++i) {
            if(u.neighbours[i] == acc) return;
        }
        u.neighbours.push(acc);
        u.account[acc] = 0;
    }

    function showUsers() public view returns (uint[]) {
        return userIds;
    }

    function showUserNeighbours(uint id) public view returns (uint[]) {
        if(!userExists(id)){
            revert("User does not exist");
        }
        return users[id].neighbours;
    }

    function showUserName(uint id) public view returns (string) {
        if(!userExists(id)){
            revert("User does not exist");
        }
        return users[id].name;
    }

    function shortestPath(uint from, uint to) public returns (bool){
        
        uint[] memory pth = new uint[](userIds.length);
        uint[] memory Q = new uint[](userIds.length);
        int[] memory P = new int[](userIds.length);
        uint[4] memory data = [0, 0, 0, to];

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

        // if(data[1] >= data[2]) return false;
        if(preparePath(pth, Q, P, data)){
            answer = "good";
        }else{
            answer = "bad";
        }
        putPathInGlobal(pth, data);
        return true;
    }

    function exploreNode(uint[] memory Q, int[] memory P, uint[4] memory data) internal returns (bool) {
        if(Q[data[1]] == data[3]) return true;

        uint cur = Q[data[1]++];
        uint i = 0;
        for(i = 0; i < users[cur].neighbours.length; ++i){
            if(!visited[users[cur].neighbours[i]]){
                visited[users[cur].neighbours[i]]=true;
                Q[data[2]++] = users[cur].neighbours[i];
                P[data[2]-1] = int(data[1]-1);
            }
        }

        return false;
    }

    function putPathInGlobal(uint[] memory path, uint[4] memory data) internal {
        uint i = 0;
        for(i = 0; i < data[0]; ++i){
            _path[i] = int(path[i]);
        }
        _path[i] = -1;
    }

    function path_() public view returns (int[]) {
        uint sz = 0;
        while(sz < _path.length && _path[sz] >= 0) sz++;

        int[] memory ret = new int[](sz);
        for(sz = 0; sz < ret.length; ++sz){
            ret[sz] = _path[sz];
        }
        return ret;
    }

    function preparePath(uint[] path, uint[] memory Q, int[] memory P, uint[4] memory data) internal pure returns (bool) {
        if(data[1] >= Q.length) return false;
        if(data[1] >= data[2]) return false;

        int node = int(data[1]);
        while(node >= 0){
            path[data[0]++] = Q[uint(node)];
            node = P[uint(node)];
        }

        return true;
    }
}