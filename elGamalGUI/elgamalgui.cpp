#include "elgamalgui.h"
#include "ui_elgamalgui.h"
#include <QtCore>
#include <QtGui>
#include <QMessageBox>

#include <fstream>
#include <string>
#include <iostream>

ElGamalGui::ElGamalGui(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::ElGamalGui)
{
    ui->setupUi(this);
}

ElGamalGui::~ElGamalGui()
{
    delete ui;
}

void ElGamalGui::on_button_gen_key_clicked()
{
    auto _key_name = this->ui->input_key_name->text();
    if (_key_name.isEmpty()) {
        QMessageBox::information(this, "Error", "Key name cannot be empty.");
        return;
    }
    std::string key_name = _key_name.toStdString();
    auto keys = generateKey();

    std::ofstream os;
    os.open(key_name + "_public_key");
    os << keys.first;
    os.close();

    os.open(key_name + "_private_key");
    os << keys.second;
    os.close();
    QMessageBox::information(this, "Information", "Keys were generated.");
}

void ElGamalGui::on_button_encode_clicked()
{
    // get the name of the key
    auto _key_name = this->ui->input_key_name->text();
    if (_key_name.isEmpty()) {
        QMessageBox::information(this, "Error", "Key name cannot be empty.");
        return;
    }

    std::string key_name = _key_name.toStdString();
    std::ifstream is;
    // open the file with the key
    is.open(key_name + "_public_key");
    // if file exists
    if (is.is_open()) {
        // read the key
        public_key_t key;
        is >> key;
        // close file as we don't need it anymore
        is.close();

        // now take the message from the textbox, encrypt it and write it back in the textbox
        std::string message = this->ui->text_input->toPlainText().toStdString();
        this->ui->text_input->setText(QString::fromStdString(encrypt_s(key, message)));
    }
    else {
        QMessageBox::information(this, "Error", "No such key found.");
    }
}

void ElGamalGui::on_button_decode_clicked()
{
    // get the name of the key
    auto _key_name = this->ui->input_key_name->text();
    if (_key_name.isEmpty()) {
        QMessageBox::information(this, "Error", "Key name cannot be empty.");
        return;
    }

    std::string key_name = _key_name.toStdString();
    std::ifstream is;
    // open the file with the key
    is.open(key_name + "_private_key");
    // if file exists
    if (is.is_open()) {
        // read the key
        private_key_t key;
        is >> key;
        // close file as we don't need it anymore
        is.close();

        // now take the message from the textbox, encrypt it and write it back in the textbox
        std::string message = this->ui->text_input->toPlainText().toStdString();
        this->ui->text_input->setText(QString::fromStdString(decrypt_s(key, message)));
    }
    else {
        QMessageBox::information(this, "Error", "No such key found.");
    }
}
