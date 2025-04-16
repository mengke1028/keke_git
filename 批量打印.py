# -*- coding: utf-8 -*-
# Keke.Meng  2025/3/12 9:56
import os
import win32print
import win32api
import fitz  # PyMuPDF
from win32com.client import Dispatch


def print_pdf(file_path, printer_name):
    pdf_document = fitz.open(file_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        temp_image_path = f"temp_page_{page_num}.png"
        pix.save(temp_image_path)
        win32api.ShellExecute(
            0,
            "print",
            temp_image_path,
            f'"{printer_name}"',
            ".",
            0
        )
        os.remove(temp_image_path)
    pdf_document.close()


def print_png(file_path, printer_name):
    win32api.ShellExecute(
        0,
        "print",
        file_path,
        f'"{printer_name}"',
        ".",
        0
    )


def print_xlsx(file_path, printer_name):
    excel = Dispatch("Excel.Application")
    workbook = excel.Workbooks.Open(file_path)
    # 设置打印机
    print(printer_name)
    excel.ActivePrinter = printer_name
    workbook.PrintOut()
    workbook.Close()
    excel.Quit()


def batch_print_files(directory, printer_name):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.pdf'):
                print(file_path)
                print_pdf(file_path, printer_name)
            elif file.lower().endswith('.png'):
                print_png(file_path, printer_name)
            # elif file.lower().endswith('.xlsx'):
            #     print_xlsx(file_path, printer_name)


if __name__ == "__main__":
    import win32print

    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
    for printer in printers:
        print(printer[2])
    print("########################")
    directory = r"C:\Users\Keke.Meng\Documents\2.28出差材料"  # 替换为实际的目录路径
    printer_name = "Generic 95BW-9SeriesPCL"
    batch_print_files(directory, printer_name)