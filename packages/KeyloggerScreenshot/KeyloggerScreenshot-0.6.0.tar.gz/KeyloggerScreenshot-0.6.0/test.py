import sys
import time

while True:
    full_name = str(sys.argv[0])
    get_name = full_name.split("\\")[-1]

    print(get_name)
    time.sleep(1)
