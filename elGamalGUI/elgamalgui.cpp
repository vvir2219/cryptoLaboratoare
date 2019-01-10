#include "elgamalgui.h"
#include "ui_elgamalgui.h"
#include <QtCore>
#include <QtGui>
#include <QMessageBox>

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
    QMessageBox::information(this, "title", this->ui->text_input->toPlainText());
}
