import MetaTrader5 as mt5
import time
import sys

print('Testing MT5 initialization...')

success = False
for attempt in range(10):
    if mt5.initialize(login=int(os.getenv('MT5_LOGIN')),
                        password=os.getenv('MT5_PASSWORD'),
                        server=os.getenv('MT5_SERVER'),
                        path=os.getenv('MT5_PATH')):
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