#include <gmp.h>
#include <gmpxx.h>
#include <time.h>

#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <sstream>

#ifndef ELGAMAL_H_JEUXOVXY
#define ELGAMAL_H_JEUXOVXY

namespace elGamal
{
	using std::pair,
		  std::vector,
		  std::string,
		  std::reverse;

	typedef mpz_class bigint;

	struct public_key_t;
	struct private_key_t;
	struct ciphertext_t;

	pair<public_key_t, private_key_t> generateKey();
	ciphertext_t encrypt(const public_key_t& key, const string& plaintext);
	string decrypt(const private_key_t& key, ciphertext_t ciphertext);

	string encrypt_s(const public_key_t& key, const string& plaintext);
	string decrypt_s(const private_key_t& key, string ciphertext);

	void test();
} /* elGamal */

#endif /* end of include guard: ELGAMAL_H_JEUXOVXY */
