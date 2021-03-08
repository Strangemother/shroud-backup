from base import TypedRequestDevice, respond
import os
from pathlib import Path


cache = {}

import os
import subprocess, platform

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')


def explore(path, in_front=True):

    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        return subprocess.run([FILEBROWSER_PATH, path], shell=in_front)

    if os.path.isfile(path):
        return subprocess.run([FILEBROWSER_PATH, '/select,', path], shell=in_front)



def open_file(filepath):
    if platform.system() == 'Darwin':       # macOS
        return subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        path = os.path.normpath(filepath)
        return subprocess.run([FILEBROWSER_PATH, path], shell=True)
        # return subprocess.run(v)
        # return os.startfile(filepath)
    else:                                   # linux variants
        return subprocess.call(('xdg-open', filepath))


class EntryAction(object):
    """
    Routines for the Action Panel relative to a given file or folder.
    """
    async def from_dir(self, directory):

        res = {
            'caption': 'A Directory'
            , 'tools': await self.get_dir_tools(directory)
        }

        return { 'actions': res }

    async def from_packet(self, packet):
        """Given a file entry packet, return a dictionary of actions.
        """
        res = {
            'caption': 'A file'
            , 'tools': await self.get_file_tools(packet)
        }

        return {'actions': res }

    async def get_dir_tools(self, directory):
        return [
            'store',
            'tag',
            'locate',
        ]

    async def get_file_tools(self, packet):
        """Return an array of tools for the action panel.
        """
        return [
            'store',
            'tag',
            'open',
            {'label': 'reveal', 'action': 'locate'},
        ]


from base import post_json

class OpenFileMixin(object):

    async def run_open_task(self, packet):
        info = packet.get_json()
        path = Path(info.get('path'))
        sp = open_file(path)
        print(sp)


class Action(TypedRequestDevice, OpenFileMixin):

    async def run_store_tags_task(self, packet):
        info = packet.get_json()
        path = Path(info.get('path'))
        tags = info.get('tags', [])
        # send JSON message to store tags of path
        print('path', path, 'tags', tags)
        v = await post_json('tags/', info)
        print(v)
        return await respond(packet, {})

    async def run_locate_task(self, packet):
        info = packet.get_json()
        path = Path(info.get('path'))
        sp = explore(path)
        print('Explorer Open', sp.returncode, sp.stderr, sp.stdout)
        # sp.kill()

class Directory(TypedRequestDevice, OpenFileMixin):

    async def run_entry_task(self, packet):
        """An directory 'entry' request from a panel to present the
        directory subcontent list or file information.
        """
        info = packet.get_json()
        loc = info.get('path')
        locpath = Path(loc)

        if locpath.is_file():
            return await self.run_file_task(packet, filepath=locpath)

        return await self.run_volume_task(packet)

    async def run_file_task(self, packet, filepath=None):

        if filepath is None:
            print('IS FILE')
            info = packet.get_json()
            loc = info.get('path')
            filepath = Path(loc)

        ea = EntryAction()
        res = await ea.from_packet(packet)
        res['path'] = self.path_stat(filepath)
        return await respond(packet, res)

    async def run_volume_task(self, packet):
        print('Directory', packet)
        # Respond with a list of info
        info = packet.get_json()
        loc = info.get('path')
        path = f"{loc}\\"

        try:
            res = await self.cache_get_files(path)
        except PermissionError as pe:
            res = {
                'error': str(pe)
            }

        await respond(packet, res)

    async def cache_get_files(self, directory):
        data = cache.get(directory, None)

        if data is None:
            data = await self.recache_files(directory)
        return data

    async def recache_files(self, directory):
        items = await self.get_files(directory)
        res = {'path': directory, 'items': items}
        ea = EntryAction()
        ac = await ea.from_dir(directory)
        res.update(ac)
        cache[directory] = res
        return res

    async def get_files(self, directory):
        # info = packet.get_json()

        try:
            scanned = os.scandir(directory)
        except PermissionError as pe:
            print('Cannot access', directory, pe)
            raise pe
            # return ()
        res = ()

        for entry in scanned:
            res += (self.path_stat(entry), )
        return res

    def path_stat(self, entry, stat=None):
        path = entry.path if hasattr(entry, 'path') else entry
        stat = stat or os.stat(path)
        # print('PAth', entry, dir(entry))
        return (entry.name,
            # path,
            entry.is_file(),
            stat.st_size,
            # stat.st_atime,
            stat.st_mtime,
            stat.st_ctime,
            )

    # async def async_depth(directory, depth=2, _current=0, stat_func=None):
    #     res = ()
    #     stat_func = stat_func or file_entry

    #     try:
    #         scanned =  os.scandir(directory)
    #     except PermissionError as pe:
    #         print('Cannot access', directory, pe)
    #         return (stat_func(Path(directory), directory), )

    #     for entry in scanned:
    #         path = entry.path

    #         if (_current < depth) and entry.is_dir():
    #             res += await async_depth(
    #                 path, depth,
    #                 _current+1,
    #                 stat_func=stat_func
    #                 )
    #             continue
    #         res += (stat_func(entry, path), )
    #     return res
