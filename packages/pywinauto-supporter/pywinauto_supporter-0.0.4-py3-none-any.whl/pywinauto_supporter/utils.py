import win32gui
import win32con
import threading
#from pywinauto import Desktop, Application
import time
import pywinauto

def run(handle):
    #https://groups.google.com/g/python_inside_maya/c/qZOWB6_8E3g
    for i in range(2):
        #change_background_color(hwnd, color1)
        win32gui.ShowWindow(handle, win32con.SW_HIDE)
        time.sleep(0.5)
        #change_background_color(hwnd, color2)
        #time.sleep(duration)
        win32gui.ShowWindow(handle, win32con.SW_SHOW)
        if i != 2 -1:
            time.sleep(0.5)

'''
def blink(process_id, handle):
    app = Application(backend='uia').connect(process=int(process_id)) #프로세스 pid로 연결하는 방법
    #app = Application(backend='uia').connect(title_re="Notepad\+\+") #정규식으로 프로그램 title을 검색해서 연결하는 방법
    window = app.window(handle=handle)
    #window.wrapper_object().set_focus()
    t = threading.Thread(target=run, args=[handle])
    t.start()
'''
def blink(handle):
    t = threading.Thread(target=run, args=[handle])
    t.start()
