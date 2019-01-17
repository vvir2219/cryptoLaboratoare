#include <iostream>
#include <fstream>

#include "elGamal.h"


int main()
{
	// generates a pair of keys
	auto keys = elGamal::generateKey();

	// writes them to files
	std::ofstream f_public("public_key");
	std::ofstream f_private("private_key");

	f_public << keys.first;
	f_private << keys.second;

	f_public.close();
	f_private.close();

	// reads them from the files
	std::ifstream f_public_in("public_key");
	std::ifstream f_private_in("private_key");

	elGamal::public_key_t public_key;
	elGamal::private_key_t private_key;

	f_public_in >> public_key;
	f_private_in >> private_key;

	f_public_in.close();
	f_private_in.close();

	// uses them for encryption and decription
	std::string message = "ana are mere";
	std::string encrypted = elGamal::encrypt_s(public_key, message);
	elGamal::ciphertext_t alphasbetas = elGamal::encrypt(public_key, message);
	std::string decrypted = elGamal::decrypt_s(private_key, encrypted);

	std::cout << "Message: " << message << "\n";
	std::cout << "Encrypted message: " << encrypted << "\n";
	std::cout << "Decrypted message: " << decrypted << "\n";
	for (auto& block : alphasbetas.val){
		std::cout << block.alpha << " " << block.beta << "\n";
	}

	return 0;
}
