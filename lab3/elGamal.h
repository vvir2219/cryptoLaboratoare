#include <gmp.h>
#include <gmpxx.h>
#include <time.h>

#include <vector>
#include <string>

#ifndef ELGAMAL_H_JEUXOVXY
#define ELGAMAL_H_JEUXOVXY

namespace elGamal
{
	using std::pair,
		  std::vector,
		  std::string;

	typedef mpz_class bigint;

	struct public_key_t;
	struct private_key_t;
	struct plaintext_block_t;
	struct ciphertext_block_t;

	pair<public_key_t, private_key_t> generateKey();
	vector<ciphertext_block_t> encrypt(const public_key_t& key, const string& plaintext);
	string decrypt(const private_key_t& key, vector<ciphertext_block_t> ciphertext);

	void test();
} /* elGamal */

#endif /* end of include guard: ELGAMAL_H_JEUXOVXY */
