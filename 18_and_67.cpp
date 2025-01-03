#include <iostream>
#include <vector>
using namespace std;

int main() {

    vector<vector<int>> matrix(100, vector<int>(100, 0));
    for (int i = 0; i < 100; i++) {
        for (int j = 0; j <= i; j++) {
            cin>>matrix[i][j];
        }
    }

    for (int i = 98; i >= 0; i--) {
        for (int j = 98; j >= 0; j--) {
            if (matrix[i][j] == 0) {
                continue;
            }

            matrix[i][j] = max(matrix[i + 1][j], matrix[i + 1][j + 1]) + matrix[i][j];
        }

        cout << endl;
    }

    cout << matrix[0][0] << endl;
    return 0;
}