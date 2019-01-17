#include "elGamal.h"

#include <iostream>

namespace elGamal
{
	/**
	 * @brief Internal state of the elGamal algorithm
	 */
	namespace
	{
		/**
		 * @brief Defines if the internal state is initialized or not
		 */
		static bool initialized = false;
		/**
		 * @brief Number of primes against which is tested the initial
		 * composition of a bit possible prime.
		 */
		static int no_primes = 10000;
		/**
		 * @brief Half of the number of digits in base 10 of the prime used in
		 * key generation.
		 */
		static unsigned int security_order = 50;
		/**
		 * @brief Internal vector of small primes for fast composite number
		 * sieving.
		 */
		static vector<bigint> smallPrimes{};
		/**
		 * @brief Random state for mersene twister uniform random number
		 * generator.
		 */
		static gmp_randstate_t randstate;

		/**
		 * @brief Initializes the internal state.
		 */
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

		/**
		 * @brief Checks if a number n is prime
		 *
		 * @param n - The number to be checked
		 *
		 * @return true if prime, false if not
		 */
		bool is_prime(const bigint& n) {
			bigint sqrtn;
			bool is_square = mpz_root(sqrtn.get_mpz_t(), n.get_mpz_t(), 2);
			if (is_square)
				return false;
			for (auto& prime : smallPrimes) {
				if (prime > sqrtn)
					return true;
				if (n % prime == 0)
					return false; // n decomposable by small primes
			}

			return mpz_probab_prime_p(n.get_mpz_t(), 50) != 0;
		}

		/**
		 * @brief Generates a random prime between a lower and an upper bound
		 *
		 * @param lo - lower bound
		 * @param hi - upper bound
		 *
		 * @return - Integer - the prime
		 */
		bigint randomPrime(const bigint& lo, const bigint& hi) {
			if (!initialized)
				initialize();

			// now i'll generate numbers between low and hi
			// test them against small primes
			// and if they are not composite of small primes
			// test with rabin-miller
			bigint rangecount = hi - lo;
			bigint big_prime;
			do {
				mpz_urandomm(big_prime.get_mpz_t(), randstate, rangecount.get_mpz_t());
				big_prime += lo;  // generate random number between low and high
			} while (!is_prime(big_prime));

			return big_prime;
		}

		/**
		 * @brief Generates a random prime of a given number of digits
		 *
		 * @param no_digits - Integer, number of digits of the generated prime
		 *
		 * @return Integer - the prime
		 */
		bigint randomPrime(unsigned long int no_digits) {
			bigint lo, hi;
			mpz_ui_pow_ui(lo.get_mpz_t(), 10, no_digits -1);
			mpz_ui_pow_ui(hi.get_mpz_t(), 10, no_digits);
			return randomPrime(lo, hi);
		}

		/**
		 * @brief Returns the number of digits of a number in a given base
		 *
		 * @param n - the number
		 * @param base - the base
		 *
		 * @return The number of digits
		 */
		unsigned int no_digits(bigint n, int base) {
			unsigned int digits = 0;
			while (n > 0){
				n /= base;
				digits++;
			}
			return digits;
		}

		/**
		 * @brief Transfrms a string into a number
		 *
		 * @param str - the string
		 * @param alphabet - the alphabet which is the base of the string
		 *
		 * @return The 10th base representaion of str
		 */
		bigint string_to_number(const string& str, const string& alphabet) {
			unsigned int base = alphabet.length();
			bigint val = 0;
			for (const char *c = str.c_str(); *c; ++c) {
				val *= base;
				val += alphabet.find(*c);
			}

			return val;
		}

		/**
		 * @brief Transforms a number into a string
		 *
		 * @param num - the number
		 * @param alphabet - the alphabet which will be the bse of the output string
		 * @param block_length - the block length of the string, if the string
		 * representation is smaller, it will be padded with 0 in the given alphabet
		 *
		 * @return The "alphabet"th base representation of num
		 */
		string number_to_string(bigint num, const string& alphabet, unsigned int block_length) {
			unsigned int base = alphabet.length();
			string str;
			while (num > 0){
				bigint pos = num % base;
				str.push_back(alphabet.at(pos.get_ui()));
				num /= base;
			}
			unsigned int str_length = str.length();
			for (unsigned int i = 0; i < block_length - str_length; ++i)
				str.push_back(alphabet.at(0));
			reverse(str.begin(), str.end());
			return str;
		}

		/**
		 * @brief Computes the necessary length of the message blocks.
		 *
		 * @param p - prime number
		 * @param alphabet - the alphabet of the message
		 *
		 * @return Number of digits in the alphabet
		 */
		unsigned int message_block_length(const bigint& p, const string& alphabet) {
			return no_digits(p, alphabet.length()) - 1;
		}
	}

	pair<public_key_t, private_key_t> generateKey() {
		if (!initialized)
			initialize();

		bigint p;
		bigint q;
		do {
			q = randomPrime(security_order);
			p = 2*q + 1;
		} while(!is_prime(p));
		// here i have a big prime p = 2q+1 where q is prime as well
		// results all subgroups of Zp* have order 1, 2, q or p-1
		// so i have to get a generator of order Zp*
		bigint g;
		bigint rangecount = p -2;
		while (1) {
			// the generator will be a number between ∈ [2..p-1]
			mpz_urandomm(g.get_mpz_t(), randstate, rangecount.get_mpz_t());
			g+=2;

			// test to see if probable generator for Zp*
			bigint res;
			// test if g^q mod p == 1 to see if it's actually a generator for Gq
			// and not Zp*
			mpz_powm(res.get_mpz_t(), g.get_mpz_t(), q.get_mpz_t(), p.get_mpz_t());
			if (res == 1)
				continue;

			// test if somehow g is a generator for G0 or G1
			mpz_powm_ui(res.get_mpz_t(), g.get_mpz_t(), 2, p.get_mpz_t());
			if (res == 1)
				continue;

			break; // i found my generator
		}
		// so i have generator g of cyclic group Zp*
		// generate random number between 1 and p -2
		bigint a;
		rangecount = p - 3;
		mpz_urandomm(a.get_mpz_t(), randstate, rangecount.get_mpz_t());
		a += 1;

		// compute g^a mod p
		bigint ga;
		mpz_powm(ga.get_mpz_t(), g.get_mpz_t(), a.get_mpz_t(), p.get_mpz_t());

		return {{p, g, ga}, {p, a}};
	}

	ciphertext_t encrypt(const public_key_t& key, const string& _plaintext) {
		if (!initialized)
			initialize();

		vector<ciphertext_block_t> encrypted;

		string plaintext = _plaintext;
		unsigned int block_length = message_block_length(key.p, alphabet);
		unsigned int padding = block_length - (plaintext.length() % block_length);
		if (plaintext.length() % block_length != 0)
			for (unsigned int i = 0; i < padding; ++i)
				plaintext.push_back(alphabet.at(0));
		unsigned int no_blocks = plaintext.length() / block_length;
		bigint rangecount = key.p -3;
		for (unsigned int i = 0; i < no_blocks; ++i) {
			bigint message = string_to_number(plaintext.substr(i*block_length, block_length), alphabet);
			bigint k;
			mpz_urandomm(k.get_mpz_t(), randstate, rangecount.get_mpz_t());
			k += 1;
			bigint alpha;
			mpz_powm(alpha.get_mpz_t(), key.g.get_mpz_t(), k.get_mpz_t(), key.p.get_mpz_t());
			bigint beta;
			mpz_powm(beta.get_mpz_t(), key.ga.get_mpz_t(), k.get_mpz_t(), key.p.get_mpz_t());
			beta *= message;
			beta %= key.p;
			encrypted.push_back({alpha, beta});
		}
		return {encrypted};
	}

	string decrypt(const private_key_t& key, ciphertext_t ciphertext) {
		unsigned int block_length = message_block_length(key.p, alphabet);
		string message = "";
		bigint minus_a = -key.a;
		for (auto& block : ciphertext.val) {
			bigint decrypted_val;
			mpz_powm(decrypted_val.get_mpz_t(), block.alpha.get_mpz_t(), minus_a.get_mpz_t(), key.p.get_mpz_t());
			decrypted_val *= block.beta;
			decrypted_val %= key.p;

			message += number_to_string(decrypted_val, alphabet, block_length);
		}
		return message;
	}

	string encrypt_s(const public_key_t& key, const string& _plaintext) {
		string encrypted = "";
		unsigned int block_length = message_block_length(key.p, alphabet) + 1;
		auto blocks = encrypt(key, _plaintext);
		for (auto& block : blocks.val) {
			encrypted += number_to_string(block.alpha, alphabet, block_length);
			encrypted += number_to_string(block.beta, alphabet, block_length);
		}

		return encrypted;
	}
	string decrypt_s(const private_key_t& key, string ciphertext) {
		ciphertext_t encrypted;
		unsigned int block_length = message_block_length(key.p, alphabet) + 1;
		unsigned int no_blocks = (ciphertext.length() / block_length) /2;
		for (unsigned int i = 0; i < no_blocks; ++i) {
			encrypted.val.push_back({
				string_to_number(ciphertext.substr(2*i*block_length, block_length), alphabet),
				string_to_number(ciphertext.substr((2*i+1)*block_length, block_length), alphabet)
					});
		}
		return decrypt(key, encrypted);
	}

	/**
	 * @brief Helper function used for unit tests
	 *
	 * @param b - boolean
	 * @param message - Error message thrown in case b does not check
	 */
	void assert_true(bool b, const string&& message) {
		if (!b)
			throw message;
	}
} /* elGamal */
