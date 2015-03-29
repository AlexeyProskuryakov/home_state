# coding:utf-8
from web.storage import DataBaseHandler

__author__ = '4ikist'

if __name__ == '__main__':
    dbh = DataBaseHandler()
    s1 = {'name': 'sensor_1', 'description': 'some sensor with number 1', 'type': 'some type', 'foo': 'bar'}
    s2 = {'name': 'sensor_2', 'description': 'some sensor with number 2', 'type': 'some type', 'foo': 'bar'}
    s1_id = dbh.add_sensor(s1)
    s2_id = dbh.add_sensor(s2)

    u1 = {'name': 'user_1', 'description': 'some user with number 1', 'email': 'user.1@gmail.com'}
    u2 = {'name': 'user_2', 'description': 'some user with number 2', 'email': 'user.2@gmail.com'}
    u3 = {'name': 'user_3', 'description': 'some user with number 3', 'email': 'user.3@gmail.com'}
    u4 = {'name': 'user_4', 'description': 'some user with number 4', 'email': 'user.4@gmail.com'}

    u1_id = dbh.add_user(u1)
    u2_id = dbh.add_user(u2)
    u3_id = dbh.add_user(u3)
    u4_id = dbh.add_user(u4)

    dbh.add_sensor_to_user(u1_id, s1_id)
    dbh.add_sensor_to_user(u1_id, s2_id)

    user_1 = dbh.get_user(u1_id)
    assert 'email' in user_1 and u1['email'] == user_1['email'] and 'name' in user_1 and user_1['name'] == u1['name']

    for sensor in dbh.get_user_sensors(u1_id):
        assert sensor in [s1, s2]