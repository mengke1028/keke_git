@echo off
REM 设置代码页为 65001 (UTF-8)
chcp 65001 > nul
REM C:\Users\Keke.Meng\AppData\Local\Programs\Python\Python37\Scripts\pyinstaller.exe -F -w D:\keke\PDF转World.py
REM C:\Users\Keke.Meng\AppData\Local\Programs\Python\Python37\Scripts\pyinstaller.exe -F -w D:\keke\bilibili.py
C:\Users\Keke.Meng\AppData\Local\Programs\Python\Python39\Scripts\pyinstaller.exe -F -w test.py
