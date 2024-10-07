#include <string>
#include <iostream>
#include <vector>
#include <stdexcept>
#include <fstream>
using namespace std;

template<typename T>
void print(const T& value = "") {
    if (value[0] == 0 || value[0] == 1){ cout << value[2] << endl;}
    else if (value[0] == 2) {
        size_t length = value[1];
        for (int i = 0; i < length; i++){
            cout << static_cast<char>(value[i+2]);
        }
        cout << endl;
    }
}

template<typename T, typename... Args>
void print(const T& value, const Args&... args){
    if (value[0] == 0 || value[0] == 1){ cout << value[2] << ' ';}
    else if (value[0] == 2) {
        size_t length = value[1];
        for (int i = 0; i < length; i++){
            cout << static_cast<char>(value[i+2]);
        }
        cout << ' ';
    }
    // else {
    //     cout << value << ' ';
    // }
    print(args...);
}

void print() {
    std::cout << std::endl;
}

std::vector<float> concate(const std::vector<float> a, const std::vector<float> b) {
    vector<float> temp(a[1]+b[1]);
    temp[0] = a[0];
    temp[1] = a[1] + b[1];
    for (int i = 2; i < a[1]+2; i++){
        temp[i] = a[i];
    }

    for (int i = 2; i < b[1]+2; i++){
        temp[i+a[1]] = b[i];
    }

    return temp;
}

vector<float> operator+(const vector<float>& lhs, const vector<float>& rhs) {
    size_t length_lhs = lhs.size();
    size_t length_rhs = rhs.size();
    if (length_lhs != length_rhs){
        throw runtime_error("Datatype MissMatch !");
    }
    if ((lhs[0] == 0 || lhs[0] == 1) && (rhs[0] == 0 || rhs[0] == 1)){
        vector<float> result = {0, lhs[1], lhs[2] + rhs[2]};
        if (lhs[0] == 1){result[0] = lhs[0];}
        else if (rhs[0] == 1) {result[0] = rhs[0];}
        else {result[0] = rhs[0];}
        return result;
    }
    else if (lhs[0] == 2 && rhs[0] == 2){
        vector<float> result(lhs[1]+rhs[1]);
        result = concate(lhs, rhs);
        return result;
    }
    else{
        return lhs;
    }
}

vector<float> operator*(const vector<float>& lhs, const vector<float>& rhs) {
    size_t length_lhs = lhs.size();
    size_t length_rhs = rhs.size();
    if ((lhs[0] == 0 || lhs[0] == 1) && (rhs[0] == 0 || rhs[0] == 1)){
        vector<float> result = {0, lhs[2], lhs[2] * rhs[2]};
        if (lhs[0] == 1){result[0] = lhs[0];}
        else if (rhs[0] == 1) {result[0] = rhs[0];}
        else {result[0] = rhs[0];}
        return result;
    }
    else if (lhs[0] == 2 && rhs[0] == 0){
        vector<float> result = lhs;
        result[1] = lhs[1]*rhs[2];
        for (int i=2; i<rhs[2]; i++){
            result = concate(result, lhs);
        }
        print(lhs);
        cout << result.size() << endl;
        return result;
    }
    else{
        return lhs;
    }
}

int integer(vector<float> temp){
    return static_cast<int>(temp[2]);
}
float floater(vector<float> temp){
    return static_cast<float>(temp[2]);
}

string str(vector<float> temp){
    string root;
    for (int i = 2; i<temp.size();i++){
        root += static_cast<char>(static_cast<int>(temp[i]));
    }
    return root;
}

vector<float> encode(int a){
    vector<float> temp = {0, 1,  static_cast<float>(a)};
    return temp;
}

vector<float> encode(float a){
    vector<float> temp = {1, 1,  a};
    return temp;
}

vector<float> encode(const string& a) {
    vector<float> temp(a.length() + 2);
    temp[0] = 2;
    temp[1] = a.length();

    for (size_t i = 0; i < a.length(); i++) {
        cout << '\0'; // there's some glitch making cout to printed inoder to add spaces
        temp[i + 2] = static_cast<int>(a[i]);
    }

    return temp;
}

vector<float> input(vector<float> a){
    cout << str(a);
    string inp;
    cin >> inp;
    vector<float> temp = encode(inp);
    return temp;
}

vector<vector<float>> range(vector<float> a) {
    vector<vector<float>> map(integer(a));
    for (int i = 0; i < integer(a); i++) {
        map[i] = vector<float>(3);
        map[i][0] = 0;
        map[i][1] = 1;
        map[i][2] = i;
    }
    return map;
}

vector<float> read(vector<float>file){
    ifstream inputFile(str(file));
    if (!inputFile) {
        std::cerr << "Unable to open file example.txt";
        vector<float> x = {0, 1, 0};
        return x; // Exit with error code
    }

    vector<float> dummy;
    dummy.emplace_back(2);
    int len = 0;
    string line;

    vector<float> chara;
    while (getline(inputFile, line)){
        len += line.length();
        vector<float> temp = encode(line);
        for (int i = 2; i<temp.size(); i++){
            chara.emplace_back(temp[i]);
        }
    }
    dummy.emplace_back(len);
    
    for (const auto& i : chara){
        dummy.emplace_back(i);
    }

    inputFile.close();
    return dummy;
}

void write(vector<float>line, vector<float>file){
    ofstream inputFile(str(file));
    if (!inputFile) {
        std::cerr << "Unable to open file example.txt";
    }
    
    inputFile << str(line) << endl;
    inputFile.close();
}