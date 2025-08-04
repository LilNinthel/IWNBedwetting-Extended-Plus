from omutsulib.services.components_service import get_components_service, OmutsuComponentType
from omutsulib.services.resources_service import get_resource_service, OmutsuResourceType
from omutsulib.services.service import OmutsuService
from omutsulib.utils.math import split_int64, splice_int64, split_uint64, MIN_INT32, splice_int24, split_int24
from omutsulib.wrappers.sim.sim import OmutsuSim

class OmutsuCombinedStatisticsService(OmutsuService):

    def has_statistic(self, instance, statistic_id):
        high_statistic_id, low_statistic_id = split_uint64(statistic_id)
        high_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, high_statistic_id)
        low_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, low_statistic_id)
        if high_statistic_instance is not None and low_statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(high_statistic_instance)
                        if statistics_tracker is not None:
                            return statistics_tracker.has_statistic(high_statistic_instance) and statistics_tracker.has_statistic(low_statistic_instance)
                    return False

    def remove_statistic(self, instance, statistic_id):
        (high_statistic_id, low_statistic_id) = split_uint64(statistic_id)
        error_statistic_id = (high_statistic_id + low_statistic_id) // 2
        high_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, high_statistic_id)
        low_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, low_statistic_id)
        if high_statistic_instance is not None:
            if low_statistic_instance is not None:
                if hasattr(instance, "is_sim") and instance.is_sim:
                    omutsu_sim = OmutsuSim(instance)
                    if omutsu_sim is not None:
                        instance = omutsu_sim.get_sim_info()
                    if instance is not None:
                        statistics_component = get_components_service().get_object_component(instance, OmutsuComponentType.STATISTIC)
                        if statistics_component is not None:
                            statistics_tracker = statistics_component.get_tracker(high_statistic_instance)
                            if statistics_tracker is not None:
                                error_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, error_statistic_id)
                                statistics_tracker.remove_statistic(high_statistic_instance)
                                statistics_tracker.remove_statistic(low_statistic_instance)
                                if error_statistic_instance is not None:
                                    statistics_tracker.remove_statistic(error_statistic_instance)

    def set_statistic_value(self, instance, statistic_id, value, add=True):
        (high_statistic_id, low_statistic_id) = split_uint64(statistic_id)
        error_statistic_id = (high_statistic_id + low_statistic_id) // 2
        high_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, high_statistic_id)
        low_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, low_statistic_id)
        error_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, error_statistic_id)
        if high_statistic_instance is not None:
            if low_statistic_instance is not None:
                if error_statistic_instance is not None:
                    if hasattr(instance, "is_sim") and instance.is_sim:
                        omutsu_sim = OmutsuSim(instance)
                        if omutsu_sim is not None:
                            instance = omutsu_sim.get_sim_info()
                        if instance is not None:
                            statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                            if statistics_component is not None:
                                statistics_tracker = statistics_component.get_tracker(high_statistic_instance)
                                if statistics_tracker is not None:
                                    (high_value, low_value) = split_int64(int(value))
                                    high_e_value = float("{:e}".format(high_value))
                                    low_e_value = float("{:e}".format(low_value))
                                    high_err_value = 0
                                    low_err_value = 0
                                    if high_value != MIN_INT32:
                                        high_err_value = int(high_value - high_e_value)
                                        statistics_tracker.set_value(high_statistic_instance, high_e_value, add=add)
                                    else:
                                        statistics_tracker.remove_statistic(high_statistic_instance)
                                    if low_value != MIN_INT32:
                                        low_err_value = int(low_value - low_e_value)
                                        statistics_tracker.set_value(low_statistic_instance, low_e_value, add=add)
                                    else:
                                        statistics_tracker.remove_statistic(low_statistic_instance)
                                    if high_err_value != 0 or low_err_value != 0:
                                        err_value = splice_int24(high_err_value, low_err_value)
                                        statistics_tracker.set_value(error_statistic_instance, err_value, add=add)
                                    else:
                                        statistics_tracker.remove_statistic(error_statistic_instance)

    def get_statistic_value(self, instance, statistic_id, add=False, default=0):
        (high_statistic_id, low_statistic_id) = split_uint64(statistic_id)
        error_statistic_id = (high_statistic_id + low_statistic_id) // 2
        high_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, high_statistic_id)
        low_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, low_statistic_id)
        error_statistic_instance = get_resource_service().get_instance(OmutsuResourceType.STATISTIC, error_statistic_id)
        if high_statistic_instance is not None and low_statistic_instance is not None:
            if hasattr(instance, "is_sim") and instance.is_sim:
                omutsu_sim = OmutsuSim(instance)
                if omutsu_sim is not None:
                    instance = omutsu_sim.get_sim_info()
                if instance is not None:
                    statistics_component = get_components_service().get_object_component(instance, (OmutsuComponentType.STATISTIC), add_dynamic=True)
                    if statistics_component is not None:
                        statistics_tracker = statistics_component.get_tracker(high_statistic_instance)
                        if statistics_tracker is not None:
                            high_statistic = statistics_tracker.get_statistic(high_statistic_instance, add=add)
                            low_statistic = statistics_tracker.get_statistic(low_statistic_instance, add=add)
                            if high_statistic is not None or low_statistic is not None:
                                error_statistic = statistics_tracker.get_statistic(error_statistic_instance, add=add)
                                high_value = MIN_INT32
                                low_value = MIN_INT32
                                high_err_value = 0
                                low_err_value = 0
                                if error_statistic is not None:
                                    err_value = int(error_statistic.get_value())
                                    if err_value > 0:
                                        (high_err_value, low_err_value) = split_int24(err_value)
                                    if high_statistic is not None:
                                        high_e_value = high_statistic.get_value()
                                        high_e_value = float("{:e}".format(high_e_value))
                                        high_value = high_e_value + high_err_value
                                    if low_statistic is not None:
                                        low_e_value = low_statistic.get_value()
                                        low_e_value = float("{:e}".format(low_e_value))
                                        low_value = low_e_value + low_err_value
                                    return splice_int64(int(high_value), int(low_value))
                    return default


_COMBINED_STATISTICS_SERVICE = OmutsuCombinedStatisticsService("combined_statistics")

def get_combined_statistics_service() -> OmutsuCombinedStatisticsService:
    return _COMBINED_STATISTICS_SERVICE
