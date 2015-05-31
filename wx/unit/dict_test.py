
def dict_test():
    dict = {}
    try:
        key = dict['key']
        if key is None:
            print 'dict not find key'
        else:
            print 'dict exist'
    except KeyError:
        print 'dict not find key'
    else:
        print 'dict exist key'

    print type(dict)

if __name__ == '__main__':
    dict_test()

