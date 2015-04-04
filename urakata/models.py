# -*- coding:utf-8 -*-
import logging
import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime
from pyramid_sqlalchemy import BaseObject as Base
logger = logging.getLogger(__name__)


class TimeMixin(object):
    ctime = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    utime = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)


class Repository(TimeMixin, Base):
    __tablename__ = "repository"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=255), default="", nullable=False, unique=True)


class Scaffold(TimeMixin, Base):
    __tablename__ = "scaffold"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=255), default="", nullable=False, unique=True)
    repository_id = sa.Column(sa.Integer, sa.ForeignKey("repository.id"))
    repository = orm.relationship(Repository, backref=orm.backref("scaffolds", cascade="all, delete-orphan"))


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
    name = sa.Column(sa.String(length=255), default="", nullable=False)
    scaffold_id = sa.Column(sa.Integer, sa.ForeignKey("scaffold.id"))


class TemplateHistory(TimeMixin, Base):
    __tablename__ = "template_history"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=255), default="", nullable=False)
    content = sa.Column(sa.Text, nullable=False, default="")
    input_encoding = sa.Column(sa.String(length=16), nullable="False", default="utf-8")
    output_encoding = sa.Column(sa.String(length=16), nullable="False", default="utf-8")
    template_id = sa.Column(sa.Integer, sa.ForeignKey("scaffold.id"))
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
