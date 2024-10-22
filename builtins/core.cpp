#include <string>
#include <iostream>
#include <vector>
#include <fstream>
#include "./core.h"

using namespace std;

vector<float> operator+(vector<float> lhs, vector<float> rhs){
    size_t len_lhs, len_rhs;
    len_lhs = lhs.size();
    len_rhs = rhs.size();
    
    // both are int or float
    if ((lhs[0] == 0 || lhs[0] == 1) && (rhs[0] == 0 || rhs[0] == 1)){
        vector<float> result;
        if (lhs[0] == 1 || rhs[0] == 1){ result.emplace_back(1); }
        else { result.emplace_back(0); }

        result.emplace_back(1);
        result.emplace_back(lhs[2]+rhs[2]);
        return result;
    }
    // both are string
    else if (lhs[0] == 2 && rhs[0] == 2){
        vector<float> result;
        result.emplace_back(2);
        result.emplace_back(lhs[1]+rhs[1]);
        size_t i = 2;
        size_t j = 2;

        for (float& x : lhs){
            if (i>0){i-=1;}
            else{
                result.emplace_back(x);
            }
        }

        for (float& x : rhs){
            if (i>0){i-=1;}
            else{
                result.emplace_back(x);
            }
        }
        return result;
    }
    else {
        return encode("Error appeared by adding to different datatype...");
    }

}

vector<float> operator-(vector<float> lhs, vector<float> rhs){
    size_t len_lhs, len_rhs;
    len_lhs = lhs.size();
    len_rhs = rhs.size();
    
    // both are int or float
    if ((lhs[0] == 0 || lhs[0] == 1) && (rhs[0] == 0 || rhs[0] == 1)){
        vector<float> result;
        if (lhs[0] == 1 || rhs[0] == 1){ result.emplace_back(1); }
        else { result.emplace_back(0); }

        result.emplace_back(1);
        result.emplace_back(lhs[2]-rhs[2]);
        return result;
    }
    else {
        return encode("Error appeared by adding to different datatype...");
    }

}

vector<float> operator*(vector<float> lhs, vector<float> rhs){
    size_t len_lhs, len_rhs;
    len_lhs = lhs.size();
    len_rhs = rhs.size();
    
    // both are int or float
    if ((lhs[0] == 0 || lhs[0] == 1) && (rhs[0] == 0 || rhs[0] == 1)){
        vector<float> result;
        if (lhs[0] == 1 || rhs[0] == 1){ result.emplace_back(1); }
        else { result.emplace_back(0); }

        result.emplace_back(1);
        result.emplace_back(lhs[2]*rhs[2]);
        return result;
    }
    // both are string
    else if ((lhs[0] == 0 && rhs[0] == 2) || (lhs[0] == 2 && rhs[0] == 0)){
        vector<float> result;
        result.emplace_back(2);
        int times;
        if (lhs[0] = 2){
            result.emplace_back(lhs[1]*rhs[2]);
            times = rhs[2];
        }
        else {
            result.emplace_back(lhs[2]*rhs[1]);
            times = lhs[2];
        }
        size_t i = 2;

        for (int j = 0; j < times; j++){
            for (float& x : lhs){
                if (i>0){i-=1;}
                else{
                    result.emplace_back(x);
                }
            }
            i = 2;
        }
        return result;
    }
    else {
        return encode("Error appeared by adding to different datatype...");
    }

}

vector<float> operator/(vector<float> lhs, vector<float> rhs){
    size_t len_lhs, len_rhs;
    len_lhs = lhs.size();
    len_rhs = rhs.size();
    
    // both are int or float
    if ((lhs[0] == 0 || lhs[0] == 1) && (rhs[0] == 0 || rhs[0] == 1)){
        vector<float> result;
        if (lhs[0] == 1 || rhs[0] == 1){ result.emplace_back(1); }
        else { result.emplace_back(0); }

        result.emplace_back(1);
        result.emplace_back(lhs[2]/rhs[2]);
        return result;
    }
    else {
        return encode("Error appeared by adding to different datatype...");
    }

}

vector<float> encode(int a) {
    return vector<float> {0, 1, static_cast<float>(a)};
}

vector<float> encode(double a){
    return vector<float> {1, 1, static_cast<float>(a)};
}

vector<float> encode(string a){
    size_t len = a.length();
    vector<float> temp;
    temp.emplace_back(2);
    temp.emplace_back(len);

    for (char& c : a){
        temp.emplace_back(static_cast<float>(static_cast<int>(c)));
    }

    return temp;
}

vector<float> type(vector<float> x){
    if (x[0] == 0) { return encode("Encoded - Integer"); }
    else if (x[0] == 1) { return encode("Encoded - Float"); }
    else if (x[0] == 2) { return encode("Encoded - String"); }
    else { return encode("Unknown"); }
}

vector<float> type(int x){
    return encode("Integer");
}

vector<float> type(float x){
    return encode("Float");
}

vector<float> type(string x){
    return encode("String");
}

// Prints
// template<typename T>
// void print(T value = "") {
//     if (value[0] == 0 || value[0] == 1){ cout << value[2] << endl; }
//     else if (value[0] == 2){
//         size_t length = value[1];
//         for (int i = 2; i < length+2; i++){
//             cout << static_cast<char>(static_cast<int>(value[i]));
//         }
//         cout << endl;
//     }
//     else if (value[0] == 3){
//         size_t length = value[1];
//         cout << "[ ";
//         for (int i = 2; i < length+2; i++){
//             cout << static_cast<int>(value[i]) << ' ';
//         }
//         cout << "]" << endl;
//     }
// }

// template<typename T, typename... Args>
// void print(T value, Args... args){
//     if (value[0] == 0 || value[0] == 1){ cout << value[2] << ' '; }
//     else if (value[0] == 2){
//         size_t length = value[1];
//         for (int i = 2; i < length+2; i++){
//             cout << static_cast<char>(static_cast<int>(value[i]));
//         }
//         cout << ' ';
//     }
//     else if (value[0] == 3){
//         size_t length = value[1];
//         cout << "[ ";
//         for (int i = 2; i < length+2; i++){
//             cout << static_cast<int>(value[i]) << ' ';
//         }
//         cout << "]";
//     }
//     print(args...);
// }

// void print(){
//     cout << endl;
// }

// converts
int decoded_int(vector<float> x){
    return static_cast<int>(x[2]);
}

float decoded_float(vector<float> x){
    return x[2];
}

string decoded_string(vector<float> x){
    string str;
    int len = x[2] + 2;
    for (int i = 2; i < len; i++){
        str+=static_cast<char>(x[i]);
    }
    return str;
}

// inputs
vector<float> input(vector<float> x){
    cout << decoded_string(x);
    string temp;
    cin >> temp;
    return encode(temp);
}

vector<float> range(vector<float> a, string callid) {
    vector<float> map;
    if (callid != "for") {
        map.emplace_back(3);
        map.emplace_back(decoded_int(a));
    }
    for (int i = 0; i < decoded_int(a); i++) {
        map.emplace_back(i);
    }
    return map;
}

vector<float> read(vector<float>file){
    ifstream inputFile(decoded_string(file));
    if (!inputFile){
        print(encode("Unable to locate file: "), file);
        return encode("");
    }

    vector<float> data;
    data.emplace_back(2);
    int len = 0;
    string line;

    vector<float> chars;
    while(getline(inputFile, line)){
        len+=line.length();
        for (char& c : line){
            chars.emplace_back(c);
        }
    }
    data.emplace_back(len);

    for (auto& i : chars){
        data.emplace_back(i);
    }

    inputFile.close();
    return data;
}

void write(vector<float>line, vector<float>file){
    ofstream inputFile(decoded_string(file));
    if (!inputFile){
        print(encode("Unable to locate file: "), file);
    }
    else{
        inputFile << decoded_string(line) << endl;
        inputFile.close();
    }
}

vector<float> len(vector<float> x){
    return vector<float> {0, 1, x[1]};
}