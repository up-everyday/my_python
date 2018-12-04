# -*- coding: utf-8 -*-
#python3
import io
import json
import csv
import os
import re
import sqlite3
from collections import OrderedDict
def comare_result(test_dict):
    db_name = r'D:/daily_run/failedcase_id_reason.db'
    conn = sqlite3.connect(db_name)
    curs = conn.cursor()
    query = 'select * from caseinfo where caseid = ?'
    for key,value in test_dict.items():
        ##Note: (key,)
        curs.execute(query,(key,))
        row = curs.fetchone()
        #result(caseid , reason , rootcause )
        if row != None and value != row[1]:
            print("\n##############################")
            print("Compare result")
            print("##############################\n")
            print("%s original result is %s" % (key,test_dict[key]))
    curs.close()
    conn.close()

def get_info_files(src):
    '''
    e.g.
    duration:
        180808_031917.@dft_server_run_daily_time_20180808031917_time.suite.suite_status.html
    case info -- HTML:
        180808_050234.@dft_server_run_daily_time_20180808050234_time.html
    case info -- log
        180808_050234.@dft_server_run_daily_time_20180808050234_time.log
    '''
    file_list = []
    html_list = []
    dur_files = []
    for root, dirs, files in os.walk(src):
        for file_name in files:
            if not file_name.endswith('.debuglog.log') and file_name.endswith('.log') and '_run_daily_' in file_name:
                file_list.append(os.path.join(root,file_name))
            if file_name.endswith('time.html') and '_run_daily_' in file_name:
                html_list.append(os.path.join(root,file_name))
            if file_name.endswith('suite.suite_status.html') and '_run_daily_' in file_name:
                dur_files.append(os.path.join(root,file_name))
    return (file_list,html_list, dur_files)

def get_failed_case_list(files):
    fail_list = []
    fail_item_template = re.compile("<td>Failed item list is \[(.*)\]</td>")
    for file_name in files:
        if file_name.endswith('.html') and '_run_daily_' in file_name:
            with io.open(file_name, 'r', encoding='utf-8') as fin:
                html_str = fin.read()
                fail_find = re.findall(fail_item_template, html_str)
                if fail_find:  # two times found, choose the first.fail_find[0]
                    fail_list.extend(re.sub(r"dft_server/|'| |\.json", "", fail_find[0]).replace("/","_").replace("-","_").split(","))
    return fail_list

def output_format(data_dict=OrderedDict(), status_dict=(OrderedDict)):
    formatted_output = OrderedDict()
    #convertion
    for k,v in data_dict.items():
        if v in formatted_output:
            formatted_output[v].append(k)
        else:
            formatted_output[v] = [k] #list

    j = 0
    for key in formatted_output:
        #list.sort
        formatted_output[key].sort()
        #output
        j = j + 1
        print("\n %d) %s :" %(j, key))
        i = 0
        for elem in formatted_output[key]:
            print("%+20s  %s" % (elem,status_dict[elem]), end = ' ')
            i = i + 1
            if i == 3:
                print()
                i = 0
def get_case_duration(dur_files = []):
    info_dict = {}
    case_id_temp = re.compile("<td>dft_server.*</td>\n<td>\d.*</td>")
    for file in  dur_files:
        with io.open(file) as dur_fp:
            content = dur_fp.read()
            info_list = re.findall(case_id_temp,content)
            for info in info_list:
                case = re.split('\n',info)
                case_id = re.search('<td>dft_server/(.*).json</td>', case[0]).group(1)
                case_dur = re.search('<td>(.*)</td>', case[1]).group(1)
                info_dict[case_id] = case_dur
        dur_fp.close()
    total_dur = 0
    for key in info_dict:
        total_dur = total_dur + int(info_dict[key])
    print("\nduration is ", total_dur)
def write_dict_into_csv(save_name, header_list=[], data_dict={}):
    tmp_dict = {}
    if os.path.exists(save_name):
        with open(save_name, "r") as csv_rd:
            dict_rd = csv.DictReader(csv_rd)
            csv_headers = dict_rd.fieldnames

            for key in csv_headers:
                if key in data_dict:
                    tmp_dict[key] = data_dict[key]
                else:
                    tmp_dict[key] = "Empty"
            for key in data_dict:
                if key in csv_headers:
                    continue
                else:
                    print("%s : \n      %s" %(key,data_dict[key]))
            for row in dict_rd:
                if tmp_dict['run_date'] == row['run_date']:
                    print("%s EXISTS!" % tmp_dict["run_date"])
                    csv_rd.close()
                    return header_list[0]
    else:
        tmp_dict = data_dict
        csv_headers = header_list
    if not os.path.exists(save_name):
        header_write_flag = True
    else:
        header_write_flag = False
    with open(save_name, "a") as csv_file:
        my_writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        if header_write_flag:
            my_writer.writeheader()
        my_writer.writerow(tmp_dict)
    csv_file.close()
def output_failedcaselist(failed_case_list=[]):
    tmp_list = []

    for case in failed_case_list:
        case = case.replace("_", "/")+'.json'
        tmp_list.append(case)
    print(json.dumps(tmp_list, indent=4))
def get_failedcases_status(failed_case_list=[]):
    status_dict = OrderedDict()
    db_name = r"D:/work/20180312_SPID-471_SPID-472_feature/SurepayDraft20180315/dft_server/DftTag.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for case in failed_case_list:
        case = case.replace("_", "/")+'.json'
        sql_str = "select case_name, case_status from DftTag where case_name='%s' " %case
        cursor.execute(sql_str)
        values = cursor.fetchall()
        tmp_key = list(values[0])
        tmp_key = tmp_key[0].split('.')[0].replace("/", "_")
        status_dict[tmp_key] = values[0][1]
    cursor.close()
    conn.close()
    return status_dict

def get_id_reanson_dict(run_date, log_files, failed_case_list=[]):
    caseid_failed_dict = {}
    caseid_failed_dict["run_date"] = run_date
    header_list =["run_date"]
    header_list.extend(failed_case_list)
    status_dict = {}
    for log_name in log_files:
        log_run_date = re.split(r'[/\\]', log_name)[-2]
        if log_run_date != run_date:
            continue
        with io.open(log_name,"r") as fin:
            for line in fin.readlines():
                for case_id in failed_case_list:
                    if (not caseid_failed_dict.get(case_id)) and (case_id in line) and ('"levelname": "ERROR"' in line):
                        tmp_dict = json.loads(line)
                        failed_str = tmp_dict["message"]
                        caseid_failed_dict[case_id] = failed_str
        fin.close()
    status_dict = get_failedcases_status(failed_case_list[:])

    #delete run_date which does note exist in the DftTag.db
    caseid_failed_dict.pop('run_date')
    output_format(caseid_failed_dict, status_dict)
    #output_failedcaselist(failed_case_list)
    #write_dict_into_csv(r"D:/daily_run/failed_case_result.csv",header_list[:], caseid_failed_dict)
    comare_result(caseid_failed_dict)
    return caseid_failed_dict

if __name__ == '__main__':
    src = r"D:/daily_run/CEVM01/181203_171003_r_1"
    run_date = re.split(r'[/\\]', src)[-1]
    failed_case_list = []
    caseid_failed_dict = OrderedDict()
    log_list,html_list, dur_files = get_info_files(src)
    failed_case_list = get_failed_case_list(html_list[:])
    failed_case_list.sort()
    print("xxx failed_case_list ", len(failed_case_list))
    get_id_reanson_dict(run_date,log_list[:],failed_case_list[:])
    #get_case_duration(dur_files[:])


