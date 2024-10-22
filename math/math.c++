#include <vector>
#include "./builtins/core.h"
#include <tuple>
using namespace std;
class math{
	public:
vector<float> abs(vector<float> x){
		if (x<encode(0)){
		return(x*-encode(2))+x;
	}
		else{
		return x;
	}
	}
vector<float> sqrt(vector<float> x){
		return x*(encode(1)/encode(2));
	}
vector<float> pow(vector<float> x,vector<float> y){
		vector<float> z = x;
		for (float& i : range(y)){
		z = z*x;
	}
		return z;
	}
		void main(){
				}
};
