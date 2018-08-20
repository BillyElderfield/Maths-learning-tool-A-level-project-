import tkinter as tk
import base64
from urllib.request import urlopen


# this is needed for when the bytes(msgr) decides to throw a bunch of slashes in the string when it is converted back
# so I made this because when ast.literal_eval(msgr) was run the slashes cause syntax errors and would crash the program.
def remove_slash(li):
    count = 0
    for i in li:
        # if character is a slash: remove it and run remove_slash() again on the new string.
        if i == "\\":
            li = li[:count]+li[count+1:]
            # if there are no more slashes in the string, then return it.
            if "\\" not in li:
                return li
            li = remove_slash(li)
            return li
        count += 1


# str(bytes("f")) returns things in the form b'f', but i want just f so I can manipulate the data easily.
def bytetostr(byte):
    byte = str(byte)
    return byte[2:-1]


# For my time taken: label widgets The time needs to be in the form minute:seconds, 00:00.
def time_format(time):
    # if the time is less than 10 minutes add a 0 at the beginning
    if (time // 60) == 0 or (time // 60) // 10 == 0:
        minutes = "0" + str((time // 60))
    else:
        minutes = str(time // 60)
    # if remaining seconds are less than 10 then add a 0 at the begining
    if (time % 60) == 0 or (time % 60) // 10 == 0:
        seconds = "0" + str(time % 60)
    else:
        seconds = str(time % 60)
    return minutes, seconds

# format the first name and second name that a user input for registration from the form before sending it off to the
# database server.
def name_format(first, second):
    return first[0].upper() + first[1:].lower() + " " + second[0].upper() + second[1:].lower()


# Grab a specific user's profile picture from the profile picture website, then format it into something tkinter can
# handle, then finally set a tk.PhotoImage object with the desired profile picture ready to be put into a tkinter label
def set_profile_pic(user_id):
    image_byt = urlopen("http://spackwell.hol.es/billymaths/profile_pics/" + str(user_id) + ".png").read()
    image_b64 = base64.encodebytes(image_byt)
    return tk.PhotoImage(data=image_b64)


# Used to sort tree view data. Sort every column by the specified column, then have the correlating data sorted as well
# by linking the sorted column to the data it's associated with using its unique result_id.
def sort_table_data(data, sortby, mode):
    data2 = []
    data2str = []
    data3 = []
    if mode == "worksheet":
        # handle stings
        if sortby in [0, 1, 5]:
            for i in data:
                # for each row in the column add just the data that needs to be sorted into a new list with the unique
                # result_id of each row and with the length of the added result_id
                data2.append(str(i[sortby])+str(i[6])+str(len(str(i[6]))+1))
        # handle numbers
        else:
            for i in data:
                # for each row in the column add just the data that needs to be sorted into a new list with the unique
                # result_id of each row and with the length of the added result_id
                data2.append(float(str(float(i[sortby]))+str(i[6])+str(len(str(i[6]))+1)))
    elif mode == "duel":
        for i in data:
            # for each row in the column add just the data that needs to be sorted into a new list with the unique
            # result_id of each row and with the length of the added result_id
            data2.append(str(i[sortby])+str(i[6])+str(len(str(i[6]))+1))
    # sort the data in this new list (the added result_id and length value added at the end of each value in data2
    # should not effect the way in which the data is sorted)
    data2 = quick_sort(data2)
    for i in data2:
        # puts all sorted data into a string data type so that they can be spliced
        data2str.append(str(i))
    # go through each peice of sorted data in sting form
    for x in data2str:
        # for each piece of data in the sorted data loop through the whole of the original data
        for y in data:
            # if the result_id of the data in the sorted list of string is the same as the result_id of the data in the
            # original list then append the data from the original list to the final list of sorted whole rows.
            if x[-int(x[-1]):-1] == str(y[6]):
                data3.append(y)
                break
    # once the data is in fully sorted rows in relation to the column specified by orderby if the data is the same as
    # the original data input into the function, then completely reverse the list because that means a column must have
    # been clicked twice
    if data3 == data:
        data3.reverse()
    return data3


# sorts a list alphabetically in descending order.
def quick_sort(data):
    data = [data]
    while True:
        complete = True
        temp_data = []
        for i in data:
            if len(i) > 1:
                left, pivot, right = sort(i)
                if len(left) != 0:
                    temp_data.append(left)
                temp_data.append(pivot)
                if len(right) != 0:
                    temp_data.append(right)
                complete = False
            else:
                temp_data.append(i)
        data = temp_data
        if complete:
            break
    sorted_data = []
    for i in data:
        if len(i) != 0:
            sorted_data.append(i[0])
    return sorted_data


def sort(li):
    left = []
    right = []
    pivot = li[int((len(li)/2)-1)]
    del li[int((len(li)/2)-1)]
    for i in li:
        if i <= pivot:
            left.append(i)
        elif i > pivot:
            right.append(i)
    return left, [pivot], right


# return the highest common factor of 3 numbers
def hcf(x, y, z):
    # if no hcf is found, then 1 will be returned
    highest_common_factor = 1
    if x > y and x > z:
        smallest = x
    elif y > x and y > z:
        smallest = y
    else:
        smallest = z
    for i in range(1, smallest + 1):
        # if a new highest factor is found, store it.
        if (x % i == 0) and (y % i == 0) and (z % i == 0):
            highest_common_factor = i
    return highest_common_factor


# get a list of factor pairs from an integer.
def get_factors(number):
    factors = []
    same = False
    for x in range(int(number)):
        for y in range(number + 1):
            # after x == y duplicate pairs will start to be made, so stop appending pairs after x == y
            if not same:
                if x * y == number:
                    factors.append((x, y))
                    if x == y:
                        same = True
    return factors
