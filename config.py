import time
# names of files and directory
log_file_name = "./results/hn_parser.log"
file_report = "./results/report.csv"
name_dir = "results"
# for argparse
default_parametr = "jobstories"
choose_categoty = ['askstories', 'showstories', 'newstories', 'jobstories', 'all']
# value of filters
from_date = (2015, 4, 23, 12, 43, 12, 0, 0, 0)
from_date = time.mktime(from_date)
score = 1

url_category = 'https://hacker-news.firebaseio.com/v0/.json?print=pretty'
url_id = 'https://hacker-news.firebaseio.com/v0/item/.json?print=pretty'

exp_table = ''' 
 <table border="2" width="100%" cellpadding="5">
 </table>
'''