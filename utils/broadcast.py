from PyQt5.QtCore import QObject, pyqtSignal



class Broadcast(QObject):
    send_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.loop = True
        self.receiver = {}
        self.send_signal.connect(self.handleSend)

    __instance = None

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Broadcast()
        return cls.__instance

    def startSend(self, key, value=None):
        msg = {
            'key': key,
            'value': value
        }
        self.send_signal.emit(msg)

    def handleSend(self, msg):
        key = msg['key']
        value = msg['value']
        if key in self.receiver:
            for item in self.receiver[key]:
                if item is not None:
                    if key == 'MethodNavigator_Search_Name_To_MethodMain' or key == 'MethodMain_Search_Name_To_MethodNavigator':
                        item(value)
                    else:
                        if value is not None and value != '':
                            item(value)
                        else:
                            item()

    def registerReceiver(self, key, value):
        if key not in self.receiver:
            self.receiver[key] = [value]
        else:
            self.receiver[key].append(value)

    def registerReceiverOnce(self, key, value):
        if key not in self.receiver:
            self.receiver[key] = [value]
