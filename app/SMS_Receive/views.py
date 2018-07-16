# _*_ coding: utf-8 _*_

import time
from . import receive
from app import db
from ..models import SMS_Receive
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import datetime
from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response


@receive.route('/')
def index():
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    msg_count = db.session.query(sqlalchemy.func.count(SMS_Receive.id)).scalar()
    last_time = db.session.query(SMS_Receive).order_by(SMS_Receive.SMS_ReceiveTime.desc()).first().SMS_ReceiveTime
    start_time = datetime.datetime.now()
    # 计算时差
    ms = (start_time - last_time).seconds
    if ms >= 86400:
        days = ms // 86400
        time_info = '%d天' % (days)
    elif ms >= 3600:
        hour = ms // 3600
        time_info = "%d小时" % (hour)
    elif ms >= 60:
        minute = ms // 60
        time_info = '%d分钟' % (minute)
    else:
        time_info = '%d秒' % (ms)
    return render_template("SMS_Receive/index.html", name=title, pageName=page_name, description=page_name,
                           pageFeatures=page_features, SMS_Count=msg_count, timeInfo=time_info)


@receive.route('/SMSContent')
def SMSContent():
    title = '首 页'
    page_name = 'Dashboard'
    page_features = 'dashboard & statistics'
    # 选择最新4条短信内容
    font_list_four = db.session.query(SMS_Receive).order_by(SMS_Receive.SMS_ReceiveTime.desc()).limit(4)
    # 如果没有数据，默认显示第一页
    page = request.args.get('page', 1, type=int)
    # 选最剩余短信内容
    pagination = db.session.query(SMS_Receive).from_self().order_by(SMS_Receive.SMS_ReceiveTime.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    surplus = pagination.items
    return render_template("SMS_Receive/sms_content.html", name=title, pageName=page_name, description=page_name,
                           pageFeatures=page_features, list_four=font_list_four, list_surplus=surplus, pagination=pagination)


def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]

@receive.route('/SMSServer', methods=['POST'])
def SMSServer():
    address = request.values.get('address', 0)
    get_date = str(request.values.get('date', 0))
    # 转换时间
    tl = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(get_date[0:10])))
    msg = request.values.get('msg', 0)
    type = request.values.get('type', 0)
    content = SMS_Receive(PhoneNumber=address, Content=msg, Type=type, SMS_ReceiveTime=tl)
    try:
        db.session.add(content)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return '1'
    else:
        return '0'
