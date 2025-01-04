#include <iostream>
#include <vector>
using namespace std;


int main() {

    int sz = 20;
    vector<vector<long long>> matrix(sz, vector<long long>(sz, 0));
    for (int i = 0; i < sz; i++) {
        for (int j = 0; j < sz; j++) {
            cin>>matrix[i][j];
        }
    }

    long long ans = 0;
    for (int i = 0; i < sz; i++) {
        for (int j = 0; j < sz; j++) {
            long long product = 1;
            for (int k = 0; k < 4 && j+k < sz; k++) {
                product *= matrix[i][j+k];
            }

            ans = max(ans, product);
            product = 1;
            for (int k = 0; k < 4 && i+k < sz; k++) {
                product *= matrix[i+k][j];
            }

            ans = max(ans, product);
            product = 1;
            for (int k = 0; k < 4 && i+k < sz && j+k < sz; k++) {
                product *= matrix[i+k][j+k];
            }

            ans = max(ans, product);
            product = 1;
            for (int k = 0; k < 4 && i+k < sz && j-k >= 0; k++) {
                product *= matrix[i+k][j-k];
            }

            ans = max(ans, product);
        }
    }

    cout<<ans<<endl;
    return 0;
}
