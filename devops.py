#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import logging
import os
from xmind2testcase.utils import get_xmind_testcase_list, get_absolute_path

"""
Convert XMind fie to devops testcase csv file 

"""


def xmind_to_devops_csv_file(xmind_file):
    """Convert XMind file to a devops csv file"""
    xmind_file = get_absolute_path(xmind_file)
    logging.info('Start converting XMind file(%s) to devops file...', xmind_file)
    testcases = get_xmind_testcase_list(xmind_file)

    fileheader = ["ID", "Work Item Type", "Title", "Test Step", "Step Action", "Step Expected", "Revision", "Area Path", "Assigned To", "State"]
    devops_testcase_rows = [fileheader]
    for testcase in testcases:
        row, row1= gen_a_testcase_row(testcase)
        devops_testcase_rows.append(row)
        devops_testcase_rows.append(row1)

    devops_file = xmind_file[:-6] + '.csv'
    if os.path.exists(devops_file):
        os.remove(devops_file)
        # logging.info('The devops csv file already exists, return it directly: %s', devops_file)
        # return devops_file

    with open(devops_file, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(devops_testcase_rows)
        logging.info('Convert XMind file(%s) to a devops csv file(%s) successfully!', xmind_file, devops_file)

    return devops_file


def final_fix_csv_file(devops_file):
    '''remove " from csv file'''
    with open(devops_file, 'r', encoding='utf8') as f:
        newlines = []
        for line in f.readlines():
            newlines.append(line.replace('"', ''))
    with open(devops_file, 'w', encoding='utf8') as f:
        for line in newlines:
            f.write(line)
    return devops_file


def gen_a_testcase_row(testcase_dict):
    tid = ''   # TODO
    assign_to = 'Guanhua Jing <guanhua.jing@vffice.com>'  # TODO
    case_title = testcase_dict['name']
    case_module = gen_case_module(testcase_dict['suite'])
    case_step = gen_case_step_and_expected_result(testcase_dict['steps'])
    revision = '1' # TODO
    path = 'CGX005.UniversalDistribution' # TODO
    state = 'design'  # TODO
    work_item_type = 'Test Case'  # TODO
    row = [tid, work_item_type, case_module+'.'+case_title, '', '', '', revision, path, assign_to, state]
    row1 = [case_step]
    return row, row1


def gen_case_module(module_name):
    if module_name:
        module_name = module_name.replace('（', '(')
        module_name = module_name.replace('）', ')')
    else:
        module_name = '/'
    return module_name


def gen_case_step_and_expected_result(steps):
    case_step = ''
    test_case_data = ''
    case_expected_result = ''

    for step_dict in steps:
        case_step += ',,,'+ str(step_dict['step_number']) + ',' + step_dict['actions'].replace('\n', '').strip() \
        +' '+ step_dict['testcasedata'].replace('\n', '').strip() +','+ step_dict['expectedresults'].replace('\n', '').strip() + ',,,\n' \
            if step_dict.get('expectedresults', '') else ''\
            if step_dict.get('testcasedata', '') else '' \


    return case_step


if __name__ == '__main__':
    xmind_file = '../docs/devops_testcase_template.xmind'
    devops_csv_file = xmind_to_devops_csv_file(xmind_file)
    print('Conver the xmind file to a devops csv file succssfully: %s', devops_csv_file)