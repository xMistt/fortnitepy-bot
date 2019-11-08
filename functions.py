import sys
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() 
def y_n(prompt):
    wan = input(prompt)
    put = wan.lower()
    while put not in ("n", "y"):
        print("ERROR Invalid input!, please enter Y or N")
        put = input("Y/N ")
    if put == "y":
        return True
    if put == "n":
        return False