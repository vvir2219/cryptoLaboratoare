#include <vector>

using std::vector;


vector<unsigned long> factor(unsigned long n)
{
	return vector<unsigned long>();
}

unsigned long phi( unsigned long n)
{
	if (n == 0)
		return 0;
	if (n == 1)
		return 1;

	unsigned long _phi = 1;
	for (auto prime : factor(n))
		_phi *= (prime - 1);

	return _phi;
}

int main(int argc, char *argv[])
{
	
	return 0;
}
