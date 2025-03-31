import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog, QLineEdit, QTableView, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QBuffer
import pyodbc
import os
from datetime import datetime, timedelta
import random
import re
import string
import smtplib
from email.message import EmailMessage


SERVER = 'PLABSQLW19S1,49172'
#SERVER = 'DESKTOP-V8CLP74'
DATABASE = 'Курсовая_100'
CONN_STR = (
    r'DRIVER={SQL Server};'
    r'SERVER=' + SERVER + ';'
    r'DATABASE=' + DATABASE + ';'
    r'Trusted_Connection=yes;'
)

class Ui_Communism(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Communism, self).__init__()
        uic.loadUi('Communism.ui', self)
        self.setWindowTitle('Вход')

        self.pushButton_2.clicked.connect(self.open_registration)
        self.pushButton.clicked.connect(self.open_avtar)
        self.pushButton_3.clicked.connect(self.write)

    def open_registration(self):
        try:
            self.registration_window = Ui_Registration()
            self.registration_window.show()  
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            
    def open_avtar(self):
        try:
            self.avtar_window = Ui_Avtar()
            self.avtar_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def write(self):
        try:
            self.write_window = Ui_Write()
            self.write_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


class Ui_Registration(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Registration, self).__init__() 
        uic.loadUi('Регистрация.ui', self)
        self.setWindowTitle('Регистрируйся, товарищ!')
        
        self.pushButton.clicked.connect(self.Exit) 
        self.pushButton_2.clicked.connect(self.Regis)  

        self.checkBox.stateChanged.connect(self.checkboxes_changed)
        self.checkBox_2.stateChanged.connect(self.checkboxes_changed)
        self.checkBox_3.stateChanged.connect(self.checkboxes_changed)

    def checkboxes_changed(self, state):
        sender = self.sender()
    
        if sender == self.checkBox and self.checkBox.isChecked():
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
        elif sender == self.checkBox_2 and self.checkBox_2.isChecked():
            self.checkBox.setChecked(False)
            self.checkBox_3.setChecked(False)
        elif sender == self.checkBox_3 and self.checkBox_3.isChecked():
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)

    def Exit(self):
        try:
            self.Exit_window = Ui_Communism()
            self.Exit_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Regis(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        confirm_password = self.lineEdit_3.text()
        email = self.lineEdit_4.text()
        

        if password != confirm_password:
            QMessageBox.critical(self, "Ошибка", "Пароли не совпадают")
            return

        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [dbo].[Customers] WHERE login = ?", username)
            existing_user = cursor.fetchone()

            if existing_user:
                QMessageBox.critical(self, "Ошибка", "Логин уже существует")
                return

            user_type = None
            if self.checkBox.isChecked():
                user_type = 'пользователь'
            elif self.checkBox_2.isChecked():
                user_type = 'администратор'
            elif self.checkBox_3.isChecked():
                user_type = 'менеджер'

            if user_type is None:
                QMessageBox.critical(self, "Ошибка", "Выберите тип пользователя")
                return

            cursor.execute(
                "INSERT INTO [dbo].[Customers] (login, password, role, email) VALUES (?, ?, ?, ?)",
                username, password, user_type, email
            )
            conn.commit()
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")

            self.main_window = Ui_Communism()
            self.main_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


class Ui_Write(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Write, self).__init__()
        uic.loadUi('Регистрация_1.ui', self)
        self.setWindowTitle('Описание')

        self.pushButton.clicked.connect(self.exit)

    def exit(self):
        try:
            self.Exit_window = Ui_Communism()
            self.Exit_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


class Ui_Avtar(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Avtar, self).__init__()
        uic.loadUi('Авторизация.ui', self)
        self.setWindowTitle('Авторизация')
        
        self.pushButton.clicked.connect(self.Exit)  
        self.pushButton_2.clicked.connect(self.Go)
        self.pushButton_3.clicked.connect(self.Forget)

    def Exit(self):
        try:
            self.Exit_window = Ui_Communism()
            self.Exit_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Forget(self):
        try:
            self.forget_window = Ui_Forget()
            self.forget_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Go(self):     
        try:
            username = self.lineEdit.text().strip()
            password = self.lineEdit_2.text().strip()

            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM [dbo].[Customers] WHERE login = ? AND password = ?", (username, password))
            user_data = cursor.fetchone()

            if user_data:
                user_type = user_data[3].strip()
                print(f"User type from database: '{user_type}'")

                if user_type == "администратор":
                    self.admin_user_window = Ui_Administrator(username)
                elif user_type == "менеджер":
                    self.admin_user_window = Ui_Manager(username)
                elif user_type == "пользователь":
                    self.admin_user_window = Ui_Shopping(username)
                else:
                    QMessageBox.critical(self, "Ошибка", "Неизвестная роль пользователя")
                    return

                self.admin_user_window.show()
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка", "Неверное имя пользователя или пароль")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


class Ui_Forget(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Forget, self).__init__()
        uic.loadUi('Замена_пароля.ui', self)
        self.setWindowTitle("Замена пароля")                     

        self.pushButton_2.clicked.connect(self.Remember)

    def Remember(self):
        username = self.lineEdit_3.text().strip()
        print(f"Username: {username}")

        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM [dbo].[Customers] WHERE login = ?", (username,))
            user_data = cursor.fetchone()
            print(f"User data: {user_data}")

            if user_data:
                email = user_data[0]
                new_password = self.generate_random_password()
                self.send_email(email, new_password)
                QMessageBox.information(self, "Успех", "Новый пароль отправлен на вашу почту.")
                
                try:
                    self.forget_window = Ui_Forget_22(username)
                    self.forget_window.show()
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при открытии нового окна: {str(e)}")
            else:
                QMessageBox.critical(self, "Ошибка", "Пользователь с таким никнеймом не найден.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка в Remember: {str(e)}")

    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    def send_email(self, to_email, new_password):
        from_email = "dsevelev2205@gmail.com"
        from_password = "nbqr jdba lfhd ssrn"
    
        subject = "Ваш новый пароль"
        body = f"Ваш новый пароль: {new_password}"

        message = EmailMessage()
        message.set_content(body)
        message['Subject'] = subject
        message['From'] = from_email
        message['To'] = to_email

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(from_email, from_password)
                server.send_message(message)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось отправить email: {str(e)}")


class Ui_Forget_22(QtWidgets.QMainWindow):
    def __init__(self, previous_username):
        super(Ui_Forget_22, self).__init__()
        uic.loadUi('Замена_пароля_2.ui', self)
        self.setWindowTitle("Замена пароля")
        
        self.previous_username = previous_username

        self.pushButton_2.clicked.connect(self.Remember_22)

    def Remember_22(self):
        try:
            new_password = self.lineEdit_2.text().strip()
            confirm_password = self.lineEdit_3.text().strip()

            if not new_password or not confirm_password:
                QMessageBox.critical(self, "Ошибка", "Пароль не может быть пустым.")
                return

            if new_password != confirm_password:
                QMessageBox.critical(self, "Ошибка", "Пароли не совпадают.")
                return

            if len(new_password) < 4:
                QMessageBox.critical(self, "Ошибка", "Пароль должен содержать не менее 4 символов.")
                return

            username = self.previous_username

            try:
                conn = pyodbc.connect(CONN_STR)
                cursor = conn.cursor()
                cursor.execute("UPDATE [dbo].[Customers] SET password = ? WHERE login = ?", (new_password, username))
                conn.commit()

                QMessageBox.information(self, "Успех", "Пароль успешно изменен.")
                self.remember_window = Ui_Communism()
                self.remember_window.show()
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))




class Ui_Shopping(QtWidgets.QMainWindow):
    def __init__(self, username):
        super(Ui_Shopping, self).__init__()
        uic.loadUi('Магазин.ui', self)
        self.setWindowTitle("Магазин игровой атрибутики 'Шевелись, Плотва!'")
        self.username = username

        self.conn_str = 'driver={SQL Server}; server=PLABSQLW19S1,49172; Database=Курсовая_100; Trusted_Connection=yes'
        self.data_db = []
        self.original_data_db = []
        self.number_page_elements = 0 
        self.items_per_page = 4 
        self.current_number_page = 1 

        self.connect_widgets()
        self.show_data()
        self.apply_styles()

        self.label_name_page.setText(f'Страница {self.current_number_page}')

    def show_data(self):
        self.get_data_from_table()
        self.draw_frames()

    def connect_widgets(self):
        self.button_exit.clicked.connect(self.Exit)
        self.button_buy.clicked.connect(self.Buy)
        self.button_back.clicked.connect(lambda: self.browsing('back'))
        self.button_next.clicked.connect(lambda: self.browsing('next'))
        self.button_fliter.clicked.connect(self.FilterCheap)
        self.button_fliter_2.clicked.connect(self.FilterExpensive)
        self.button_flitering.clicked.connect(self.ApplyFilters)

    def get_data_from_table(self):
        conn = None
        cursor = None
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            cursor.execute('SELECT ID, Name_product, Price, Count_product, Pictury, Description FROM Product')
            self.data_db = cursor.fetchall()
        
            if not self.data_db:
                print("Нет данных в таблице Product.")
            else:
                for row in self.data_db:
                    print(f"ID: {row.ID}, Name: {row.Name_product}, Price: {row.Price}, Count: {row.Count_product}")

            self.original_data_db = self.data_db
        except pyodbc.Error as ex:
            QMessageBox.critical(self, "Ошибка", str(ex.args[1]))
        finally:
            if cursor is not None:
                cursor.close()  
            if conn is not None:    
                conn.close()  

    def draw_frames(self, default_image_path='images/2.png'):
        self.listWidget.clear()

        for item_list in self.data_db[self.number_page_elements:self.number_page_elements + self.items_per_page]:
            item_widget = QtWidgets.QWidget()
            item_layout = QtWidgets.QVBoxLayout(item_widget)

            pictury_data = item_list[4]

            if isinstance(pictury_data, bytes):
                image = QtGui.QImage.fromData(pictury_data)
                pixmap = QtGui.QPixmap.fromImage(image)
            else:
                pixmap = QtGui.QPixmap(default_image_path)

            if pixmap.isNull():
                pixmap = QtGui.QPixmap(default_image_path)

            image_label = QtWidgets.QLabel()
            image_label.setPixmap(pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio))
            item_layout.addWidget(image_label)

            scroll_area = QtWidgets.QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setFixedHeight(100)

            description_label = QtWidgets.QLabel(f'''
    {item_list[1]} | Цена: {item_list[2]} рублей | Остаток: {item_list[3]} | Описание: {item_list[5]}
    ''')
            description_label.setWordWrap(True)
            description_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

            scroll_area.setWidget(description_label)

            item_layout.addWidget(scroll_area)

            item_widget.setMinimumHeight(200)
            item_widget.setMaximumHeight(300)
            item_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

            list_item = QtWidgets.QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.listWidget.addItem(list_item)
            self.listWidget.setItemWidget(list_item, item_widget)

            list_item.setData(QtCore.Qt.UserRole, item_list[0])
            list_item.setData(QtCore.Qt.UserRole + 1, item_list[1])


    def browsing(self, act):
        if act == 'next' and self.number_page_elements + self.items_per_page < len(self.data_db):
            self.current_number_page += 1
            self.number_page_elements += self.items_per_page
        elif act == 'back' and self.number_page_elements > 0:
            self.current_number_page -= 1
            self.number_page_elements -= self.items_per_page

        self.label_name_page.setText(f'Страница {self.current_number_page}')
        self.draw_frames()

    def FilterCheap(self):
        self.data_db.sort(key=lambda x: x[2])
        self.reset_pagination()
        self.draw_frames()

    def FilterExpensive(self):
        self.data_db.sort(key=lambda x: x[2], reverse=True)
        self.reset_pagination()
        self.draw_frames()

    def ApplyFilters(self):
        filter_text = self.lineEdit.text().strip().lower()
        if filter_text:
            self.data_db = [product for product in self.original_data_db if filter_text in product[1].lower()]
        else:
            self.data_db = self.original_data_db

        self.reset_pagination()
        self.draw_frames()

    def reset_pagination(self):
        self.number_page_elements = 0
        self.current_number_page = 1
        self.label_name_page.setText(f'Страница {self.current_number_page}')

    def Exit(self):
        self.Exit_window = Ui_Communism()
        self.Exit_window.show()
        self.close()

    def Buy(self):
        selected_item = self.listWidget.currentItem()
        if selected_item:
            product_id = selected_item.data(QtCore.Qt.UserRole)
            product_name = selected_item.data(QtCore.Qt.UserRole + 1)
            print(f"Выбранный товар: {product_name} (ID: {product_id})") 
            self.Buy_window = Ui_Confirmation(self.username, product_name, self.conn_str, self)
            self.Buy_window.show()
        else:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите товар для покупки.")

    def apply_styles(self):
        self.listWidget.setStyleSheet("""
            QListWidget {
                font-size: 20px; 
                font-family: 'Bahnschrift Condensed'; 
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QListWidget::item {
                border: 1px solid rgb(0, 0, 0);
                margin: 5px;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #F4E8D3;
                color: rgb(0, 0, 0);
            }
        """)

class Ui_Confirmation(QtWidgets.QMainWindow):
    def __init__(self, username, product_name, conn_str, shopping_window):
        super(Ui_Confirmation, self).__init__()
        uic.loadUi('Подтверждение.ui', self)
        self.setWindowTitle('Подтверждение покупки')
        self.username = username
        self.product_name = product_name
        self.conn_str = conn_str
        self.shopping_window = shopping_window

        self.button_next.clicked.connect(self.Next)
        self.button_exit.clicked.connect(self.Exit)

        self.product_info = self.get_product_info(product_name)

    def get_product_info(self, product_name):
        if not product_name:
            QMessageBox.warning(self, "Ошибка", "Имя товара не указано.")
            return None

        product_name = product_name.strip().lower()
        print(f"Ищем товар: {product_name}") 
        conn = None
        cursor = None
        try:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            product = cursor.execute('SELECT ID, Count_product FROM Product WHERE LOWER(Name_product) = ?', product_name).fetchone()
        
            if product is None:
                print(f"Товар '{product_name}' не найден в базе данных.")
            else:
                print(f"Найден товар: {product}")
        
            return product
        except pyodbc.Error as ex:
            QMessageBox.critical(self, "Ошибка", str(ex.args[1]))
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def Exit(self):
        self.close()

    def Next(self):
        if self.product_info:
            product_id, count_product = self.product_info

            if count_product > 0:
                new_count = count_product - 1
                conn = None
                cursor = None
                try:
                    conn = pyodbc.connect(self.conn_str)
                    cursor = conn.cursor()
                    cursor.execute('UPDATE Product SET Count_product = ? WHERE ID = ?', new_count, product_id)
                    conn.commit()

                    self.shopping_window.get_data_from_table()
                    self.shopping_window.reset_pagination()
                    self.shopping_window.draw_frames()

                    self.next_window = Ui_Email(self.username, self.product_name)
                    self.next_window.show()
                    self.close()
                except pyodbc.Error as ex:
                    QMessageBox.critical(self, "Ошибка", str(ex.args[1]))
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Товар закончился.")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить информацию о товаре.")



class Ui_Email(QtWidgets.QMainWindow):
    def __init__(self, username, product_name):
        super(Ui_Email, self).__init__()
        uic.loadUi('Укажите_почту.ui', self)
        self.setWindowTitle('Укажите почту')
        self.username = username
        self.product_name = product_name
        self.button_next.clicked.connect(self.Next)

    def get_user_id(self, username):
        conn = None
        cursor = None
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("SELECT ID FROM Customers WHERE login = ?", (username,))
            user_id = cursor.fetchone()
            return user_id[0] if user_id else None
        except pyodbc.Error as ex:
            QMessageBox.critical(self, "Ошибка базы данных", str(ex.args[1]))
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def Next(self):
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if not self.validate_email(email):
            QMessageBox.warning(self, "Ошибка", "Введите корректный адрес электронной почты.")
            return

        if not password:
            QMessageBox.warning(self, "Ошибка", "Пароль не может быть пустым.")
            return

        user_id = self.get_user_id(self.username)

        if user_id is None:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден.")
            return

        try:
            self.save_credentials(user_id, email, password)
            if self.get_user_id(self.username) is not None:
                self.next_window = Ui_Delivery(self.username, self.product_name)
                self.next_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить учетные данные.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def save_credentials(self, user_id, email, password):
        conn = None
        cursor = None
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Account_in_a_game (ID_login, Email, Password) VALUES (?, ?, ?)",
                           (user_id, email, password))
            conn.commit()
            QMessageBox.information(self, "Успех", "Данные успешно сохранены.")
        except pyodbc.Error as ex:
            QMessageBox.critical(self, "Ошибка базы данных", str(ex.args[1]))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

class Ui_Delivery(QtWidgets.QMainWindow):
    def __init__(self, username, product_name):
        super(Ui_Delivery, self).__init__()
        uic.loadUi('Доставка.ui', self)
        self.setWindowTitle('Доставка')
        self.username = username
        self.product_name = product_name
        self.lineEdit_product_name.setText(self.product_name)
        self.lineEdit_product_name.setReadOnly(True)
        self.lineEdit.setReadOnly(True)

        self.button_next.clicked.connect(self.Next)

        self.delivery_time = self.calculate_delivery_time()
        self.display_delivery_time()

    def calculate_delivery_time(self):
        current_time = datetime.now()
        delivery_duration = timedelta(hours=2 + (2 * random.random()))
        delivery_time = current_time + delivery_duration
        return delivery_time

    def display_delivery_time(self):
        self.lineEdit.setText(self.delivery_time.strftime('%H:%M'))

    def Next(self):
        try:
            current_datetime = datetime.now()
            current_date = current_datetime.strftime('%Y-%m-%d')
            current_time = self.delivery_time.strftime('%H:%M')

            product_info = self.get_product_info(self.lineEdit_product_name.text())
            if product_info is None:
                QMessageBox.warning(self, "Ошибка", "Продукт не найден.")
                return

            product_id, count_product = product_info 

            self.save_product_info(product_id, current_date, current_time)
            self.next_window = Ui_Warning(self.username, self.product_name)
            self.next_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def get_product_info(self, product_name):
        if not product_name:
            QMessageBox.warning(self, "Ошибка", "Имя товара не указано.")
            return None

        product_name = product_name.strip().lower()
        conn = None
        cursor = None
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            product = cursor.execute('SELECT ID, Name_product, Price, Count_product FROM Product WHERE LOWER(Name_product) = ?', product_name).fetchone()
    
            if product is None:
                QMessageBox.warning(self, "Ошибка", f"Товар '{product_name}' не найден в базе данных.")
                return None
    
            return product[0], product[3] 
        except pyodbc.Error as ex:
            QMessageBox.critical(self, "Ошибка", str(ex.args[1]))
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def save_product_info(self, product_id, delivery_date, delivery_time):
        conn = None
        cursor = None
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("UPDATE Product SET Date = ?, Time_in_a_account = ? WHERE ID = ?",
                           (delivery_date, delivery_time, product_id))
            conn.commit()
            QMessageBox.information(self, "Успех", "Информация о продукте успешно обновлена.")
        except pyodbc.Error as ex:
            QMessageBox.critical(self, "Ошибка базы данных", str(ex.args[1]))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

class Ui_Warning(QtWidgets.QMainWindow):
    def __init__(self, username, product_name):
        super(Ui_Warning, self).__init__()
        uic.loadUi('Предупреждение.ui', self)
        self.setWindowTitle('Предупреждение')
        self.username = username
        self.product_name = product_name

        self.button_next.clicked.connect(self.Next)

    def Next(self):
        try:
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))








class Ui_Administrator(QtWidgets.QMainWindow):
    def __init__(self, username):
        super(Ui_Administrator, self).__init__()
        uic.loadUi('Окно_администратора.ui', self)
        self.setWindowTitle('Администрация')

        self.username = username
        self.pushButton.clicked.connect(self.Delete)
        self.pushButton_2.clicked.connect(self.Save)
        self.pushButton_3.clicked.connect(self.Exit)
        self.pushButton_4.clicked.connect(self.Add)

        self.tableView.setModel(QStandardItemModel())
        self.load_users()

        self.changes_made = False 
        self.deleted_users = []

        self.tableView.model().itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        self.changes_made = True

    def load_users(self):
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("SELECT login, password, role, email FROM [dbo].[Customers]")
            users = cursor.fetchall()

            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(['Имя пользователя', 'Пароль', 'Роль', 'Почта'])

            for user in users:
                row = [QStandardItem(user[0]), QStandardItem(user[1]), QStandardItem(user[2]), QStandardItem(user[3])]
                model.appendRow(row)

            self.tableView.setModel(model)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Delete(self):
        try:
            selected_index = self.tableView.currentIndex()
            if not selected_index.isValid():
                QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите пользователя для удаления.")
                return

            login = self.tableView.model().item(selected_index.row(), 0).text()
            self.deleted_users.append(login)
            self.tableView.model().removeRow(selected_index.row())
            self.changes_made = True
            QMessageBox.information(self, "Успех", "Пользователь помечен для удаления.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Save(self):
        if not self.changes_made:
            QMessageBox.warning(self, "Предупреждение", "Нет изменений для сохранения.")
            return

        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()

            for login in self.deleted_users:
                cursor.execute("DELETE FROM [dbo].[Customers] WHERE login = ?", login)
                print(f"Удален пользователь: {login}")

            existing_logins = set()
            cursor.execute("SELECT login FROM [dbo].[Customers]")
            for row in cursor.fetchall():
                existing_logins.add(row[0])

            for row in range(self.tableView.model().rowCount()):
                login = self.tableView.model().item(row, 0).text()
                password = self.tableView.model().item(row, 1).text()
                role = self.tableView.model().item(row, 2).text()
                email = self.tableView.model().item(row, 3).text()

                print(f"Обработка пользователя: {login}, Пароль: {password}, Роль: {role}, Почта: {email}")

                if login in existing_logins:
                    cursor.execute("UPDATE [dbo].[Customers] SET password = ?, role = ?, email = ? WHERE login = ?", password, role, email, login)
                    print(f"Обновлен пользователь: {login}")
                else:
                    cursor.execute("INSERT INTO [dbo].[Customers] (login, password, role, email) VALUES (?, ?, ?, ?)", login, password, role, email)
                    existing_logins.add(login)
                    print(f"Добавлен новый пользователь: {login}")

            conn.commit()
            conn.close()

            self.changes_made = False
            self.deleted_users.clear() 
            self.load_users()
            QMessageBox.information(self, "Успех", "Изменения успешно сохранены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Add(self):
        try:
            login = self.lineEdit_login.text()
            password = self.lineEdit_password.text()
            role = self.comboBox_role.currentText()
            email = self.lineEdit_email.text()

            if not login or not password or not email:
                QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все поля.")
                return

            model = self.tableView.model()
            row = [QStandardItem(login), QStandardItem(password), QStandardItem(role), QStandardItem(email)]
            model.appendRow(row)
            self.changes_made = True
            QMessageBox.information(self, "Успех", "Пользователь добавлен.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Exit(self):
        try:
            self.Exit_window = Ui_Communism()
            self.Exit_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


class Ui_Manager(QtWidgets.QMainWindow):
    def __init__(self, username):
        super(Ui_Manager, self).__init__()
        uic.loadUi("Окно_менеджера.ui", self)
        self.setWindowTitle("Менеджеризация")

        self.username = username
        self.pushButton.clicked.connect(self.Delete)
        self.pushButton_2.clicked.connect(self.Save)
        self.pushButton_3.clicked.connect(self.Exit)
        self.pushButton_4.clicked.connect(self.Add)
        self.pushButton_5.clicked.connect(self.select_image)
        self.pushButton_6.clicked.connect(self.Extra_extra)

        self.tableView.setModel(QStandardItemModel())
        self.load_products()
        self.is_editing = False
        self.changes_made = False
        self.deleted_products = []
        self.new_products = [] 

        self.original_data = []
        self.tableView.model().itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        self.changes_made = True

    def load_products(self):
        try:
            print("Подключение к базе данных...")
            with pyodbc.connect(CONN_STR) as conn:
                cursor = conn.cursor()
                query = "SELECT ID, Name_product, Price, Count_product, Pictury, Description FROM [dbo].[Product]"
                print(f"Выполняемый запрос: {query}")
                cursor.execute(query)
                products = cursor.fetchall()
                print(f"Загружено товаров: {len(products)}")

                model = QStandardItemModel()
                model.setHorizontalHeaderLabels(['ID', 'Имя товара', 'Цена', 'Количество товаров', 'Изображение товара', 'Описание товара'])

                for product in products:
                    row = [
                        QStandardItem(str(product[0])), 
                        QStandardItem(product[1]),     
                        QStandardItem(str(product[2])),  
                        QStandardItem(str(product[3])),  
                        QStandardItem(),                 
                        QStandardItem(product[5])        
                    ]

                    if product[4]:
                        pixmap = QPixmap()
                        if pixmap.loadFromData(product[4]):
                            item = QStandardItem()
                            item.setData(pixmap, Qt.DecorationRole)
                            row[4] = item
                        else:
                            print("Не удалось загрузить изображение из бинарных данных.")

                    model.appendRow(row)

                self.tableView.setModel(model)
        except Exception as e:
            print(f"Ошибка при загрузке товаров: {e}")
            QMessageBox.critical(self, "Ошибка", str(e))

    def select_image(self):
        pictury_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)")
        if pictury_path:
            relative_path = os.path.relpath(pictury_path)
            self.lineEdit_pictury.setText(relative_path)

    def Delete(self):
        try:
            selected_index = self.tableView.currentIndex()
            if not selected_index.isValid():
                QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите товар для удаления.")
                return

            product_id = self.tableView.model().item(selected_index.row(), 0).text()
            self.deleted_products.append(product_id)
            self.tableView.model().removeRow(selected_index.row())
            self.changes_made = True
            QMessageBox.information(self, "Успех", "Товар помечен для удаления.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            
    def Add(self):
        if self.is_editing:
            QMessageBox.warning(self, "Предупреждение", "Сначала сохраните изменения.")
            return

        try:
            product = self.lineEdit_product.text().strip()
            price = int(self.lineEdit_price.text().strip())
            count_product = int(self.lineEdit_count.text().strip())
            description = self.lineEdit_description.text().strip()
            pictury_path = self.lineEdit_pictury.text().strip()

            if not product or not description:
                QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все поля.")
                return
    
            if price <= 0 or count_product <= 0:
                QMessageBox.warning(self, "Ошибка", "Цена и количество должны быть положительными числами.")
                return

            if not pictury_path:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите изображение.")
                return

            with open(pictury_path, 'rb') as file:
                pictury_data = file.read()

            if not pictury_data:
                QMessageBox.warning(self, "Ошибка", "Не удалось прочитать изображение.")
                return

            self.new_products.append((product, price, count_product, pictury_data, description))

            model = self.tableView.model()
            row = [
                QStandardItem(str(model.rowCount() + 1)),
                QStandardItem(product),                     
                QStandardItem(str(price)),                   
                QStandardItem(str(count_product)),          
                QStandardItem(),                           
                QStandardItem(description)                   
            ]

            pixmap = QPixmap()
            if pixmap.loadFromData(pictury_data):
                item = QStandardItem()
                item.setData(pixmap, Qt.DecorationRole)
                row[4] = item
            else:
                print("Не удалось загрузить изображение из бинарных данных.")

            model.appendRow(row)

            self.changes_made = True
            QMessageBox.information(self, "Успех", "Товар успешно добавлен.")
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Цена и количество должны быть числовыми значениями.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Save(self):
        if not self.changes_made:
            QMessageBox.warning(self, "Предупреждение", "Нет изменений для сохранения.")
            return

        try:
            model = self.tableView.model()
            with pyodbc.connect(CONN_STR) as conn:
                cursor = conn.cursor()
                conn.autocommit = False


                for product_id in self.deleted_products:
                    cursor.execute("DELETE FROM [dbo].[Product] WHERE ID = ?", product_id)

                for row in range(model.rowCount()):
                    product_id = model.item(row, 0).text()
                    product = model.item(row, 1).text()
                    price = int(model.item(row, 2).text())
                    count_product = int(model.item(row, 3).text())
                    description = model.item(row, 5).text()

                    pixmap_item = model.item(row, 4)
                    if pixmap_item:
                        pixmap = pixmap_item.data(Qt.DecorationRole)
                        buffer = QBuffer()
                        buffer.open(QBuffer.ReadWrite)
                        if not pixmap.save(buffer, "PNG"):
                            raise Exception("Не удалось сохранить изображение в бинарном формате.")
                        pictury_data = buffer.data()
                    else:
                        pictury_data = b'' 

                    cursor.execute("""
                        UPDATE [dbo].[Product]
                        SET Name_product = ?, Price = ?, Count_product = ?, Pictury = ?, Description = ?
                        WHERE ID = ?
                    """, (product, price, count_product, pyodbc.Binary(pictury_data), description, product_id))

                for new_product in self.new_products:
                    cursor.execute("""
                        INSERT INTO [dbo].[Product] (Name_product, Price, Count_product, Pictury, Description) 
                        VALUES (?, ?, ?, ?, ?)
                    """, new_product)

                conn.commit()
                self.changes_made = False
                self.deleted_products.clear() 
                self.new_products.clear() 
                self.load_products() 
                QMessageBox.information(self, "Успех", "Изменения успешно сохранены.")
        except Exception as e:
            conn.rollback() 
            QMessageBox.critical(self, "Ошибка", str(e))

    def Exit(self):
        self.Exit_window = Ui_Communism() 
        self.Exit_window.show()
        self.close()

    def Extra_extra(self):
        try:
            self.extra_window = Ui_Extra(self.username)
            self.extra_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


class Ui_Extra(QtWidgets.QMainWindow):
    def __init__(self, username):
        super(Ui_Extra, self).__init__()
        uic.loadUi('Дополнительно.ui', self) 
        self.setWindowTitle('Менеджеризация')

        self.username = username
        self.pushButton.clicked.connect(self.Delete)
        self.pushButton_2.clicked.connect(self.Save)
        self.pushButton_3.clicked.connect(self.Exit)

        self.tableView.setModel(QStandardItemModel())
        self.load_accounts()

        self.changes_made = False 
        self.deleted_accounts = [] 

        self.tableView.model().itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        self.changes_made = True

    def load_accounts(self):
        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()
            cursor.execute("SELECT ID_login, Email, Password, Time_in_a_account, Date FROM [dbo].[Account_in_a_game]")
            accounts = cursor.fetchall()

            print("Данные извлечены:", accounts)

            if not accounts:
                QMessageBox.warning(self, "Предупреждение", "Нет записей для отображения.")
                return

            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(['ID_login', 'Email', 'Password', 'Time_in_a_account', 'Date'])

            for account in accounts:
                print("Добавляем запись:", account) 
                row = [
                    QStandardItem(str(account[0])),
                    QStandardItem(str(account[1])), 
                    QStandardItem(str(account[2])), 
                    QStandardItem(str(account[3])),
                    QStandartItem(str(account[4]))
                ]
                model.appendRow(row)

            self.tableView.setModel(model)
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Delete(self):
        try:
            selected_index = self.tableView.currentIndex()
            if not selected_index.isValid():
                QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите аккаунт для удаления.")
                return

            id_login = self.tableView.model().item(selected_index.row(), 0).text()
            self.deleted_accounts.append(id_login)
            self.tableView.model().removeRow(selected_index.row())
            self.changes_made = True
            QMessageBox.information(self, "Успех", "Аккаунт помечен для удаления.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Save(self):
        if not self.changes_made:
            QMessageBox.warning(self, "Предупреждение", "Нет изменений для сохранения.")
            return

        try:
            conn = pyodbc.connect(CONN_STR)
            cursor = conn.cursor()

            for id_login in self.deleted_accounts:
                cursor.execute("DELETE FROM [dbo].[Account_in_a_game] WHERE ID_login = ?", id_login)
                print(f"Удален аккаунт: {id_login}")

            for row in range(self.tableView.model().rowCount()):
                id_login = self.tableView.model().item(row, 0).text().strip()
                email = self.tableView.model().item(row, 1).text().strip()
                password = self.tableView.model().item(row, 2).text().strip()

                print(f"Обработка аккаунта: {id_login}, Email: {email}, Пароль: {password}")

                cursor.execute("INSERT INTO [dbo].[Account_in_a_game] (ID_login, Email, Password, Time_in_a_account, Date) VALUES (?, ?, ?, ?, ?)", id_login, email, password, time_in_a_account, date)
                print(f"Добавлен новый аккаунт: {id_login}")

            conn.commit() 
            conn.close()

            self.changes_made = False  
            self.deleted_accounts.clear()
        
            self.load_accounts()  
            QMessageBox.information(self, "Успех", "Изменения успешно сохранены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def Exit(self):
        self.Exit_window = Ui_Manager(self.username)
        self.Exit_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_Communism()
    window.show()
    sys.exit(app.exec_())
