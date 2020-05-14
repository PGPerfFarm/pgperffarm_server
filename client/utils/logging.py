import sys
import time


def log(message):
    ''

    print ('%(epoch)s	%(date)s	%(message)s' % {
        'epoch': time.time(),
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'message': message})

    sys.stdout.flush()
