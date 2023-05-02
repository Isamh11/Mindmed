from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
ui, _ = loadUiType('mindmed.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.b01.clicked.connect(self.login)

        
        self.menu21.triggered.connect(self.show_add_new_member_tab)
        self.b211.clicked.connect(self.save_member_informatom)
        self.menu22.triggered.connect(self.show_edit_member_tab)
        self.b500.clicked.connect(self.fill_information_of_the_selected_member)
        self.b221.clicked.connect(self.edit_member_information)
        self.b222.clicked.connect(self.delete_member_information) 
        
        
# Login form #####

    def login(self):
        un = self.tb01.text()
        pw = self.tb02.text()
        if (un == "admin" and pw == "1979"):
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self,"Mental Health Management System", "Invalid admin login details, Try again !")
            self.l01.setText("Invalid admin login details, Try again !")


############## Add New Member ###########

    def show_add_new_member_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.fill_next_member_id()


    def fill_next_member_id(self):
        try:
            member_id = 0
            mydb = con.connect(host="localhost", user="root", password="Isam2023", db = "MindMed")
            cursor = mydb.cursor()
            cursor.execute("select * from member")
            result = cursor.fetchall()
            if result:
                for member in result:
                    member_id += 1
                self.l211.setText(str(member_id + 1))
        except con.Error as e:
            print("Error occured in select member ID" + e)
        finally:
            cursor.close()
            mydb.close()           
     

    def save_member_informatom(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="Isam2023", db = "MindMed")
            cursor = mydb.cursor()
            member_id =self.l211.text()
            first_name =self.tb212.text()
            last_name = self.tb213.text()
            gender = self.cb214.currentText()
            date_of_birth = "-".join([self.tb215_1.text(), self.tb215_2.text(), self.tb215_3.text()])
            mobail_num= self.tb216.text()
            email = self.tb217.text()
            address = self.tb218.text()
            city= self.tb219.text()
            department = self.cb220.currentText()
            comment = self.tb221.text()
         
            sql_insert_member = "insert into member (memberID,first_name,last_name,gender,date_of_birth,mobail_number,email,address,city,department,comment) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (member_id,first_name,last_name,gender,date_of_birth, mobail_num,email,address,city,department,comment)
            
            if(first_name!="" and last_name!="" and gender!="" and date_of_birth!="" and mobail_num!="" and address!="" and city!="" and department!="" and comment!=""):
                cursor.execute(sql_insert_member ,value)
                mydb.commit()
                self.l210.setText("Member information saved successfully")
                QMessageBox.information(self, "Mental health management system","Member information added successfully!")
            else:
                QMessageBox.information(self,"Mental Health Management System", "Missing Member information, Try again !")
                self.l210.setText("IMissing Member information, Try again !")

            self.l210.setText("Add New Member")
            self.tb212.setText("")
            self.tb213.setText("")
            self.cb214.setCurrentText("")
            self.tb215_1.setText("")
            self.tb215_2.setText("")
            self.tb215_3.setText("")
            self.tb216.setText("")
            self.tb217.setText("")
            self.tb218.setText("")
            self.tb219.setText("")
            self.cb220.setCurrentText("")
            self.tb221.setText("")
            self.tabWidget.setCurrentIndex(1)
    
        except con.Error as e:
            self.l210.setText("Error occured in save memberID information" + e)
        finally:
            cursor.close()
            mydb.close()



def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':

    main()
