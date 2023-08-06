# pywinauto-supporter

```
import win32gui
import win32con
import threading
import time
import pywinauto
from pywinauto_supporter.utils import blink

app = pywinauto.application.Application(backend='uia').connect(title='계산기')
#app = Application(backend='uia').connect(process=int(process_id)) #프로세스 pid로 연결하는 방법
#app = Application(backend='uia').connect(title_re="Notepad\+\+") #정규식으로 프로그램 title을 검색해서 연결하는 방법
top_window = app.top_window()

one_window = top_window.child_window(title="1")
#one_window.wrapper_object().click_input()

#blink(top_window.handle)
blink(one_window.handle)
```
