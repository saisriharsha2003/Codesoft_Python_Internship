import sqlite3
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox

# Connect to the database or create a new one if it doesn't exist
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# Create a table to store tasks if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task_name TEXT NOT NULL,
        due_date TEXT,
        status TEXT
    )
""")
conn.commit()

def add_task(task_name, due_date=None):
    if due_date is not None:
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
    cursor.execute("INSERT INTO tasks (task_name, due_date, status) VALUES (?, ?, ?)",
                   (task_name, due_date, "Pending"))
    conn.commit()

def update_task(task_id, new_task_name):
    cursor.execute("UPDATE tasks SET task_name=? WHERE id=?", (new_task_name, task_id))
    conn.commit()

def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

def complete_task(task_id):
    cursor.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
    conn.commit()

def get_all_tasks():
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

class ToDoListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("To-Do List Application")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label_task = QLabel("Task:")
        self.entry_task = QLineEdit()

        self.label_date = QLabel("Due Date (YYYY-MM-DD):")
        self.entry_date = QLineEdit()

        self.button_add_task = QPushButton("Add")
        self.button_add_task.clicked.connect(self.on_add_task)
        self.button_add_task.setStyleSheet("background-color: #007bff; color: white;")

        self.layout.addWidget(self.label_task)
        self.layout.addWidget(self.entry_task)

        self.layout.addWidget(self.label_date)
        self.layout.addWidget(self.entry_date)

        self.layout.addWidget(self.button_add_task)

        self.task_list = QTableWidget(self)
        self.task_list.setColumnCount(1)
        self.task_list.setHorizontalHeaderLabels(["Task Name"])
        self.task_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.layout.addWidget(self.task_list)

        self.refresh_task_list()

        self.central_widget.setLayout(self.layout)

    def on_add_task(self):
        task_name = self.entry_task.text()
        due_date = self.entry_date.text()
        add_task(task_name, due_date)
        self.refresh_task_list()

    def on_edit_task(self, row):
        task_id = int(self.task_list.item(row, 0).data(32))
        new_task_name, ok_pressed = QInputDialog.getText(self, "Edit Task", "Enter new task name:", QLineEdit.Normal, self.task_list.item(row, 0).text())
        if ok_pressed and new_task_name.strip():
            update_task(task_id, new_task_name.strip())
            self.refresh_task_list()

    def on_delete_task(self, row):
        task_id = int(self.task_list.item(row, 0).data(32))
        reply = QMessageBox.question(self, "Delete Task", "Are you sure you want to delete this task?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_task(task_id)
            self.refresh_task_list()

    def on_complete_task(self, row):
        task_id = int(self.task_list.item(row, 0).data(32))
        complete_task(task_id)
        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_list.clearContents()
        self.task_list.setRowCount(0)

        tasks = get_all_tasks()
        for task in tasks:
            row_position = self.task_list.rowCount()
            self.task_list.insertRow(row_position)
            item = QTableWidgetItem(task[1])
            item.setData(32, task[0])
            self.task_list.setItem(row_position, 0, item)

            button_layout = QHBoxLayout()

            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: #0056b3; color: white;")
            edit_button.setFixedSize(60, 30)
            edit_button.clicked.connect(lambda _, row=row_position: self.on_edit_task(row))
            button_layout.addWidget(edit_button)

            delete_button = QPushButton("Remove")
            delete_button.setStyleSheet("background-color: #ff0000; color: white;")
            delete_button.setFixedSize(60, 30)
            delete_button.clicked.connect(lambda _, row=row_position: self.on_delete_task(row))
            button_layout.addWidget(delete_button)

            complete_button = QPushButton("Completed")
            complete_button.setStyleSheet("background-color: #00cc00; color: white;")
            complete_button.setFixedSize(80, 30)
            complete_button.clicked.connect(lambda _, row=row_position: self.on_complete_task(row))
            button_layout.addWidget(complete_button)

            container_widget = QWidget()
            container_widget.setLayout(button_layout)
            self.task_list.setCellWidget(row_position, 0, container_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoListApp()
    window.show()
    sys.exit(app.exec_())

# Close the database connection when the program ends
conn.close()
