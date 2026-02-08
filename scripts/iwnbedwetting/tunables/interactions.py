import sims4.resources
from traits.trait_tracker import TraitPickerSuperInteraction
from omutsulib.enums.traits import IwnBedwettingTrait
import services


class IwnBedwettingTraitPickerSuperInteraction(TraitPickerSuperInteraction):
    
    @classmethod
    def _trait_selection_gen(cls, target):
        trait_manager = services.get_instance_manager(sims4.resources.Types.TRAIT)
        trait_tracker = target.sim_info.trait_tracker

        target_traits = set()
        target_traits.add(IwnBedwettingTrait.INCONTINENCE)
        target_traits.add(IwnBedwettingTrait.BEDWETTER)
        target_traits.add(IwnBedwettingTrait.PANTS_WETTER)
        target_traits.add(IwnBedwettingTrait.PANTS_POOPER)
        target_traits.add(IwnBedwettingTrait.DESPERATION_ENTHUSIAST)
        target_traits.add(IwnBedwettingTrait.TOILET_BAN)
        target_traits.add(IwnBedwettingTrait.DIAPERED_247)
        target_traits.add(IwnBedwettingTrait.NO_MESSY_DIAPERS)
        target_traits.add(IwnBedwettingTrait.DIAPER_CURIOUS)
        target_traits.add(IwnBedwettingTrait.NEVER_POTTY_TRAINED)
        target_traits.add(IwnBedwettingTrait.MACKICO_ABDL)
        target_traits.add(IwnBedwettingTrait.HAPPILY_MESSY)
        target_traits.add(IwnBedwettingTrait.LOVES_DIAPERS)
        target_traits.add(IwnBedwettingTrait.UNHAPPILY_DIAPERED)
        target_traits.add(IwnBedwettingTrait.LITTLE)
        target_traits.add(IwnBedwettingTrait.DIAPER_DEPENDENT)
        target_traits.add(IwnBedwettingTrait.UNIVERSAL_CAREGIVER)
        target_traits.add(IwnBedwettingTrait.HATES_DIAPER_CHANGES)
        target_traits.add(IwnBedwettingTrait.RASH_PROOF)
        target_traits.add(IwnBedwettingTrait.PEES_DURING_CHANGES)
        target_traits.add(IwnBedwettingTrait.NO_SELF_DIAPER_CHANGES)
        target_traits.add(IwnBedwettingTrait.HYPERACTIVE_BLADDER)
        target_traits.add(IwnBedwettingTrait.TOTAL_URINARY_INCONTINENCE)
        target_traits.add(IwnBedwettingTrait.DIAPERED_247_MEDICAL)
        target_traits.add(IwnBedwettingTrait.SLEEPS_IN_DIAPERS)

        traits = {trait_manager.get(trait_id) for trait_id in target_traits}
        
        if cls.is_add:
            for trait in traits:
                if trait is None:
                    continue
                if not cls._match_trait_type(trait):
                    pass
                elif trait.sim_info_fixup_actions:
                    pass
                elif trait_tracker.can_add_trait(trait) or not trait_tracker.has_trait(trait) or cls.already_equipped_tooltip is not None:
                    yield trait
        else:
            for trait in traits:
                if trait is None:
                    continue
                if not cls._match_trait_type(trait):
                    pass
                elif not trait_tracker.has_trait(trait):
                    pass
                else:
                    yield trait