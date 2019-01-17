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
	std::string decrypted = elGamal::decrypt_s(private_key, encrypted);

	std::cout << "Message: " << message << "\n";
	std::cout << "Encrypted message: " << encrypted << "\n";
	std::cout << "Decrypted message: " << decrypted << "\n";

	// get the name of the key
    std::string key_name = "ion";
    std::ifstream is;
    // open the file with the key
    is.open(key_name + "_public_key");
    // if file exists
    if (is.is_open()) {
        // read the key
		elGamal::public_key_t key;
        is >> key;
        // close file as we don't need it anymore
        is.close();

        // now take the message from the textbox, encrypt it and write it back in the textbox
        std::string message = "ana are mere";
        std::string encrypted = encrypt_s(key, message);
		std::cout << encrypted << "\n";
        //this->ui->text_input->setText(QString::fromStdString(encrypt_s(key, message)));
    }
    else {
		std::cout << "Could not open key file.\n";
    }
	return 0;
}
