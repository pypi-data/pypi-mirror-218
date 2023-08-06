
import os
import threading
from fyerstest.data_ws import FyersDataSocket
import time
import cProfile
import psutil

# Specify your access token
def dataSocket():
    access_token = "XC4EOD67IM-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2ODg3MDM1NTEsImV4cCI6MTY4ODc3NjIxMSwibmJmIjoxNjg4NzAzNTUxLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCa3A1SV9hRzdxTWxCSUZzWVkyVWVRWVNNZU8wRlJjcENYcE9ZQVo5aVJjSDRhSXlFMWl0R0Jma1ZhS1BPU1FCQjYtQzFMcW5odEtNRW56X3RNS3BnSlRMQVZrTS1XcXdET0RtQXFxVHdfUnBJYmpjTT0iLCJkaXNwbGF5X25hbWUiOiJWSU5BWSBLVU1BUiBNQVVSWUEiLCJvbXMiOiJLMSIsImZ5X2lkIjoiWFYyMDk4NiIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.kLZ6YLFKAZo1SjPDG_xGtpPT1rOLJKDakr4FlG6IMCs"

    # Specify the data type and symbols you want to subscribe to
    data_type = "SymbolUpdate"

    # Create an instance of FyersDataSocket
    fyData = FyersDataSocket(access_token=access_token, log_path=None, litemode=False)


    # Subscribe to the specified symbols and data type
    symbols = ['NSE:NIFTY50-INDEX']#, "NSE:HDFC-EQ",'NSE:ICICIFIN-EQ','NSE:PRECAM-EQ','NSE:IIFLSEC-EQ','NSE:TRIVENI-EQ','NSE:KOTAKSILVE-EQ','NSE:AIAENG-EQ','NSE:EKC-EQ','NSE:VIMTALABS-EQ','NSE:NAHARINDUS-EQ','NSE:ORIENTABRA-EQ','NSE:QUICKHEAL-EQ','NSE:REPRO-EQ','NSE:HARRMALAYA-EQ','NSE:EBBETF0433-EQ','NSE:ICICI10GS-EQ','NSE:PVRINOX-EQ','NSE:GALAXYSURF-EQ','NSE:CELEBRITY-EQ','NSE:NITINSPIN-EQ','NSE:ROHLTD-EQ','NSE:ENIL-EQ','NSE:GSPL-EQ','NSE:ICICICOMMO-EQ','NSE:JAGRAN-EQ','NSE:SULA-EQ','NSE:GVKPIL-EQ','NSE:SAKUMA-EQ','NSE:KEC-EQ','NSE:HCL-INSYS-EQ','NSE:JKCEMENT-EQ','NSE:LANDMARK-EQ','NSE:MARINE-EQ','NSE:M&MFIN-EQ','NSE:AHL-EQ','NSE:BLKASHYAP-EQ','NSE:HDFC-EQ','NSE:NITCO-EQ','NSE:CENTURYPLY-EQ','NSE:KEI-EQ','NSE:HDFCBANK-EQ','NSE:SOLARINDS-EQ','NSE:GALLANTT-EQ','NSE:MALUPAPER-EQ','NSE:KFINTECH-EQ','NSE:HEG-EQ','NSE:SGL-EQ','NSE:UTTAMSUGAR-EQ','NSE:SDBL-EQ','NSE:KKCL-EQ','NSE:BHAGERIA-EQ','NSE:SUNTV-EQ','NSE:GPIL-EQ','NSE:RSYSTEMS-EQ','NSE:EMKAY-EQ','NSE:ELIN-EQ','NSE:KELLTONTEC-EQ','NSE:LOKESHMACH-EQ','NSE:BALPHARMA-EQ']
    # symbols = ['NSE:NIFTY50-INDEX']
    print(len(symbols))
    fyData.subscribe(symbols=symbols, data_type=data_type)
    time.sleep(6)
    symbols = ['NSE:SBIN-EQ','NSE:ADANIENT-EQ']
    fyData.subscribe(symbols=symbols, data_type="DepthUpdate")

if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    pid = os.getpid()

    # Call the function you want to profile
    dataSocket()
    while True:
        # Retrieve the current CPU utilization as a percentage
        cpu_percent = psutil.cpu_percent(interval=1)
        # memory_usage = psutil.virtual_memory().used / (1024 * 1024)
        process = psutil.Process(pid)
        memory_info = process.memory_info()
        memory_usage = memory_info.rss / (1024 * 1024)
        print('\n')

        # Print or store the CPU utilization as desired
        print(f"CPU Utilization: {cpu_percent}%")
        print(f"Memory Usage: {memory_usage:.2f} MB")
        print('\n')

    # profiler.disable()
    # profiler.print_stats(sort='cumtime')










# globals_dict = globals()
# locals_dict = locals()

# cProfile.runctx('dataSocket()', globals_dict, locals_dict)

#     # 

# Unsubscribe from the specified symbols and data type
# time.sleep(6)
# symbols = ["NSE:NIFTY50-INDEX"]
# fyData.unsubscribe(symbols=symbols, data_type=data_type)

# time.sleep(6)
# symbols = ['NSE:SBIN-EQ','NSE:ADANIENT-EQ']
# fyData.subscribe(symbols=symbols, data_type="DepthUpdate")

# # Keep the socket running to receive real-time data
# fyData.keep_running()

