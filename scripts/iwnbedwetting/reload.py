# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\Users\Pilzkopf\Documents\Electronic Arts\Sims 4 Python Script Workspace\My Script Mods\IwnBedWetting_Python_3.3.5-3.7\Scripts\reload.py
# Compiled at: 2017-06-29 21:34:52
# Size of source mod 2**32: 801 bytes
import sims4.commands
import sims4.reload as r
import os.path

@sims4.commands.Command('reload', command_type=(sims4.commands.CommandType.Live))
def reload_maslow(module: str, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        dirname = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dirname, module) + '.py'
        output('Reloading {}'.format(filename))
        reloaded_module = r.reload_file(filename)
        if reloaded_module is not None:
            output('Done reloading!')
        else:
            output('Error loading module or module does not exist')
    except BaseException as e:
        try:
            output('Reload failed: ')
            for v in e.args:
                output(v)

        finally:
            e = None
            del e