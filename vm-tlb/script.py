import os
import matplotlib.pyplot as plt

NUM_TRIALS = 4000
PAGE_NUM_EXP_LIMIT = 10
TLB_RUNTIME = "tlb"

def run_tlb():
    with open("output.txt", "w") as file:
        for exp in range(0, PAGE_NUM_EXP_LIMIT+1):
            PAGE_NUM = 2**exp
            command = f"./{TLB_RUNTIME} {PAGE_NUM} {NUM_TRIALS} >> output.txt"
            os.system(command)

def generate_graph():

    # Read the file and extract values
    x_values = []
    y_values = []

    with open("output.txt", "r") as file:
        for line in file:
            value = float(line.strip())
            y_values.append(value)
            x_values.append(2 ** (len(y_values)-1))

    # Plot the scatter plot
    plt.scatter(x_values, y_values)
    plt.xscale('log')
    plt.xlabel("Number of Pages")
    plt.ylabel("Time Per Access(ns)")
    plt.title("TLB Size Measurement")
    # plt.show()
    plt.savefig("fig")


if __name__ == '__main__':
    run_tlb()
    generate_graph()