import matplotlib.pyplot as plt
import os

project_path = os.path.dirname(__file__)
def compute_limit(data_list):
    """
    Remove None type's data and return correct limit

    Parameters:
        - data_list (list): streams data, but only one in ten.

    Returns:
        - limit (float): The biggest number in data_list * 1.1

    Raises:
        - AttributeError
        - KeyError

    A really simple function. Really!

    >>> data_list = requests_data["time"]
    >>> compute_limit(data_list)

    """
    try:
        limit = max(data_list)
        return limit
    except:
        for x in range(0,len(data_list)):
            if data_list[x] == None:
                data_list[x] = -10
        return max(data_list)

def draw_pic(X,Y1,Y2,Xlim,Ylim1,Ylim2,xlable,Y1lable,Y2lable,position,figure,IO_door):
    """
    Draw a picture according to the parameters.

    Parameters:
        - X (list): X-axis data list
        - Y1 (list): Left Y-axis data list
        - Y2 (list): Right Y-axis data list
        - Xlim (float): limit of X-axis
        - Ylim1 (float): limit of left Y-axis
        - Ylim2 (float): limit of right Y-axis
        - xlable (str): name of X-axis
        - Y1lable (str): name of left Y-axis
        - Y2lable (str): name of right Y-axis
        - position (int): total row + picture's column + NO.  Ex.321
        - figure (object): a object from  plt.figure()
        - IO_door (str): represent data is indoor or outdoor

    Returns:
        - Void

    Raises:
        - AttributeError
        - KeyError

    A really simple function. Really!

    >>> X = plot_data_list["time"]
    >>> Y1 = plot_data_list["heartrate"]
    >>> Y2 = plot_data_list["altitude"]
    >>> xlim = compute_limit(X)
    >>> Y1lim = compute_limit(Y1)
    >>> Y2lim = compute_limit(Y2)
    >>> figure1 = plt.figure(1,figsize=[20,10])
    >>> IO_door = "indoor"
    >>> draw_pic(X,Y1,Y2,xlim,Y1lim,Y2lim,"Time(sec)","Heartrate(bpm)","Altitude(m)",311,figure1,IO_door)


    """
    picture = figure.add_subplot(position)
    picture.plot(X, Y1)
    picture.set_xlabel(xlable)
    picture.set_ylabel(Y1lable)
    #picture.legend(loc='upper right')
    if Xlim > 0:
        picture.set_xlim(0, Xlim)
    else:
        picture.set_xlim(0, 5)
    if Ylim1 > 0:
        picture.set_ylim(0, Ylim1)
    else:
        picture.set_ylim(0, 5)
    if IO_door == "outdoor":
        ax2 = picture.twinx()
        ax2.fill_between(X, 0, Y2, color='c', alpha= 0.5)
        ax2.set_ylabel(Y2lable)
        if Xlim > 0:
            ax2.set_xlim(0, Xlim)
        else:
            ax2.set_xlim(0, 5)
        if Ylim2 > 0:
            ax2.set_ylim(0, Ylim2)
        else:
            ax2.set_ylim(0, 5)

    return figure