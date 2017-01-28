DEV_URL = 'https://mailassist.herokuapp.com/'
PROD_URL = 'http://192.168.1.41:8000/'
DEV = True
NOTIFICATION_MSG='notification message'
def redirectHelper():
    global DEV_URL
    global PROD_URL
    global DEV
    if DEV:
        return DEV_URL
    return PROD_URL