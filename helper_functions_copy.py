# Contains helper functions for your apps!
from os import listdir, remove
import os.path
import os
# If the io following files are in the current directory, remove them!
# 1. 'currency_pair.txt'
# 2. 'currency_pair_history.csv'
# 3. 'trade_order.p'

def check_for_and_del_io_files(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        print("pass")
if __name__ == '__main__':
 check_for_and_del_io_files('currency_pair.txt')
 check_for_and_del_io_files('currency_pair_history.csv')
 check_for_and_del_io_files('trade_order.p')

 #pass # nothing gets returned by this function, so end it with 'pass'.


