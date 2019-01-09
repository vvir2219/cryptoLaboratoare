#include <vector>
#include <tuple>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

using std::vector;
using std::tuple;
using std::make_tuple;
using std::get;


// returns a vector of (prime_factor, power)
vector<tuple<unsigned long, unsigned long>> factor(unsigned long n)
{
	auto factors = vector<tuple<unsigned long, unsigned long>>();
	auto current_factor = 2;
	while (n > 1){
		if (n % current_factor == 0){
			auto power = 0;
			while (n % current_factor == 0){
				n = n / current_factor;
				++power;
			}
			factors.push_back(make_tuple(current_factor, power));
		}
		else{
			current_factor++;
		}
	}

	return factors;
}

unsigned long phi( unsigned long n)
{
	if (n == 0)
		return 0;
	if (n == 1)
		return 1;

	double _phi = 1;
	auto factors = factor(n);
	printf("%ld = ", n);

	for (auto factor : factors){
		auto prime = get<0>(factor);
		auto power = get<1>(factor);
		printf("%ld^%ld + ", prime, power);
		_phi *= (1 - 1.0/prime);
	}
	_phi *= n;
	printf("0 -->  phi(%ld) = %ld\n", n, (unsigned long)_phi);

	return _phi;
}

int main(int argc, char *argv[])
{
	if (argc != 3){
		fprintf(stderr, "Usage: ./a.out value bound\n Prints all numbers between 0 and b which respect phi(i) = value\n");
		return -1;
	}

	auto good_values = vector<unsigned long>();
	unsigned int value = atoi(argv[1]);
	unsigned int bound = atoi(argv[2]);

	for(unsigned int i = 0; i < bound; ++i){ 
		if (phi(i) == value)
			good_values.push_back(i);
	}
	printf("\n");
	printf("Values for which phi(n) == %d\n", value);

	for (auto value : good_values) {
		printf("%ld ", value);
	}
	printf("\n");

	return 0;
}
