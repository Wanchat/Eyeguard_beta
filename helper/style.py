from PyQt5.QtWidgets import QApplication, QWidget

class Style():

    def initgui(self):

        self.text = """
        QPushButton{
            font-family: Helvetica-Normal,"Times New Roman",Times, serif;
            font-size: 12px;
            background-color: #b3b3b3;
            border-radius: 15px;
            color: #333333;
            }
            
        QPushButton:hover{
            background-color: #cccccc;
            }
            
        QLabel{
            color: #333333;
            font-family: Helvetica-Normal,"Times New Roman",Times, serif;
            
            }
            
            
            
            
            """
        return self.text
# border-image: url(logo_eyeguard.svg);
#             background-color: transparent;