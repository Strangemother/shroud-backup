import json

from serv.server.devices import Device
import requests


class TypedRequestDevice(Device):
    mine_key = 'key'

    async def run_task(self, packet):
        """Run the task as an event expected for this type.
        """
        info = packet.get_json()
        _type = info.get('type', 'request')
        name = f'run_{_type}_task'

        if hasattr(self, name):
            return await getattr(self, name)(packet)


async def post_json(path, content):
    try:
        data = json.dumps(content)
    except Exception as exc:
        import pdb; pdb.set_trace()  # breakpoint 3cee3398x //

    v = requests.post(f'http://127.0.0.1:10002/{path}', data=data)
    return v


async def respond(packet, data=None, **options):
    _id = packet.get_json().get('_id')
    d = {'_id': _id }
    d.update(data or {}, **options)
    await packet.owner.send_text(json.dumps(d))
