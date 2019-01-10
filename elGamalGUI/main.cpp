#include "elgamalgui.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    ElGamalGui w;
    w.show();

    return a.exec();
}
