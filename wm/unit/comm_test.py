import time
import datetime 

def time_test():
    ts = time.time()
    print int(ts)

def hour_test():
    curr = datetime.datetime.now()
    print curr
    print curr.hour

def day_test():
    print datetime.date.today()

def set_test():
    k_set = {'id': 'set_id', 'menu': 'set_menu'}
    if 'id' not in k_set or 'menu' not in k_set:
        print 'error'
    else:
        print 'ok'

    print type(k_set)

def type_test():
    t_set = {}
    t_s = 'a'
    print type(t_set)
    print type(t_s)

def arr_test():
    l = [1,2,3,4,5,6,7,8,9,10,11]
    l_len = len(l)
    l = l[(l_len - 10) : l_len]
    print l

    map = {'menu': 'sage:asg'}
    print map['menu'].split(':')[0]

def week_test():
    print datetime.date.today().weekday() 
    print datetime.date.today().isoweekday() 

def repeat_test():
    arr = [1, 2, 3, 4, 4, 5, 6, 7, 7, 8, 9, 11, 11]
    b = set(arr)
    print b
    print list(b)
    print [i for i in b]

def ref_test():
    a = {'1':1, '2':2}
    print 'a:',a
    b = a
    b['3'] = 3
    print 'a&b:',a,b

def arrdel_test():
    a = [1, 2, 3, 4, 5, 6]
    b = [2, 5]
    ok = []
    for i in a:
        find = False
        for j in b:
            if i == j:
                find = True
        if find is False:
            ok.append(i)
        a = ok
    print 'a=',a,'\nb=',b,'\nok=',ok

def func(a=None, b=None, c=None):
    a.append(b)
    c['c'] += 1

def func_test():
    a = []
    b = [1, 2, 3, 4, 5, 6]
    c = {'c': 0} 
    for i in b:
        func(a, i, c)
    print a,b,c

if __name__ == '__main__':
    #time_test()
    #day_test()
    hour_test()
    #set_test()
    #type_test()
    #week_test()
    #arr_test()
    #repeat_test()
    #ref_test()
    #arrdel_test()
    #func_test()

