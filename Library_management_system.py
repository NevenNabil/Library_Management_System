import datetime
import MySQLdb
import MySQLdb.connections
import MySQLdb.cursors
import pyqtgraph as pg
from PyQt5.QtWidgets import *

from xlrd import *
from xlsxwriter import *

# from PyQt5.uic import loadUiType
# main, _ = loadUiType('main.ui')

from main import Ui_MainWindow

employee_id = 0
employee_branch = 0


class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.ui = main
        self.setWindowTitle('Library Management System')
        self.ui_changes()
        self.db_connect()
        self.open_login_tab()
        self.handle_button()
        self.handle_checkboxes()
        self.show_all_categories()
        self.show_branches()
        self.show_author()
        self.show_publishers()
        self.show_all_books()
        self.show_all_clients()
        self.show_employee()
        self.show_history()
        self.show_all_sales()

        self.retrieve_day_work()
        self.get_dashboard_data()

        self.date_1.setDate(datetime.datetime.now())

    def ui_changes(self):
        self.tabWidget.tabBar().setVisible(False)

    def db_connect(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='toor', db='library_db')
        print('connection Accepted')
        self.cur = self.db.cursor()  # ابعتله بيانات يحولها الي db
        print('connection Accepted')

    def open_login_tab(self):
        self.groupBox_5.hide()
        self.lineEdit_50.setText('')
        self.lineEdit_49.setText('')
        self.statusBar().showMessage(' ')
        self.tabWidget.setCurrentIndex(0)
        self.pushButton_18.hide()

    def user_login_permissions(self):
        username = self.lineEdit_50.text()
        password = self.lineEdit_49.text()

        self.cur.execute('''SELECT id, name, password,branch FROM employee ''')
        data = self.cur.fetchall()

        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 1
        table = 7

        for row in data:
            if str(row[1]) == username and row[2] == password:
                global employee_id, employee_branch
                employee_id = (row[0])
                employee_branch = (row[3])

                self.dis_groupBox.setEnabled(True)

                self.cur.execute('''SELECT * FROM employee_permissions WHERE employee_name=%s ''', (username,))
                user_permissions = self.cur.fetchone()

                self.pushButton.setEnabled(True)

                if user_permissions[2] == 1:
                    self.pushButton_2.setEnabled(True)
                if user_permissions[3] == 1:
                    self.pushButton_4.setEnabled(True)
                if user_permissions[4] == 1:
                    self.pushButton_3.setEnabled(True)
                if user_permissions[5] == 1:
                    self.pushButton_5.setEnabled(True)
                if user_permissions[6] == 1:
                    self.pushButton_6.setEnabled(True)
                if user_permissions[7] == 1:
                    self.pushButton_7.setEnabled(True)
                if user_permissions[8] == 1:
                    self.pushButton_10.setEnabled(True)
                if user_permissions[9] == 1:
                    self.pushButton_11.setEnabled(True)
                if user_permissions[10] == 1:
                    self.pushButton_17.setEnabled(True)
                if user_permissions[11] == 1:
                    self.pushButton_69.setEnabled(True)
                if user_permissions[12] == 1:
                    self.pushButton_43.setEnabled(True)
                if user_permissions[13] == 1:
                    self.pushButton_46.setEnabled(True)
                if user_permissions[14] == 1:
                    self.pushButton_48.setEnabled(True)
                if user_permissions[15] == 1:
                    self.pushButton_78.setEnabled(True)
                if user_permissions[16] == 1:
                    self.pushButton_49.setEnabled(True)
                if user_permissions[17] == 1:
                    self.pushButton_50.setEnabled(True)
                if user_permissions[18] == 1:
                    self.pushButton_51.setEnabled(True)
                if user_permissions[19] == 1:
                    self.pushButton_52.setEnabled(True)
                if user_permissions[20] == 1:
                    self.pushButton_32.setEnabled(True)
                if user_permissions[21] == 1:
                    self.pushButton_38.setEnabled(True)
                if user_permissions[22] == 1:
                    self.pushButton_35.setEnabled(True)
                if user_permissions[23] == 1:
                    self.pushButton_36.setEnabled(True)
                if user_permissions[25] == 1:
                    self.pushButton_66.setEnabled(True)
                if user_permissions[26] == 1:
                    self.pushButton_67.setEnabled(True)
                self.open_daily_movement_tab()
            else:
                self.groupBox_5.show()
        username_ = 'Employee Name: ' + str(username)

        self.cur.execute('''
                                INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                VALUES (%s,%s,%s,%s,%s,%s)
                                ''',
                         (employee_id, action, table, date, employee_branch, username_))
        self.db.commit()
        self.show_history()

    ##########################################################

    def open_daily_movement_tab(self):
        self.statusBar().showMessage(' ')
        self.tabWidget.setCurrentIndex(1)
        self.pushButton_18.show()
        self.retrieve_day_work()
        self.lineEdit.clear()
        self.lineEdit_17.clear()

    def open_books_tab(self):
        self.statusBar().showMessage(' ')
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget_2.setCurrentIndex(0)
        self.show_all_books()

    def open_client_tab(self):
        self.statusBar().showMessage(' ')
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_3.setCurrentIndex(0)
        self.show_all_clients()

    def open_dashboard_tab(self):
        self.statusBar().showMessage(' ')
        self.get_dashboard_data()
        self.tabWidget.setCurrentIndex(4)

    def open_history_tab(self):
        self.statusBar().showMessage(' ')
        self.tabWidget.setCurrentIndex(5)
        self.show_history()

    def open_report_tab(self):
        self.statusBar().showMessage(' ')
        self.tabWidget.setCurrentIndex(6)
        self.show_all_sales()

    def open_setting_tab(self):
        self.statusBar().showMessage(' ')
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_4.setCurrentIndex(0)
        self.show_branches()
        self.show_employee()
        self.checkBox_27.setChecked(False)
        self.checkBox_28.setChecked(False)
        self.checkBox_29.setChecked(False)
        self.checkBox_47.setChecked(False)
        self.checkBox_48.setChecked(False)
        self.checkBox_26.setChecked(False)
        self.checkBox_25.setChecked(False)
        self.checkBox_22.setChecked(False)
        self.checkBox_24.setChecked(False)
        self.checkBox_21.setChecked(False)
        self.checkBox_20.setChecked(False)
        self.checkBox_18.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_17.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_23.setChecked(False)
        self.checkBox_11.setChecked(False)
        self.checkBox_10.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox.setChecked(False)

    def open_login_logout_tab(self):
        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 2
        table = 7
        sql = '''SELECT name FROM employee WHERE id =%s'''
        self.cur.execute(sql, [employee_id])
        employee_name = self.cur.fetchone()
        employee_name_ = 'Employee Name: ' + str(employee_name[0])
        self.cur.execute('''
                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                            VALUES (%s,%s,%s,%s,%s,%s)
                                        ''',
                         (employee_id, action, table, date, employee_branch, employee_name_))
        self.db.commit()
        self.show_history()
        self.open_login_tab()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.pushButton_4.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.pushButton_69.setEnabled(False)
        self.pushButton_10.setEnabled(False)
        self.pushButton_11.setEnabled(False)
        self.pushButton_17.setEnabled(False)
        self.pushButton_78.setEnabled(False)
        self.pushButton_43.setEnabled(False)
        self.pushButton_46.setEnabled(False)
        self.pushButton_48.setEnabled(False)
        self.pushButton_49.setEnabled(False)
        self.pushButton_50.setEnabled(False)
        self.pushButton_51.setEnabled(False)
        self.pushButton_52.setEnabled(False)
        self.pushButton_32.setEnabled(False)
        self.pushButton_35.setEnabled(False)
        self.pushButton_36.setEnabled(False)
        self.pushButton_38.setEnabled(False)
        self.pushButton_66.setEnabled(False)
        self.pushButton_67.setEnabled(False)

    ##########################################################

    def handle_button(self):
        self.pushButton.clicked.connect(self.open_daily_movement_tab)
        self.pushButton_2.clicked.connect(self.open_books_tab)
        self.pushButton_4.clicked.connect(self.open_client_tab)
        self.pushButton_3.clicked.connect(self.open_dashboard_tab)
        self.pushButton_5.clicked.connect(self.open_history_tab)
        self.pushButton_6.clicked.connect(self.open_report_tab)
        self.pushButton_7.clicked.connect(self.open_setting_tab)
        self.pushButton_18.clicked.connect(self.open_login_logout_tab)

        self.pushButton_8.clicked.connect(self.handle_to_day_work)
        self.pushButton_49.clicked.connect(self.add_branch)
        self.pushButton_50.clicked.connect(self.add_publisher)
        self.pushButton_51.clicked.connect(self.add_author)
        self.pushButton_52.clicked.connect(self.add_category)
        self.pushButton_32.clicked.connect(self.add_employee)
        self.pushButton_10.clicked.connect(self.add_new_book)
        self.pushButton_43.clicked.connect(self.add_new_client)

        self.pushButton_12.clicked.connect(self.edit_book_search)
        self.pushButton_11.clicked.connect(self.edit_book)
        self.pushButton_17.clicked.connect(self.delete_book)
        self.pushButton_9.clicked.connect(self.all_books_filter)
        self.pushButton_69.clicked.connect(self.book_export_report)
        self.pushButton_82.clicked.connect(self.daily_sales_export_report)
        self.pushButton_13.clicked.connect(self.search_history)
        self.pushButton_80.clicked.connect(self.history_export_report)
        self.pushButton_78.clicked.connect(self.client_export_report)
        self.pushButton_20.clicked.connect(self.show_all_books)
        self.pushButton_44.clicked.connect(self.show_all_clients)
        self.pushButton_29.clicked.connect(self.show_history)

        self.pushButton_47.clicked.connect(self.edit_client_search)
        self.pushButton_42.clicked.connect(self.all_client_search)
        self.pushButton_46.clicked.connect(self.edit_client)
        self.pushButton_48.clicked.connect(self.delete_client)

        self.pushButton_36.clicked.connect(self.check_employee)
        self.pushButton_38.clicked.connect(self.edit_employee_data)
        self.pushButton_35.clicked.connect(self.delete_employee)
        self.pushButton_67.clicked.connect(self.update_employee_permission)
        self.pushButton_66.clicked.connect(self.check_employee_permission)

        self.pushButton_16.clicked.connect(self.user_login_permissions)
        self.pushButton_19.clicked.connect(self.get_dashboard_data)

    ##########################################################

    def disable_date_1(self):
        if self.comboBox.currentIndex() == 1:
            self.date_1.setEnabled(False)
            self.label_30.setEnabled(False)
        else:
            self.date_1.setEnabled(True)
            self.label_30.setEnabled(True)

    def handle_to_day_work(self):
        book_title = self.lineEdit.text()
        client_national_id = self.lineEdit_17.text()
        book_type = self.comboBox.currentIndex()
        ###############################################################
        self.cur.execute('''SELECT name FROM client WHERE national_id=%s''', (client_national_id,))
        client_name = self.cur.fetchall()
        self.cur.execute('''SELECT national_id FROM client WHERE name=%s''', (client_name,))
        client_national_id = self.cur.fetchall()
        ###############################################################
        self.cur.execute('''SELECT title FROM books WHERE code=%s''', (book_title,))
        book_name = self.cur.fetchall()
        self.cur.execute('''SELECT code FROM books WHERE title=%s''', (book_name,))
        book_title = self.cur.fetchall()
        ###############################################################
        date = datetime.datetime.now()
        global employee_id, employee_branch

        branch_id_branch = int(employee_branch) + 1

        if book_type == 0:
            from_date = str(datetime.date.today())
            to_date = self.date_1.date()
            to_date = to_date.toPyDate()

            self.cur.execute('''
                INSERT INTO daily_movements(book_id ,client_id, type, date ,branch_id, Book_from, Book_to, employee_id )
                VALUES (%s, %s, %s, %s, %s, %s , %s,%s)
            ''', (book_title, client_national_id, book_type, date, branch_id_branch, from_date, to_date, employee_id))
        else:
            self.cur.execute('''
                            INSERT INTO daily_movements(book_id ,client_id, type, date ,branch_id, employee_id )
                            VALUES (%s, %s, %s, %s, %s,%s)
                        ''', (
                book_title, client_national_id, book_type, date, branch_id_branch, employee_id))

        action = 3
        table = 6
        type_ = self.comboBox.currentText()
        type__ = 'Operation Type: ' + str(type_)
        self.cur.execute('''
                        INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        ''',
                         (employee_id, action, table, date, employee_branch, type__))

        self.db.commit()
        self.retrieve_day_work()
        self.show_history()
        self.lineEdit.setText('')
        self.lineEdit_17.setText('')
        self.statusBar().showMessage('Operation has been added successfully')

    def retrieve_day_work(self):
        self.cur.execute('''
                            SELECT book_id, type,client_id,book_from, book_to FROM daily_movements
                         ''')
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                if column == 0:
                    sql = '''SELECT title FROM books WHERE code=%s'''
                    self.cur.execute(sql, [item])
                    book_name = self.cur.fetchone()
                    if str(book_name) == 'None':
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(book_name[0])))
                elif column == 1:
                    if item == 0:
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str('Rent')))
                    else:
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str('Retrieve')))
                elif column == 2:
                    sql = '''SELECT name FROM client WHERE national_id=%s'''
                    self.cur.execute(sql, [item])
                    client_name = self.cur.fetchone()
                    if str(client_name) == 'None':
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(client_name[0])))
                elif column == 2:
                    sql = '''SELECT name FROM client WHERE national_id=%s'''
                    self.cur.execute(sql, [item])
                    client_name = self.cur.fetchone()
                    if str(client_name) == 'None':
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str(client_name[0])))
                else:
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    ##########################################################

    def show_all_categories(self):
        self.comboBox_11.clear()
        self.comboBox_9.clear()
        self.comboBox_3.clear()
        self.cur.execute('''
        SELECT Category_name FROM category  
        ''')
        categories = self.cur.fetchall()  # هيروح يتبع كل الجاتيجريس الموجودة في الجدول
        for category in categories:
            self.comboBox_11.addItem(str(category[0]))
            self.comboBox_9.addItem(str(category[0]))
            self.comboBox_3.addItem(str(category[0]))

    def show_employee(self):
        self.comboBox_33.clear()
        self.comboBox_19.clear()
        self.cur.execute('''
                SELECT name FROM employee  
                ''')
        employees = self.cur.fetchall()
        for employee in employees:
            self.comboBox_33.addItem(employee[0])
            self.comboBox_19.addItem(employee[0])

    def show_branches(self):
        self.comboBox_17.clear()
        self.comboBox_18.clear()
        self.cur.execute('''SELECT name FROM branch
         ''')

        branches = self.cur.fetchall()
        for branch in branches:
            self.comboBox_17.addItem(branch[0])
            self.comboBox_18.addItem(branch[0])

    def show_publishers(self):
        self.comboBox_5.clear()
        self.comboBox_10.clear()
        self.cur.execute('''SELECT name FROM publisher
         ''')
        publishers = self.cur.fetchall()
        for publisher in publishers:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_10.addItem(publisher[0])

    def show_author(self):
        self.comboBox_8.clear()
        self.comboBox_4.clear()
        self.cur.execute('''SELECT name FROM author
             ''')
        authors = self.cur.fetchall()
        for author in authors:
            self.comboBox_8.addItem(author[0])
            self.comboBox_4.addItem(author[0])

    def show_all_clients(self):
        self.tableWidget_12.setRowCount(0)
        self.tableWidget_12.insertRow(0)
        self.lineEdit_72.clear()
        self.comboBox_61.setCurrentIndex(0)
        self.cur.execute('''
                    SELECT name, mail, phone, national_id, date FROM client
                 ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                self.tableWidget_12.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_12.rowCount()
            self.tableWidget_12.insertRow(row_position)

    ##########################################################

    def show_history(self):
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)
        self.cur.execute('''
                    SELECT employee_id, employee_branch, employee_action, affected_table, operation_date, data  FROM history
                         ''')
        data_ = self.cur.fetchall()
        for row, form in enumerate(data_):
            for col, item in enumerate(form):
                if col == 0:
                    sql = '''SELECT name FROM employee WHERE id =%s'''
                    self.cur.execute(sql, [item])
                    employee_name = self.cur.fetchone()
                    if str(employee_name) == 'None':
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(employee_name[0])))

                elif col == 1:
                    sql = '''SELECT name FROM branch WHERE id =%s'''
                    self.cur.execute(sql, [item + 1])
                    branch_name = self.cur.fetchone()
                    if str(branch_name) == 'None':
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(branch_name[0])))

                elif col == 2:
                    action = ' '
                    if item == 1:
                        action = 'Login'
                    if item == 2:
                        action = 'Logout'
                    if item == 3:
                        action = 'Add'
                    if item == 4:
                        action = 'Edit'
                    if item == 5:
                        action = 'Delete'
                    if item == 6:
                        action = 'Search'
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(action)))

                elif col == 3:
                    table = ' '
                    if item == 1:
                        table = 'Book'
                    if item == 2:
                        table = 'Client'
                    if item == 3:
                        table = 'History'
                    if item == 4:
                        table = 'Branch'
                    if item == 5:
                        table = 'Category'
                    if item == 6:
                        table = 'Daily Movements'
                    if item == 7:
                        table = 'Employee'
                    if item == 8:
                        table = 'Publisher'
                    if item == 9:
                        table = 'Author'
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(table)))

                else:
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)

    def search_history(self):
        employee_name_ = self.comboBox_19.currentText()
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)
        self.cur.execute('''SELECT id FROM employee WHERE name=%s  ''',
                         (employee_name_,))
        data = self.cur.fetchone()
        data = data[0]

        self.cur.execute('''SELECT employee_id, employee_branch, employee_action, affected_table, operation_date, 
                            data FROM history WHERE employee_id=%s  ''',
                         (data,))
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 0:
                    sql = '''SELECT name FROM employee WHERE id =%s'''
                    self.cur.execute(sql, [item])
                    employee_name = self.cur.fetchone()
                    if str(employee_name) == 'None':
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(employee_name[0])))

                elif col == 1:
                    sql = '''SELECT name FROM branch WHERE id =%s'''
                    self.cur.execute(sql, [item + 1])
                    branch_name = self.cur.fetchone()
                    if str(branch_name) == 'None':
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(branch_name[0])))

                elif col == 2:
                    action = ' '
                    if item == 1:
                        action = 'Login'
                    if item == 2:
                        action = 'Logout'
                    if item == 3:
                        action = 'Add'
                    if item == 4:
                        action = 'Edit'
                    if item == 5:
                        action = 'Delete'
                    if item == 6:
                        action = 'Search'
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(action)))

                elif col == 3:
                    table = ' '
                    if item == 1:
                        table = 'Book'
                    if item == 2:
                        table = 'Client'
                    if item == 3:
                        table = 'History'
                    if item == 4:
                        table = 'Branch'
                    if item == 5:
                        table = 'Category'
                    if item == 6:
                        table = 'Daily Movements'
                    if item == 7:
                        table = 'Employee'
                    if item == 8:
                        table = 'Publisher'
                    if item == 9:
                        table = 'Author'
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(table)))
                else:
                    self.tableWidget_3.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)

    def history_export_report(self):
        self.cur.execute('''
                            SELECT employee_id, employee_branch, employee_action, affected_table, operation_date, data FROM history
                                 ''')
        data = self.cur.fetchall()
        excel_file = Workbook('history_report.xlsx')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0, 0, 'Employee Name')
        sheet1.write(0, 1, 'Branch')
        sheet1.write(0, 2, 'Action')
        sheet1.write(0, 3, 'Table')
        sheet1.write(0, 4, 'Date')
        sheet1.write(0, 5, 'Additional Data')

        column_number = 1
        for row, form in enumerate(data):
            row_number = 0
            for col, item in enumerate(form):
                if col == 0:
                    sql = '''SELECT name FROM employee WHERE id=%s'''
                    self.cur.execute(sql, [item])
                    employee_name = self.cur.fetchone()
                    if str(employee_name) == 'None':
                        sheet1.write(column_number, row_number, str('None'))
                    else:
                        sheet1.write(column_number, row_number, str(employee_name[0]))
                elif col == 1:
                    sql = '''SELECT name FROM branch WHERE id=%s'''
                    self.cur.execute(sql, [item + 1])
                    branch_name = self.cur.fetchone()
                    if str(branch_name) == 'None':
                        sheet1.write(column_number, row_number, str('None'))
                    else:
                        sheet1.write(column_number, row_number, str(branch_name[0]))
                elif col == 2:
                    action = ' '
                    if item == 1:
                        action = 'Login'
                    if item == 2:
                        action = 'Logout'
                    if item == 3:
                        action = 'Add'
                    if item == 4:
                        action = 'Edit'
                    if item == 5:
                        action = 'Delete'
                    if item == 6:
                        action = 'Search'
                    sheet1.write(column_number, row_number, str(action))
                elif col == 3:
                    table = ' '
                    if item == 1:
                        table = 'Book'
                    if item == 2:
                        table = 'Client'
                    if item == 3:
                        table = 'History'
                    if item == 4:
                        table = 'Branch'
                    if item == 5:
                        table = 'Category'
                    if item == 6:
                        table = 'Daily Movements'
                    if item == 7:
                        table = 'Employee'
                    if item == 8:
                        table = 'Publisher'
                    if item == 9:
                        table = 'Author'
                    sheet1.write(column_number, row_number, str(table))
                else:
                    sheet1.write(column_number, row_number, str(item))
                row_number += 1
            column_number += 1
        excel_file.close()
        self.statusBar().showMessage('History report has been created successfully')

    ##########################################################

    def get_dashboard_data(self):
        year = self.spinBox.value()
        self.cur.execute('''
            SELECT COUNT(book_id), EXTRACT(MONTH FROM Book_from) as month
            FROM daily_movements
            WHERE year(Book_from) =%s
            GROUP BY month
        ''' % year)
        data = self.cur.fetchall()
        books_count = []
        rent_count = []

        for row in data:
            books_count.append(row[1] - 1)
            rent_count.append(row[0])

        self.widget_2.clear()

        barchart = pg.BarGraphItem(x=books_count, height=rent_count, width=.25)
        barchart.setPos(1, 0)
        self.widget_2.plotItem.vb.setLimits(xMin=0, xMax=12, yMin=0)
        self.widget_2.addItem(barchart)
        self.widget_2.setBackground('transparent')

        self.widget_2.setTitle('Sales')
        self.widget_2.addLegend()
        self.widget_2.setLabel('left', 'Number of books borrowed', color='white', size=45)
        self.widget_2.showGrid(x=True, y=True)

    def show_all_sales(self):
        self.cur.execute('''
                        SELECT book_id, type,client_id,book_from, book_to, branch_id, employee_id, date FROM daily_movements
                     ''')
        data = self.cur.fetchall()

        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.insertRow(0)
        for row, form in enumerate(data):
            for column, item in enumerate(form):
                if column == 0:
                    sql = '''SELECT title FROM books WHERE code=%s'''
                    self.cur.execute(sql, [item])
                    book_name = self.cur.fetchone()
                    if str(book_name) == 'None':
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(book_name[0])))
                elif column == 1:
                    if item == 0:
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str('Rent')))
                    else:
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str('Retrieve')))
                elif column == 2:
                    sql = '''SELECT name FROM client WHERE national_id=%s'''
                    self.cur.execute(sql, [item])
                    client_name = self.cur.fetchone()
                    if str(client_name) == 'None':
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(client_name[0])))
                elif column == 5:
                    sql = '''SELECT name FROM branch WHERE id =%s'''
                    self.cur.execute(sql, [item])
                    branch_name = self.cur.fetchone()
                    if str(branch_name) == 'None':
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(branch_name[0])))

                elif column == 6:
                    sql = '''SELECT name FROM employee WHERE id=%s'''
                    self.cur.execute(sql, [item])
                    employee_name = self.cur.fetchone()
                    if str(employee_name) == 'None':
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(employee_name[0])))
                else:
                    self.tableWidget_10.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_10.rowCount()
            self.tableWidget_10.insertRow(row_position)

    ##########################################################

    def handle_checkboxes(self):
        self.checkBox_27.toggled.connect(self.handle_all_checkboxes)

        self.checkBox.toggled.connect(self.handle_checkboxes_book)
        self.checkBox_2.toggled.connect(self.handle_checkboxes_book)
        self.checkBox_3.toggled.connect(self.handle_checkboxes_book)
        self.checkBox_17.toggled.connect(self.handle_checkboxes_book)
        self.checkBox_7.toggled.connect(self.handle_checkboxes_book_tab)

        self.checkBox_4.toggled.connect(self.handle_checkboxes_client)
        self.checkBox_5.toggled.connect(self.handle_checkboxes_client)
        self.checkBox_6.toggled.connect(self.handle_checkboxes_client)
        self.checkBox_18.toggled.connect(self.handle_checkboxes_client)
        self.checkBox_8.toggled.connect(self.handle_checkboxes_client_tab)

        self.checkBox_20.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_21.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_24.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_22.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_25.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_26.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_28.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_29.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_47.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_48.toggled.connect(self.handle_checkboxes_setting)
        self.checkBox_23.toggled.connect(self.handle_checkboxes_setting_tab)

        self.checkBox_9.toggled.connect(self.handle_all_checkboxes2)
        self.checkBox_10.toggled.connect(self.handle_all_checkboxes2)
        self.checkBox_11.toggled.connect(self.handle_all_checkboxes2)
        self.comboBox.currentIndexChanged.connect(self.disable_date_1)

    def daily_sales_export_report(self):
        self.cur.execute('''
                            SELECT book_id, type,client_id,book_from, book_to, branch_id, employee_id, date FROM daily_movements
                         ''')
        data = self.cur.fetchall()
        excel_file = Workbook('daily_movements_report.xlsx')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0, 0, 'Book Title')
        sheet1.write(0, 1, 'Type')
        sheet1.write(0, 2, 'Client Name')
        sheet1.write(0, 3, 'From')
        sheet1.write(0, 4, 'To')
        sheet1.write(0, 5, 'Branch')
        sheet1.write(0, 6, 'Employee')
        sheet1.write(0, 7, 'Date')

        column_number = 1
        for row, form in enumerate(data):
            row_number = 0
            for col, item in enumerate(form):
                if col == 0:
                    sql = '''SELECT title FROM books WHERE code=%s'''
                    self.cur.execute(sql, [item])
                    book_name = self.cur.fetchone()
                    if str(book_name) == 'None':
                        sheet1.write(column_number, row_number, str('None'))
                    else:
                        sheet1.write(column_number, row_number, str(book_name[0]))
                elif col == 1:
                    if item == 0:
                        sheet1.write(column_number, row_number, str('Rent'))
                    else:
                        sheet1.write(column_number, row_number, str('Retrieve'))
                elif col == 2:
                    sql = '''SELECT name FROM client WHERE national_id=%s'''
                    self.cur.execute(sql, [item])
                    client_name = self.cur.fetchone()
                    if str(client_name) == 'None':
                        sheet1.write(column_number, row_number, str('None'))
                    else:
                        sheet1.write(column_number, row_number, str(client_name[0]))
                elif col == 5:
                    sql = '''SELECT name FROM branch WHERE id=%s'''
                    self.cur.execute(sql, [item + 1])
                    branch_name = self.cur.fetchone()
                    if str(branch_name) == 'None':
                        sheet1.write(column_number, row_number, str('None'))
                    else:
                        sheet1.write(column_number, row_number, str(branch_name[0]))
                elif col == 6:
                    sql = '''SELECT name FROM employee WHERE id=%s'''
                    self.cur.execute(sql, [item])
                    employee_name = self.cur.fetchone()
                    if str(employee_name) == 'None':
                        sheet1.write(column_number, row_number, str('None'))
                    else:
                        sheet1.write(column_number, row_number, str(employee_name[0]))
                else:
                    sheet1.write(column_number, row_number, str(item))
                row_number += 1
            column_number += 1
        excel_file.close()
        self.statusBar().showMessage('Daily movements report has been created successfully')

    def handle_all_checkboxes(self):
        if self.checkBox_27.isChecked():
            self.checkBox_28.setChecked(True)
            self.checkBox_29.setChecked(True)
            self.checkBox_47.setChecked(True)
            self.checkBox_48.setChecked(True)
            self.checkBox_26.setChecked(True)
            self.checkBox_25.setChecked(True)
            self.checkBox_22.setChecked(True)
            self.checkBox_24.setChecked(True)
            self.checkBox_21.setChecked(True)
            self.checkBox_20.setChecked(True)
            self.checkBox_18.setChecked(True)
            self.checkBox_6.setChecked(True)
            self.checkBox_5.setChecked(True)
            self.checkBox_4.setChecked(True)
            self.checkBox_17.setChecked(True)
            self.checkBox_3.setChecked(True)
            self.checkBox_2.setChecked(True)
            self.checkBox_23.setChecked(True)
            self.checkBox_11.setChecked(True)
            self.checkBox_10.setChecked(True)
            self.checkBox_9.setChecked(True)
            self.checkBox_8.setChecked(True)
            self.checkBox_7.setChecked(True)
            self.checkBox.setChecked(True)

    def handle_all_checkboxes2(self):
        if self.checkBox_28.isChecked() and self.checkBox_29.isChecked() and self.checkBox_47.isChecked() and \
                self.checkBox_48.isChecked() and self.checkBox_25.isChecked() and \
                self.checkBox_22.isChecked() and self.checkBox_24.isChecked() and self.checkBox_21.isChecked() and \
                self.checkBox_20.isChecked() and self.checkBox_18.isChecked() and \
                self.checkBox_6.isChecked() and self.checkBox_5.isChecked() and self.checkBox_4.isChecked() and \
                self.checkBox_17.isChecked() and self.checkBox_3.isChecked() and \
                self.checkBox_2.isChecked() and self.checkBox_23.isChecked() and self.checkBox_11.isChecked() and \
                self.checkBox_10.isChecked() and self.checkBox_9.isChecked() and self.checkBox_8.isChecked() and \
                self.checkBox_7.isChecked() and self.checkBox.isChecked():
            self.checkBox_27.setChecked(True)
        else:
            self.checkBox_27.setChecked(False)

    def handle_checkboxes_book(self):
        self.handle_all_checkboxes2()
        if self.checkBox.isChecked() == False and self.checkBox_2.isChecked() == False and \
                self.checkBox_3.isChecked() == False and \
                self.checkBox_17.isChecked() == False:
            self.checkBox_7.setChecked(False)

        elif self.checkBox.isChecked():
            self.checkBox_7.setChecked(True)

        elif self.checkBox_2.isChecked():
            self.checkBox_7.setChecked(True)

        elif self.checkBox_3.isChecked():
            self.checkBox_7.setChecked(True)

        elif self.checkBox_17.isChecked():
            self.checkBox_7.setChecked(True)

    def handle_checkboxes_book_tab(self):
        self.handle_all_checkboxes2()
        if self.checkBox_7.isChecked() == False:
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_17.setChecked(False)

    def handle_checkboxes_client(self):
        self.handle_all_checkboxes2()
        if self.checkBox_4.isChecked() == False and self.checkBox_5.isChecked() == False and \
                self.checkBox_6.isChecked() == False and self.checkBox_18.isChecked() == False:
            self.checkBox_8.setChecked(False)

        elif self.checkBox_4.isChecked():
            self.checkBox_8.setChecked(True)

        elif self.checkBox_5.isChecked():
            self.checkBox_8.setChecked(True)

        elif self.checkBox_6.isChecked():
            self.checkBox_8.setChecked(True)

        elif self.checkBox_18.isChecked():
            self.checkBox_8.setChecked(True)

    def handle_checkboxes_client_tab(self):
        self.handle_all_checkboxes2()
        if self.checkBox_8.isChecked() == False:
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_18.setChecked(False)

    def handle_checkboxes_setting(self):
        self.handle_all_checkboxes2()
        if self.checkBox_20.isChecked() == False and self.checkBox_21.isChecked() == False and \
                self.checkBox_22.isChecked() == False and self.checkBox_24.isChecked() == False and \
                self.checkBox_26.isChecked() == False and self.checkBox_28.isChecked() == False and \
                self.checkBox_29.isChecked() == False and self.checkBox_47.isChecked() == False and \
                self.checkBox_48.isChecked() == False and self.checkBox_25.isChecked() == False:
            self.checkBox_23.setChecked(False)
        elif self.checkBox_20.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_21.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_22.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_24.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_25.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_26.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_28.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_29.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_47.isChecked():
            self.checkBox_23.setChecked(True)
        elif self.checkBox_48.isChecked():
            self.checkBox_23.setChecked(True)

    def handle_checkboxes_setting_tab(self):
        self.handle_all_checkboxes2()
        if self.checkBox_23.isChecked() == False:
            self.checkBox_20.setChecked(False)
            self.checkBox_21.setChecked(False)
            self.checkBox_22.setChecked(False)
            self.checkBox_24.setChecked(False)
            self.checkBox_25.setChecked(False)
            self.checkBox_26.setChecked(False)
            self.checkBox_28.setChecked(False)
            self.checkBox_29.setChecked(False)
            self.checkBox_47.setChecked(False)
            self.checkBox_48.setChecked(False)

    def check_employee_permission(self):
        employee_name = self.comboBox_33.currentText()
        self.cur.execute('''SELECT * FROM employee_permissions WHERE employee_name=%s ''', (employee_name,))
        user_permissions = self.cur.fetchone()

        self.checkBox_27.setChecked(False)
        self.checkBox_28.setChecked(False)
        self.checkBox_29.setChecked(False)
        self.checkBox_47.setChecked(False)
        self.checkBox_48.setChecked(False)
        self.checkBox_26.setChecked(False)
        self.checkBox_25.setChecked(False)
        self.checkBox_22.setChecked(False)
        self.checkBox_24.setChecked(False)
        self.checkBox_21.setChecked(False)
        self.checkBox_20.setChecked(False)
        self.checkBox_18.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_17.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_23.setChecked(False)
        self.checkBox_11.setChecked(False)
        self.checkBox_10.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox.setChecked(False)

        if user_permissions[2] == 1:
            self.checkBox_7.setChecked(True)
        if user_permissions[3] == 1:
            self.checkBox_8.setChecked(True)
        if user_permissions[4] == 1:
            self.checkBox_9.setChecked(True)
        if user_permissions[5] == 1:
            self.checkBox_10.setChecked(True)
        if user_permissions[6] == 1:
            self.checkBox_11.setChecked(True)
        if user_permissions[7] == 1:
            self.checkBox_23.setChecked(True)
        if user_permissions[8] == 1:
            self.checkBox.setChecked(True)
        if user_permissions[9] == 1:
            self.checkBox_2.setChecked(True)
        if user_permissions[10] == 1:
            self.checkBox_3.setChecked(True)
        if user_permissions[11] == 1:
            self.checkBox_17.setChecked(True)
        if user_permissions[12] == 1:
            self.checkBox_4.setChecked(True)
        if user_permissions[13] == 1:
            self.checkBox_5.setChecked(True)
        if user_permissions[14] == 1:
            self.checkBox_6.setChecked(True)
        if user_permissions[15] == 1:
            self.checkBox_18.setChecked(True)
        if user_permissions[16] == 1:
            self.checkBox_21.setChecked(True)
        if user_permissions[17] == 1:
            self.checkBox_20.setChecked(True)
        if user_permissions[18] == 1:
            self.checkBox_24.setChecked(True)
        if user_permissions[19] == 1:
            self.checkBox_22.setChecked(True)
        if user_permissions[20] == 1:
            self.checkBox_25.setChecked(True)
        if user_permissions[21] == 1:
            self.checkBox_26.setChecked(True)
        if user_permissions[22] == 1:
            self.checkBox_28.setChecked(True)
        if user_permissions[23] == 1:
            self.checkBox_29.setChecked(True)
        if user_permissions[24] == 1:
            self.checkBox_27.setChecked(True)
        if user_permissions[25] == 1:
            self.checkBox_47.setChecked(True)
        if user_permissions[26] == 1:
            self.checkBox_48.setChecked(True)

    def update_employee_permission(self):
        employee_name = self.comboBox_33.currentText()
        if self.checkBox_27.isChecked():
            self.cur.execute('''UPDATE employee_permissions SET employee_name=%s, books_tab=%s,
                                client_tab=%s, dashboard_tab=%s ,history_tab=%s ,reports_tab=%s ,settings_tab=%s,add_book=%s,
                                edit_book=%s, delete_book=%s, export_book=%s ,add_client=%s ,edit_client=%s ,
                                delete_client=%s,export_client=%s, add_branch=%s, add_publisher=%s, 
                                add_author=%s ,add_category=%s ,add_employee=%s, edit_employee=%s ,delete_employee=%s ,
                                check_employee=%s, is_admin=%s ,check_permissions=%s,apply_permissions=%s WHERE 
                                employee_name = %s ''',
                             (employee_name, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                              employee_name))
            self.db.commit()
            self.checkBox_27.setChecked(False)
            self.checkBox_28.setChecked(False)
            self.checkBox_29.setChecked(False)
            self.checkBox_47.setChecked(False)
            self.checkBox_48.setChecked(False)
            self.checkBox_26.setChecked(False)
            self.checkBox_25.setChecked(False)
            self.checkBox_22.setChecked(False)
            self.checkBox_24.setChecked(False)
            self.checkBox_21.setChecked(False)
            self.checkBox_20.setChecked(False)
            self.checkBox_18.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_17.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_23.setChecked(False)
            self.checkBox_11.setChecked(False)
            self.checkBox_10.setChecked(False)
            self.checkBox_9.setChecked(False)
            self.checkBox_8.setChecked(False)
            self.checkBox_7.setChecked(False)
            self.checkBox.setChecked(False)

            self.statusBar().showMessage('All permissions has been added successfully')
        else:
            books_tab = 0
            clients_tab = 0
            dashboard_tab = 0
            history_tab = 0
            reports_tab = 0
            settings_tab = 0

            if self.checkBox_7.isChecked():
                books_tab = 1
            if self.checkBox_8.isChecked():
                clients_tab = 1
            if self.checkBox_9.isChecked():
                dashboard_tab = 1
            if self.checkBox_10.isChecked():
                history_tab = 1
            if self.checkBox_11.isChecked():
                reports_tab = 1
            if self.checkBox_23.isChecked():
                settings_tab = 1

            add_book = 0
            edit_book = 0
            delete_book = 0
            export_book = 0

            if self.checkBox.isChecked():
                add_book = 1
            if self.checkBox_2.isChecked():
                edit_book = 1
            if self.checkBox_3.isChecked():
                delete_book = 1
            if self.checkBox_17.isChecked():
                export_book = 1

            add_client = 0
            edit_client = 0
            delete_client = 0
            export_client = 0

            if self.checkBox_4.isChecked():
                add_client = 1
            if self.checkBox_5.isChecked():
                edit_client = 1
            if self.checkBox_6.isChecked():
                delete_client = 1
            if self.checkBox_18.isChecked():
                export_client = 1

            add_branch = 0
            add_publisher = 0
            add_author = 0
            add_category = 0
            add_employee = 0
            edit_employee = 0
            delete_employee = 0
            check_employee = 0
            is_admin = 0
            check_permissions = 0
            apply_permissions = 0

            if self.checkBox_21.isChecked():
                add_branch = 1
            if self.checkBox_20.isChecked():
                add_publisher = 1
            if self.checkBox_24.isChecked():
                add_author = 1
            if self.checkBox_22.isChecked():
                add_category = 1
            if self.checkBox_25.isChecked():
                add_employee = 1
            if self.checkBox_26.isChecked():
                edit_employee = 1
            if self.checkBox_28.isChecked():
                delete_employee = 1
            if self.checkBox_29.isChecked():
                check_employee = 1
            if self.checkBox_47.isChecked():
                check_permissions = 1
            if self.checkBox_48.isChecked():
                apply_permissions = 1

            self.cur.execute('''UPDATE employee_permissions SET employee_name=%s, books_tab=%s,
                                client_tab=%s, dashboard_tab=%s ,history_tab=%s ,reports_tab=%s ,settings_tab=%s,add_book=%s,
                                edit_book=%s, delete_book=%s, export_book=%s ,add_client=%s ,edit_client=%s ,
                                delete_client=%s, export_client=%s, add_branch=%s, add_publisher=%s, 
                                add_author=%s ,add_category=%s ,add_employee=%s, edit_employee=%s ,delete_employee=%s,
                                check_employee=%s ,is_admin=%s ,check_permissions=%s, apply_permissions=%s WHERE 
                                employee_name = %s ''',
                             (employee_name, books_tab, clients_tab, dashboard_tab, history_tab, reports_tab,
                              settings_tab,
                              add_book, edit_book, delete_book, export_book, add_client,
                              edit_client, delete_client, export_client, add_branch, add_publisher,
                              add_author, add_category, add_employee, edit_employee, delete_employee, check_employee,
                              is_admin, check_permissions, apply_permissions,
                              employee_name))
            self.db.commit()

            self.checkBox_28.setChecked(False)
            self.checkBox_29.setChecked(False)
            self.checkBox_47.setChecked(False)
            self.checkBox_48.setChecked(False)
            self.checkBox_26.setChecked(False)
            self.checkBox_25.setChecked(False)
            self.checkBox_22.setChecked(False)
            self.checkBox_24.setChecked(False)
            self.checkBox_21.setChecked(False)
            self.checkBox_20.setChecked(False)
            self.checkBox_18.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_17.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_23.setChecked(False)
            self.checkBox_11.setChecked(False)
            self.checkBox_10.setChecked(False)
            self.checkBox_9.setChecked(False)
            self.checkBox_8.setChecked(False)
            self.checkBox_7.setChecked(False)
            self.checkBox.setChecked(False)

        self.cur.execute('''SELECT * FROM employee_permissions WHERE employee_name=%s ''', (employee_name,))
        user_permissions = self.cur.fetchone()

        self.pushButton.setEnabled(True)

        if user_permissions[2] == 1:
            self.pushButton_2.setEnabled(True)
        else:
            self.pushButton_2.setEnabled(False)
        if user_permissions[3] == 1:
            self.pushButton_4.setEnabled(True)
        else:
            self.pushButton_4.setEnabled(False)
        if user_permissions[4] == 1:
            self.pushButton_3.setEnabled(True)
        else:
            self.pushButton_3.setEnabled(False)
        if user_permissions[5] == 1:
            self.pushButton_5.setEnabled(True)
        else:
            self.pushButton_5.setEnabled(False)
        if user_permissions[6] == 1:
            self.pushButton_6.setEnabled(True)
        else:
            self.pushButton_6.setEnabled(False)
        if user_permissions[7] == 1:
            self.pushButton_7.setEnabled(True)
        else:
            self.pushButton_7.setEnabled(False)
        if user_permissions[8] == 1:
            self.pushButton_10.setEnabled(True)
        else:
            self.pushButton_10.setEnabled(False)
        if user_permissions[9] == 1:
            self.pushButton_11.setEnabled(True)
        else:
            self.pushButton_11.setEnabled(False)
        if user_permissions[10] == 1:
            self.pushButton_17.setEnabled(True)
        else:
            self.pushButton_17.setEnabled(False)
        if user_permissions[11] == 1:
            self.pushButton_69.setEnabled(True)
        else:
            self.pushButton_69.setEnabled(False)
        if user_permissions[12] == 1:
            self.pushButton_43.setEnabled(True)
        else:
            self.pushButton_43.setEnabled(False)
        if user_permissions[13] == 1:
            self.pushButton_46.setEnabled(True)
        else:
            self.pushButton_46.setEnabled(False)
        if user_permissions[14] == 1:
            self.pushButton_48.setEnabled(True)
        else:
            self.pushButton_48.setEnabled(False)
        if user_permissions[15] == 1:
            self.pushButton_78.setEnabled(True)
        else:
            self.pushButton_78.setEnabled(False)
        if user_permissions[16] == 1:
            self.pushButton_49.setEnabled(True)
        else:
            self.pushButton_49.setEnabled(False)
        if user_permissions[17] == 1:
            self.pushButton_50.setEnabled(True)
        else:
            self.pushButton_50.setEnabled(False)
        if user_permissions[18] == 1:
            self.pushButton_51.setEnabled(True)
        else:
            self.pushButton_51.setEnabled(False)
        if user_permissions[19] == 1:
            self.pushButton_52.setEnabled(True)
        else:
            self.pushButton_52.setEnabled(False)
        if user_permissions[20] == 1:
            self.pushButton_32.setEnabled(True)
        else:
            self.pushButton_32.setEnabled(False)
        if user_permissions[21] == 1:
            self.pushButton_38.setEnabled(True)
        else:
            self.pushButton_38.setEnabled(False)
        if user_permissions[22] == 1:
            self.pushButton_35.setEnabled(True)
        else:
            self.pushButton_35.setEnabled(False)
        if user_permissions[23] == 1:
            self.pushButton_36.setEnabled(True)
        else:
            self.pushButton_36.setEnabled(False)
        if user_permissions[25] == 1:
            self.pushButton_66.setEnabled(True)
        else:
            self.pushButton_66.setEnabled(False)
        if user_permissions[26] == 1:
            self.pushButton_67.setEnabled(True)
        else:
            self.pushButton_67.setEnabled(False)

        self.comboBox_33.setCurrentIndex(0)

        self.statusBar().showMessage('Permissions has been added successfully')

    ##########################################################

    def add_branch(self):
        branch_name = self.lineEdit_87.text()
        branch_location = self.lineEdit_89.text()
        self.cur.execute('''
            INSERT INTO branch(name,location)
            VALUES (%s , %s)
        ''', (branch_name, branch_location))
        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 3
        table = 4
        branch_name_ = 'Branch Name: ' + str(branch_name)
        self.cur.execute('''
                        INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        ''',
                         (employee_id, action, table, date, employee_branch, branch_name_))

        self.db.commit()
        self.show_branches()
        self.lineEdit_87.setText('')
        self.lineEdit_89.setText('')
        self.show_history()
        self.statusBar().showMessage('Branch has been added successfully')

    def add_category(self):
        category_name = self.lineEdit_95.text()
        parent_category = self.comboBox_11.currentText()  # هنا اخدت تيكست مش انديكس علشان ارجع بال id
        query = '''SELECT id FROM category WHERE Category_name=%s'''
        self.cur.execute(query, [parent_category])
        data = self.cur.fetchone()
        self.cur.execute('''
        INSERT INTO category(category_name,parent_category)
        VALUES (%s,%s)
        ''', (category_name, parent_category))
        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 3
        table = 5
        category_name_ = 'Category Name: ' + str(category_name)
        self.cur.execute('''
                        INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        ''',
                         (employee_id, action, table, date, employee_branch, category_name_))

        self.db.commit()  # علشان يحفط الجدول في الداتا بيز مش اليموري
        self.show_all_categories()
        self.lineEdit_95.setText('')
        self.comboBox_11.setCurrentIndex(0)

        self.show_history()
        self.statusBar().showMessage('Category has been added successfully')

    def add_publisher(self):
        publisher_name = self.lineEdit_90.text()
        publisher_location = self.lineEdit_91.text()
        self.cur.execute('''
                    INSERT INTO publisher(name,location)
                    VALUES (%s , %s)
                ''', (publisher_name, publisher_location))
        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 3
        table = 8
        publisher_name_ = 'Publisher Name: ' + str(publisher_name)
        self.cur.execute('''
                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            ''',
                         (employee_id, action, table, date, employee_branch, publisher_name_))
        self.db.commit()

        self.show_publishers()
        self.lineEdit_90.setText('')
        self.lineEdit_91.setText('')
        self.show_history()
        self.statusBar().showMessage('Publisher has been added successfully')

    def add_author(self):
        author_name = self.lineEdit_92.text()
        author_location = self.lineEdit_93.text()
        self.cur.execute('''
                            INSERT INTO author(name,location)
                            VALUES (%s , %s)
                        ''', (author_name, author_location))
        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 3
        table = 9
        author_name_ = 'Author Name: ' + str(author_name)
        self.cur.execute('''
                                    INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                    VALUES (%s,%s,%s,%s,%s,%s)
                                    ''',
                         (employee_id, action, table, date, employee_branch, author_name_))
        self.db.commit()

        self.show_author()
        self.lineEdit_92.setText('')
        self.lineEdit_93.setText('')
        self.statusBar().showMessage('Author has been added successfully')

    ##########################################################

    def add_employee(self):
        employee_name = self.lineEdit_16.text()
        employee_mail = self.lineEdit_18.text()
        employee_phone = self.lineEdit_19.text()
        employee_branch_ = self.comboBox_17.currentIndex()
        national_id = self.lineEdit_20.text()
        priority = self.lineEdit_21.text()
        password = self.lineEdit_22.text()
        password2 = self.lineEdit_23.text()
        date = datetime.datetime.now()
        global employee_id, employee_branch
        action = 3
        table = 7
        employee_name_ = 'Employee Name: ' + str(employee_name)
        if password == password2:
            self.cur.execute('''
            INSERT INTO employee(name,mail,phone,branch,national_id,date,priority,password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ''', (
                employee_name, employee_mail, employee_phone, employee_branch_, national_id, date, priority, password))

            self.cur.execute('''
                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            ''',
                             (employee_id, action, table, date, employee_branch, employee_name_))

            self.db.commit()

            self.cur.execute('''INSERT INTO employee_permissions(employee_name, books_tab,
                                            client_tab, dashboard_tab ,history_tab ,reports_tab ,settings_tab,add_book,
                                            edit_book, delete_book, export_book ,add_client ,edit_client ,
                                            delete_client, export_client, add_branch, add_publisher, 
                                            add_author ,add_category ,add_employee, edit_employee ,delete_employee,
                                            check_employee ,is_admin,check_permissions, apply_permissions)
                                             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                             (employee_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

            self.db.commit()
            self.lineEdit_16.setText('')
            self.lineEdit_18.setText('')
            self.lineEdit_19.setText('')
            self.lineEdit_20.setText('')
            self.lineEdit_21.setText('')
            self.lineEdit_22.setText('')
            self.lineEdit_23.setText('')
            self.comboBox_17.setCurrentIndex(0)
            self.show_employee()
            self.show_history()

            self.statusBar().showMessage('Employee has been added successfully')
        else:
            self.statusBar().showMessage('wrong password')

    def check_employee(self):
        self.lineEdit_29.setText('')
        self.lineEdit_28.setText('')
        self.lineEdit_27.setText('')
        self.lineEdit_31.setText('')
        self.lineEdit_30.setText('')
        self.comboBox_18.setCurrentIndex(0)
        employee_name = self.lineEdit_25.text()
        global temp_employee_name
        temp_employee_name = employee_name
        self.cur.execute('''SELECT * FROM employee ''')
        data = self.cur.fetchall()

        for row in data:
            if row[1] == employee_name:
                self.groupBox_6.setEnabled(True)
                self.lineEdit_29.setText(row[2])
                self.lineEdit_28.setText((row[3]))
                self.comboBox_18.setCurrentIndex(int(row[8]))
                self.lineEdit_27.setText(str(row[5]))
                self.lineEdit_31.setText(str(row[6]))
                self.lineEdit_30.setText(str(row[7]))

    def edit_employee_data(self):
        employee_name = self.lineEdit_25.text()
        global temp_employee_name
        employee_mail = self.lineEdit_29.text()
        employee_phone = self.lineEdit_28.text()
        employee_branch_ = self.comboBox_18.currentIndex()
        employee_national_id = self.lineEdit_27.text()
        employee_priority = self.lineEdit_31.text()
        employee_password2 = self.lineEdit_30.text()

        date = datetime.datetime.now()
        self.cur.execute('''UPDATE employee SET name = %s, mail=%s, phone=%s, national_id=%s, priority=%s,password=%s ,branch=%s
                  WHERE name = %s ''',
                         (
                             employee_name, employee_mail, employee_phone, employee_national_id, employee_priority,
                             employee_password2,
                             employee_branch_, temp_employee_name))

        global employee_id, employee_branch
        action = 4
        table = 7
        employee_name_ = 'Employee Name: ' + str(employee_name)
        self.cur.execute('''
                        INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        ''',
                         (employee_id, action, table, date, employee_branch, employee_name_))

        self.db.commit()
        self.lineEdit_25.setText('')
        self.lineEdit_29.setText('')
        self.lineEdit_28.setText('')
        self.lineEdit_27.setText('')
        self.lineEdit_31.setText('')
        self.lineEdit_30.setText('')
        self.comboBox_18.setCurrentIndex(0)
        self.groupBox_6.setEnabled(False)
        self.show_employee()
        self.show_history()
        self.statusBar().showMessage('Employee data has been updated successfully')

    def delete_employee(self):
        employee_name = self.lineEdit_25.text()
        date = datetime.datetime.now()
        QMessageBox.warning(self, 'مسح الموظف', "هل انت متاكد من مسح الموظف",
                            QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes:
            sql = '''DELETE FROM employee WHERE name=%s'''
            self.cur.execute(sql, [employee_name])
            sql = '''DELETE FROM employee_permissions WHERE employee_name=%s'''
            self.cur.execute(sql, [employee_name])
            global employee_id, employee_branch
            action = 5
            table = 7
            employee_name_ = 'Employee Name: ' + str(employee_name)
            self.cur.execute('''
                                INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                VALUES (%s,%s,%s,%s,%s,%s)
                                ''', (employee_id, action, table, date, employee_branch, employee_name_))

            self.db.commit()
            self.lineEdit_25.setText('')
            self.lineEdit_29.setText('')
            self.lineEdit_28.setText('')
            self.lineEdit_27.setText('')
            self.lineEdit_31.setText('')
            self.lineEdit_30.setText('')
            self.comboBox_18.setCurrentIndex(0)
            self.groupBox_6.setEnabled(False)
            self.show_employee()
            self.show_history()
            self.statusBar().showMessage('Employee has been deleted successfully')

    ##########################################################

    def add_new_book(self):
        book_title = self.lineEdit_3.text()
        category_id = self.comboBox_3.currentIndex()
        description = self.textEdit.toPlainText()
        price = self.lineEdit_6.text()
        code = self.lineEdit_5.text()
        publisher = self.comboBox_5.currentIndex()
        author = self.comboBox_4.currentIndex()
        status = self.comboBox_6.currentIndex()
        part_order = self.lineEdit_7.text()
        bar_code = self.lineEdit_24.text()
        date = datetime.datetime.now()

        self.cur.execute('''
                            INSERT INTO books(title,description,category_id,code,barcode,parts_order,price,Publisher_id
                            ,Author_id,status,date)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ''', (book_title, description, category_id, code, bar_code, part_order, price, publisher, author
                                                       , status, date))
        global employee_id, employee_branch

        action = 3
        table = 1
        book_title_ = 'Book Name: ' + str(book_title)
        self.cur.execute('''
                        INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                        VALUES (%s,%s,%s,%s,%s,%s)
                        ''', (employee_id, action, table, date, employee_branch, book_title_))
        self.db.commit()

        self.lineEdit_3.setText('')
        self.textEdit.setText('')
        self.lineEdit_6.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_24.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)

        self.show_all_books()
        self.show_history()
        self.statusBar().showMessage('Book has been added successfully')

    def show_all_books(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        self.cur.execute('''
                            SELECT code,title,category_id,Author_id,Publisher_id,price,parts_order,date,status FROM books
                         ''')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 2:
                    sql = '''SELECT category_name FROM category WHERE id=%s'''
                    self.cur.execute(sql, [item + 1])
                    category_name = self.cur.fetchone()
                    if str(category_name) == 'None':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))
                elif col == 3:
                    sql = '''SELECT name FROM author WHERE id =%s'''
                    self.cur.execute(sql, [(item + 1)])  # زودت الايتم 1 عشان idبيبدا العد من 1 مش الصفر
                    author_name = self.cur.fetchone()
                    if str(author_name) == 'None':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(author_name[0])))
                elif col == 4:
                    sql = '''SELECT name FROM publisher WHERE id =%s'''
                    self.cur.execute(sql, [(item + 1)])  # زودت الايتم 1 عشان idبيبدا العد من 1 مش الصفر
                    publisher_name = self.cur.fetchone()
                    if str(publisher_name) == 'None':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(publisher_name[0])))
                elif col == 8:
                    if item == '0':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('New')))
                    elif item == '1':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('Used')))
                    elif item == '2':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('Damaged')))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)
            self.lineEdit_2.setText('')

    def all_books_filter(self):
        book_title = self.lineEdit_2.text()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        self.cur.execute('''SELECT code,title,category_id,Author_id,Publisher_id,price,parts_order,date,status FROM books WHERE 
                            title=%s ''', (book_title,))
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 2:
                    sql = '''SELECT category_name FROM category WHERE id=%s'''
                    self.cur.execute(sql, [item + 1])
                    category_name = self.cur.fetchone()
                    if str(category_name) == 'None':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(category_name[0])))
                elif col == 3:
                    sql = '''SELECT name FROM author WHERE id =%s'''
                    self.cur.execute(sql, [(item + 1)])  # زودت الايتم 1 عشان idبيبدا العد من 1 مش الصفر
                    author_name = self.cur.fetchone()
                    if str(author_name) == 'None':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(author_name[0])))
                elif col == 4:
                    sql = '''SELECT name FROM publisher WHERE id =%s'''
                    self.cur.execute(sql, [(item + 1)])  # زودت الايتم 1 عشان idبيبدا العد من 1 مش الصفر
                    publisher_name = self.cur.fetchone()
                    if str(publisher_name) == 'None':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('None')))
                    else:
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(publisher_name[0])))
                elif col == 8:
                    if item == '0':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('New')))
                    elif item == '1':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('Used')))
                    elif item == '2':
                        self.tableWidget_2.setItem(row, col, QTableWidgetItem(str('Damaged')))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)

    def edit_book_search(self):
        global book_code
        book_code = self.lineEdit_13.text()
        self.lineEdit_11.clear()
        self.lineEdit_9.clear()
        self.lineEdit_12.clear()
        self.lineEdit_14.clear()
        self.textEdit_2.clear()
        self.comboBox_9.setCurrentIndex(0)
        self.comboBox_10.setCurrentIndex(0)
        self.comboBox_8.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        sql = ('''
                        SELECT * FROM books WHERE code=%s
                 ''')
        self.cur.execute(sql, [book_code])
        data = self.cur.fetchone()
        self.lineEdit_11.setText(data[1])  # book title زرار
        self.comboBox_9.setCurrentIndex(int(data[9]))  # category زرار
        self.lineEdit_9.setText(str(data[6]))  # price
        self.lineEdit_12.setText(str(data[5]))  # part order
        self.lineEdit_14.setText(str(data[4]))  # barcode
        self.comboBox_10.setCurrentIndex(int(data[10]))  # publisher
        self.comboBox_8.setCurrentIndex(int(data[11]))  # author
        self.comboBox_7.setCurrentIndex(int(data[7]))  # status
        self.textEdit_2.setPlainText(str(data[2]))

    def edit_book(self):
        global book_code
        book_title = self.lineEdit_11.text()
        category_id = self.comboBox_9.currentIndex()
        description = self.textEdit_2.toPlainText()
        price = self.lineEdit_9.text()
        code = self.lineEdit_13.text()
        publisher = self.comboBox_10.currentIndex()
        author = self.comboBox_8.currentIndex()
        status = self.comboBox_7.currentIndex()
        part_order = self.lineEdit_12.text()
        bar_Code = self.lineEdit_14.text()
        date = datetime.datetime.now()

        self.cur.execute('''UPDATE books SET title=%s, description=%s, code=%s, barcode=%s,parts_order=%s,price=%s ,status=%s
         ,Category_id=%s ,Publisher_id=%s,Author_id=%s WHERE code = %s ''',
                         (book_title, description, code, bar_Code, part_order, price, status, category_id, publisher,
                          author,
                          book_code))

        global employee_id, employee_branch

        action = 4
        table = 1
        book_title_ = 'Book Name: ' + str(book_title)
        self.cur.execute('''
                                INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                VALUES (%s,%s,%s,%s,%s,%s)
                                ''', (employee_id, action, table, date, employee_branch, book_title_))

        self.db.commit()
        self.show_history()
        self.show_all_books()
        self.lineEdit_13.clear()
        self.lineEdit_11.clear()
        self.lineEdit_9.clear()
        self.lineEdit_12.clear()
        self.lineEdit_14.clear()
        self.textEdit_2.clear()
        self.comboBox_9.setCurrentIndex(0)
        self.comboBox_10.setCurrentIndex(0)
        self.comboBox_8.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.statusBar().showMessage('Book data has been updated successfully')

    def delete_book(self):
        book_code = self.lineEdit_13.text()
        date = datetime.datetime.now()
        QMessageBox.warning(self, 'مسح الكتاب', "هل انت متاكد من مسح الكتاب",
                            QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes:
            sql = '''DELETE FROM books WHERE code=%s'''
            global employee_id, employee_branch
            action = 5
            table = 1
            book_code_ = 'Book Code: ' + str(book_code)
            self.cur.execute('''
                                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                            VALUES (%s,%s,%s,%s,%s,%s)
                                            ''', (employee_id, action, table, date, employee_branch, book_code_))

            self.cur.execute(sql, [book_code])
            self.db.commit()
            self.show_all_books()
            self.lineEdit_13.clear()
            self.lineEdit_11.clear()
            self.lineEdit_9.clear()
            self.lineEdit_12.clear()
            self.lineEdit_14.clear()
            self.textEdit_2.clear()
            self.comboBox_9.setCurrentIndex(0)
            self.comboBox_10.setCurrentIndex(0)
            self.comboBox_8.setCurrentIndex(0)
            self.comboBox_7.setCurrentIndex(0)
            self.statusBar().showMessage('Book has been deleted successfully')

    def book_export_report(self):
        self.cur.execute('''
                    SELECT code,title,category_id,Author_id,parts_order,date,status,price FROM books
                 ''')
        data = self.cur.fetchall()
        excel_file = Workbook('books_report.xlsx')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0, 0, 'Book Code')
        sheet1.write(0, 1, 'Book Title')
        sheet1.write(0, 2, 'Category')
        sheet1.write(0, 3, 'Author')
        sheet1.write(0, 4, 'Part order')
        sheet1.write(0, 5, 'Date')
        sheet1.write(0, 6, 'Status')
        sheet1.write(0, 7, 'Price')

        column_number = 1
        for row, form in enumerate(data):
            row_number = 0
            for col, item in enumerate(form):
                if col == 2:
                    sql = '''SELECT category_name FROM category WHERE id=%s'''
                    self.cur.execute(sql, [item + 1])
                    category_name = self.cur.fetchone()
                    if str(category_name) == 'None':
                        sheet1.write(column_number, row_number, str('None'))
                    else:
                        sheet1.write(column_number, row_number, str(category_name[0]))
                elif col == 3:
                    sql = '''SELECT name FROM author WHERE id =%s'''
                    self.cur.execute(sql, [item + 1])
                    author_name = self.cur.fetchone()
                    if str(author_name) == 'None':
                        sheet1.write(column_number, row_number, str('None'))
                    else:
                        sheet1.write(column_number, row_number, str(author_name[0]))
                elif col == 6:
                    if item == '0':
                        sheet1.write(column_number, row_number, str('New'))
                    elif item == '1':
                        sheet1.write(column_number, row_number, str('Used'))
                    elif item == '2':
                        sheet1.write(column_number, row_number, str('Damaged'))
                else:
                    sheet1.write(column_number, row_number, str(item))
                row_number += 1
            column_number += 1
        excel_file.close()

        self.statusBar().showMessage('Book report has been created successfully')

    ##########################################################

    def add_new_client(self):
        client_name = self.lineEdit_73.text()
        client_mail = self.lineEdit_74.text()
        client_phone = self.lineEdit_75.text()
        client_national_id = self.lineEdit_76.text()
        date = datetime.datetime.now()
        self.cur.execute('''
        INSERT INTO client (name,mail,phone,national_id,date )
        VALUES(%s,%s,%s,%s,%s)
        ''', (client_name, client_mail, client_phone, client_national_id, date))

        global employee_id, employee_branch
        action = 3
        table = 2
        client_name_ = 'Client Name: ' + str(client_name)
        self.cur.execute('''
                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            ''',
                         (employee_id, action, table, date, employee_branch, client_name_))

        self.db.commit()

        self.lineEdit_73.setText('')
        self.lineEdit_74.setText('')
        self.lineEdit_75.setText('')
        self.lineEdit_76.setText('')

        self.show_all_clients()
        self.show_history()
        self.statusBar().showMessage('Client has been added successfully')

    def all_client_search(self):
        client_data = self.lineEdit_72.text()
        self.tableWidget_12.setRowCount(0)
        self.tableWidget_12.insertRow(0)
        if self.comboBox_61.currentIndex() == 0:
            self.cur.execute('''SELECT name, mail, phone, national_id, date FROM client WHERE name=%s  ''',
                             (client_data,))
            data = self.cur.fetchall()
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_12.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_12.rowCount()
                self.tableWidget_12.insertRow(row_position)
        elif self.comboBox_61.currentIndex() == 1:
            self.cur.execute('''SELECT name, mail, phone, national_id, date FROM client WHERE mail=%s  ''',
                             (client_data,))
            data = self.cur.fetchall()
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_12.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_12.rowCount()
                self.tableWidget_12.insertRow(row_position)
        elif self.comboBox_61.currentIndex() == 2:
            self.cur.execute('''SELECT name, mail, phone, national_id, date FROM client WHERE national_id=%s  ''',
                             (client_data,))
            data = self.cur.fetchall()
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_12.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_12.rowCount()
                self.tableWidget_12.insertRow(row_position)
        elif self.comboBox_61.currentIndex() == 3:
            self.cur.execute('''SELECT name, mail, phone, national_id, date FROM client WHERE phone=%s  ''',
                             (client_data,))
            data = self.cur.fetchall()
            for row, form in enumerate(data):
                for col, item in enumerate(form):
                    self.tableWidget_12.setItem(row, col, QTableWidgetItem(str(item)))
                    col += 1
                row_position = self.tableWidget_12.rowCount()
                self.tableWidget_12.insertRow(row_position)

    def edit_client(self):
        client_name = self.lineEdit_85.text()
        client_mail = self.lineEdit_83.text()
        client_phone = self.lineEdit_84.text()
        client_national_id = self.lineEdit_82.text()
        date = datetime.datetime.now()
        client_data = self.lineEdit_86.text()
        global employee_id, employee_branch
        action = 4
        table = 2

        if self.comboBox_60.currentIndex() == 0:
            self.cur.execute('''UPDATE client SET name=%s, mail=%s, phone=%s, national_id=%s WHERE name = %s''',
                             (client_name, client_mail, client_phone, client_national_id, client_data))
            client_data_ = 'Client Name: ' + str(client_data)
            self.cur.execute('''
                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            ''',
                             (employee_id, action, table, date, employee_branch, client_data_))

        if self.comboBox_60.currentIndex() == 1:
            self.cur.execute('''UPDATE client SET name=%s, mail=%s, phone=%s, national_id=%s WHERE mail = %s''',
                             (client_name, client_mail, client_phone, client_national_id, client_data))
            client_data_ = 'Client Mail: ' + str(client_data)
            self.cur.execute('''
                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            ''',
                             (employee_id, action, table, date, employee_branch, client_data_))

        if self.comboBox_60.currentIndex() == 2:
            self.cur.execute('''UPDATE client SET name=%s, mail=%s, phone=%s, national_id=%s WHERE national_id = %s''',
                             (client_name, client_mail, client_phone, client_national_id, client_data))
            client_data_ = 'Client Phone: ' + str(client_data)
            self.cur.execute('''
                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            ''', (employee_id, action, table, date, employee_branch, client_data_))

        if self.comboBox_60.currentIndex() == 3:
            self.cur.execute('''UPDATE client SET name=%s, mail=%s, phone=%s, national_id=%s WHERE national_id = %s''',
                             (client_name, client_mail, client_phone, client_national_id, client_data))
            client_data_ = 'Client National ID: ' + str(client_data)
            self.cur.execute('''
                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            ''', (employee_id, action, table, date, employee_branch, client_data_))

        self.db.commit()
        self.show_all_clients()
        self.show_all_books()
        self.lineEdit_86.setText('')
        self.lineEdit_85.setText('')
        self.lineEdit_83.setText('')
        self.lineEdit_84.setText('')
        self.lineEdit_82.setText('')
        self.comboBox_60.setCurrentIndex(0)
        self.statusBar().showMessage('Client data has been updated successfully')

    def delete_client(self):
        client_data = self.lineEdit_86.text()
        date = datetime.datetime.now()
        QMessageBox.warning(self, 'مسح العميل', "هل انت متاكد من مسح العميل",
                            QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes:

            global employee_id, employee_branch
            action = 5
            table = 2

            if self.comboBox_60.currentIndex() == 0:
                sql = '''DELETE FROM client WHERE name=%s '''
                self.cur.execute(sql, [client_data])

                client_data_ = 'Client Name: ' + str(client_data)
                self.cur.execute('''
                                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                            VALUES (%s,%s,%s,%s,%s,%s)
                                            ''', (employee_id, action, table, date, employee_branch, client_data_))

            if self.comboBox_60.currentIndex() == 1:
                sql = ''' DELETE FROM client WHERE mail=%s '''
                self.cur.execute(sql, [client_data])

                client_data_ = 'Client Mail: ' + str(client_data)
                self.cur.execute('''
                                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                            VALUES (%s,%s,%s,%s,%s,%s)
                                            ''', (employee_id, action, table, date, employee_branch, client_data_))

            if self.comboBox_60.currentIndex() == 2:
                sql = ''' DELETE FROM client WHERE phone=%s '''
                self.cur.execute(sql, [client_data])

                client_data_ = 'Client Phone: ' + str(client_data)
                self.cur.execute('''
                                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                            VALUES (%s,%s,%s,%s,%s,%s)
                                            ''', (employee_id, action, table, date, employee_branch, client_data_))

            if self.comboBox_60.currentIndex() == 3:
                sql = ''' DELETE FROM client WHERE national_id=%s '''
                self.cur.execute(sql, [client_data])

                client_data_ = 'Client National ID: ' + str(client_data)
                self.cur.execute('''
                                            INSERT INTO history(employee_id, employee_action,affected_table,operation_date,employee_branch,data)
                                            VALUES (%s,%s,%s,%s,%s,%s)
                                            ''', (employee_id, action, table, date, employee_branch, client_data_))

            self.db.commit()
            self.show_all_clients()
            self.show_all_books()
            self.lineEdit_86.setText('')
            self.lineEdit_85.setText('')
            self.lineEdit_83.setText('')
            self.lineEdit_84.setText('')
            self.lineEdit_82.setText('')
            self.statusBar().showMessage('Client has been deleted successfully')

    def edit_client_search(self):
        client_data = self.lineEdit_86.text()
        self.lineEdit_85.setText('')
        self.lineEdit_83.setText('')
        self.lineEdit_84.setText('')
        self.lineEdit_82.setText('')
        self.comboBox_60.setCurrentIndex(0)
        if self.comboBox_60.currentIndex() == 0:
            sql = ''' SELECT * FROM client WHERE name=%s '''
            self.cur.execute(sql, [client_data])
            data = self.cur.fetchone()

        if self.comboBox_60.currentIndex() == 1:
            sql = ''' SELECT * FROM client WHERE mail=%s '''
            self.cur.execute(sql, [client_data])
            data = self.cur.fetchone()

        if self.comboBox_60.currentIndex() == 2:
            sql = ''' SELECT * FROM client WHERE national_id=%s '''
            self.cur.execute(sql, [client_data])
            data = self.cur.fetchone()

        if self.comboBox_60.currentIndex() == 3:
            sql = ''' SELECT * FROM client WHERE phone=%s '''
            self.cur.execute(sql, [client_data])
            data = self.cur.fetchone()

        self.lineEdit_85.setText(str(data[1]))
        self.lineEdit_83.setText(str(data[2]))
        self.lineEdit_84.setText(str(data[3]))
        self.lineEdit_82.setText(str(data[5]))

    def client_export_report(self):
        self.cur.execute('''
                            SELECT name, mail, phone, national_id FROM client
                         ''')
        data = self.cur.fetchall()
        excel_file = Workbook('clients_report.xlsx')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0, 0, 'Client Code')
        sheet1.write(0, 1, 'Client Title')
        sheet1.write(0, 2, 'Client Phone')
        sheet1.write(0, 3, 'Client National Id')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1
        excel_file.close()
        self.statusBar().showMessage('Client report has been created successfully')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    input()


if __name__ == '__main__':
    main()
