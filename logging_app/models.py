# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import mongoengine
from mongoengine import Document, EmbeddedDocument, fields
import uuid

# Create your models here.
class Users(Document):
    username = fields.StringField(max_length=200,primary_key=True)
    email = fields.StringField(max_length=200)
    password = fields.StringField(max_length=200)
    def __str__(self):
        return self.username

class Session(Document):
    id = fields.StringField(primary_key=True)
    username = fields.ReferenceField(Users, reverse_delete_rule=mongoengine.CASCADE)
    status = fields.BooleanField(default=False)
    loginTime = fields.DateTimeField(default=datetime.now, blank=True)
    logoutTime = fields.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.username
    
class Events(Document):
    username = fields.ReferenceField(Users, reverse_delete_rule=mongoengine.CASCADE)
    sessionId = fields.ReferenceField(Session, reverse_delete_rule=mongoengine.CASCADE)
    action = fields.StringField(max_length=200)
    attribute = fields.DictField()
    eventTime = fields.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return '%s %s' % (self.username, self.action)