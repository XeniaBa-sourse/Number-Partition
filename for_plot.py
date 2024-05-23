from data import my_data
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from factorization import print_factorization


def for_table(n1, n2=None):
    if n2 == None:
        data = my_data(num1=n1)
        d = data.loc[data['Натуральное число n'] == n1]
        #print(d.to_numpy())
        matching_row = [(x[0],)+tuple(x[2:]) for x in d.to_numpy()]
    else:
        matching_row = []
        data = my_data(num1=n1, num2=n2)
        d = data[(data['Натуральное число n'] >= n1) & (data['Натуральное число n'] <= n2) & (data['Самоассоциированные разбиения'] ==  1)]
        for idx, row in d.iterrows():
            val = print_factorization(int(row['Частное степени разбиения']))
            #print(row)
            matching_row.append((row[0],)+tuple(row[2:-2]) + (val,))
    return matching_row

def get_column_values(tree, col):
    values = []
    for child in tree.get_children():
        values.append(tree.item(child, 'values')[col])
    return values


def for_plots(tree, num_col_x, num_col_y, y_label, title,  root):
    x = get_column_values(tree, num_col_x)
    x = [int(i) for i in x]

    y = get_column_values(tree, num_col_y)
    y = [int(i) for i in y]

    x_y = list(zip(x, y))
    counter = Counter([item[1] for item in x_y])
    y_set = []
    how_much_y = []

    for key, values in counter.items():
        if values >= 1:
            y_set.append(key)
            how_much_y.append(values)

    fig, ax = plt.subplots()
    ax.scatter(y_set, how_much_y)
    ax.set_xlabel('Кол-во разбиений', fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_title(title,  fontsize=12)

    ax.yaxis.grid(True)
    ax.xaxis.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    return canvas_widget

def for_asociated_part(n1, n2, root):
    data = my_data(num1=n1, num2=n2)
    x = [i for i in range(int(n1), int(n2) + 1)]
    y = [len(data[(data['Натуральное число n'] == i) & data['Самоассоциированные разбиения'] == 1]) for i in x]
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_xlabel('Натурльное число n', fontsize=12)
    ax.set_ylabel('Кол-во самоассоциированных разбиений', fontsize=12)
    ax.set_title('Cмоассоциированные разбиения', fontsize=12)
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    return canvas_widget

#print(for_table(3, 5))
