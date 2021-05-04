import datetime
import gzip
import logging
import os
import sys
from urllib.error import HTTPError
from urllib.request import urlopen
from xml.dom.minidom import parseString


logger = logging.getLogger()
log_file = None
logger.addHandler(logging.StreamHandler(sys.stderr))


class Mode:
    # file mode
    write = 0
    append = 1
    change = 2


class Action:
    # feature action (changes only)
    add = 0
    update = 1
    delete = 2


def check_log():
    # check if log file exists and print message about that
    if log_file and os.path.exists(str(log_file)):
        message("NOTICE: CHECK OUT '%s' FOR WARNINGS!" % log_file)


def check_file(filename):
    # check input VFR file exists
    if not filename:
        return None

    if filename.startswith('-'):
        fatal('No input file specified')
    if not os.path.isfile(filename):
        fatal("'%s' doesn't exists or it's not a file" % filename)

    return filename


def fatal(msg):
    # print fatal error message and exit
    sys.exit('ERROR: ' + str(msg))


def warning(msg):
    # print warning message
    # sys.stderr.write('WARNING: %s%s' % (str(msg), os.linesep))
    logger.warning(msg)


def error(msg):
    # print error message
    sys.stderr.write('ERROR: %s%s' % (str(msg), os.linesep))


def message(msg):
    # print message to stdout
    sys.stdout.write('-' * 80 + os.linesep)
    sys.stdout.write(msg + os.linesep)
    sys.stdout.write('-' * 80 + os.linesep)
    sys.stdout.flush()


def parse_xml_gz(filename):
    # parse VFR (XML) file
    message("Comparing OGR layers and input XML file (may take some time)...")
    infile = gzip.open(filename)
    content = infile.read()

    # parse xml file content
    dom = parseString(content)
    data = dom.getElementsByTagName('vf:Data')[0]
    if data is None:
        fatal("vf:Data not found")

    item_list = []
    for item in data.childNodes:
        item_list.append(item.tagName.lstrip('vf:'))

    return item_list


def compare_list(list1, list2):
    # compare to list of XML nodes (see parse_xml_gz())
    for item in list1:
        if item not in list2:
            print("+ %s" % item)

    for item in list2:
        if item not in list1:
            print("- %s" % item)


def download_vfr(url):
    # download VFR file to local disc
    message("Downloading %s into current directory..." % url)
    local_file = os.path.basename(url)
    fd = open(local_file, 'wb')
    try:
        fd.write(urlopen(url).read())
    except HTTPError as e:
        fd.close()
        if e.code == 404:
            error("File '%s' not found" % url)
    fd.close()
    return local_file


def last_day_of_month(string=True):
    # get last day of current month
    today = datetime.date.today()
    if today.month == 12:
        day = today.replace(day=31)
    else:
        day = (today.replace(month=today.month+1, day=1) - datetime.timedelta(days=1))
    if string:
        return day.strftime("%Y%m%d")
    return day


def yesterday(string=True):
    # get formated yesterday
    today = datetime.date.today()
    day = today - datetime.timedelta(days=1)
    if string:
        return day.strftime("%Y%m%d")
    return day


def remove_option(options, name):
    # remove specified option from list
    i = 0
    for opt in options:
        if opt.startswith(name):
            del options[i]
            return
        i += 1


def get_date_interval(date):
    # get date internal
    dlist = []
    if ':' not in date:
        return [date]

    if date.startswith(':'):
        date_start = last_day_of_month(string=False) + datetime.timedelta(days=1)
        date_end = datetime.datetime.strptime(date[1:], "%Y%m%d").date()
    elif date.endswith(':'):
        date_start = datetime.datetime.strptime(date[:-1], "%Y%m%d").date()
        date_end = yesterday(string=False)
    else:
        s, e = date.split(':', 1)
        date_start = datetime.datetime.strptime(s, "%Y%m%d").date()
        date_end = datetime.datetime.strptime(e, "%Y%m%d").date()

    d = date_start
    delta = datetime.timedelta(days=1)
    while d <= date_end:
        dlist.append(d.strftime("%Y%m%d"))
        d += delta

    return dlist
