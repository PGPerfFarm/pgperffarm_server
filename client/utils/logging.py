import sys
import time


def log(message):
    ''

    print ('%(date)s	%(message)s' % {
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'message': message})

    sys.stdout.flush()
