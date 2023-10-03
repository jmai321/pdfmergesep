# Jonathan Mai
# jonathannmai@gmail.com
# GitHub: @jmai321
import tkinter as tk
import tkinter.simpledialog
import easygui
from PyPDF2 import PdfWriter, PdfReader

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter and Merger")
        self.split_button = tk.Button(root, text="Split PDF", command=self.split_pdf)
        self.split_button.pack(pady=20)
        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=20)

    def split_pdf(self):
        file_path = easygui.fileopenbox(default="*.pdf", filetypes=["*.pdf"])
        if file_path:
            pages = tkinter.simpledialog.askstring("Input", "Enter pages to extract (e.g., 1,3,5-7):")
            if pages:
                output_path = easygui.filesavebox(default="*.pdf", filetypes=["*.pdf"])
                if output_path:
                    pdf_writer = PdfWriter()
                    pdf_reader = PdfReader(file_path)
                    selected_pages = self.parse_pages(pages, len(pdf_reader.pages))
                    for page_num in selected_pages:
                        pdf_writer.add_page(pdf_reader.pages[page_num - 1])
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                    easygui.msgbox("PDF has been split and saved.", "Success")

    def merge_pdfs(self):
        file_paths = easygui.fileopenbox(default="*.pdf", filetypes=["*.pdf"], multiple=True)
        if file_paths and len(file_paths) >= 2:
            output_path = easygui.filesavebox(default="*.pdf", filetypes=["*.pdf"])
            if output_path:
                pdf_writer = PdfWriter()
                for file_path in file_paths:
                    pdf_reader = PdfReader(file_path)
                    for page_num in range(len(pdf_reader.pages)):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                easygui.msgbox("PDF files have been merged.", "Success")

    def parse_pages(self, page_string, total_pages):
        pages = []
        ranges = page_string.split(',')
        for r in ranges:
            if '-' in r:
                start, end = map(int, r.split('-'))
                pages.extend(range(start, end + 1))
            else:
                pages.append(int(r))
        return [p for p in pages if 1 <= p <= total_pages]

root = tk.Tk()
app = PDFApp(root)
root.mainloop()
