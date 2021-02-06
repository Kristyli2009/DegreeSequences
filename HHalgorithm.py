#!usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import matplotlib.backends.backend_pdf


def choice_file_screen():
    choice = input("Please enter 1 for the input from a file or 2 for the input from the screen: ")
    if choice == '1':
        data = input_data_from_file()
    elif choice == '2':
        data = input_data_from_screen()
    else:
        print('Invalid input!')
        return False
    return data


def input_data_from_file():
    """read data from a file and store them in a list and return it"""
    numbers = []
    data_file = input("Please enter the file name with extension: ")
    with open(data_file) as file:
        for line in file:
            if line.strip().isnumeric():
                numbers.append(line.strip())
            else:
                print("Invalid input!")
                return False
    return numbers


def input_data_from_screen():
    """ input data from the keyboard and into a list and then return it"""
    txt = input("Please enter the number of vertices and followed by the degree sequence in non-increasing order: ")
    numbers = txt.strip().split()
    return numbers


def convert_str_to_int(numbers):
    d_seq = []
    for i in range(len(numbers)-1):
        if numbers[i+1].isnumeric():
            d_seq.append(int(numbers[i+1]))
        else:
            print("Invalid input!")
            return False

    return d_seq


def is_valid_input(numbers):
    if numbers[0].isnumeric():
        length = int(numbers[0])
        d_seq = convert_str_to_int(numbers)
    else:
        print('Invalid input!')
        return False
    return length, d_seq


def max_hh(array):
    max_n = max(array)
    pivot = array.index(max_n)
    return max_n, pivot


def min_hh(array):
    while array[-1] == 0:
        array = array[:-1]
    arr1 = sorted(array)
    min_n = min(arr1)
    i = 0
    while min_n == 0:
        min_n = arr1[i]
        i += 1
    pivot = len(array) - array[::-1].index(min_n) - 1
    return min_n, pivot


def ur_hh(index_arr, array):
    pivot = random.choice(index_arr)
    degree = array[pivot]
    return degree, pivot


def pr_hh(index_arr, array2, array, x_value):
    prob_arr = probility_array(array2, x_value)
    pivot_list = random.choices(index_arr, cum_weights=prob_arr, k=1)
    pivot = pivot_list[0]
    degree = array[pivot]
    return degree, pivot


def parr_hh(index_arr, array2, array, x_value):
    prob_arr = probility_array(array2, x_value)
    pivot_list = random.choices(index_arr, cum_weights=prob_arr, k=1)
    pivot = pivot_list[0]
    degree = array[pivot]
    return degree, pivot


def probility_array(array2, x_value):
    pro_arr = []
    total = 0
    try:
        for i in range(len(array2)):
            total += math.pow(array2[i], x_value)
    except ZeroDivisionError:
        print("ZeroDivisionError, please use MIN-HH algorithm!")

    try:
        for i in range(len(array2)):
            prob = ((math.pow(array2[i], x_value)) / total) * 100
            prob = int(round(prob))
            pro_arr.append(prob)
    except ZeroDivisionError:
        print("ZeroDivisionError, please use MIN-HH algorithm!")

    return pro_arr


def neighbors(graph, array, pivot, degree, pivot_arr):
    i = 1
    new_arr = array.copy()
    while i <= degree:
        k = new_arr.index(max(new_arr))
        graph.add_edge(pivot, k)
        array[k] -= 1
        new_arr[k] = 0
        i += 1
        if array[k] == 0:
            pivot_arr.remove(k)
        elif array[k] < 0:
            return False


def havel_hakimi_alg(graph, array, choice, index_arr, x_value):
    array2 = []
    for i in range(len(array)):
        if array[i] != 0:
            array2.append(array[i])
    if index_arr:
        if choice == 1:
            degree, pivot = max_hh(array)
        elif choice == 2:
            degree, pivot = min_hh(array)
        elif choice == 3:
            degree, pivot = ur_hh(index_arr, array)
        elif choice == 4:
            degree, pivot = pr_hh(index_arr, array2, array, 1)
        else:
            degree, pivot = parr_hh(index_arr, array2, array, x_value)

        array[pivot] = 0
        neighbors(graph, array, pivot, degree, index_arr)
        index_arr.remove(pivot)
        havel_hakimi_alg(graph, array, choice, index_arr, x_value)


def label_graph_title(choice, x_value):
    if choice == 1:
        plt.title("This graph is constructed by MAX-HH algorithm")
    elif choice == 2:
        plt.title("This graph is constructed by MIN-HH algorithm")
    elif choice == 3:
        plt.title("This graph is constructed by UR-HH algorithm")
    elif choice == 4:
        plt.title("This graph is constructed by PR-HH algorithm")
    elif choice == 5:
        plt.title("This graph is constructed by ParR-HH algorithm with X={}".format(x_value))


def draw_the_graph(array, size, choice):
    label = {}
    for i in range(size):
        label[i] = "D{}:{}".format(i + 1, array[i])
    graph = nx.Graph()

    index_arr = [i for i in range(len(array))]
    x_value = 0
    if choice == 5:
        x = input("Please enter a value for X: ")
        x_value = int(x)
    if sum(array) == 0:
        print("Null graph")
        for i in range(len(array)):
            graph.add_node(i)
    else:
        havel_hakimi_alg(graph, array, choice, index_arr, x_value)
    fig = plt.figure()
    label_graph_title(choice, x_value)

    h = nx.relabel_nodes(graph, label)

    nx.draw_circular(h, with_labels=True, node_size=800, node_color='lightblue', font_color='red', font_weight='bold')
    pdf.savefig(fig)
    plt.show()


def is_graphic(array, size, choice):
    if array[0] >= size:
        print(D_seq)
        print("No, this degree sequence D is not graphic.")
        return False
    elif size > len(array):
        print(D_seq)
        print("No, this degree sequence D is not graphic.")
        return False
    elif sum(array) % 2 != 0:
        print(D_seq)
        print("No, this degree sequence D is not graphic.")
        return False
    else:
        return draw_the_graph(array, size, choice)


if __name__ == '__main__':
    pdf = matplotlib.backends.backend_pdf.PdfPages("output3.pdf")

    for i in range(7):
        Data = choice_file_screen()

        n_vertices, D_seq = is_valid_input(Data)

        ch = int(input("""Please enter which the algorithm you would like to use:
                                                1: MAX-HH algorithm
                                                2: MIN-HH algorithm
                                                3: UR-HH algorithm
                                                4: PR-HH algorithm
                                                5: ParR-HH algorithm
                                                """))
        choices = [1, 2, 3, 4, 5]
        if ch not in choices:
            print("Invalid input")
        is_graphic(D_seq, n_vertices, ch)

    pdf.close()
