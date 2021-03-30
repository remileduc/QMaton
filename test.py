from PyQt5.QtWidgets import QApplication

app = QApplication(['--platform offscreen'])
print(f"My pid: {app.applicationPid()}")
app.quit()
