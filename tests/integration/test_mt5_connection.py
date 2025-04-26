import MetaTrader5 as mt5
import time
import sys

print('Testing MT5 initialization...')

success = False
for attempt in range(12):
    if mt5.initialize():
        print('MT5 initialized successfully')
        mt5.shutdown()
        success = True
        break
    else:
        print(f'Attempt {attempt+1}: Not ready yet, sleeping...')
        time.sleep(5)

if not success:
    print('Failed to initialize MT5 after waiting.')
    sys.exit(1)