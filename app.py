from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning
from for_plot import *
from tkinter import filedialog
from openpyxl import Workbook


#Отображение виджетов окна Разбиение одного числа
def for_one_n():
    tree.delete(*tree.get_children())
    shadow_list = [num_a, num1_a, res, tree]
    for i in shadow_list:
        i.place_forget()
    num.place(x=30, y=20, width=125, height=30)
    cmb.place(x=160, y=20, width=155, height=30)
    give_result.place(x=330, y=20, width=225, height=35)
    TableMargin.place(x=10, y=50, width=850, height=500)
    tree.column('#7', stretch=NO, minwidth=0, width=150)
    tree.place(x=10, y=50, width=650, height=500)

#Отображение виджета окна Самоассоциированные разбиения
def for_associated():
    tree.delete(*tree.get_children())
    shadow_list = [num, cmb, give_result, tree]
    for i in shadow_list:
        i.place_forget()
    num_a.place(x=30, y=20, width=125, height=30)
    num1_a.place(x=160, y=20, width=125, height=30)
    res.place(x=330, y=20, width=225, height=35)
    TableMargin.place(x=10, y=50, width=850, height=500)
    tree.column('#7', stretch=NO, minwidth=0, width=0)
    tree.column('#6',stretch=NO, minwidth=0, width=200 )
    tree.place(x=10, y=50, width=650, height=500)

#Сохранние таблицы на диск
def save_treeview_to_excel():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        workbook = Workbook()
        sheet = workbook.active
        columns = ['n', 'part', 'vector', 'rank', 'characteristic', 'degree', 'associated']
        sheet.append(columns)
        for child in tree.get_children():
            values = [value for value in tree.item(child, 'values')]
            sheet.append(values)
        workbook.save(file_path)

#Обработка кнопки РАЗБИЕНИЯ ОДНОГО ЧИСЛА
def check():
    tree.delete(*tree.get_children())
    global num
    numer = num.get()
    if not numer.isdigit():
        num.delete(0, END)
        showwarning(title="Предупреждение", message="Введите натуральное число")
    elif int(numer)>64:
        showwarning(title="Предупреждение", message="Введите натуральное число меньше 64")
    else:
        matching_rows = for_table(int(numer))
        for row_data in matching_rows:
            n, p, v, r, c, degree, a = row_data
            tree.insert('', 0, values=(n, p, v, r, c, degree, a))
        if cmb.get() == 'Ранг':
            plot_widget = for_plots(tree, 0, 3, y_label='Ранг заданного n',title='Распределение рангов', root=root)
            plot_widget.place(x=680, y=30, width=480, height=500)
        elif cmb.get() == 'Частное':
            plot_widget = for_plots(tree, 0, 5, y_label='Частное', title='Частное сепени разбиения',  root=root)
            plot_widget.place(x=680, y=30, width=480, height=500)

#Обработка кнопки САМОАССОЦИРОВАННЫЕ РАЗБИЕНИЯ
def check_a():
    tree.delete(*tree.get_children())
    global num1_a, num_a
    n1, n2 = num_a.get(), num1_a.get()
    if not n1.isdigit() or not n2.isdigit():
        num_a.delete(0, END)
        num1_a.delete(0, END)
        showwarning(title="Предупреждение", message="Введите натуральные числа")
    elif int(n1) >= int(n2):
        num_a.delete(0, END)
        num1_a.delete(0, END)
        showwarning(title="Предупреждение", message="Неверно введенный диапазон")
    elif int(n2)>64 and int(n1)>64:
        showwarning(title="Предупреждение", message="Введите натуральное число меньше 64")
    else:
        matching_rows = for_table(int(n1), int(n2))
        for row_data in matching_rows:
            n, p, v, r, c, degree = row_data
            tree.insert('', 0, values=(n, p, v, r, c, degree))
        plot_widget = for_asociated_part(n1, n2, root=root)
        plot_widget.place(x=700, y=30, width=450, height=500)

def command_exit():
    root.destroy()


#ИНИЦИАЛИЗИРУЕМ ОКНО ПРИЛОЖЕНИЯ
root = Tk()

root.title('Числа, связанные с разбиением')
width = 1180    #задаем ширину окна
height = 600    #задаем высоту окна
screen_width = root.winfo_screenwidth()     #шиниа экрана
screen_height = root.winfo_screenheight()   #высота экрана
#Располагаем окно по центру
x = (screen_width/2)-(width/2)
y = (screen_height/2)-(height/2)
root.geometry('%dx%d+%d+%d'%(width, height, x, y))

#МЕНЮ
root.option_add("*tearOff", FALSE)
mainMenu = Menu(root)
filemenu = Menu()
filemenu.add_command(label='Сохранить таблицу',
                     font=('Times', 14),
                     command=save_treeview_to_excel)
filemenu.add_command(label='Помощь',font=('Times', 14))
filemenu.add_separator()
filemenu.add_command(label='Выход',font=('Times', 14),
                     command=command_exit)

mainMenu.add_cascade(label='Файл', menu=filemenu, font=('Times', 14))
mainMenu.add_cascade(label='Разбиения одного числа', command=for_one_n,
                     font=('Times', 14))
mainMenu.add_cascade(label='Самоассоциированные разбиения', command=for_associated,
                     font=('Times', 14))

#Экран с разбиением одного числа
num = Entry(root, font=('Times', 18))

choice = ['Частное', 'Ранг']
cmb = ttk.Combobox(root,values=choice, width=100, font=('Times', 18))

give_result = Button(root,
                     text='Получить разбиения',
                     command=check,
                     justify='center', font=('Times', 18),
                     width=35, height=110)



#Виджеты для экрана самоассоциированных разбиений
num_a =  Entry(root, font=('Times', 18))
num1_a =  Entry(root, font=('Times', 18))

res =Button(root, text='Получить результаты', command=check_a, justify='center', font=('Times', 18), width=35, height=110)


#Результирующая таблица
style = ttk.Style(root)
style.configure("Treeview.Heading",
                font=('Times', 18))
style.configure('Treeview', rowheight=36, font=('Times', 18))

TableMargin = Frame(root, width=500)

scrollbarx = Scrollbar(TableMargin,orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin,orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=('n','part', 'vector','rang', 'characteristic', 'degree', 'associated','factor'),
                    height=20, selectmode='extended',
                    yscrollcommand=scrollbary.set,
                    xscrollcommand=scrollbarx.set)

tree.heading('n', text='Число', anchor=W)
tree.heading('part', text='Разбиение', anchor=W)
tree.heading('vector', text='Вектор', anchor=W)
tree.heading('rang', text='Ранг', anchor=W)
tree.heading('characteristic', text='Характеристика', anchor=W)
tree.heading('degree', text='Частное степени', anchor=W)
tree.heading('associated', text='Самоассоциированное', anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=50)
tree.column('#2', stretch=NO, minwidth=0, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=80)
tree.column('#4', stretch=NO, minwidth=0, width=50)
tree.column('#5', stretch=NO, minwidth=0, width=100)
tree.column('#6', stretch=NO, minwidth=0, width=100)
tree.column('#7', stretch=NO, minwidth=0, width=150)

root.config(menu=mainMenu)
root.protocol("WM_DELETE_WINDOW", root.destroy)
root.mainloop()

