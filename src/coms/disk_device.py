from serv.server.devices import Device

from disks.simple import get_drives_bit
from disks.complex import get_logical
from base import post_json, respond

import json
import math

import requests

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
        _type = info.get('type', 'request')
        name = f'run_{_type}_task'

        if hasattr(self, name):
            return await getattr(self, name)(packet)

    async def run_request_task(self, packet):
        """send the logical of this local machine
        """
        if self.logical is None:
            # DB collect,
            # Assert Update (simple)
            await self.send_bits(packet)
        await self.send_logical(packet)

    async def run_store_task(self, packet):
        """Store the give list of drives as the _definitive_ list of disks
        to monitor.
        """
        info = packet.get_json()
        drives = info.get('drives')
        print('\nStore drives', len(drives))

        v = post_json('drives/', drives)

        # await packet.owner.send_text(d)
        await respond(packet, v.json())

    async def send_bits(self, packet):
        bits = self.bits or get_drives_bit()
        await respond(packet, {'letters': bits})
        self.bits = bits

    async def send_logical(self, packet):
        # Push Update if required (complex.)
        logical = self.get_logical_content()
        await respond(packet, logical=logical)

    def get_logical_content(self):
        if self.logical:
            return self.logical

        logical = get_logical(self.fields)
        self.logical = self.clean_logicals(logical)
        return logical

    def clean_logicals(self, logical):
        for item in logical:
            item['size_str'] = convert_size(int(item['size'] or '0'))
            item['free_space_str'] = convert_size(int(item['free_space'] or '0'))
            item['size'] = int(item['size'] or '0')
            item['free_space'] = int(item['free_space'] or '0')
            item['drive_type_str'] = self.types.get(item['drive_type'])


