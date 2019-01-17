#ifndef ELGAMALGUI_H
#define ELGAMALGUI_H

#include <QMainWindow>
#include "elGamal.h"

using elGamal::generateKey;
using elGamal::encrypt_s;
using elGamal::decrypt_s;

using elGamal::public_key_t;
using elGamal::private_key_t;

namespace Ui {
class ElGamalGui;
}

class ElGamalGui : public QMainWindow
{
    Q_OBJECT

public:
    explicit ElGamalGui(QWidget *parent = nullptr);
    ~ElGamalGui();

private slots:
    void on_button_gen_key_clicked();

    void on_button_encode_clicked();

    void on_button_decode_clicked();

private:
    Ui::ElGamalGui *ui;
};

#endif // ELGAMALGUI_H
