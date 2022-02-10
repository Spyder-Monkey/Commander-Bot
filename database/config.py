from configparser import ConfigParser
import os

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def config_poll_db(filename=DIR+'\database\database.ini', section='mysql_poll'):
    # create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the file {1}'.format(section, filename))

    return db
