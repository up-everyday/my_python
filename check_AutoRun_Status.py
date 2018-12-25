import os
import sys
import time
if __name__ == '__main__':
    while(1):
        print("sys.argv is ",sys.argv )
        if len(sys.argv) != 3:
                print("Auto_complete_check shoud have 3 parameters")
                exit(-1)
        else:
            print("####check AutoRun finished or not")
            proc_flag = False
            proc_flag = False
            log_name = sys.argv[2]
            with open(log_name, 'rt') as f:
                for line in f :
                    if "Complete to run the selected cases, please check" in line:
                        print("from log, AutoRun finished.")
                        log_flag = True
                    else:
                        print("AutoRun is running")
            query_cmd = "ps -ef|grep " + sys.argv[1]
            output = os.popen(query_cmd)
            for line in output:
                #print("line is ", line)
                hostname = sys.argv[1]
                proc_str = '{}/AutoRun_beta20180824'.format(hostname)
                if proc_str in line:
                    print("from proc,AutoRun Finished")
                    proc_flag = True
            if log_flag and proc_flag:
                break
            else:
                print("sleep 5")
                time.sleep(5)
