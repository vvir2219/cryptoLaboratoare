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

/**
 * @brief elGamal class, defines, public_key_t, private_key_t, ciphertext_t.
 * Functions : generateKey - generates a pair of containing public and private key
 * 			   encrypt, decrypt - encrypts and decrypts, works on blocks
 * 			   encrypt_s, decrypt_s - as above but works on strings
 */
namespace elGamal
{
	using std::pair,
		  std::vector,
		  std::string,
		  std::reverse;

	typedef mpz_class bigint;

	static string alphabet = " `1234567890-=~!@#$%^&*()_+qwertyuiop[{}]\\|asdfghjkl;:'\"zxcvbnm,<.>/?QWERTYUIOPASDFGHJKLZXCVBNM\n";
	static char separator = '\n';

	struct public_key_t {
		bigint p, g, ga;

		friend std::ostream & operator<<(std::ostream &os, const public_key_t& k) {
			os << k.g << separator << k.ga << separator << k.p;
			return os;
		}
		friend std::istream& operator >>(std::istream &is, public_key_t& k) {
			is >> k.g >> k.ga >> k.p;
			return is;
		}
	};

	struct private_key_t {
		bigint p, a;

		friend std::ostream & operator<<(std::ostream &os, const private_key_t& k) {
			os << k.a << separator << k.p;
			return os;
		}
		friend std::istream& operator >>(std::istream &is, private_key_t& k) {
			is >> k.a >> k.p;
			return is;
		}
	};

	struct plaintext_block_t {
		bigint value;
	};

	struct ciphertext_block_t {
		bigint alpha, beta;
	};

	struct ciphertext_t {
		vector<ciphertext_block_t> val;
	};

	/**
	 * @brief Generates public and private key
	 *
	 * @return A pair containg <public_key_t, private_key_t>
	 */
	pair<public_key_t, private_key_t> generateKey();
	/**
	 * @brief Encrypts a plaintext given as string using the provided key
	 *
	 * @param key public_key_t, returned by generateKey
	 * @param plaintext string, any string within the alphabet of the elGamal class
	 *
	 * @return ciphertext - ciphertext as a vector of tuples of numbers
	 */
	ciphertext_t encrypt(const public_key_t& key, const string& plaintext);
	/**
	 * @brief Decrypts the ciphertext (ciphertext_t) using a key
	 *
	 * @param key private_key_t, returned by generateKey
	 * @param ciphertext ciphertext_t returned by the encrypt method
	 *
	 * @return string - the plaintext
	 */
	string decrypt(const private_key_t& key, ciphertext_t ciphertext);

	/**
	 * @brief Encrypts a plaintext given as string using the provided key
	 *
	 * @param key public_key_t, returned by generateKey
	 * @param plaintext string, any string within the alphabet of the elGamal class
	 *
	 * @return string - encrypted text
	 */
	string encrypt_s(const public_key_t& key, const string& plaintext);
	/**
	 * @brief Decrypts the ciphertext (ciphertext_t) using a key
	 *
	 * @param key private_key_t, returned by generateKey
	 * @param string
	 *
	 * @return string - the plaintext
	 */
	string decrypt_s(const private_key_t& key, string ciphertext);

	void test();
} /* elGamal */

#endif /* end of include guard: ELGAMAL_H_JEUXOVXY */
