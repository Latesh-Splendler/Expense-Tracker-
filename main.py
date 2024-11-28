from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QLineEdit, QDateEdit, QVBoxLayout, QHBoxLayout, QTableWidget, QMessageBox, QTableWidgetItem, QHeaderView 
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys
from PyQt5.QtCore import QDate, Qt

class ExpenseApp(QWidget):
  def __init__(self):
    super().__init__()

    self.resize(650, 750)
    self.setWindowTitle("Expense Tracker")



    self.date_box = QDateEdit()
    self.dropdown = QComboBox()
    self.amount = QLineEdit()
    self.description = QLineEdit()

    self.add_button = QPushButton("Add Expense")
    self.delete_button = QPushButton("Delete Expense")
    self.add_button.clicked.connect(self.add_expense)
    self.delete_button.clicked.connect(self.delete_expense)


    self.table = QTableWidget()
    self.table.setColumnCount(5)
    self.table.setHorizontalHeaderLabels( ["Id", "Date", "Category", "Amount", "Desciption"])
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.table.sortByColumn(1, Qt.DescendingOrder)


    self.dropdown.addItems(["Food", "Transportation", "Shopping", "Etica", "Lofty Corbon", "Other"])
    self.setStyleSheet("""
                       QWidget {background-color: #9be4ea;}

                       QLabel{
                         color: #333;
                         font-size: 12px;
                       }

                       QLineEdit, QComboBox, QDateEdit{
                         background-color: #9be4ea;
                         border: 1px solid #ccc;
                         color: #333;
                         padding: 5px;
                       }

                       QTableWidget{
                         background-color: #9be4ea;
                         border: 1px solid #ccc;
                         color: #333;
                         selection-background-color: #ddd;
                       }

                       QPushButton{
                         background-color: #4CAF50;
                         color: #fff;
                         padding: 5px;
                         border: none;
                         border-radius: 2px;
                         font-size: 12px;
                       }

                       QPushButton::hover{
                         background-color: #3e8e41;

                       }

    """)


    self.master_layout = QVBoxLayout()
    self.row1 = QHBoxLayout()
    self.row2 = QHBoxLayout()
    self.row3 = QHBoxLayout()

    self.row1.addWidget(QLabel("Date:"))
    self.row1.addWidget(self.date_box)
    self.row1.addWidget(QLabel("Category:"))
    self.row1.addWidget(self.dropdown)

    self.row2.addWidget(QLabel("Amount:"))
    self.row2.addWidget(self.amount)
    self.row2.addWidget(QLabel("Description:"))
    self.row2.addWidget(self.description)

    self.row3.addWidget(self.add_button)
    self.row3.addWidget(self.delete_button)

    self.master_layout.addLayout(self.row1)
    self.master_layout.addLayout(self.row2)
    self.master_layout.addLayout(self.row3)


    self.master_layout.addWidget(self.table)

    self.setLayout(self.master_layout)

    self.load_table()



  def load_table(self):
      self.table.setRowCount(0)


      query = QSqlQuery("SELECT * FROM expenses")
      row = 0
      while query.next():
        expense_Id = query.value(0)
        Date = query.value(1)
        Category = query.value(2)
        Amount = query.value(3)
        Description = query.value(4)


        self.table.insertRow(row)
        self.table.setItem(row, 0,QTableWidgetItem(str(expense_Id)))
        self.table.setItem(row, 1,QTableWidgetItem(Date))
        self.table.setItem(row, 2,QTableWidgetItem(Category))
        self.table.setItem(row, 3,QTableWidgetItem(str(Amount)))
        self.table.setItem(row, 4,QTableWidgetItem(Description))


        row += 1



  def add_expense(self):
      Date = self.date_box.date().toString("yyyy-MM-dd")
      Category = self.dropdown.currentText()
      Amount = self.amount.text()
      Description = self.description.text()       


      query = QSqlQuery()
      query.prepare("""INSERT INTO expenses (Date, Category, Amount, Description) 
                   VALUES (?, ?, ?, ?)

                   """)
     
      query.addBindValue(Date)
      query.addBindValue(Category)
      query.addBindValue(Amount)
      query.addBindValue(Description)
      query.exec_()


      self.dropdown.setCurrentIndex(0)
      self.amount.clear()
      self.description.clear()
      self.date_box.setDate(QDate.currentDate())

      self.load_table()


  def delete_expense(self):
     selected_row = self.table.currentRow()
     if selected_row == -1:
        QMessageBox.warning(self, "No Expense Choosen", "Choose an Expense to delete bro") 
        return
     expense_Id = int(self.table.item(selected_row, 0).text())


     confirm = QMessageBox.question(self, "You sure", "Delete Expense?", QMessageBox.Yes | QMessageBox.No)


     if confirm == QMessageBox.No:
        return
     

     query = QSqlQuery()
     query.prepare("DELETE FROM expenses WHERE id = ?")
     query.addBindValue(expense_Id)
     query.exec_()

     self.load_table()
                  






database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
   QMessageBox.critical(None, "Error","Could not open the Database")
   sys.exit(1)



query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS expenses (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             Date TEXT,
             Category TEXT,
             Amount REAL,
             Description TEXT
            
            )
    """)






if __name__ in "__main__":
    app = QApplication([])  
    main = ExpenseApp()  
    main.show()
    app.exec_()







    



