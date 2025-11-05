import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt


class KeyPressViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.normal_key_map = {
            '48': '0',
            '49': '1',
            '50': '2',
            '51': '3',
            '52': '4',
            '53': '5',
            '54': '6',
            '55': '7',
            '56': '8',
            '57': '9',
            '65': 'A',
            '66': 'B',
            '67': 'C',
            '68': 'D',
            '69': 'E',
            '70': 'F',
            '71': 'G',
            '72': 'H',
            '73': 'I',
            '74': 'J',
            '75': 'K',
            '76': 'L',
            '77': 'M',
            '78': 'N',
            '79': 'O',
            '80': 'P',
            '81': 'Q',
            '82': 'R',
            '83': 'S',
            '84': 'T',
            '85': 'U',
            '86': 'V',
            '87': 'W',
            '88': 'X',
            '89': 'Y',
            '90': 'Z',
            '16777264': 'F1',
            '16777265': 'F2',
            '16777266': 'F3',
            '16777267': 'F4',
            '16777268': 'F5',
            '16777269': 'F6',
            '16777270': 'F7',
            '16777271': 'F8',
            '16777272': 'F9',
            '16777273': 'F10',
            '16777274': 'F11',
            '16777275': 'F12',
            '16777216': 'Esc',
            '96': '`',
            '126': '~',
            '33': '!',
            '64': '@',
            '35': '#',
            '36': '$',
            '37': '%',
            '94': '^',
            '38': '&',
            '42': '*',
            '40': '(',
            '41': ')',
            '45': '-',
            '95': '_',
            '61': '=',
            '43': '+',
            '16777219': 'Backspace',
            '16777222': 'Insert',
            '16777232': 'Home',
            '16777238': 'PgUp',
            '16777253': 'Num Lock',
            '47':'/',
            '16777217':'Tab',
            '91':'[',
            '123':'{',
            '93':']',
            '125':'}',
            '92':'\\',
            '124':'|',
            '16777223':'Delete',
            '16777233':'End',
            '16777239':'PgDn',
            '16777235':'↑',
            '16777237':'↓',
            '16777234':'←',
            '16777236':'→',
            '16777252': 'Caps Lock',
            '59': ';',
            '58': ':',
            '39': "'",
            '34': '"',
            '16777220':'Enter',
            '44':',',
            '60':'<',
            '46':'.',
            '62':'>',
            '63':'?',
            '16777221':'Num Enter',
            '32':'Space',
            '16777301':'Right Click',
            


        }

        self.special_key_map = {
            '16777249': 'Ctrl',
            '16777248': 'Shift',
            '16777251': 'Alt',
            '16777250': 'Win',
        }

        self.setWindowTitle('键盘按键查看器')
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def keyPressEvent(self, event):
        # 捕获按键事件
        key = str(event.key())
        
        flag = False    
        if key in self.special_key_map:
            print(self.special_key_map[key])
            flag = True
        if key in self.normal_key_map:
            print(self.normal_key_map[key])
            flag = True
        if not flag:
            print(key)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KeyPressViewer()
    sys.exit(app.exec_())
