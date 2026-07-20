class Solution {
public:
    bool isAnagram(const string& s, const string& t) {
        if (s.size() != t.size()) {
            return false;
        }

        int counts[26] = {}; // all 26 elements are 0

        for (int i = 0; i < s.size(); i++) {
            counts[s[i] - 'a']++;
            counts[t[i] - 'a']--;
        }

        for (int c : counts) {
            if (c != 0) return false;
        }

        return true;
}
};