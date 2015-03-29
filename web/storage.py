# coding:utf-8
from bson.dbref import DBRef
from pymongo import MongoClient
import hashlib

__author__ = '4ikist'


def password_hash(password):
    return hashlib.md5().update(password).hexdigest()


class DataError(Exception):
    pass


sensor_collection = 'sensors'
user_collection = 'users'


class DataBaseHandler(object):
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['home_state']
        self.sensors = self.db[sensor_collection]
        self.users = self.db[user_collection]

    def add_sensor(self, sensor_data):
        sensor_id = self.sensors.insert(sensor_data)
        return sensor_id

    def add_user(self, user_data):
        user_id = self.users.insert(user_data)
        return user_id

    def add_sensor_to_user(self, user_id, sensor_id):
        user = self.get_user(user_id)

        sensors = user.get('sensors', [])
        sensors.append(DBRef(sensor_collection, sensor_id))
        user['sensors'] = sensors
        self.users.save(user)

    def get_user(self, user_id):
        user = self.users.find_one({'_id': user_id})
        return user

    def get_user_sensors(self, user_id):
        user = self.get_user(user_id)
        if user is None:
            raise DataError('user is not exists')

        for sensor in user.get('sensors', []):
            yield self.db.dereference(sensor)


    def is_user_exists(self, username):
        user = self.users.find_one({'username': username})
        return user is not N

    def check_user(self, username, password):
        user = self.users.find_one({'username': username})
        if not user: return False
        phash = user.get('phash')
        if phash == password_hash(password):
            return user.get('_id')
        return False

