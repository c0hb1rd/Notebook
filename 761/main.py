from tkinter import ttk, filedialog
import tkinter
import os
import subprocess
import time
import threading


class MyWindow:
    def __init__(self, **options):
        self.window = tkinter.Tk()
        self.window.wm_minsize(
            width=1280 if 'width' not in options else options['width'],
            height=800 if 'height' not in options else options['height']
        )

        self.window.bind("<Escape>", lambda e: self.window.quit())

        self.console = tkinter.Text(self.window, width=70, height=15)
        self.console.insert(tkinter.END, 'console')
        self.console.place(x=640, y=20)

        self.log = tkinter.Text(self.window, width=70, height=15)
        self.log.insert(tkinter.END, 'log')
        self.log.place(x=640, y=280)

        self.widget_map = {
            'entry': tkinter.Entry,
            'button': tkinter.Button,
            'label': tkinter.Label
        }

        self.combox_list = []

        self.conf = {
            'args': '',
            'dirs': [],
            'src': '',
            'com': ''
        }

        self.edit = self.new_edit(20, 20)
        self.edit2 = self.new_edit(20, 60)

        self.select = self.new_select(['选择编译器', '编译器1', '编译器2', '编译器3'], 20, 100, lambda arg: print(self.select.get()))

        self.new_button('选择源码', 20 + 150, 24 - 5, self.open)
        self.new_button('开始编译', 20 + 150, 64 - 5, self.run)

    # def scrollbar_handler(self, *args, **options):
    #     kind = args[0]
    #     cur_pos = self.scrollbar.get()[0]
    #
    #     if kind == 'moveto':
    #         print(args, options)
    #         print('[*]Pos:', args[1])
    #         print(float(args[1]))
    #         self.scrollbar.set(float(args[1]) + cur_pos, 0)
    #
    #     elif kind == 'scroll':
    #         if args[2] == 'units':
    #             self.scrollbar.set(cur_pos + int(args[1]) / 100, 0)

    def open(self):
        path = filedialog.askdirectory()
        self.edit.set(path)

        for line in self.combox_list:
            line['btn'].destroy()
            line['label'].destroy()
        count = 0
        x = 20
        y = 140
        for line in os.listdir(path):
            p = os.path.join(path, line)
            if os.path.isdir(p):
                self.create_checkbtn(line, x + count, y)
                l = len(line) * 11
                count += l if l > 60 else 60
                if count >= 450:
                    y += 30
                    x = 20
                    count = 0

                    # self.window.wm_minsize(self.window.winfo_width(), y)

    def run(self):
        check = []
        for line in self.combox_list:
            if line['select'].get() == '1':
                check.append(line['content'])

        self.conf['dirs'] = check
        self.conf['args'] = self.edit2.get()
        self.conf['src'] = self.edit.get()
        self.conf['com'] = self.select.get()

        self.console.delete(0.0, tkinter.END)

        for line in self.conf['dirs']:
            self.execute(line)

    def execute(self, path):
        path = os.path.join(self.conf['src'], path)

        self.console.insert(tkinter.END, 'Processing "' + path + '"...\n')
        output = subprocess.getoutput(path + '/configure ' + self.conf['args'])

        self.console.insert(tkinter.END, 'Finish\n')

        self.log.delete(0.0, tkinter.END)
        self.log.insert(tkinter.END, output)

    def create_label(self, text=None, x=None, y=None):
        label = tkinter.Label(self.window, text=text)
        label.place(x=x, y=y)

        return label

    def create_checkbtn(self, title, x, y):
        value = tkinter.StringVar()
        checkbtn = tkinter.Checkbutton(self.window, variable=value)
        checkbtn.bind("<<CheckbuttonSelected>>", lambda x: print(1))

        label = self.create_label(title, x=x + 25, y=y)

        checkbtn.place(x=x, y=y)
        self.combox_list.append({
            'select': value,
            'content': title,
            'btn': checkbtn,
            'label': label
        })

        return value

    def new_select(self, obj, x=None, y=None, event=None):
        list_box = ttk.Combobox(self.window)
        list_box['values'] = obj
        list_box.current(0)

        if event:
            list_box.bind("<<ComboboxSelected>>", event)

        list_box.place(x=x, y=y)

        return list_box

    def new_edit(self, x=None, y=None):
        value = tkinter.StringVar()
        entry = tkinter.Entry(self.window, width=15, textvariable=value)
        entry.place(x=x, y=y)
        entry.focus()
        return value

    def new_button(self, text=None, x=None, y=None, bind=None):
        button = tkinter.Button(self.window, text=text, command=bind)
        button.place(x=x, y=y)
        return button

    def mainloop(self):
        self.window.mainloop()


MyWindow().mainloop()
