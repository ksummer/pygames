choice = input("Would you like the string printed vertically or horizontally?:\n")
flag = 0
while flag == 0:
    if choice == "horizontally":
        print("Hello World!")
        flag = 1
    else:
        if choice == "vertically":
            print("""H
E
L
L
O

W
O
R
L
D""")
            flag = 1
        else:
            print("Choice not valid. Please type either 'horizonally' or 'veritcally'.")
            choice = input("Would you like the string printed vertically or horizontally?:\n")
input("\nPress Enter to exit")
