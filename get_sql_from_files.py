import os
import sys
import io
import re
def get_sql_files(src):
    '''
    '''
    sql_list = []
    for root, dirs, files in os.walk(src):
        for file_name in files:
            if file_name.endswith('.sql') :
                sql_list.append(os.path.join(root,file_name))
    return sql_list
def get_table_statment(file_list):
    truncate_table_template = re.compile("TRUNCATE TABLE.*")
    for file_name in file_list:
        with io.open(file_name, 'r') as fin:
            statment_str = fin.read()
            statment_find = re.findall(truncate_table_template, statment_str)
            if statment_find:
                print(statment_find[0] )
if __name__ == '__main__':
    src_dir = r"D:\daily_run\xsf"
    #src_dir = sys.argv[1]
    sql_list = get_sql_files(src_dir)
    get_table_statment(sql_list)
