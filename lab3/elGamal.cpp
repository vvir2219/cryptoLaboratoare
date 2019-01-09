#include "elGamal.h"

#include <iostream>

namespace elGamal
{
	namespace
	{
		static bool initialized = false;
		static int no_primes = 10000;
		static vector<bigint> smallPrimes{};
		static gmp_randstate_t randstate;

		void initialize() {
			smallPrimes.clear();

			smallPrimes.push_back(2);
			for (int i = 1; i < no_primes; ++i) {
				smallPrimes.push_back(0);
				mpz_nextprime(smallPrimes.back().get_mpz_t(), smallPrimes.at(i-1).get_mpz_t());
			}

			// initialize the state of the random algorithm
			gmp_randinit_mt(randstate); // mersene twister
			struct timespec spec;
			clock_gettime(CLOCK_MONOTONIC, &spec);
			unsigned long int seed = spec.tv_nsec;
			gmp_randseed_ui(randstate, seed);
			initialized = true;
		}

		mp_bitcnt_t no_bits(const bigint& n) {
			mp_bitcnt_t remaining = mpz_popcount(n.get_mpz_t()), last = -1;
			while (remaining) {
				last = mpz_scan1(n.get_mpz_t(), last + 1);
				remaining--;
			}
			return last;
		}

		bigint randomPrime(const bigint& lo, const bigint& hi) {
			if (!initialized)
				initialize();

			// now i'll generate numbers between low and hi
			// test them against small primes
			// and if they are not composite of small primes
			// test with rabin-miller
			bigint rangecount = hi - lo;
			int isPrime = 0;
			bigint big_prime;
			while(!isPrime) {
				mpz_urandomm(big_prime.get_mpz_t(), randstate, rangecount.get_mpz_t());
				big_prime += lo;  // generate random number between low and high
				for (auto& prime : smallPrimes)
					if (big_prime % prime == 0)
						continue; // big_prime decomposable by small primes

				isPrime = mpz_probab_prime_p(big_prime.get_mpz_t(), 50);
			}

			return big_prime;
		}

		bigint randomPrime(unsigned long int no_digits) {
			bigint lo, hi;
			mpz_ui_pow_ui(lo.get_mpz_t(), 10, no_digits -1);
			mpz_ui_pow_ui(hi.get_mpz_t(), 10, no_digits);
			return randomPrime(lo, hi);
		}

	}

	struct public_key_t {
		bigint p, g, ga;
	};

	struct private_key_t {
		bigint p, a;
	};

	struct plaintext_block_t {
		bigint value;
	};

	struct ciphertext_block_t {
		bigint alpha, beta;
	};

	pair<public_key_t, private_key_t> generateKey() {
		return {{}, {}};
	}

	vector<ciphertext_block_t> encrypt(const public_key_t& key, const string& plaintext) {
		return {};
	}

	string decrypt(const private_key_t& key, vector<ciphertext_block_t> ciphertext) {
		return "";
	}

	void test() {
		using namespace std;

		cout << randomPrime(100) << "\n";
		initialized = false;
	}
} /* elGamal */
