from datetime import tzinfo, timedelta, datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    fullname = db.Column(db.String(64))
    address = db.Column(db.String(64))
    province_region_id = db.Column(db.Integer, db.ForeignKey('CH_REGION.ID'))
    city_region_id = db.Column(db.Integer, db.ForeignKey('CH_REGION.ID'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()
        self.follow(self)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id) \
            .filter(Follow.follower_id == self.id)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_user_posts', id=self.id),
            'followed_posts_url': url_for('api.get_user_followed_posts',
                                          id=self.id),
            'post_count': self.posts.count()
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class CH_REGION(db.Model):
    __tablename__ = 'CH_REGION'
    ID = db.Column(db.Integer, primary_key=True)
    PARENT_ID = db.Column(db.Integer)
    REGION_ID = db.Column(db.Integer)
    REGION_PARENT_ID = db.Column(db.Integer)
    REGION_NAME = db.Column(db.String(100))
    REGION_TYPE = db.Column(db.Integer)
    ZIPCODE = db.Column(db.String(50))
    QUHAO = db.Column(db.String(50))
    Status = db.Column(db.Boolean)
    city_region = db.relationship('User', foreign_keys=[User.city_region_id],
                                  backref=db.backref('city_regions', lazy='joined'),
                                  lazy='dynamic')
    province_region = db.relationship('User', foreign_keys=[User.province_region_id],
                                      backref=db.backref('province_regions', lazy='joined'), lazy='dynamic')


# 材料类别
class MaterialClassification(db.Model):
    __tablename__ = 'material_classification'
    id = db.Column(db.Integer, primary_key=True)
    classification_name = db.Column(db.String(64), index=True, unique=True)
    classification_icon = db.Column(db.String(64))
    classification_since = db.Column(db.DateTime, default=datetime.utcnow)
    classification_catalog = db.relationship('ClassificationCatalog', backref='MaterialClassification', lazy='dynamic')


# 类别目录
class ClassificationCatalog(db.Model):
    __tablename__ = 'classification_catalog'
    id = db.Column(db.Integer, primary_key=True)
    catalog_name = db.Column(db.String(64), index=True)
    classification_id = db.Column(db.Integer, db.ForeignKey('material_classification.id'))
    catalog_since = db.Column(db.DateTime, default=datetime.utcnow)


# 材料品牌
class MaterialClassificationBrand(db.Model):
    __tablename__ = 'material_brand'
    b_id = db.Column(db.Integer, primary_key=True)
    b_name = db.Column(db.VARCHAR(50), index=True)
    b_rel_id = db.Column(db.Integer, db.ForeignKey('material_item.i_id'))
    material_product = db.relationship('MaterialProduct', backref='MaterialClassificationBrand')


# 材料项目
class MaterialItem(db.Model):
    __tablename__ = 'material_item'
    i_id = db.Column(db.Integer, primary_key=True)
    i_name = db.Column(db.UnicodeText(50))
    i_parent_id = db.Column(db.Integer, db.ForeignKey('material_item.i_id'))
    material_brand = db.relationship('MaterialClassificationBrand', backref='MaterialItem')
    material_product = db.relationship('MaterialProduct', backref='MaterialItem')
    i_fk_i = db.relationship('MaterialItem')
    i_ref_pn = db.relationship('MaterialProductName', backref='MaterialItem')


# 具体产品
class MaterialProduct(db.Model):
    __tablename__ = 'material_product'
    p_id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.VARCHAR(50), default=None)
    b_name = db.Column(db.VARCHAR(50), db.ForeignKey('material_brand.b_name'), default=None, index=True)
    p_fk_p = db.Column(db.Integer, db.ForeignKey('material_product.p_id'), default=None, index=True)
    p_fk_i = db.Column(db.Integer, db.ForeignKey('material_item.i_id'), default=None, index=True)
    p_rel_p = db.relationship('MaterialProduct')
    p_rel_pp = db.relationship('MaterialProductProperty', backref='material_product')


# 产品属性
class MaterialProductProperty(db.Model):
    __tablename__ = 'material_product_pro'
    pp_id = db.Column(db.Integer, primary_key=True)
    pp_fk_p = db.Column(db.Integer, db.ForeignKey('material_product.p_id'), index=True)
    pp_fk_pv = db.Column(db.Integer, db.ForeignKey('material_product_value.pv_id'), index=True)
    pp_fk_pn = db.Column(db.Integer, db.ForeignKey('material_pro_name.pro_id'), index=True)


# 产品sku
class MaterialProductSKU(db.Model):
    __tablename__ = 'material_product_sku'
    ps_id = db.Column(db.Integer, primary_key=True)
    pd_fk_id = db.Column(db.Integer, db.ForeignKey('material_product.p_id'), default=None, index=True)
    pd_num = db.Column(db.Integer, default=None)
    pd_price = db.Column(db.DECIMAL(10, 4), default=None)
    pd_name = db.Column(db.VARCHAR(50), default=None)
    pd_properties = db.Column(db.VARCHAR(300), default=None)


# 产品名称
class MaterialProductName(db.Model):
    __tablename__ = 'material_pro_name'
    pro_id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.VARCHAR(50))
    pro_fk_id = db.Column(db.Integer, db.ForeignKey('material_item.i_id'), index=True)
    pro_has_otherName = db.Column(db.CHAR(2), default=0)
    pro_has_color = db.Column(db.CHAR(2), default=0)
    pro_has_enum = db.Column(db.CHAR(2), default=0)
    pro_has_input = db.Column(db.CHAR(2), default=0)
    pro_is_key = db.Column(db.CHAR(2), default=0)
    pro_is_sale = db.Column(db.CHAR(2), default=0)
    pro_is_must = db.Column(db.CHAR(2), default=0)
    pn_rel_pv = db.relationship('MaterialProductValue', backref='material_pro_name')
    pn_rel_pp = db.relationship('MaterialProductProperty', backref='material_pro_name')


# 材料值表
class MaterialProductValue(db.Model):
    __tablename__ = 'material_product_value'
    pv_id = db.Column(db.Integer, primary_key=True)
    pv_name = db.Column(db.VARCHAR(50))
    pv_fk_pid = db.Column(db.Integer, db.ForeignKey('material_pro_name.pro_id'), index=True)
    pv_rel_pp = db.relationship('MaterialProductProperty', backref='material_product_value')


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
            'comments_url': url_for('api.get_post_comments', id=self.id),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code', 'em', 'i',
                        'strong']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id),
            'post_url': url_for('api.get_post', id=self.post_id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)


# 页面相关内容（包括描述、标题等内容）
class PageRelated(db.Model):
    __tablename__ = 'page_related'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    description = db.Column(db.String(64))
    # 页面功能
    page_features = db.Column(db.String(64))


# 短信接收相关表
class SMS_Receive(db.Model):
    __tablename__ = 'SMS_Receive'
    id = db.Column(db.Integer, primary_key=True)
    PhoneNumber = db.Column(db.String(32))
    Content = db.Column(db.String(512))
    SMS_ReceiveTime = db.Column(db.DateTime, index=True)
    Type=db.Column(db.String(32))


db.event.listen(Comment.body, 'set', Comment.on_changed_body)
