import os
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot as plt
import database as db

# CONFIG TEST
path = "C:/Users/user/facial_recognition/"  # your path

# Facial recognition functions
def face(img, faces):
    data = plt.imread(img)
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]
        x2, y2 = x1 + ancho, y1 + alto
        plt.subplot(1, len(faces), i + 1)
        plt.axis("off")
        face_img = cv2.resize(data[y1:y2, x1:x2], (150, 200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, face_img)
        plt.imshow(data[y1:y2, x1:x2])

# Login dialog
class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 400, 200)
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Enter username")
        self.user_input.setAlignment(Qt.AlignCenter)
        self.capture_btn = QPushButton("Capture Face", self)
        self.capture_btn.clicked.connect(self.capture_face)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Login", self))
        layout.addWidget(self.user_input)
        layout.addWidget(self.capture_btn)
        self.setLayout(layout)

    def capture_face(self):
        user_login = self.user_input.text()
        img = f"{user_login}_login.jpg"
        img_user = f"{user_login}.jpg"

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow("Login Facial", frame)
            if cv2.waitKey(1) == 27:  # Press Esc to exit
                break

        cv2.imwrite(img, frame)
        cap.release()
        cv2.destroyAllWindows()

        pixels = plt.imread(img)
        faces = MTCNN().detect_faces(pixels)

        face(img, faces)
        # Compatibility check logic here (use your original logic from compatibility function)

        self.close()

# Register dialog
class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.setGeometry(200, 200, 400, 200)
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Enter username")
        self.user_input.setAlignment(Qt.AlignCenter)
        self.capture_btn = QPushButton("Capture Face", self)
        self.capture_btn.clicked.connect(self.capture_face)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Register", self))
        layout.addWidget(self.user_input)
        layout.addWidget(self.capture_btn)
        self.setLayout(layout)

    def capture_face(self):
        user_reg_img = self.user_input.text()
        img = f"{user_reg_img}.jpg"

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow("Register Facial", frame)
            if cv2.waitKey(1) == 27:  # Press Esc to exit
                break

        cv2.imwrite(img, frame)
        cap.release()
        cv2.destroyAllWindows()

        pixels = plt.imread(img)
        faces = MTCNN().detect_faces(pixels)

        face(img, faces)

        # Save to database
        res_bd = db.registerUser(user_reg_img, path + img)
        if res_bd["affected"]:
            print("Successfully registered!")
        else:
            print("Registration failed!")

        self.close()

# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CIAS Facial Recognition")
        self.setGeometry(100, 100, 500, 300)

        # Title label
        self.label = QLabel("¡Bienvenido(a)!", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px;")
        self.label.setGeometry(0, 30, 500, 50)

        # Login button
        self.login_btn = QPushButton("Iniciar Sesión", self)
        self.login_btn.setGeometry(150, 100, 200, 50)
        self.login_btn.clicked.connect(self.show_login_dialog)

        # Register button
        self.register_btn = QPushButton("Registrarse", self)
        self.register_btn.setGeometry(150, 200, 200, 50)
        self.register_btn.clicked.connect(self.show_register_dialog)

    def show_login_dialog(self):
        login_dialog = LoginDialog(self)
        login_dialog.exec_()

    def show_register_dialog(self):
        register_dialog = RegisterDialog(self)
        register_dialog.exec_()

# Main application
if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
