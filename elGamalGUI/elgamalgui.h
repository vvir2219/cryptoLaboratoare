#ifndef ELGAMALGUI_H
#define ELGAMALGUI_H

#include <QMainWindow>

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

private:
    Ui::ElGamalGui *ui;
};

#endif // ELGAMALGUI_H
