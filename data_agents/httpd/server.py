import json
import datetime
import asyncio


from aiohttp import web
import aiorest

from dateutil.parser import parse as parse_datetime

from aiopg.pool import create_pool


import settings


loop = asyncio.get_event_loop()
server = aiorest.RESTServer(hostname=settings.BIND, loop=loop)
pool = loop.run_until_complete(create_pool(settings.DSN))


@asyncio.coroutine
def accept_hub_state(request):
    hub_packet = request.json_body

    if 'generated' not in hub_packet:
        return {
            'status': 'error',
            'reason': 'generated field is not presented in hub packet'
        }

    generated = hub_packet['generated']
    raw_hub_packet = request._request_body.decode('utf-8')
    device_id = request.matchdict['id']

    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute('''
            insert into hubs_data(hub_id, hub_data, generated)
            values (%s, %s, %s)
            returning id;
        ''', (device_id, raw_hub_packet, generated))
        recid, = yield from cur.fetchone()
    return {'status': 'ok', 'recid': recid}


@asyncio.coroutine
def get_data_by_time_range(hub_id, from_date, to_date, cursor):
    return (yield from cur.fetchall())


@asyncio.coroutine
def get_data_by_seq_range(hub_id, from_seq, to_seq, cursor):
    return (yield from cur.fetchall())



@asyncio.coroutine
def get_hub_state(request):
    hub_id = request.matchdict['id']
    now = datetime.datetime.now()

    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date', now.isoformat())

    # for synchronisation purposes
    from_seq = int(request.args.get('from_seq', '0'))
    to_seq = int(request.args.get('to_seq', '0'))


    with (yield from pool) as conn:
        cur = yield from conn.cursor()

        if from_date and to_date:
            from_date = parse_datetime(from_date)
            to_date = parse_datetime(to_date)
            where = '''generated BETWEEN %s AND %s'''
            params = (hub_id, from_date, to_seq)
        elif from_seq and to_seq:
            where = '''id BETWEEN %s and %s'''
            params = (hub_id, from_seq, to_seq)
        else:
            return {
                'status': 'error',
                'reason': 'missing from_date-to_date or '
                            'from_seq-to_seq params'
            }

    yield from cur.execute('''
            SELECT id, hub_data, accepted, generated
            FROM hubs_data
            WHERE
                hub_id = %s AND
                {where}
    '''.format(where=where), params)

    ret = yield from cur.fetchall()

    def update_data_item(data, recid, accepted, generated):
        data.update({
            'accepted': accepted.isoformat(),
            'generated': generated.isoformat(),
            'seq': recid
        })
        return data

    return {'state': [
        update_data_item(data, recid, accepted, generated)
        for recid, data, accepted, generated in ret
    ]}


server.add_url('POST', '/hubs/{id}', accept_hub_state)
server.add_url('GET', '/hubs/{id}', get_hub_state)

srv = loop.run_until_complete(loop.create_server(
    server.make_handler,
    settings.BIND,
    settings.PORT
))

try:
    loop.run_forever()
except KeyboardInterupt:
    pass
