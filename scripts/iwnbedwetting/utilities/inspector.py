# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: C:\Users\Pilzkopf\Documents\Electronic Arts\Sims 4 Python Script Workspace\My Script Mods\IwnBedWetting_Python_3.3.5-3.7\Scripts\inspector.py
# Compiled at: 2017-10-20 10:48:12
# Size of source mod 2**32: 4470 bytes
import inspect
import os.path

from server_commands.tuning_commands import get_managers
from sims4.commands import Command, CheatOutput, CommandType
from sims4.resources import get_resource_key


@Command('inspect.custom', command_type=(CommandType.Live))
def custom_command(_connection=None):
    output = CheatOutput(_connection)
    output('inspect.custom running')
    try:
        IwnBedWetting_commodity_Motive_Bladder_Skill = get_tuning(11213649246133307228)
        IwnBedWetting_commodity_Motive_Bladder_Skill.decay_rate = 0.0734
        output('IwnBedWetting_commodity_Motive_Bladder_Skill decay {}'.format(IwnBedWetting_commodity_Motive_Bladder_Skill.decay_rate))
        output('** The play area is empty, add custom code to actually do something')
    except BaseException as e:
        try:
            for v in e.args:
                output('** Exception: {}'.format(v))

        finally:
            e = None
            del e

    output('inspect.custom finished')


def inspector_log(str):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'inspector.log')
    with open(filename, 'a') as fp:
        fp.write('{}\n'.format(str))


def resolve_attrs(tuning, attrs, output):
    cur_attr = tuning
    attrlist = attrs.split('.')
    for attr in attrlist:
        if hasattr(cur_attr, attr):
            cur_attr = getattr(tuning, attr)
        else:
            output('Attribute {} not found in tuning instance'.format(attr))
            return

    return cur_attr


def get_tuning(tuning_id):
    managers = get_managers()
    for name in managers:
        if name != 'objects':
            instance_manager = managers.get(name, None)
            key = get_resource_key(tuning_id, instance_manager.TYPE)
            tuning = instance_manager.get(key)
            if tuning:
                return tuning

    return tuning


def inspect_tuning(obj, output):
    for k, v in inspect.getmembers(obj):
        if not k.startswith('__'):
            output('  {}={}'.format(k, v))


@Command('inspect', command_type=(CommandType.Live))
def inspect_command(tuning_id: int=0, attrs='', _connection=None):
    output = CheatOutput(_connection)
    if tuning_id == 0:
        output('Must specify the tuning ID')
        return
    tuning = get_tuning(tuning_id)
    output('********************************************************************************')
    output('inspect {} {}'.format(tuning_id, attrs))
    output('{}'.format(tuning.__name__))
    output('********************************************************************************')
    if tuning is None:
        output('Tuning ID {} not found'.format(tuning_id))
        return
    if attrs != '':
        tuning = resolve_attrs(tuning, attrs, output)
    if tuning:
        inspect_tuning(tuning, output)


@Command('inspect.log', command_type=(CommandType.Live))
def log_command(tuning_id: int=0, attrs='', _connection=None):
    output = CheatOutput(_connection)
    if tuning_id == 0:
        output('Must specify the tuning ID')
        return
    tuning = get_tuning(tuning_id)
    if tuning is None:
        output('Tuning ID {} not found'.format(tuning_id))
        return
    inspector_log('********************************************************************************')
    name = tuning.__name__
    inspector_log('inspect.log {} {}'.format(tuning_id, attrs))
    inspector_log('{}'.format(name))
    inspector_log('********************************************************************************')
    if attrs != '':
        tuning = resolve_attrs(tuning, attrs, output)
    if tuning:
        inspect_tuning(tuning, inspector_log)
        output('Logged inspection of {} {}'.format(name, attrs))