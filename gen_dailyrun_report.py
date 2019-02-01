import os
import re
def get_files(src):
    file_list = []
    for root, dirs, files in os.walk(src):
        for name in files:
            if "Automation_test_report.html" in name:
                file_list.append(os.path.join(root,name))
    return file_list

def gen_report_csv(files, result_csv_name):
    suc_item_template = re.compile(r"Successful cases: <span>(.*)</span></div>")
    fail_item_template = re.compile(r"Failed cases: <span>(.*)</span></div>")
    total_item_template = re.compile(r"Total cases:<span>(.*)</span></div>")
    content = ""
    print("%s exists?  " %result_csv_name, os.path.exists(result_csv_name))
    if not os.path.exists(result_csv_name):
        with open(result_csv_name, 'a') as f:
	    #f.write(" date , Success , Failed , Total , Path\n")
	    f.write(" date , Success , Failed , Total\n")
    else:
        with open(result_csv_name, 'r') as f:
            content = f.read()
        f.close()
    for name in files:
        if name in content:
            print("%s ##EXITTS## in %s " % (name,result_csv_name))
            continue
        #with open(name, 'r', encoding='utf-8') as fin:
	with open(name, 'r') as fin:
            html_str = fin.read()
            suc_found = re.findall(suc_item_template, html_str)
            fail_found = re.findall(fail_item_template, html_str)
            total_found = re.findall(total_item_template, html_str)
            if suc_found and fail_found and total_found:
                print(name, suc_found, fail_found, total_found)
		run_date = re.split(r'[/\\]', name)[-2]
                result_str = suc_found[0] + ',' + fail_found[0] + ',' + total_found[0]
                with open(result_csv_name, 'a') as f:
		    f.write(run_date+',')
		    f.write(result_str)
		    #f.write(name)
		    f.write("\n")
if __name__ == '__main__':
    src = r"/home/cedailyrun/log/automation183_ITU_CVM03"
    result_csv_name = r"daily_run_result_ITU_CVM03.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)


    src = r"/home/cedailyrun/log/automation183_ITU_CVM04"
    result_csv_name = r"daily_run_result_ITU_CVM04.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)


    src = r"/home/cedailyrun/log/automation189_ITU_CEVM01"
    result_csv_name = r"daily_run_result_ITU_CEVM01.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)

    src = r"/home/cedailyrun/log/automation312_5/"
    result_csv_name = r"daily_run_result_312_5_ANSI_CVM06.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)

    src = r"/home/cedailyrun/log/automation312_4/"
    result_csv_name = r"daily_run_result_312_4_ANSI_CVM05.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)


    src = r"/home/cedailyrun/log/automation_ANSI_CHSP05A_CVM05"
    result_csv_name = r"daily_run_result_automation_ANSI_CHSP05A.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)


    src = r"/home/cedailyrun/log/automation312_ANSI_CEVM02_CVM06"
    result_csv_name = r"daily_run_result_automation312_ANSI_CEVM02.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)


    src = r"/home/cedailyrun/log/automation312_ANSI_SPVM165B/"
    result_csv_name = r"daily_run_result_automation312_ANSI_SPVM165B.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)
    
    src = r"/home/cedailyrun/log/automation189_itu_BJRMS22A/SurepayDraft/result/"
    result_csv_name = r"daily_run_ITU_BJRMS22A.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)

    src = r"/home/cedailyrun/log/automation189_itu_BJRMS22B/SurepayDraft/result/"
    result_csv_name = r"daily_run_ITU_BJRMS22B.csv"
    files = get_files(src)
    gen_report_csv(files[:], result_csv_name)



