# program by Stupka Bogdan

import argparse
import logging
import config
import json
import os
import csv
import re
from urllib import request

# for del tag in text area
pattern = r"<.+>.*<.+>"


def main():
    logic = create_dir(config.name_dir)
    print("Directory created!")

    log_format = "('%(asctime)s - %(name)s - %(levelname)s - %(message)s')"
    logging.basicConfig(filename=config.log_file_name,
                        level=logging.INFO, format=log_format)
    logging.info('Program was started!')

    if logic:
        logging.info("The directory {} created!".format(config.name_dir))
    else:
        logging.info(f"The directory {config.name_dir} has allready been"
                     f" received!".format(config.name_dir))

    need_category = received_parametrs()

    list_id = received_data_for_catalog(need_category, config.url_category)

    list_data_id = received_data_id(list_id, config.url_id)
    logging.info('Data of every id {} received!'.format(need_category))
    print('Data of every id the category {} received!'.format(need_category))

    filter_data = myfilter(list_data_id, config.from_date, config.score)

    print('Write data to file...')
    file_write(config.file_report, filter_data)
    print('ALL OK! Data recorded')
    return


def create_dir(dir_name):
    try:
        os.makedirs(dir_name)
        return True
    except OSError:
        return False


def received_parametrs():
    arg_parser = argparse.ArgumentParser(
        description='Great Description To Be Here')
    try:
        arg_parser.add_argument("-c", "--catalog", type=str,
                                choices=config.choose_categoty,
                                default=config.default_parametr,
                                help="category for parsing")
    except Exception as i:
        logging.error("Error :", i)

    options = arg_parser.parse_args()
    logging.info('Parameters console received!')
    print("Parametrs  console received!")

    return options.catalog


def file_write(name_file, data):
    with open(name_file, "w", newline="") as file:
        logging.info('File report.csv created!')
        columns = ['by', 'descendants', 'id', 'kids', 'score',
                   'time', 'text', 'title', 'type', 'url']
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        logging.info('Header write to file report.csv !')
        writer.writerows(data)
        logging.info('Data write to file report.csv !')
    return


def received_data_for_catalog(catalog, exp_url):
    url_category = exp_url[:38] + catalog + exp_url[38:]
    print('Receive data...')
    try:
        response = request.urlopen(url_category)
        data = json.loads(response.read())
        print('ALL OK! All id categoty {} received!'.format(catalog))
        logging.info('ALL OK! All id categoty {} received!'.format(catalog))
    except Exception as my_error:
        logging.error('This is an error message :', my_error)
        print('error :', my_error)
    return data


def received_data_id(list_of_id, exp_url):
    mydata = []

    print('Receive and add data for every id...')
    for i, item in enumerate(list_of_id):
        url_id = exp_url[:43] + str(item) + exp_url[43:]
        try:
            response = request.urlopen(url_id)
            data_dict = json.loads(response.read())
            mydata.append(data_dict.copy())
            logging.info('Data of {}-th element received and add'.format(i))
        except Exception as my_error:
            logging.error('This is an error message : {}'.format(my_error))

    return mydata


# this is function, wich search element(according to the given parametrs)
# and in this elements(in area 'text') delete tag
def myfilter(data_for_every_id, filter_data, filter_score):
    print('Filtering data...')
    new_list_data = []
    for item in data_for_every_id:
        if filter_score <= int(item['score']) and \
                        filter_data <= int(item['time']):
            # clear tag in area "text"
            if 'text' in item.keys():
                my_search = re.findall(pattern, item['text'])
                if len(my_search) >= 1:
                    for dupl in my_search:
                        item['text'] = item['text'].replace(dupl, '')
            new_list_data.append(item.copy())

    print('Data is filtred out!')
    logging.info('Data is filtered out')
    return new_list_data


main()
