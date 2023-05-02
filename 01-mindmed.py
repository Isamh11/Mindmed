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


################### Edit Member ###################

    def show_edit_member_tab(self):
        self.tabWidget.setCurrentIndex(5)
        self.choose_member_id_in_comobox()

    def choose_member_id_in_comobox(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="Isam2023", db = "MindMed")
            cursor = mydb.cursor()
            member_id = self.l5000.text()  # retrieve the text value

            cursor.execute("select * from member where memberID ='"+ member_id +"'")

            result = cursor.fetchall()
            if result:
                self.tb501.clear()
                for mem in result:
                    self.tb501.addItem(str(mem[0]))

        except con.Error as e:
            print("Error occurred for the selected employee ID in the combobox" + e)
        finally:
            cursor.close()
            mydb.close()
           

    def fill_information_of_the_selected_member(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="Isam2023", db="MindMed")
            cursor = mydb.cursor()

            cursor.execute("SELECT * FROM member WHERE memberID = %s", (self.tb501.text(),))
            result = cursor.fetchone()
            if result:
                self.tb222.setText(str(result[1]))
                self.tb223.setText(str(result[2]))
                self.cb224.setCurrentText(str(result[3]))
                self.tb225_1.setText(str(result[4][0:4]))
                self.tb225_2.setText(str(result[4][5:7]))
                self.tb225_3.setText(str(result[4][-2:]))
                self.tb226.setText(str(result[5]))
                self.tb227.setText(str(result[6]))
                self.tb228.setText(str(result[7]))
                self.tb229.setText(str(result[8]))
                self.cb230.setCurrentText(str(result[9]))
                self.tb231.setText(str(result[10]))
            else:
                QMessageBox.information(self,"Mental Health Management System", "No member found with this ID")


        except con.Error as e:
            print("Error occurred while filling the selected member ID:", e)
        finally:
            cursor.close()
            mydb.close()


    def edit_member_information(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="Isam2023", db = "MindMed")
            cursor = mydb.cursor()
            member_id =self.tb501.text()
            first_name =self.tb222.text()
            last_name = self.tb223.text()
            gender = self.cb224.currentText()
            date_of_birth = "-".join([self.tb225_1.text(), self.tb225_2.text(), self.tb225_3.text()])
            mobail_num= self.tb226.text()
            email = self.tb227.text()
            address = self.tb228.text()
            city= self.tb229.text()
            department = self.cb230.currentText()
            comment = self.tb231.text()
            
            sql_insert_member = "update member set first_name ='"+ first_name +"',last_name ='"+ last_name +"',gender ='"+ gender +"',date_of_birth ='"+ date_of_birth +"',mobail_number ='"+ mobail_num +"',email ='"+ email +"',address ='"+ address +"',city ='"+ city +"',department ='"+ department +"',comment ='"+ comment +"' where memberID = '"+ member_id +"'"

            if(first_name!="" and last_name!="" and gender!="" and date_of_birth!="" and mobail_num!="" and address!="" and city!="" and department!="" and comment!=""):
                cursor.execute(sql_insert_member)
                mydb.commit()
                self.l21.setText("Member information edit successfully")
                QMessageBox.information(self, "Mental health management system","Member information edit successfully!")
            else:
                QMessageBox.information(self,"Mental Health Management System", "Missing Member information, Try again !")
                self.l220.setText("Missing Member information, Try again !")                  
            
            self.tb501.setText("")
            self.tb222.setText("")
            self.tb223.setText("")
            self.cb224.setCurrentText("")
            self.tb225_1.setText("")
            self.tb225_2.setText("")
            self.tb225_3.setText("")
            self.tb226.setText("")
            self.tb227.setText("")
            self.tb228.setText("")
            self.tb229.setText("")
            self.cb230.setCurrentText("")
            self.tb231.setText("")
            self.tabWidget.setCurrentIndex(1)
            
        except con.Error as e:
            self.l220.setText("Error occured in edit selected member" + e)
        finally:
            cursor.close()
            mydb.close()


    def delete_member_information(self):
        delete_message = QMessageBox.question(self,"Delete", "Are you sure you want to delete this member",QMessageBox.Yes|QMessageBox.No )
        if delete_message == QMessageBox.Yes:
            try:
                mydb = con.connect(host="localhost", user="root", password="Isam2023", db = "MindMed")
                cursor = mydb.cursor()
                member_id =self.tb501.text()
                sql_delete_member = "update member set first_name='Deleted', last_name='Deleted', gender='', date_of_birth='', mobail_number='', email='', address='', city='', department='', comment='Deleted by Admin' where memberID = '"+ member_id +"'"
                cursor.execute(sql_delete_member)
                mydb.commit()
                self.l220.setText("Member information deleted successfully")
                QMessageBox.information(self, "Mental health management system","Member information deleted successfully!")

                self.tb501.setText("")
                self.tb222.setText("")
                self.tb223.setText("")
                self.cb224.setCurrentText("")
                self.tb225_1.setText("")
                self.tb225_2.setText("")
                self.tb225_3.setText("")
                self.tb226.setText("")
                self.tb227.setText("")
                self.tb228.setText("")
                self.tb229.setText("")
                self.cb230.setCurrentText("")
                self.tb231.setText("")
                self.tabWidget.setCurrentIndex(1)
            
            except con.Error as e:
                self.l220.setText("Error occured in delete selected member" + e)
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
