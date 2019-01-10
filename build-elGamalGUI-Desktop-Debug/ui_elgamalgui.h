/********************************************************************************
** Form generated from reading UI file 'elgamalgui.ui'
**
** Created by: Qt User Interface Compiler version 5.12.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ELGAMALGUI_H
#define UI_ELGAMALGUI_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_ElGamalGui
{
public:
    QWidget *centralWidget;
    QPushButton *button_gen_key;
    QPushButton *button_encode;
    QPushButton *button_decode;
    QTextEdit *text_input;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *ElGamalGui)
    {
        if (ElGamalGui->objectName().isEmpty())
            ElGamalGui->setObjectName(QString::fromUtf8("ElGamalGui"));
        ElGamalGui->resize(400, 275);
        centralWidget = new QWidget(ElGamalGui);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        button_gen_key = new QPushButton(centralWidget);
        button_gen_key->setObjectName(QString::fromUtf8("button_gen_key"));
        button_gen_key->setGeometry(QRect(10, 0, 89, 28));
        button_encode = new QPushButton(centralWidget);
        button_encode->setObjectName(QString::fromUtf8("button_encode"));
        button_encode->setGeometry(QRect(10, 210, 89, 28));
        button_decode = new QPushButton(centralWidget);
        button_decode->setObjectName(QString::fromUtf8("button_decode"));
        button_decode->setGeometry(QRect(110, 210, 89, 28));
        text_input = new QTextEdit(centralWidget);
        text_input->setObjectName(QString::fromUtf8("text_input"));
        text_input->setGeometry(QRect(10, 30, 381, 171));
        ElGamalGui->setCentralWidget(centralWidget);
        mainToolBar = new QToolBar(ElGamalGui);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        ElGamalGui->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(ElGamalGui);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        ElGamalGui->setStatusBar(statusBar);

        retranslateUi(ElGamalGui);

        QMetaObject::connectSlotsByName(ElGamalGui);
    } // setupUi

    void retranslateUi(QMainWindow *ElGamalGui)
    {
        ElGamalGui->setWindowTitle(QApplication::translate("ElGamalGui", "ElGamalGui", nullptr));
        button_gen_key->setText(QApplication::translate("ElGamalGui", "generate key", nullptr));
        button_encode->setText(QApplication::translate("ElGamalGui", "encode", nullptr));
        button_decode->setText(QApplication::translate("ElGamalGui", "decode", nullptr));
    } // retranslateUi

};

namespace Ui {
    class ElGamalGui: public Ui_ElGamalGui {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ELGAMALGUI_H
