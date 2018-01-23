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


class catalog(object):

    name_catalog = ''
    data = []
    data_items = []
    new_list_data = []

    def received_parametrs(self):
        arg_parser = argparse.ArgumentParser (description='Great Description To Be Here')
        try:
            arg_parser.add_argument ("-c", "--catalog", type=str, choices=config.choose_categoty,
                                     default=config.default_parametr, help="category for parsing")
        except Exception as i:
            logging.error ("Error :", i)

        options = arg_parser.parse_args ()
        logging.info ('Parameters console received!')
        print ("Parametrs  console received!")

        catalog.name_catalog = options.catalog

    def request_catalog(self):
        print ('Receive data of catalog...')

        my_catalog = catalog.name_catalog

        if catalog.name_catalog == 'all':
            for my_catalog in config.choose_categoty[:-1]:
                exp_url = config.url_category[:38] + my_catalog + config.url_category[38:]
                try:
                    response = request.urlopen (exp_url)
                    catalog.data += json.loads (response.read ())
                    print ('ALL OK! All id categoty {} received!'.format (my_catalog))
                    logging.info ('ALL OK! All id categoty {} received!'.format (my_catalog))
                except Exception as my_error:
                    logging.error ('This is an error message :', my_error)
                    print ('error :', my_error)
        else:
            exp_url = config.url_category[:38] + my_catalog + config.url_category[38:]
            try:
                response = request.urlopen (exp_url)
                catalog.data = json.loads (response.read ())
                print ('ALL OK! All id categoty {} received!'.format (my_catalog))
                logging.info ('ALL OK! All id categoty {} received!'.format (my_catalog))
            except Exception as my_error:
                logging.error ('This is an error message :', my_error)
                print ('error :', my_error)

    def request_items(self):

        print ('Receive and add data for every id...')
        for i, item in enumerate(catalog.data):
            exp_url = config.url_id[:43] + str (item) + config.url_id[43:]
            try:
                response = request.urlopen (exp_url)
                data_dict = json.loads (response.read ())
                catalog.data_items.append (data_dict.copy ())
                logging.info ('Data of {}-th element received and add'.format (i))
            except Exception as my_error:
                logging.error ('This is an error message : {}'.format (my_error))

    def filter(self):
        print ('Filtering data...')
        for item in catalog.data_items:
            if config.score <= int (item['score']) and config.from_date <= int (item['time']):
                # clear tag in area "text"
                if 'text' in item.keys ():
                    my_search = re.findall (pattern, item['text'])
                    if len (my_search) >= 1:
                        for dupl in my_search:
                            item['text'] = item['text'].replace (dupl, '')
                catalog.new_list_data.append(item.copy ())
        print('Data is filtred out!')
        logging.info('Data is filtered out')

    def file_write(self):
        try:
            os.makedirs (config.name_dir)
            print ('dir created')
        except OSError:
            print('dir already created')
        with open (config.file_report, "w", newline="") as file:
            logging.info ('File report.csv created!')
            columns = ['by', 'descendants', 'id', 'kids', 'score', 'time', 'text', 'title', 'parts', 'type', 'url']
            writer = csv.DictWriter (file, fieldnames=columns)
            writer.writeheader ()
            logging.info ('Header write to file report.csv !')
            writer.writerows (catalog.new_list_data)
            logging.info ('Data write to file report.csv !')


if __name__ == "__main__":
    log_format = "('%(asctime)s - %(name)s - %(levelname)s - %(message)s')"
    logging.basicConfig(filename=config.log_file_name,
                            level=logging.INFO, format=log_format)
    logging.info('Program was started!')

    first = catalog()
    first.received_parametrs()
    first.request_catalog()
    first.request_items()
    logging.info ('Data of every id {} received!'.format (catalog.name_catalog))
    print ('Data of every id the category {} received!'.format (catalog.name_catalog))
    first.filter()
    print('Write data to file...')
    print(first.new_list_data)
    print('ALL OK! Data recorded')