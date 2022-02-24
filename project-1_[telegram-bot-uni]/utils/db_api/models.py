from utils.db_api.db import Ops
from loader import db
import peewee as pw


class BaseModel(pw.Model):
    class Meta:
        database = db


class Groups(BaseModel, Ops):
    group_id = pw.BigIntegerField(unique=True, primary_key=True)
    group_title = pw.CharField()
    group_major = pw.CharField()
    group_user_id = pw.CharField()


class User(BaseModel, Ops):
    username = pw.CharField(default=None, null=True)
    first_name = pw.CharField()
    last_name = pw.CharField()
    phoneNumber = pw.CharField()
    email = pw.CharField()
    learningYear = pw.IntegerField()
    Major = pw.CharField()
    user_id = pw.CharField(primary_key=True)
    role = pw.CharField(default=None, null=True)
    is_approve = pw.BooleanField(default=False, null=True)


class PostApproval(BaseModel, Ops):
    post_user_id = pw.CharField()
    post_message_id = pw.CharField(primary_key=True)
    post_chat_ids = pw.CharField()


db.create_tables([PostApproval, Groups, User])  # TODO Autoloader for tables
