#ifndef CORE_H
#define CORE_H

#include <string>
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

// Encodes
vector<float> encode(int a);
vector<float> encode(double a);
vector<float> encode(string a);

// Types
vector<float> type(vector<float> x);
vector<float> type(int x);
vector<float> type(float x);
vector<float> type(string x);

// Operator overloads
vector<float> operator+(vector<float> lhs, vector<float> rhs);
vector<float> operator-(vector<float> lhs, vector<float> rhs);
vector<float> operator*(vector<float> lhs, vector<float> rhs);
vector<float> operator/(vector<float> lhs, vector<float> rhs);

// Prints
template<typename T>
void print(T value = "");

template<typename T, typename... Args>
void print(T value, Args... args);

void print();

// Converts
int decoded_int(vector<float> x);
float decoded_float(vector<float> x);
string decoded_string(vector<float> x);

// Inputs
vector<float> input(vector<float> x = encode(""));

vector<float> range(vector<float> a, string callid = "");

vector<float> read(vector<float> file);
void write(vector<float> line, vector<float> file);

// Utility
vector<float> len(vector<float> x);

// Include the implementation for template functions here as templates need to be defined in the header file

template<typename T>
void print(T value) {
    if (value[0] == 0 || value[0] == 1) {
        cout << value[2] << endl;
    }
    else if (value[0] == 2) {
        size_t length = value[1];
        for (int i = 2; i < length + 2; i++) {
            cout << static_cast<char>(static_cast<int>(value[i]));
        }
        cout << endl;
    }
    else if (value[0] == 3) {
        size_t length = value[1];
        cout << "[ ";
        for (int i = 2; i < length + 2; i++) {
            cout << static_cast<int>(value[i]) << ' ';
        }
        cout << "]" << endl;
    }
}

template<typename T, typename... Args>
void print(T value, Args... args) {
    if (value[0] == 0 || value[0] == 1) {
        cout << value[2] << ' ';
    }
    else if (value[0] == 2) {
        size_t length = value[1];
        for (int i = 2; i < length + 2; i++) {
            cout << static_cast<char>(static_cast<int>(value[i]));
        }
        cout << ' ';
    }
    else if (value[0] == 3) {
        size_t length = value[1];
        cout << "[ ";
        for (int i = 2; i < length + 2; i++) {
            cout << static_cast<int>(value[i]) << ' ';
        }
        cout << "]";
    }
    print(args...);
}

#endif // CORE_H
