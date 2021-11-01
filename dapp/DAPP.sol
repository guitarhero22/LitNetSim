pragma solidity ^0.4.25;

contract DAPP {
    struct User {
        uint id;
        uint bal;
        uint[] neighbours;
        mapping (uint => int) account;
    }

    mapping (uint => User) users;
    uint[] userIds;

    function checkIfUserExists(uint id) internal view returns (bool) {
        for(uint i = 0; i < userIds.length; ++i){
            if (userIds[i] == id) return true;
        }
        return false;
    }

   function checkIfAccountExists(uint id1, uint id2) internal view returns (bool) {
        User memory user1 = users[id1];
        User memory user2 = users[id2];
        uint i = 0;
        for(i = 0; i < user1.neighbours.length; ++i){
            if(id1 == user1.neighbours[i]) {
                return true;
            }
        }
        for(i = 0; i < user2.neighbours.length; ++i){
            if(id2 == user2.neighbours[i]) {
                return true;
            }
        }
        return false;
    }

    function registerUser(uint id) payable public {
        if(checkIfUserExists(id)){
            revert("ID already Taken");
            return;
        }

        userIds.push(id);
        User memory user;
        user.id = id;
        user.bal = 0;

        users[id] = user;
        return;
    }

    function creatAcc(uint id1 , uint id2) payable public {
        if(!checkIfUserExists(id1) || !checkIfUserExists(id2)){
            revert("One of the Users Not registered");
            return;
        }

        if(checkIfAccountExists(id1, id2)){
            revert("Account Already Exists");
            return;
        }

        users[id1].neighbours.push(id2);
        users[id2].neighbours.push(id1);
        users[id1].account[id2] = 0;
        users[id2].account[id2] = 0;
    }
}

/**
    library UintSet {

        struct SetStorage {
            uint data;
            int l; 
            int r;
        }

        struct Set {
            // SetStorage[] store;
            uint[] data;
            int[] l; 
            int[] r;
            uint sz;
        }

        function insert(uint[] set, int[] l, int[] r, uint sz, uint root, uint n) public view returns (uint){

            if(sz == 0){
                sz ++;
                set[sz - 1] = n;
                r[sz - 1] = -1;
                l[sz - 1] = -1;
                return sz;
            }

            if(set[root] == n) return sz;

            if(set[root] < n){
                if(l[root] == -1){
                    sz ++;
                    set[sz - 1] = n;
                    r[sz - 1] = -1;
                    l[sz - 1] = -1;
                    l[root] = int(sz - 1);
                    return sz;
                }
                return insert(set, l, r, sz, uint(l[root]), n);
            }else{
                if(r[root] == -1){
                    sz ++;
                    set[sz - 1] = n;
                    r[sz - 1] = -1;
                    l[sz - 1] = -1;
                    r[root] = int(sz - 1);
                    return sz;
                }
                return insert(set, l, r, sz, uint(r[root]), n);
            }

            return sz;
        }

        // function find(Set set, int r, uint f) public view returns (bool){
        function find(uint[] set, int[] l, int[] r, uint sz, uint root, uint f) public view returns (bool){
            if(sz == 0) return false;

            if(f == set[root]) return true;

            if(f < set[root]){
                if(l[root] != -1){
                    return find(set, l, r, sz, uint(l[root]), f);
                }
                return false; 
            }else{
                if(r[root] != -1){
                    return find(set, l, r, sz, uint(r[root]), f);
                }
                return false;
            }
        }

    }
*/

/** 
    function findShortestPath(uint from, uint to) internal view returns (int[1001]){

        intPairUint[1001] memory Q;
        uint i = 0;
        uint j = 0;

        Q[j++] = intPairUint(from, int(-1));
        UintSet.Set memory set;
        UintSet.insert(set.data, set.l, set.r, set.sz, 0, from);

        int ans = -1;
        while(i < j){
            if(to == Q[i].Q) {
                ans = int(i);
                break;
            }

            for(uint k = 0; k < users[Q[i].Q].neighbours.length; ++k){
                if(UintSet.find(set.data, set.l, set.r, set.sz, 0, users[Q[i].Q].neighbours[k])) continue;

                UintSet.insert(set.data, set.l, set.r, set.sz, 0, users[Q[i].Q].neighbours[k]);
                Q[j++] = intPairUint(users[Q[i].Q].neighbours[k], int(i));
            }

            i++;
        }

        int[1001] memory path;
        i = 0;
        while(ans > 0){
            path[i++] = int(Q[uint(ans)].Q);
            ans = Q[uint(ans)].p;
        }
        path[i++] = -1;
        return path;
    }


*/
 