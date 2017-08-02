# -*- coding: utf-8 -*-
# # Author: Jenner.Luo
from binascii import crc32
import cookielib
from decimal import Decimal
import json
import os
import random
import re
import string
import time
from StringIO import StringIO
import datetime
import urllib
import urllib2
from dateutil import parser
from django.db import connection
import poster


def now_time(format_str="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format_str, time.localtime())


def is_url(url_str):
    """判断是否是url
    :param url_str:
    :return:
    """
    # ret = re.search(r'^https?://', url_str, re.IGNORECASE)
    ret = re.search(r'^((https|http|ftp|rtsp|mms)?://)',
                    url_str, re.IGNORECASE)
    return True if ret else False


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """# 动态生成特定的ID
    :param size:
    :param chars:
    :return:
    """
    return ''.join(random.choice(chars) for x in range(size))


def first_minus_second(first_datetime, second_datetime):
    """
    # 求两个日期时候的差
    :type first_datetime: object
    :param first_datetime: 
    :param second_datetime: 
    :return: 
    """
    a = parser.parse(str(first_datetime))
    b = parser.parse(str(second_datetime))
    c = (a - b).total_seconds()
    # print 'first_datetime=',  a
    # print 'second_datetime=', b
    # print 'a - b=', dir(a - b)
    # print 'a - b=', a - b
    # print 'minus result =', c
    return c


def post_method(url, data, url_encode=False, enable_cookie=False, return_json=False):
    req = urllib2.Request(url)
    if url_encode:
        data = urllib.urlencode(data)
    if enable_cookie:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req, data)
    else:
        response = urllib2.urlopen(req, data)
    content = response.read()
    return json.loads(content) if return_json else content


def do_poster(params, target_url, return_json=True):
    """将文件post到其它站点
    :param params: form-data中媒体文件标识，有filename、filelength、content-type等信息
    :param target_url: 需要将文件post过去的目标站点
    :param return_json:  post结束后对应站点返回的信息是否格式成json
    :return:
    """
    opener = poster.streaminghttp.register_openers()
    opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    datagen, headers = poster.encode.multipart_encode(params)
    # 创建请求对象
    request_obj = urllib2.Request(target_url, datagen, headers)
    # 实际执行请求并取得返回
    res = urllib2.urlopen(request_obj).read()
    return json.loads(res) if return_json else res


def post_file(file_dir, target_url, file_key='file', other_params={}, remove_file=False, return_json=True):
    """
    :param file_dir:  文件的路径  {'file': open("test.txt", "rb"), 'name': 'upload test'}
    :param target_url: 需要将文件post过去的目标站点
    :param remove_file: post结束后是否删除本地文件的标识
    :param return_json: post结束后对应站点返回的信息是否格式成json
    :return:
    # headers 包含必须的 Content-Type 和 Content-Length
    # datagen 是一个生成器对象，返回编码过后的参数，这里如果有多个参数的话依次添加即可
    """
    post_result = None
    try:
        params = {file_key: open(file_dir, 'rb')}
        if other_params:
            params.update(other_params)
        post_result = do_poster(params, target_url, return_json=True)
        if remove_file:
            os.remove(file_dir)
    except Exception as e:
        print 'POST FILE ERROR:', e
    return post_result


def get_method(url, params={}, return_json=False):
    param_str = ''
    if params:
        for key in params:
            if params.has_key(key):
                param_str += '&' + str(key) + '=' + str(params.get(key))
        param_str = '?' + param_str
    url += param_str
    response = urllib2.urlopen(url)
    con = response.read()
    return json.loads(con) if return_json else con


def crc32_(_str):
    """计算字符串的 CRC32 编码,返回一个整数,可能带符号
    Args:
        str:    例如 abcd
    Returns:
        str:    例如 -310194927
    Example:
    """
    return crc32(_str) & 0xffffffff
    # return crc32(_str)


def md5_str(_str):
    """对字符串计算 md5 编码.
    Args:
        str:    待计算的字符串
    Returns:
        string: 返回32位字符串
    Example:
    >>> u = Utils()
    >>> print u.md5_str('54321')
    01cfcd4f6b8770febfb40cb906715822
    """
    import hashlib

    m = hashlib.md5(_str)
    m.digest()
    return m.hexdigest()


def uriToID(str_uri):
    if re.compile(r'\/api\/v(\d+)\/(.*?)\/(\d+)\/?').search(str_uri):
        return re.sub(r'\/api\/v(\d+)\/(.*?)\/(\d+)\/?', r'\3', str_uri)
    else:
        return str_uri


def isUri(str_uri):
    return re.compile(r'\/api\/v(\d+)\/(.*?)\/(\d+)\/?').search(str_uri)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def month_range(year=None, month=None):
    """
    """
    import calendar
    from datetime import date

    if not year:
        year = date.today().year
    if not month:
        month = date.today().month
    first_tm = '%s-%s-%s 00:00:00' % (year, month, 1)
    last_tm = '%s-%s-%s 23:59:59' % (year, month,
                                     calendar.monthrange(year, month)[1])
    return first_tm, last_tm


def format_num(num, format=2):
    str_ = "{0:." + str(format) + "f}"
    return str_.format(num)


def get_discount(total, discount_rate, decimal_num=2):
    decimal_total = Decimal(total, decimal_num)
    # decimal_left = (Decimal(100, decimal_num)-Decimal(discount_rate, decimal_num))
    # decimal_rate = decimal_left / Decimal(100, decimal_num)
    decimal_rate = Decimal(discount_rate, decimal_num) / \
        Decimal(100, decimal_num)
    res = decimal_total * decimal_rate
    return res


def read_dir(dir_str, file_list=[]):
    dir_list = os.listdir(dir_str)
    for item in dir_list:
        new_dir = dir_str + '/' + item
        if os.path.isdir(new_dir):
            read_dir(new_dir, file_list=file_list)
        else:
            file_list.append(new_dir)
    return file_list


def delay_days(start_date, days, format_str="%Y-%m-%d"):
    """
    #日期延迟 date delay
    :param start_date:
    :param days:
    :param format:
    :return:
    """
    date = datetime.datetime.strptime(start_date, format_str)
    return (date + datetime.timedelta(days=days)).strftime(format_str)


def format_data_dict(data_dict, key_list=[]):
    new_dict = {}
    for key in key_list:
        new_dict[key] = data_dict.get(key, '')
    return new_dict


def format_obj_needed_data(obj, key_list=[]):
    data_dict = {}
    for key in key_list:
        if hasattr(obj, key):
            data_dict[key] = getattr(obj, key)
        else:
            data_dict[key] = ""
    return data_dict


# https://docs.djangoproject.com/en/dev/topics/db/sql/
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def custom_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    return dictfetchall(cursor)


def update_obj_field_values(obj, data_dict, do_save=True):
    for key in data_dict:
        obj.__setattr__(key, data_dict.get(key, ''))
    if do_save:
        obj.save()
    return obj


def delete_file_folder(src):
    """
    :param src:
    """
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_folder(itemsrc)
        try:
            os.rmdir(src)
        except:
            pass


def make_dir(path):
    """
    :param dir_str:
    """
    if not os.path.exists(path):
        os.mkdir(path)
