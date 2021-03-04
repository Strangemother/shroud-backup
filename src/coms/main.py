from serv.server.host import *
from serv.server.devices import Device


def automain():
    print('Stack device Recv')
    host.broadcast_mode = True
    host.devices += (Recv(), Drives(),)


class Recv(Device):

    async def read_packet(self, packet):
        print('Recv(device) packet', packet)
        info = packet.get_json()
        print(info)

from disks.simple import get_drives_bit
from disks.complex import get_logical

import json
import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


class Drives(Device):
    """Given a message through the devices read_packet, capture "key == drives"
    to run the attached task. The "type" defines the input request.

        {'type': 'request', 'key': 'drives', '_id': '0.5fi0r2ap2oo'}
    """
    mine_key = 'key'
    bits = None
    logical = None

    fields = (
            ("Caption", "string",),
            ("Compressed", "boolean",),
            ("FreeSpace", "uint64",),
            ("Name", "string",),
            ("ProviderName", "string",),
            ("Size", "uint64",),
            ("SystemName", "string",),
            ("VolumeName", "string",),

            # 3 HDD, 4 NETWORK HDD, 5, CDROM
            ("DriveType", "uint32",),
        )

    types = {
        0: "Unknown",
        1: "No Root Directory",
        2: "Removable Disk",
        3: "Local Disk",
        4: "Network Drive",
        5: "Compact Disc",
        6: "RAM Disk",
    }

    async def run_task(self, packet):
        """Run the task as an event expected for this type.
        """
        info = packet.get_json()
        print('Run drives request', info)

        if self.logical is None:
            # DB collect,
            # Assert Update (simple)
            await self.send_bits(packet)
        await self.send_logical(packet)

    async def send_bits(self, packet):
        bits = self.bits or get_drives_bit()
        _id = packet.get_json().get('_id')
        await packet.owner.send_text(
            json.dumps({'letters': bits, '_id': _id})
            )
        self.bits = bits

    async def send_logical(self, packet):
        # Push Update if required (complex.)
        logical = self.get_logical_content()
        _id = packet.get_json().get('_id')
        await packet.owner.send_text(
            json.dumps({'logical': logical, '_id': _id})
            )

    def get_logical_content(self):
        if self.logical:
            return self.logical

        logical = self.logical or get_logical(self.fields)

        for item in logical:
            item['size_str'] = convert_size(int(item['size'] or '0'))
            item['free_space_str'] = convert_size(int(item['free_space'] or '0'))
            item['drive_type_str'] = self.types.get(item['drive_type'])
        self.logical = logical

        return logical

automain()
