def check_perfect_number(checknumber):
    c = []
    if checknumber == 0 or checknumber == 1 or checknumber == 2:
        return False
    for x  in range(1,int(checknumber/2)):
        if checknumber%x == 0:
            c.append(x)
    sums = sum(c)
    if sums == int(checknumber):
        return True
    else:
        return False
    
def get_perfect_number(initial:int,final:int) ->int:
    if initial == 0 or final == 1:
        initial = 2
    b=""
    c=[]
    for x in range(int(initial),int(final)):
        for i in range(1,x):
            if x%i == 0:
                b = b + "+" + str(i)
        sums = eval(b)
        if sums == x:
            c.append(str(x))
        b = ""
    return c
