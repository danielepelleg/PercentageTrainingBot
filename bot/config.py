from configparser import ConfigParser

def config(filename = 'database.ini', section='production'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    
    # get section, default to postgresql
    db = {}
    if parser._sections[section]:
        db = parser._sections[section]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
