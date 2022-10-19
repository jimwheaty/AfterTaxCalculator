import matplotlib.pyplot as plt
import numpy as np
from money import calculator

def plot_lines(x, y1, y2, y3, z1, z2, z3, plot_title='Plot Title', label_x='Label X Axis', label_y='Label Y Axis', label1='Label Y1', label2='Label Y2', label3='Label Y3'):
    plt.plot(x, y1, label=label1, color='blue')
    plt.plot(x, y2, label=label2, color='red')
    plt.plot(x, y3, label=label3, color='green')
    plt.plot(x, z1, label=label1, color='blue', ls='--')
    plt.plot(x, z2, label=label2, color='red', ls='--')
    plt.plot(x, z3, label=label3, color='green', ls='--')
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.legend()
    plt.savefig('plot.png', dpi=300)
    plt.show()

def main():
    x_axis = [i for i in range(20000,100000,1000)]
    y_1 = [calculator(x, 'employee')[6] for x in x_axis]
    y_2 = [calculator(x, 'freelancer')[6] for x in x_axis]
    y_3 = [calculator(x, 'company')[6] for x in x_axis]

    z_1 = [calculator(x, 'employee')[8] for x in x_axis]
    z_2 = [calculator(x, 'freelancer')[8] for x in x_axis]
    z_3 = [calculator(x, 'company')[8] for x in x_axis]
    plot_lines(x_axis, y_1, y_2, y_3, z_1, z_2, z_3, plot_title='Σύγκριση εισοδημάτων', label_x='Μεικτό ετήσιο εισόδημα', label_y='Καθαρό ετήσιο εισόδημα', label1='Υπάλληλος', label2='Ελεύθερος επαγγελματίας', label3='Εταιρία')

main()