from tkinter import *
from tkinter.ttk import *
from tkinter import font, colorchooser, filedialog, messagebox
import os
import tempfile

root = Tk()

# ---------- Globals ----------
file_path = ''
fontStyle = 'arial'
fontSize = 10


# ---------- Functions ----------
def status_bar_function(event=None):
    if textArea.edit_modified():
        word = len(textArea.get(0.0, END).split())
        characters = len(textArea.get(0.0, 'end-1c').replace(' ', ''))  # remove the "newline" character from the end
        statusBar.config(text=f'Characters: {characters} Words: {word}')
    textArea.edit_modified(False)


def new_file(event=None):
    global file_path
    file_path = ''
    textArea.delete(0.0, END)  # delete everything
    root.title('Text Editor')  # always set the title


def open_file(event=None):
    global file_path
    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File',
                                           filetypes=(('Text File', 'txt'), ('All Files', '*.*')))

    if file_path != '':  # if the file is not empty
        textArea.delete(0.0, END)
        with open(file_path, 'r') as f:
            content = f.read()
            textArea.insert(END, content)
        root.title(os.path.basename(file_path))  # get only the file name and set it as title


def save_file(event=None):
    if file_path == '':  # clean file
        save_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                                 filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
        with open(save_path, 'w') as f:
            content = textArea.get(0.0, END)
            f.write(content)
        root.title(os.path.basename(save_path))
    else:
        content = textArea.get(0.0, END)
        with open(file_path, 'w') as f:
            f.write(content)


def save_as_file(event=None):
    save_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                             filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
    content = textArea.get(0.0, END)
    with open(save_path, 'w') as f:
        f.write(content)
    if file_path != '':
        os.remove(file_path)


def print_file(event=None):
    file = tempfile.mktemp('.txt')
    open(file, 'w').write(textArea.get(1.0, END))
    os.startfile(file, 'print')


def exit_file(event=None):
    if textArea.edit_modified():
        result = messagebox.askyesnocancel('Warning', 'Do you want to save the file ?')
        if result:
            if file_path != '':  # clicks on "Yes" | and | if the file contains something
                content = textArea.get(0.0, END)
                with open(file_path, 'w') as f:
                    f.write(content)
                root.destroy()
            else:  # clicks on "Yes" | and | the file is empty
                content = textArea.get(0.0, END)
                save_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                                         filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
                with open(save_path, 'w') as f:
                    f.write(content)
                root.destroy()
        elif not result:  # clicks on "No"
            root.destroy()
        else:  # clicks on "Cancel"
            pass
    else:  # if nothing has been changed simply close the window
        root.destroy()


def find():
    def find_words():
        textArea.tag_remove('match', 1.0, END)  # remove highlight
        # 1.0 - line 1, first character (1.0) or (0.0)
        start_position = '1.0'
        word = find_entry_field.get()
        if word:  # execute the loop only there is a word
            while True:
                start_position = textArea.search(word, start_position, stopindex=END)
                if not start_position:
                    break
                end_position = f'{start_position}+{len(word)}c'
                textArea.tag_add('match', start_position, end_position)
                textArea.tag_config('match', foreground='red', background='yellow')
                start_position = end_position

    def replace_words():
        word = find_entry_field.get()
        replace_word = replace_entry_field.get()
        content = textArea.get(1.0, END)
        new_content = content.replace(word, replace_word)
        textArea.delete(1.0, END)  # delete row before replace
        textArea.insert(1.0, new_content)

    root1 = Toplevel()  # create window on top of other window
    root1.title('Find')
    root1.geometry('450x250+500+200')
    root1.resizable(False, False)
    label_frame = LabelFrame(root1, text='Find/Replace')
    label_frame.pack(pady=50)

    find_label = Label(label_frame, text='Find')
    find_label.grid(row=0, column=0, padx=5, pady=5)
    find_entry_field = Entry(label_frame)
    find_entry_field.grid(row=0, column=1, padx=5, pady=5)

    replace_label = Label(label_frame, text='Replace')
    replace_label.grid(row=1, column=0, padx=5, pady=5)
    replace_entry_field = Entry(label_frame)
    replace_entry_field.grid(row=1, column=1, padx=5, pady=5)

    find_button = Button(label_frame, text='FIND', command=find_words)
    find_button.grid(row=2, column=0, padx=5, pady=5)

    replace_button = Button(label_frame, text='REPLACE', command=replace_words)
    replace_button.grid(row=2, column=1, padx=5, pady=5)

    def do_something():
        textArea.tag_remove('match', 1.0, END)  # remove highlight after close the window
        root1.destroy()

    root1.protocol('WM_DELETE_WINDOW', do_something)  # change the functionality of the close button
    root1.mainloop()


def toolbar_hide():
    if not show_toolbar.get():
        toolBar.pack_forget()
    else:
        textArea.pack_forget()
        toolBar.pack(fill=X)
        textArea.pack(fill=BOTH, expand=True)


def statusbar_hide():
    if not show_statusbar.get():
        statusBar.pack_forget()
    else:
        statusBar.pack()


def change_theme(bg_color, fg_color):
    textArea.config(bg=bg_color, fg=fg_color)


def font_style(event=None):  # it must contain a parameter
    global fontStyle
    fontStyle = font_variable.get()
    textArea.config(font=(fontStyle, fontSize))


def font_size(event=None):
    global fontSize
    fontSize = size_variable.get()
    textArea.config(font=(fontStyle, fontSize))


def bold_text():
    text_property = font.Font(font=textArea['font']).actual()
    if text_property['weight'] == 'normal':
        textArea.config(font=(fontStyle, fontSize, 'bold'))
    if text_property['weight'] == 'bold':
        textArea.config(font=(fontStyle, fontSize, 'normal'))


def italic_text():
    text_property = font.Font(font=textArea['font']).actual()
    if text_property['slant'] == 'roman':
        textArea.config(font=(fontStyle, fontSize, 'italic'))
    if text_property['slant'] == 'italic':
        textArea.config(font=(fontStyle, fontSize, 'roman'))


def underline_text():
    text_property = font.Font(font=textArea['font']).actual()
    if text_property['underline'] == 0:
        textArea.config(font=(fontStyle, fontSize, 'underline'))
    if text_property['underline'] == 1:
        textArea.config(font=(fontStyle, fontSize))


def color_select():
    color = colorchooser.askcolor()
    textArea.config(fg=color[1])


def align_left():
    data = textArea.get(0.0, END)
    textArea.tag_config('left', justify=LEFT)
    textArea.delete(0.0, END)
    textArea.insert(INSERT, data, 'left')


def align_center():
    data = textArea.get(0.0, END)
    textArea.tag_config('center', justify=CENTER)
    textArea.delete(0.0, END)
    textArea.insert(INSERT, data, 'center')


def align_right():
    data = textArea.get(0.0, END)
    textArea.tag_config('right', justify=RIGHT)
    textArea.delete(0.0, END)
    textArea.insert(INSERT, data, 'right')


# Window
root.title("Text Editor")
root.geometry("1200x620+10+10")  # +10+10 from where the window to start (10x10 px in the top left corner of screen)
root.resizable(False, False)  # not resizable


# ---------- Menu Bar ----------
menuBar = Menu(root)
root.config(menu=menuBar)


# ---------- File ----------

# File Menu Items
fileMenu = Menu(menuBar, tearoff=False)
menuBar.add_cascade(label='File', menu=fileMenu)


# File Menu Icons
newImage = PhotoImage(file='icons/new.png')
openImage = PhotoImage(file='icons/open.png')
saveImage = PhotoImage(file='icons/save.png')
saveAsImage = PhotoImage(file='icons/saveas.png')
printImage = PhotoImage(file='icons/print.png')
exitImage = PhotoImage(file='icons/exit.png')


# File Menu SubItems
fileMenu.add_command(label='New', accelerator='Ctrl+N', image=newImage, compound=LEFT, command=new_file)
fileMenu.add_command(label='Open', accelerator='Ctrl+O', image=openImage, compound=LEFT, command=open_file)
fileMenu.add_command(label='Save', accelerator='Ctrl+S', image=saveImage, compound=LEFT, command=save_file)
fileMenu.add_command(label='Save As', accelerator='Ctrl+Alt+S', image=saveAsImage, compound=LEFT,
                     command=save_as_file)
fileMenu.add_command(label='Print', accelerator='Ctrl+P', image=printImage, compound=LEFT, command=print_file)
fileMenu.add_separator()
fileMenu.add_command(label=' Exit', accelerator='Ctrl+Q', image=exitImage, compound=LEFT, command=exit_file)


# ---------- Edit ----------

# Edit Menu Items
editMenu = Menu(menuBar, tearoff=False)
menuBar.add_cascade(label='Edit', menu=editMenu)


# Edit Menu Icons
undoImage = PhotoImage(file='icons/undo.png')
cutImage = PhotoImage(file='icons/cut.png')
copyImage = PhotoImage(file='icons/copy.png')
pasteImage = PhotoImage(file='icons/paste.png')
selectImage = PhotoImage(file='icons/checked.png')
clearImage = PhotoImage(file='icons/clear.png')
findImage = PhotoImage(file='icons/find.png')


# Edit Menu SubItems
editMenu.add_command(label='Undo', accelerator='Ctrl+Z', image=undoImage, compound=LEFT)
editMenu.add_command(label='Cut', accelerator='Ctrl+X', image=cutImage, compound=LEFT,
                     command=lambda: textArea.event_generate('<Control x>'))
editMenu.add_command(label='Copy', accelerator='Ctrl+C', image=copyImage, compound=LEFT,
                     command=lambda: textArea.event_generate('<Control c>'))
editMenu.add_command(label='Paste', accelerator='Ctrl+V', image=pasteImage, compound=LEFT,
                     command=lambda: textArea.event_generate('<Control v>'))
editMenu.add_command(label='Select All', accelerator='Ctrl+A', image=selectImage, compound=LEFT,
                     command=lambda: textArea.event_generate('<Control a>'))
editMenu.add_command(label='Clear', accelerator='Ctrl+Alt+X', image=clearImage, compound=LEFT,
                     command=lambda: textArea.delete(0.0, END))
editMenu.add_command(label='Find', accelerator='Ctrl+F', image=findImage, compound=LEFT, command=find)


# ---------- View ----------

# View Menu Item
viewMenu = Menu(menuBar, tearoff=False)
menuBar.add_cascade(label='View', menu=viewMenu)


# View Menu Icon
toolbarImage = PhotoImage(file='icons/hide.png')
statusbarImage = PhotoImage(file='icons/status.png')


# View Menu SubItem
show_toolbar = BooleanVar()
show_toolbar.set(True)
viewMenu.add_checkbutton(label='Tool Bar', variable=show_toolbar, onvalue=True, offvalue=False,
                         image=toolbarImage, compound=LEFT, command=toolbar_hide)
show_statusbar = BooleanVar()
show_statusbar.set(True)
viewMenu.add_checkbutton(label='Status Bar', variable=show_toolbar, onvalue=True, offvalue=False,
                         image=statusbarImage, compound=LEFT, command=statusbar_hide)


# ---------- Themes ----------

# Themes Menu Items
themesMenu = Menu(menuBar, tearoff=False)
menuBar.add_cascade(label='Themes', menu=themesMenu)


# Themes Menu Icons
lightImage = PhotoImage(file='icons/light.png')
darkImage = PhotoImage(file='icons/dark.png')


# Themes Menu SubItems
theme_select = StringVar()
themesMenu.add_radiobutton(label='Light Theme', variable=theme_select, image=lightImage, compound=LEFT,
                           command=lambda: change_theme('white', 'black'))
themesMenu.add_radiobutton(label='Dark Theme', variable=theme_select, image=darkImage, compound=LEFT,
                           command=lambda: change_theme('black', 'white'))


# ---------- Tool Bar ----------
toolBar = Label(root)
toolBar.pack(side=TOP, fill=X)
statusBar = Label(root)
statusBar.pack(side=BOTTOM, fill=X)


# Font Family
font_family = font.families()
font_variable = StringVar()
fontFamilyCombobox = Combobox(toolBar, width=30, values=font_family, state='readonly', textvariable=font_variable)
fontFamilyCombobox.current(font_family.index('Arial'))
fontFamilyCombobox.grid(row=0, column=0, padx=5)


# Font Size
size_variable = IntVar()
fontSizeCombobox = Combobox(toolBar, width=15, values=tuple(range(8, 81)), state='readonly',
                            textvariable=size_variable)
fontSizeCombobox.current(2)
fontSizeCombobox.grid(row=0, column=1, padx=5)


# Bold
boldImage = PhotoImage(file='icons/bold.png')
boldButton = Button(toolBar, image=boldImage, command=bold_text)
boldButton.grid(row=0, column=2, padx=5)


# Italic
italicImage = PhotoImage(file='icons/italic.png')
italicButton = Button(toolBar, image=italicImage, command=italic_text)
italicButton.grid(row=0, column=3, padx=5)


# Underline
underlineImage = PhotoImage(file='icons/underline.png')
underlineButton = Button(toolBar, image=underlineImage, command=underline_text)
underlineButton.grid(row=0, column=4, padx=5)


# Text Color
colorTextImage = PhotoImage(file='icons/text-color.png')
colorTextButton = Button(toolBar, image=colorTextImage, command=color_select)
colorTextButton.grid(row=0, column=5, padx=5)


# Left Align
leftAlignImage = PhotoImage(file='icons/align-left.png')
leftAlignButton = Button(toolBar, image=leftAlignImage, command=align_left)
leftAlignButton.grid(row=0, column=6, padx=5)


# Center Align
centerAlignImage = PhotoImage(file='icons/align-center.png')
centerAlignButton = Button(toolBar, image=centerAlignImage, command=align_center)
centerAlignButton.grid(row=0, column=7, padx=5)


# Right Align
rightAlignImage = PhotoImage(file='icons/align-right.png')
rightAlignButton = Button(toolBar, image=rightAlignImage, command=align_right)
rightAlignButton.grid(row=0, column=8, padx=5)


# ---------- Text Area ----------
scroolbar = Scrollbar(root)
scroolbar.pack(fill=Y, side=RIGHT)

textArea = Text(root, yscrollcommand=scroolbar.set, font=('arial', 10), undo=True)
textArea.pack(fill=BOTH, expand=True)

scroolbar.config(command=textArea.yview)


# ---------- Bindings ----------
root.bind("<Control-o>", open_file)
root.bind("<Control-n>", new_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-Alt-s>", save_as_file)
root.bind("<Control-p>", print_file)
root.bind("<Control-q>", exit_file)

fontFamilyCombobox.bind('<<ComboboxSelected>>', font_style)
fontSizeCombobox.bind('<<ComboboxSelected>>', font_size)

textArea.bind("<<Modified>>", status_bar_function)

root.mainloop()
