#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

// User solution is injected here
// USER_CODE_START
vector<int> two_sum(vector<int>& nums, int target) {
    return {};
}
// USER_CODE_END

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    int target;
    cin >> target;

    vector<int> result = two_sum(nums, target);
    for (int i = 0; i < result.size(); i++) {
        if (i > 0) cout << " ";
        cout << result[i];
    }
    cout << endl;

    return 0;
}