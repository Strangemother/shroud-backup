import os
from pathlib import Path

from serv.server.host import *
from serv.server.devices import Device
from base import TypedRequestDevice, respond
import disk_device
import directory_device


def automain():
    print('Stack device Recv')
    host.broadcast_mode = True
    host.devices += (
        Recv(),
        disk_device.Drives(),
        Name(),
        directory_device.Action(),
        directory_device.Directory(),
        )


class Name(TypedRequestDevice):
    """Given a message through the devices read_packet, capture "key == drives"
    to run the attached task. The "type" defines the input request.

        {'type': 'request', 'key': 'drives', '_id': '0.5fi0r2ap2oo'}
    """

    async def run_store_task(self, packet):
        """Store the give list of drives as the _definitive_ list of disks
        to monitor.
        """

        info = packet.get_json()
        name = info.get('name')
        print('\nStore name', name)
        # v = requests.post('http://127.0.0.1:10002/drives/', data=data)
        # await packet.owner.send_text(d)
        await respond(packet, {'name': name})



class Recv(Device):

    async def read_packet(self, packet):
        print('Recv(device) packet', packet)
        info = packet.get_json()
        print(info)




automain()
