__author__ = 'Matthew'
import numpy as np
import matplotlib.pyplot as plt


def moving_average(interval, window_size):
    interval = np.asarray(interval)
    interval = interval[:,0]
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


def plot_evolution(action_history, fig_num=1, subplot_num=121):

    # plot configuration
    fig = plt.figure(fig_num)
    plot = fig.add_subplot(subplot_num)
    plot.plot(moving_average(action_history, 1), '.')
    plt.ion()
    plt.show()
    plt.title("Action vs Time")
    plt.xlabel("Time Step")
    plt.ylabel("M(t)")

    return plot

def plot_model(Expert, x_idx=1, y_idx=0, fig_num=1, subplot_num=122):

    # plot configuration
    fig = plt.figure(fig_num)
    plot = fig.add_subplot(subplot_num)
    plt.ion()
    plt.show()
    plt.hold(True)
    plt.title("Prediction Models")
    plt.xlabel("M(t)")
    plt.ylabel("S(t+1)")

    # this is leaf node
    if Expert.left is None and Expert.right is None:


        # plot the exemplars in the training set
        training_data = list(zip(*Expert.training_data))
        training_label = list(zip(*Expert.training_label))
        X = training_data[x_idx]
        Y = training_label[y_idx]
        plot.plot(X, Y, ".")

        # plot the model
        pts = list(np.arange(round(min(X)), round(max(X)), 0.1))
        try:
            plot.plot(pts, Expert.predict_model.predict(list(zip(*[pts, pts]))), color="k", linewidth=3)
        except Exception:
            pass

    else:
        plot_model(Expert.left, x_idx, y_idx, fig_num, subplot_num)
        plot_model(Expert.right, x_idx, y_idx, fig_num, subplot_num)

def plot_regional_mean_errors(mean_error_history, fig_num=2, subplot_num=111):
    tree_colours = ['r', 'g', 'b', 'y', 'c', 'm', 'y', 'k']
     # plot configuration
    fig = plt.figure(fig_num)
    plot = fig.add_subplot(subplot_num)
    plt.ion()
    plt.show()
    plt.hold(True)
    plt.title("Mean Error vs Time")
    plt.xlabel("Time Step")
    plt.ylabel("Mean Error")

    max_len = len(mean_error_history[-1])
    for t in range(len(mean_error_history)):
        padding = [None]*(max_len - len(mean_error_history[t]))
        mean_error_history[t] = mean_error_history[t] + padding

    data = zip(*mean_error_history)
    i = 0
    for region in data:
        i += 1
        plot.plot(range(len(region)), region, tree_colours[i%len(tree_colours)]+'.')

    # for t in range(len(mean_error_history)):
    #
    #
    #     plot(t, mean_error_history[t], 'b.')
    #     # for region in range(len(mean_error_history[t])):
    #     #     plot.plot(t,mean_error_history[t][region], tree_colours[region%len(tree_colours)]+'.')
