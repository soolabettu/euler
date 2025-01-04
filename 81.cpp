#include <iostream>
#include <vector>
using namespace std;


int main() {

    int sz = 80;
    vector<vector<int>> matrix(sz, vector<int>(sz, 0));
    for (int i = 0; i < sz; i++) {
        for (int j = 0; j < sz; j++) {
            cin>>matrix[i][j];
        }
    }

    for (int i = 1;i < sz;++i) {
        matrix[0][i] += matrix[0][i-1];
    }

    for (int i = 1;i < sz;++i) {
        matrix[i][0] += matrix[i-1][0];
    }


    for (int i = 1; i < sz; i++) {
        for (int j = 1; j < sz; j++) {
            matrix[i][j] += min(matrix[i-1][j], matrix[i][j-1]);
        }
    }

    // for (int i = 0; i < sz; i++) {
    //     for (int j = 0; j < sz; j++) {
    //         cout<<matrix[i][j]<<" ";
    //     }
    //     cout<<endl;
    // }

    cout<<matrix[sz-1][sz-1]<<endl;
    return 0;
}
