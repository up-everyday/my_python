
import os
import re
import time
import shutil
import configparser
import threading
from tkinter import *
from ftplib import FTP
from tkinter.filedialog import *
from tkinter import messagebox as msgbox



#from pyh import *
#import zipfile

#from bs4 import BeautifulSoup

ftp_servie = "135.242.16.160"
dataview_list = ['data_request', 'request_data', 'ref_buck', 'req_token','sub_data', 'req_audit', 'Hier_Req', 'sub_debit',
                 'sub_debit_amt', 'req_idx', 'sub_credit', 'feat_pack', 'get_sub_info', 'adjust_balance',
                 'ref_buck', 'req_bundle', 'auth_sub', 'req_counter', 'sc_recharge',  'cc_recharge', 'request_bal',]

#ftp上所有feature list，如果有增加，那修改这个list。
success_feature_list = ["123123", "123456", "1234567", "55555", "72624", "729263", "731590", "731658", "732478", "732534", "732673", "732784",
                        "732998",	"74335", "75091", "75891", "76543", "76955", "77003", "77003porting", "77004", "77135", "77136", "77158",
                        "77228", "77265", "77269", "77301", "77310", "77314", "77324", "77339", "77351", "77359", "77372", "77375", "77383",
                        "77439", "77451", "77461", "77487", "77488", "77499", "77514", "77579", "77581", "77588", "77592", "77595", "77601",
                        "77615", "77616", "77617", "77617porting", "77619", "77631", "77635", "77662", "77663", "77669", "77675", "77685",
                        "77689", "77701", "77730", "77737", "77738", "77739", "77741", "77759", "77765", "77777", "77792", "77799", "77800",
                        "77801", "77802", "77834", "77835", "77840", "77842", "77853", "77858", "77859", "77860", "77862", "77863", "77864",
                        "77864porting", "77865", "77866", "77872", "77873", "77874", "77876", "77877", "77881", "77882", "77887", "77896",
                        "77897", "77902", "77932", "77952", "77953", "77957", "77979", "77979porting", "77984", "77989", "77996", "78004",
                        "78008", "78009", "78014", "78015", "78016", "78018", "78019", "78021", "78042", "78052", "78060", "78062", "78067",
                        "78068", "78069", "78072", "78074", "78077", "78080", "78081", "78082", "78089", "78091", "78091porting", "78113",
                        "78117", "78120", "78129", "78145", "78150", "78155", "78156", "78167", "78169", "78170", "78172", "78175", "78178",
                        "78184", "78190", "78192", "78196", "78206", "78221", "78226", "78228", "78229", "78230", "78232", "78240", "78242",
                        "78243", "78244", "78249", "78250", "78253", "78256", "78259", "78260", "78264", "78267", "78268", "78269", "78274",
                        "78282", "78285", "78286", "78287", "78308", "78321", "78330", "78332", "78334", "78335", "78341", "78350", "78363",
                        "800726", "800726porting", "800735", "800782", "800787", "800799", "800807", "800809", "800821", "800830", "800832",
                        "800850", "800859", "800867", "800872", "800878", "800882", "800886", "800900", "800925", "800926", "800963", "88888",
                        "asda-123", "lucylv", "SPID-0", "SPID-101", "SPID-112", "SPID-115", "SPID-116", "SPID-150", "SPID-154", "SPID-155",
                        "SPID-170", "SPID-182", "SPID-183", "SPID-186", "SPID-187", "SPID-189", "SPID-190", "SPID-203", "SPID-213", "SPID-237",
                        "SPID-239", "SPID-241", "SPID-242", "SPID-248", "SPID-25", "SPID-256", "SPID-261", "SPID-262", "SPID-263", "SPID-3",
                        "SPID-31", "SPID-311", "SPID-349", "SPID-75", "SPID-82", "SPID-96", "77159", "77208"]


rtdb_list = ["Counter_RTDB", "GPRSSIM", "XB_RTDB", "SIM_RTDB", "SCR_RTDB","GN_RTDB", "SGL_RTDB",  "RE_RTDB", "RC_NRC_RTDB",
            "UA_RTDB", "SIMSD_RTDB", "SFF_RTDB", "SDD_RTDB",
            "DP_RTDB", "AI_RTDB", "Vortex_RTDB", "MNP_RTDB",  "EZSIM_RTDB",
            "EZSZ_RTDB", "GNMDN_RTDB", "MDNGN_RTDB", "TID_RTDB", "VCCSIM_RTDB", "SUR_RTDB",
            "CDZA_RTDB", "HM_RTDB", "SH_RTDB", "FSN_RTDB", "TOKEN_RTDB", "EZZNB_RTDB", "MDN_RTDB", "CLIINFO_RTDB", "ID2MDN_RTDB",
            "MDNCLI_RTDB", "ROAMER_RTDB", "GTM_RTDB", "PSCRDB", "SLTBL_RTDB", "SY_RTDB",
            "GCUPL", "RCNR_RTDB", "TID_RTDB","GCIPL", "AECI_RTDB", "Prom_Usg_RTDB","Promotion_RTDB","CDB_RTDB"]



#在PC上保存log的位置，可自行修改。
#PC_location = "D:/Program Files/sllunit/pass_log/"
global PC_location
#保存获取的ftp上对应case的log的全名。
failed_cases_list = {}
pass_case_info = {}
find_failed_case_result = {}

global tmp_reasult

global failed_reason
failed_reason = {}

global configure_file_path
configure_file_path = "D:/Program Files/sllunit/pass_log"
#如果在pass log中找到dataview，就置位为True。
# global dataview_flag
# dataview_flag = False

#dft server上pass log存在，但是有可能为0 B，没有内容,例如77730/fr3273.所以需要设置一个flag，如果log内容为0B，就跳过后续步骤。
global log_exist
log_exist = {}
global pass_log_has_read_completed

#result log文件位置。
global result_log
#result_log = "D:/Program Files/sllunit/SurepayDraft_12C/result/test/180122_151637.@dft_server_77324_fn4467.log"
#result_log = "D:/Program Files/sllunit/SurepayDraft_12C/result/180323_114049.@dft_server_run_search_time_20180323114049_time.log"
#result_log = "D:/Program Files/sllunit/pass_log/180322_175652.@dft_server_run_search_time_20180322175652_time.log"

#failed_log_path = "D:/Program Files/sllunit/SurepayDraft_12a/result/ANSI_RTDB_20180309/"

#用于下载对应feature的case，需要提供feature和case号。
def log_download(feature, case):
    global log_exist
    filelist = []
    tmp_path = PC_location  + feature
    if os.path.exists(tmp_path):
        os.chdir(tmp_path)
    else:
        os.makedirs(tmp_path)
        os.chdir(tmp_path)
    try:
        myftp = FTP(ftp_servie)
    except:
        print ("ftp server is wrong")
        exit(-1)
    myftp.login()
    myftp.cwd("DftLog" + "/" + feature)
    tmplist = myftp.nlst()
    #print (tmplist)
    tmp_flag = True
    for i in tmplist:
        if case in i and tmp_flag:
            filelist.append(i)
            tmp_flag = False
        else:
            continue
    if len(filelist) < 1:
        print ("there is no case named " + case)
        exit(-1)
    #print (filelist)
    for i in filelist:
        (name, extension) = os.path.splitext(i)
        if extension == ".log":
            log_file = open(feature + "_" + case + "_passed.log", "wb")
            myftp.retrbinary('RETR %s' %i, log_file.write)
            log_file.close()
            #time.sleep(2)
            break
        elif extension == ".zip":
            zip_file = open(feature + "_" + case + "_passed.zip", "wb")
            myftp.retrbinary('RETR %s' %i, zip_file.write)
            zip_file.close()
            #log_file = open(feature + "_" + case + "_passed.log", "wb")
            #shutil.unpack_archive(feature + "_" + case + "_passed.zip")
            #time.sleep(2)
            break
        else:
            print ("there is no pass log named " + case + "of feature " + feature)
            #exit(-1)

    #[name, extension] = os.path.splitext()
    #log_content = open(feature + "_" + case + "_passed.log", "r")
    if os.path.exists(feature + "_" + case + "_passed.log") and os.path.getsize(feature + "_" + case + "_passed.log"):
        log_exist[feature + "_" + case] = True
    elif os.path.exists(feature + "_" + case + "_passed.zip") and os.path.getsize(feature + "_" + case + "_passed.zip"):
        log_exist[feature + "_" + case] = True
    else:
        log_exist[feature + "_" + case] = False




#测试上面的函数
#log_download('77701', 'fs2657')


def pass_log_src_download():
    for feature in success_feature_list:
        tmp_path = PC_location + feature
        if os.path.exists(tmp_path):
            os.chdir(tmp_path)
        else:
            os.makedirs(tmp_path)
            os.chdir(tmp_path)
        try:
            myftp = FTP(ftp_servie)
        except:
            print("ftp server is wrong")
            exit(-1)
        myftp.login()
        myftp.cwd("DftLog" + "/" + feature)
        tmp_file_list = myftp.nlst()
        for file in tmp_file_list:
            if "ReadMe" in file:
                with open(PC_location +  "all_feature_src_info.txt", "ab") as src_file:
                    tmp_info = bytes("Below src info is about " + feature + "\n", encoding='utf8')
                    src_file.write(tmp_info )
                    # src_file.writelines("\n")
                    myftp.retrbinary('RETR %s' %file, src_file.write)
                    # src_file.writelines("\n")
                    src_file.close()

#这个程序把ftp上的所有feature的src 信息都拷贝下来，不用再去一个个找。只用运行一次就行。
# pass_log_src_download()

def get_failed_case_list(result_path):
    global tmp_reasult
    tmp_reasult = {}
    with open(result_path) as f:
        for line in f.readlines():
            line = eval(line)
            if line['levelname'] == 'ERROR':
                temlist = line['id']
                #print (temlist)
                #print (temlist)
                for feature in success_feature_list:
                    if feature in temlist:
                        #print(feature)
                        #print (temlist)
                        #failed_cases_list[feature] =
                        temcase = (re.search(r'[a-z]{2}\d{4}', temlist).group(0))
                        failed_cases_list[temcase] = feature
                        tmp_reasult[temcase] = feature
                        # if (feature + "_" + temcase) in tmp_reasult:
                        #     tmp_reasult[feature + "_" + temcase] = tmp_reasult[feature + "_" + temcase] + "\n"\
                        #                                            + (str(line["id"].split(".")) + ":"
                        #                                            + line["message"])
                        # else:
                        #     tmp_reasult[feature + "_" + temcase] = str(line["id"].split(".")) + ":"\
                        #                                            + line["message"]
    f.close()


    #print (failed_cases_list)
            #print (line['levelname'])
            #if line["levelname"] == "ERROR":
             #   print (line)

#get_failed_case_list(result_log)


def find_right_case_info(feature, case):
    #global dataview_flag
    #dataview_flag = False
    #start = time.clock()
    global pass_log_has_read_completed
    pass_log_has_read_completed = False
    tmp_path = PC_location  + feature
    #temlist = []
    if not(os.path.exists(tmp_path)):
        print ("the path is wrong!")
        exit(-1)
    os.chdir(tmp_path)
    tmp_flag = True
    tmp_case_info = []
    #tmpa = tmpb = 0
    while tmp_flag:
        for root, dirs, files in os.walk(tmp_path):
            for file in files:
                if case in file:
                    (name, extension) = os.path.splitext(file)
                    if extension == ".log" and tmp_flag:
                        tmp_flag = False
                        with open(file, "r") as f:
                            #length = len(f)
                            for linea in f.readlines():
                                #tmpa = tmpa + 1
                                line = linea[:-5]
                                #print(line)
                                if "TRACE:" in line and "read_completed" in line:
                                    #tmpb = tmpb + 1
                                    for rtdb in rtdb_list:
                                        if (re.search(rtdb, line)) != None:
                                            pass_log_has_read_completed = True
                                            tmp_case_info.append(rtdb + "!read_completed")
                                    for dataview in dataview_list:
                                        #dataview = dataview + "!read_completed"
                                        if (re.search(dataview, line)) != None:
                                        #if temdataview != None:
                                            #name = feature + "_" + case
                                            pass_log_has_read_completed = True
                                            tmp_case_info.append(dataview + "!read_completed")
                                            #tmp_flag = False
                                            #dataview_flag = True

                    elif extension == ".zip":
                        #print (file)
                        shutil.unpack_archive(file)
                        os.remove(file)
                        #os.rename(file, feature + "_" + case + "_passed.log")
                        find_right_case_info(feature, case)
                    else:
                        print ("there is no pass log of " + feature + " " + case + " in the path")
                        break
                        #exit(-1)
    # if not(dataview_flag):
    #     print ("this case " + case + " has no dataview!")
    #     pass_case_info[feature + "_" + case] = None
    # else:
    if pass_log_has_read_completed:
        #print("the env is bad!")
        tmp_case_info = list(set(tmp_case_info))
        pass_case_info[feature + "_" + case] = tmp_case_info
    else:
        pass_case_info[feature + "_" + case] = None
        #tmp_case_info.clear()
        #del failed_cases_list[case]


#find_right_case_info('77701', 'fs2657')




def find_failed_case_info(feature, caseid):
    global failed_reason
    failed_info = []
    file_name = os.path.split(result_log)[-1]
    timestamp = re.search(r'\d{14}', file_name).group(0)
    #global dataview_flag
    # if not (os.path.exists(result_log)):
    #     print ("wrong failed log path!")
    #     exit(-1)
    # if dataview_flag:
    for key, value in pass_case_info.items():
        tmp_flag = len(value)
    parent_path = os.path.dirname(result_log)
    for root, dirs, files in os.walk(parent_path):
        os.chdir(root)
        # print (root)
        for file in files:
            if caseid in file and tmp_flag:
                # print(root + file)
                (name, extension) = os.path.splitext(file)
                (name, extension) = os.path.splitext(name)
                # print (extension)
                if extension == ".debuglog" and timestamp in name:
                    for key, value in pass_case_info.items():
                        #print(value)
                        for i in value:
                            failed_flag = True
                            with open(root + "/" + file, "r") as f:
                                for line in f.readlines():
                                    info_search = i
                                    if "TRACE:" in line and "read_completed" in line:
                                        tmpresult = re.search(info_search, line)
                                        if tmpresult != None:
                                            # print("dataview " + dataview_search + " is OK!")
                                            tmp_flag = tmp_flag - 1
                                            failed_flag = False
                                            break
                                    #elif "TRACE:" in line and "read_received" in line:
                                        # break
                            if failed_flag:
                                (info, read_completed) = i.split("!")
                                tmp = info + " is bad in the log！"
                                failed_info.append(tmp)
                #     # print (file)
                #     shutil.copy(root + "/" + file,
                #                 PC_location + feature + "/" + feature + "_" + caseid + "_failed.log")

        if tmp_flag:
            find_failed_case_result[feature + "_" + caseid] = "the env of " + feature + "_" + caseid + " is bad"
            tmp_flag = False
                #else:
    if len(failed_info) > 1:
        failed_reason[feature + "_" + caseid] = failed_info


def delete_blank(case_list_path):
    file1 = open(case_list_path + "case_env_info_list.txt", "r")
    file2 = open(case_list_path + "case_env_info_list.txt.bak", "w")
    try:
        for line in file1.readlines():
            if line == "\n":
                line = line.strip("\n")
            file2.write(line)
    finally:
        file1.close()
        file2.close()

#delete_blank("D:/Program Files/sllunit/pass_log/")



# def change_path(log_path):
#     log_path = log_path.replace('\', '/')


def read_configration(configure_file_path):
    global result_log
    global PC_location
    conf = configparser.ConfigParser()
    os.chdir(configure_file_path)
    if not (os.path.exists('configuration_file.ini')):
        configuration_file = open('configuration_file.ini', "w")
        conf.read('configuration_file.ini')
        conf.add_section("file_path")
        conf.set("file_path", "log_path", "replace with your log path, such as"
                " D:/Program Files/sllunit/SurepayDraft_BJRMS12B/result/180330_103711.@dft_server_run_search_time_20180330103711_time.log")
        conf.set("file_path", "PC_path", "replace with your PC path"
                 " such as D:/Program Files/sllunit/pass_log/")
        conf.write(open('configuration_file.ini', "w"))
        configuration_file.close()
        msgbox.showerror("ERROR", "Please configure your parameter in configuration_file.ini!")
    else:
        #filename = askopenfile(initialdir="D:/")
        conf.read('configuration_file.ini')
        result_log = conf.get("file_path", "log_path")
        PC_location = conf.get("file_path", "PC_path")

#path = "D:/Program Files/sllunit/pass_log"
#read_configration(path)



def test():
    global result_log
    global PC_location
    global log_exist
    global pass_log_has_read_completed
    start = time.clock()
    #configure_file_path = var1.get()
    #read_configration(file_path)
    # PC_location = var2.get()
    #result_log.replace("\", "/")
    #result_log = result_log
    #    content = {}
    if not (os.path.exists(PC_location + "case_env_info_list.txt")):
        file = open(PC_location + "case_env_info_list.txt", "w")
        file.close()
    get_failed_case_list(result_log)
    feature = ""
    case = ""
    tmp_list = []
    for key in failed_cases_list:
        with open(PC_location + "case_env_info_list.txt", "r") as f:
            for line in f.readlines():
                if key in line:
                    linen = eval(line)
                    if linen[failed_cases_list[key] + "_" + key] == None:
                        tmp_list.append(key)
                        break
                    else:
                        pass_case_info[failed_cases_list[key] + "_" + key] = linen[
                            failed_cases_list[key] + "_" + key]
                        find_failed_case_info(failed_cases_list[key], key)
                        tmp_list.append(key)
                        pass_case_info.clear()
                        break
                # dataview_flag = False
    # for key in pass_case_info:
    #     if pass_case_info[key] == None:
    #         pass_case_info.pop(key)
    if len(tmp_list) > 0:
        for i in range(len(tmp_list)):
            del failed_cases_list[tmp_list[i]]
    if len(failed_cases_list) > 0:
        # tmpa_list = failed_cases_list
        for key in failed_cases_list:
            # print (failed_cases_list)
            threading.Thread(log_download(failed_cases_list[key], key)).start()
            #t.join()
        for key, value in log_exist.items():
            if value:
                [tmpfeature, tmpcase] = key.split("_")
                find_right_case_info(tmpfeature, tmpcase)
                if pass_log_has_read_completed:
                    find_failed_case_info(tmpfeature, tmpcase)
            tmp = str(pass_case_info)
            # if len(tmp) > 15:
            with open(PC_location + "case_env_info_list.txt", "a") as f:
                # content[failed_cases_list[key] + "_" + key] = pass_case_info[failed_cases_list[key] + "_" + key]
                # print (len("!read_completed"))
                # print (tmp)
                pass_case_info.clear()
                f.writelines("\n" + tmp)
                f.close()

    # 生成一个json文件，列出由于env问题fail的case list.
    if len(find_failed_case_result) > 0:
        # file_path = os.path.dirname(result_log)
        file_name = os.path.split(result_log)[-1]
        # file_name = os.path.split(".")[:-2]
        jsonfile = PC_location + file_name + "_env_issue.json"
        with open(jsonfile, "w") as f:
            f.write("[" + "\n")
            for key in find_failed_case_result:
                tmp = str(key)
                [feature, case] = tmp.split("_")
                tmp_reasult.pop(case)
                f.write('"' + feature + "/" + case + '.json",' + "\n")
            f.write('"' + feature + "/" + case + '.json"' + "\n")
            f.write("]")
            f.close()

    # 如果有与env无关的case fail，那么就生成下面的html文件，列出feature caseid和fail的原因。
    if len(tmp_reasult) > 0:
        file_name = os.path.split(result_log)[-1]
        realfailedcase = PC_location + file_name + "_real_failed_case_list.html"
        with open(realfailedcase, "w+") as f:
            f.write("""
                <html lang="en">
                <head>
                  <title>Test</title>
                </head>
                <body>
                <table>
                """)
            f.write("<H1>REPORT for %s</H1>" % result_log)
            for key in tmp_reasult:
                f.write('<tr>')
                f.write('<td bgcolor="ff0000"; style=" width:196px;font-size:30px;">%s</td>' % (
                        str(tmp_reasult[key]) + "_" + key))
                f.write('</tr>')
                f.write('<tr>')
                f.write('<td bgcolor="00FF80"; style=" width:196px;">LEVEL</td>')
                f.write('<td bgcolor="00FF80"; style=" width:196px;">TASK</td>')
                f.write('<td bgcolor="00FF80"; style=" width:196px;">MESSAGE</td>')
                with open(result_log, "r") as l:
                    for line in l.readlines():
                        linen = eval(line)
                        if key in linen["id"] and linen["levelname"] == "ERROR":
                            f.write('<tr>')
                            tmplinea = str(linen["id"])
                            tmplinea = tmplinea.split(".")
                            tmplineb = str(linen["message"])
                            f.write('<td style=" width:196px;background:yellow;">%s</td>' % "ERROR" + os.linesep)
                            f.write('<td style=" width:196px;background:yellow;">%s</td>' % tmplinea[-1] + os.linesep)
                            f.write('<td style=" width:300px;background:yellow;">%s</td>' % tmplineb + os.linesep)
                            f.write('</tr>')
                l.close()
                f.write('</tr>')
            f.write("</table>")
            f.write('</body></html>')
            f.close()
    if len(failed_reason) > 0:
        file_name = os.path.split(result_log)[-1]
        failed_info_file = PC_location + file_name + "_env_failed_info.txt"
        with open(failed_info_file, "w") as file:
            for key in failed_reason:
                tmp_str = str(failed_reason[key])
                file.write(key + "\n")
                file.write(tmp_str + "\n")
            failed_reason.clear()
            file.close()


    # print(time.clock() - start)
    # print("there are %d case failed due to env issue!" % len(find_failed_case_result))
    msgbox.showinfo("Info","time spend is " + str(time.clock() - start) + "秒")
    #msgbox.showinfo("there are %d case failed due to env issue!" % len(find_failed_case_result))
    top.destroy()

def get_pc_path():
    global PC_location
    PC_location = askdirectory()

def get_result_log_path():
    global result_log
    result_log = askopenfilename(filetypes=[('log', '.log')])
    print (result_log)

if __name__ == "__main__":
    global result_log
    global PC_location
    top = Tk()
    # 获取屏幕宽和高。
    width = top.winfo_screenwidth()
    height = top.winfo_screenheight()
    top.title("env_issue")  # 设置窗口标题
    # 设置显示窗口居中。
    top.geometry("%dx%d+%d+%d" %(200, 150, (width - 200)/2, (height - 150)/2))
    label1 = Label(top, text="select your configure file path：")          ##.grid(row=0, column = 1)    #, sticky=W)
    label1.pack()  # row = 1, column = 1)
    var1 = StringVar()
    button1 = Button(top, text="select PC_location", command=get_pc_path)
    button2 = Button(top, text="select result_log", command=get_result_log_path)
    button1.pack()
    button2.pack()
    #entry1 = Entry(top, textvariable=var1)
    # label2 = Label(top, text="PC_location：")###    .grid(row=2, column = 1)    #, sticky=W)
    # label3 = Label(top, text="result_log：")
    # var2 = StringVar()
    # entry2 = Entry(top, textvariable=var2)
    # label2.pack()
    # label3.pack()
    #entry1.pack()   #row = 1, column = 2)
    # label2.pack()   #row = 2, column = 1)
    # entry2.pack()   #row = 2, column = 2)
    # file_path = askopenfilename()
    # file_path = askdirectory(initialdir=configure_file_path)
    # read_configration(file_path)
    button = Button(top, text = "start running", command = test)
    button.pack(side=BOTTOM)   #row = 4, column = 2)
    top.mainloop()

#PC_location = "D:/Program Files/sllunit/pass_log/"
#result_log = "D:/Program Files/sllunit/SurepayDraft_BJRMS12B/result/180402_173521.@dft_server_run_search_time_20180402173521_time.log"
#result_log = "D:/Program Files/sllunit/SurepayDraft_12a/result/180329_182950.@dft_server_run_search_time_20180329094133_time.log"
#result_log = "D:/Program Files/sllunit/SurepayDraft_12a/result/180329_094133.@dft_server_run_search_time_20180329094133_time.log

