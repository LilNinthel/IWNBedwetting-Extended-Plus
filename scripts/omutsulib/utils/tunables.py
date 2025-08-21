import sims4.collections


def create_tunable_instance(tunable_class, *args, **kwargs):
    tunable_template = tunable_class(*args)._template
    tunable_arguments = dict(((k, v.default) for (k, v) in tunable_template.tunable_items.items()))
    (tunable_arguments.update)(**kwargs)
    return tunable_template._create_dict(tunable_arguments, ())


def dictionary_to_immutable_slots(items):
    immutable_slots_cls = sims4.collections.make_immutable_slots_class(items.keys())
    return immutable_slots_cls(items)
