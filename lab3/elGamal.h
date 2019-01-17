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

/*! \mainpage
 *
 * \section intro_sec Introduction
 *
 * In cryptography, the ElGamal encryption system is an asymmetric key encryption algorithm for public-key cryptography
 * which is based on the Diffie–Hellman key exchange.
 * The system provides an additional layer of security by asymmetrically encrypting keys previously used for symmetric message encryption.
 * It was described by Taher Elgamal in 1985. ElGamal encryption is used in the free GNU Privacy Guard software, recent versions of PGP, and other cryptosystems.
 * The Digital Signature Algorithm (DSA) is a variant of the ElGamal signature scheme, which should not be confused with ElGamal encryption.
 * ElGamal encryption can be defined over any cyclic group G.
 * Its security depends upon the difficulty of a certain problem in G related to computing discrete logarithms.
 *
 * \section install_sec The algorithm
 * ElGamal encryption consists of three components: the key generator, the encryption algorithm, and the decryption algorithm.
 *
 * \subsection key_generation Key generation
 *
 * The key generator works as follows:
 *
 * - Alice generates an efficient description of a cyclic group G, of order q, with generator g.
 * - Alice chooses an x randomly from [1..q-1].
 * - Alice computes h = g^x.
 * - Alice publishes h, along with the description of G, q, g as her public key.
 *   Alice retains x as her private key, which must be kept secret.
 *
 * \subsection encryption Encryption
 *
 * The encryption algorithm works as follows: to encrypt a message m to Alice under her public key (G,q,g,h),
 *
 * - Bob chooses a random y from [1...q-1], then calculates alpha =g^y.
 * - Bob calculates the shared secret s = h^y = g^xy.
 * - Bob maps his message m onto an element m' of G.
 * - Bob calculates beta = m' * s.
 * - Bob sends the ciphertext (alpha, beta) = (g^y, m' * h^y) = (g^y, m' * g^xy)} to Alice.
 *
 * Note that one can easily find h^y if one knows m'.
 * Therefore, a new y is generated for every message to improve security. For this reason, y is also called an ephemeral key.
 *
 * \subsection decryption Decryption
 *
 * The decryption algorithm works as follows: to decrypt a ciphertext (alpha, beta) with her private key x,
 *
 * - Alice calculates the shared secret s:=alpha^x
 * - and then computes m':=beta * s^(-1) which she then converts back into the plaintext message m,
 *   where s^(-1) is the inverse of s in the group G.
 *   (E.g. modular multiplicative inverse if G is a subgroup of a multiplicative group of integers modulo n).
 *
 * The decryption algorithm produces the intended message, since
 *
 *     beta * s^(-1) = m' * h^y * (g^xy)^(-1) = m' * g^xy * g^(-xy) = m'.
 *
 * \subsection credits Credits
 * - Vitca Vlad Ilie (grupa 237)
 * - Hanc Bogdan (grupa 332)
 */

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

	/**
	 * @brief Bigint class used everywhere within this algorithm.
	 */
	typedef mpz_class bigint;

	/**
	 * @brief The alphabet upon which the encryption and decryption takes place
	 *
	 * @return string - alphabet as a sequence of distinct characters
	 */
	//static string alphabet = " `1234567890-=~!@#$%^&*()_+qwertyuiop[{}]\\|asdfghjkl;:'\"zxcvbnm,<.>/?QWERTYUIOPASDFGHJKLZXCVBNM\n";
	static string alphabet = " abcdefghijklmnopqrstuvwxyz";


	/**
	 * @brief Separator of keys in the serialization and deserialization of
	 * public and private keys
	 */
	static char separator = '\n';

	/**
	 * @brief Structured public key, used in encryption.
	 * Contains:
	 *  - p : a big prime
	 *  - g : a generator of Zp
	 *  - ga : g^a
	 */
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

	/**
	 * @brief Structured private key, used in decryption.
	 * Contains:
	 *  - p : a big prime
	 *  - a : random number which is used as private key
	 */
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

	/**
	 * @brief Text block as an integer
	 */
	struct plaintext_block_t {
		bigint value;
	};

	/**
	 * @brief Ciphertext block as a pair of integers (alpha, beta)
	 */
	struct ciphertext_block_t {
		bigint alpha, beta;
	};

	/**
	 * @brief Vector of ciphertext blocks
	 */
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
} /* elGamal */

#endif /* end of include guard: ELGAMAL_H_JEUXOVXY */
