from caches import cached_test
from event_testing.resolver import SingleSimResolver, DoubleSimResolver
from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from event_testing.test_based_score_threshold import TestBasedScoreThresholdTest
from event_testing.test_variants import SituationRunningTest
from event_testing.tests import TestList, CompoundTestList
from relationships.relationship_tests import RelationshipTest
from sims.sim_info_tests import SimInfoTest, TraitTest, BuffTest
from sims4.math import Threshold, Operator
OmutsuThreshold = Threshold
OmutsuOperator = Operator
OmutsuBaseTest = BaseTest
OmutsuTestList = TestList
OmutsuCompoundTestList = CompoundTestList
OmutsuTestResult = TestResult
omutsu_cached_test = cached_test
OmutsuSimInfoTest = SimInfoTest
OmutsuTraitTest = TraitTest
OmutsuBuffTest = BuffTest
OmutsuRelationshipTest = RelationshipTest
OmutsuSituationRunningTest = SituationRunningTest
OmutsuBasedScoreThresholdTest = TestBasedScoreThresholdTest
OmutsuSingleSimResolver = SingleSimResolver
OmutsuDoubleSimResolver = DoubleSimResolver
POSITIVE_TEST_RESULT = OmutsuTestResult.TRUE
NEGATIVE_TEST_RESULT = OmutsuTestResult.NONE
