from peewee import *
from playhouse.mysql_ext import MySQLDatabase
from .config import config_poll_db
import datetime
from emojis import EmojiList

db_config = config_poll_db()

HOST = db_config["host"]
MYSQL_USERNAME = db_config["user"]
MYSQL_PASSWORD = db_config["password"]
DB_NAME = db_config["database"]

db = MySQLDatabase(
    host=HOST,
    user=MYSQL_USERNAME,
    password=MYSQL_PASSWORD,
    database=DB_NAME
)

class BaseModel(Model):
    class Meta:
        database = db

class Poll(BaseModel):
    poll_id = BigIntegerField(null=False, primary_key=True) # Primary Key
    poll_name = CharField(null=False, max_length=256) # Poll question
    up_vote_count = IntegerField(null=False, default=0)
    down_vote_count = IntegerField(null=False, default=0)
    shrug_vote_count = IntegerField(null=False, default=0)
    poll_creator = CharField(null=False, max_length=255)
    create_date = DateTimeField(default=datetime.datetime.now) # Date created

class Options(BaseModel):
    option_id = AutoField() # Primary Key
    option_name = CharField(null=False, max_length=128)
    # Foreign Key pointing back to poll table
    poll_id = ForeignKeyField(Poll)

# Initialize database tables
def init_tables():
    try:
        print('Creating tables...\t', end='')
        db.connect(reuse_if_open=True)
        db.create_tables([Poll, Options])
        db.close()
        print('SUCCESS')
    except Exception as err:
        print(err)
        db.close()

# Inserts a new poll into the DB
def create_new_poll(msg_id, poll_title, creator):
    try:
        print('Inserting poll...', end='')
        db.connect(reuse_if_open=True)
        poll = Poll.create(poll_id=msg_id, poll_name=poll_title, poll_creator=creator)
        db.close()
        print('SUCCESS')
        return poll
    except Exception as e:
        print(e)
        db.close()
        return None

# Insert a new option into the DB
def create_new_option(option_title, msg_id):
    try:
        print('Inserting option...', end='')
        db.connect(reuse_if_open=True)
        option = Options.create(option_name=option_title, poll_id=msg_id)
        db.close()
        print('SUCCESS')
        return option
    except Exception as err:
        print(err)
        db.close()
        return None

def drop_tables():
    MODELS = (Poll, Options)
    try:
        print('Dropping tables...\t', end='')
        db.connect(reuse_if_open=True)
        db.drop_tables(MODELS)
        db.close()
        print('SUCCESSFUL')
    except Exception as err:
        print(err)
        db.close()
        return None