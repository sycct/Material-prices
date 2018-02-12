from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User, CH_REGION
from .forms import LoginForm, RegistrationForm, PasswordResetForm, PasswordResetRequestForm
from app import db
from ..email import send_email
from flask_login import current_user
import json


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    title = '登陆'
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'Invalid username or password.','danger')
    return render_template("auth/login.html", form=form, name=title)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    name = '用户注册'
    ch_region = CH_REGION.query.filter_by(REGION_TYPE=1).all()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    fullname=form.fullname.data,
                    address=form.address.data,
                    province_region_id=request.values.get('country', 0),
                    city_region_id=request.values.get('city', 0))
        db.session.add(user)
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, name=name, ch_region=ch_region)


@auth.route('/country', methods=['GET', 'POST'])
def country():
    ID = request.values.get('country', 0)
    city = CH_REGION.query.filter_by(PARENT_ID=ID).all()
    list = []
    for item in city:
        data = [item.ID, item.REGION_NAME]
        list.append(data)
    return json.dumps(list)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed you account.Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash(u'A new confirmation email has been sent to you by email.','success')
    return redirect(url_for('main.index'))


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    title = '忘记密码'
    if not current_user.is_anonymous:
        # 验证密码是否为登录状态，如果是，则终止重置密码
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # 如果用户存在
            token = user.generate_reset_token()
            # 调用User模块中的generate_reset_token函数生成验证信息
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
            # 调用send_email函数，渲染邮件内容之后发送重置密码邮件
        flash(u'An email with instructions to reset your password has been '
              'sent to you.','info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, name=title,token=None)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    name = "重设密码"
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            # 修改密码
            db.session.commit()
            # 加入数据库的session，这里不需要.commit()，在配置文件中已经配置了自动保存
            flash(u'Your password has been updated.','success')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form, name=name, token=token)
