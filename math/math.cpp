#include "/home/bluefox/Documents/document.bak/Documents/Avntum/builtins/core.h"
#include <vector>
#include <tuple>
using namespace std;
class math{
	public:
vector<float> sqrt(vector<float> x){
		return x*encode(1)/encode(2);
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