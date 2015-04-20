from app import cm
from boto.dynamodb2.table import Table

tb_stops = Table('stops', connection=cm.db)
tb_stops_loc = Table('stops_loc', connection=cm.db)
tb_users = Table('users', connection=cm.db)
tb_test = Table('test', connection=cm.db)
tb_schedule = Table('schedule', connection=cm.db)
