# -*- coding:utf-8 -*-
import logging
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm.session import object_session
from datetime import datetime
from pyramid_sqlalchemy import BaseObject as Base
from pyramid_sqlalchemy import Session as ObjectSession
from .exceptions import ModelException
Session = ObjectSession
logger = logging.getLogger(__name__)


class TimeMixin(object):
    ctime = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    utime = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)


class Account(TimeMixin, Base):
    __tablename__ = "account"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=255), default="", nullable=False, unique=True)

    def register_key(self, key, expired_at=None):
        apikey = APIKey(key=key, account=self, expired_at=expired_at)
        session = object_session(self)
        session.add(apikey)
        return apikey

    def register_repository(self, name):
        repository = Repository(name=name, account=self)
        session = object_session(self)
        session.add(repository)
        return repository


class APIKey(TimeMixin, Base):
    __tablename__ = "apikey"
    id = sa.Column(sa.Integer, primary_key=True)
    account_id = sa.Column(sa.Integer, sa.ForeignKey("account.id"))
    account = orm.relationship(Account, backref=orm.backref("apikeys", cascade="all, delete-orphan"))
    key = sa.Column(sa.String(length=255), nullable=False)  # xxx:
    expired_at = sa.Column(sa.DateTime, nullable=True)

    def is_expired(self, now=None):
        now = now or datetime.utcnow()
        return self.expired_at and now > self.expired_at


class Repository(TimeMixin, Base):
    __tablename__ = "repository"
    id = sa.Column(sa.Integer, primary_key=True)
    account_id = sa.Column(sa.Integer, sa.ForeignKey("account.id"))
    account = orm.relationship(Account, backref=orm.backref("repositories", cascade="all, delete-orphan"))
    name = sa.Column(sa.String(length=255), default="", nullable=False, unique=True)

    def register_scaffold(self, name, version):
        scaffold = Scaffold(name=name, version=version, repository=self)
        session = object_session(self)
        session.add(scaffold)
        return scaffold

    def has_scaffold(self, name):
        return bool(self.get_scaffold(name))

    def get_scaffold(self, name):
        for s in self.scaffolds:
            if s.name == s.name:
                return s


class Scaffold(TimeMixin, Base):
    __tablename__ = "scaffold"
    id = sa.Column(sa.Integer, primary_key=True)
    version = sa.Column(sa.String(length=16), default="0.0.1", nullable=False)
    name = sa.Column(sa.String(length=255), default="", nullable=False, unique=True)
    repository_id = sa.Column(sa.Integer, sa.ForeignKey("repository.id"))
    repository = orm.relationship(Repository, backref=orm.backref("scaffolds", cascade="all, delete-orphan"))

    def register_template(self, name, content, input_encoding="utf-8", output_encoding="utf-8"):
        template = Template(name=name,
                            scaffold=self,
                            content=content,
                            input_encoding=input_encoding,
                            output_encoding=output_encoding)
        session = object_session(self)
        session.add(template)
        return template

    def is_version_conflict(self, version):
        if version == self.version:
            return True
        session = object_session(self)
        qs = session.query(ScaffoldHistory).filter(
            ScaffoldHistory.scaffold == self,
            ScaffoldHistory.version == version
        )
        if session.query(qs.exists()).scalar():
            return True
        # for history in self.histories:
        #     if history.version == version:
        #         return True
        return False

    def swap(self, name, version):
        if self.is_version_conflict(version):
            raise ModelException("version conflict")
        history = ScaffoldHistory(name=self.name, version=self.version, scaffold=self)
        history.swap(self)
        self.name = name
        self.version = version
        session = object_session(self)
        session.add(history)
        session.query(Template).filter(Template.scaffold == self).delete()
        session.add(self)
        return self


class Template(TimeMixin, Base):
    __tablename__ = "template"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=255), default="", nullable=False, unique=True)
    content = sa.Column(sa.Text, nullable=False, default="")
    input_encoding = sa.Column(sa.String(length=16), nullable="False", default="utf-8")
    output_encoding = sa.Column(sa.String(length=16), nullable="False", default="utf-8")
    scaffold_id = sa.Column(sa.Integer, sa.ForeignKey("scaffold.id"))
    scaffold = orm.relationship(Scaffold, backref=orm.backref("templates", cascade="all, delete-orphan"))


# transaction
class ScaffoldHistory(TimeMixin, Base):
    __tablename__ = "scaffold_history"
    id = sa.Column(sa.Integer, primary_key=True)
    version = sa.Column(sa.String(length=16), default="0.0.1", nullable=False)
    name = sa.Column(sa.String(length=255), default="", nullable=False)
    scaffold_id = sa.Column(sa.Integer, sa.ForeignKey("scaffold.id"))
    scaffold = orm.relationship(Scaffold, backref=orm.backref("histories", cascade="all, delete-orphan"))

    __table_args__ = (
        sa.UniqueConstraint("name", "version"),
    )

    def swap(self, scaffold):
        for t in scaffold.templates:
            self.templates.append(
                TemplateHistory(name=t.name,
                                content=t.content,
                                input_encoding=t.input_encoding,
                                output_encoding=t.output_encoding))


class TemplateHistory(TimeMixin, Base):
    __tablename__ = "template_history"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=255), default="", nullable=False)
    content = sa.Column(sa.Text, nullable=False, default="")
    input_encoding = sa.Column(sa.String(length=16), nullable="False", default="utf-8")
    output_encoding = sa.Column(sa.String(length=16), nullable="False", default="utf-8")
    scaffold_history_id = sa.Column(sa.Integer, sa.ForeignKey("scaffold_history.id"))
    scaffold = orm.relationship(ScaffoldHistory, backref=orm.backref("templates", cascade="all, delete-orphan"))


class ApplyLog(Base):
    __tablename__ = "applylog"
    id = sa.Column(sa.Integer, primary_key=True)
    ctime = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    scaffold_id = sa.Column(sa.Integer, sa.ForeignKey("scaffold.id"))
    status = sa.Column(sa.Enum("success", "failure"))
    traceback = sa.Column(sa.Text, nullable=False, default="")
    args = sa.Column(sa.Text, nullable=False, default="")
    scaffold = orm.relationship(Scaffold, backref=orm.backref("logs", cascade="all, delete-orphan"))
