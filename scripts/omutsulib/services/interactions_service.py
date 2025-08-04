from omutsulib.services.service import OmutsuService
from omutsulib.wrappers.enum import OmutsuIntEnum, OmutsuLongFlagsEnum

class OmutsuPriority(OmutsuIntEnum):
    Low = 1
    High = 2
    Critical = 3


class OmutsuQueueInsertStrategy(OmutsuIntEnum):
    LAST = 0
    NEXT = 1
    FIRST = 2


class OmutsuFinishingType(OmutsuIntEnum):
    KILLED = 0
    AUTO_EXIT = 1
    DISPLACED = 2
    NATURAL = 3
    RESET = 4
    USER_CANCEL = 5
    SI_FINISHED = 6
    TARGET_DELETED = 7
    FAILED_TESTS = 8
    TRANSITION_FAILURE = 9
    INTERACTION_INCOMPATIBILITY = 10
    INTERACTION_QUEUE = 11
    PRIORITY = 12
    SOCIALS = 13
    WAIT_IN_LINE = 14
    OBJECT_CHANGED = 15
    SITUATIONS = 16
    CRAFTING = 17
    LIABILITY = 18
    DIALOG = 19
    CONDITIONAL_EXIT = 20
    FIRE = 21
    WEDDING = 22
    ROUTING_FORMATION = 23
    UNKNOWN = 24


class OmutsuInteractionSource(OmutsuIntEnum):
    PIE_MENU = 0
    AUTONOMY = 1
    BODY_CANCEL_AOP = 2
    CARRY_CANCEL_AOP = 3
    SCRIPT = 4
    UNIT_TEST = 5
    POSTURE_GRAPH = 6
    SOCIAL_ADJUSTMENT = 7
    REACTION = 8
    GET_COMFORTABLE = 9
    SCRIPT_WITH_USER_INTENT = 10
    VEHICLE_CANCEL_AOP = 11


class OmutsuInteractionContext:
    SOURCE_PIE_MENU = OmutsuInteractionSource.PIE_MENU
    SOURCE_AUTONOMY = OmutsuInteractionSource.AUTONOMY
    SOURCE_BODY_CANCEL_AOP = OmutsuInteractionSource.BODY_CANCEL_AOP
    SOURCE_CARRY_CANCEL_AOP = OmutsuInteractionSource.CARRY_CANCEL_AOP
    SOURCE_SCRIPT = OmutsuInteractionSource.SCRIPT
    SOURCE_UNIT_TEST = OmutsuInteractionSource.UNIT_TEST
    SOURCE_SOCIAL_ADJUSTMENT = OmutsuInteractionSource.SOCIAL_ADJUSTMENT
    SOURCE_REACTION = OmutsuInteractionSource.REACTION
    SOURCE_GET_COMFORTABLE = OmutsuInteractionSource.GET_COMFORTABLE
    SOURCE_VEHICLE_CANCEL_AOP = OmutsuInteractionSource.VEHICLE_CANCEL_AOP
    SOURCE_SCRIPT_WITH_USER_INTENT = OmutsuInteractionSource.SCRIPT_WITH_USER_INTENT
    SOURCE_POSTURE_GRAPH = OmutsuInteractionSource.POSTURE_GRAPH
    TRANSITIONAL_SOURCES = frozenset((SOURCE_SOCIAL_ADJUSTMENT, SOURCE_GET_COMFORTABLE, SOURCE_POSTURE_GRAPH))


class OmutsuParticipantType(OmutsuLongFlagsEnum):
    Invalid = 0
    Actor = 1
    Object = 2
    TargetSim = 4
    Listeners = 8
    All = 16
    AllSims = 32
    Lot = 64
    CraftingProcess = 128
    JoinTarget = 256
    CarriedObject = 512
    Affordance = 1024
    InteractionContext = 2048
    CustomSim = 4096
    AllRelationships = 8192
    CraftingObject = 16384
    ActorSurface = 32768
    ObjectChildren = 65536
    LotOwners = 131072
    CreatedObject = 262144
    PickedItemId = 524288
    StoredSim = 1048576
    PickedObject = 2097152
    SocialGroup = 4194304
    OtherSimsInteractingWithTarget = 8388608
    PickedSim = 16777216
    ObjectParent = 33554432
    SignificantOtherActor = 67108864
    SignificantOtherTargetSim = 134217728
    OwnerSim = 268435456
    StoredSimOnActor = 536870912
    Unlockable = 1073741824
    LiveDragActor = 2147483648
    LiveDragTarget = 4294967296
    PickedZoneId = 8589934592
    SocialGroupSims = 17179869184
    PregnancyPartnerActor = 34359738368
    PregnancyPartnerTargetSim = 68719476736
    SocialGroupAnchor = 137438953472
    TargetSurface = 274877906944
    ActiveHousehold = 549755813888
    ActorPostureTarget = 1099511627776
    InventoryObjectStack = 2199023255552
    AllOtherInstancedSims = 4398046511104
    CareerEventSim = 8796093022208
    StoredSimOnPickedObject = 17592186044416
    SavedActor1 = 35184372088832
    SavedActor2 = 70368744177664
    SavedActor3 = 140737488355328
    SavedActor4 = 281474976710656
    LotOwnerSingleAndInstanced = 562949953421312
    LinkedPostureSim = 1125899906842624
    AssociatedClub = 2251799813685248
    AssociatedClubMembers = 4503599627370496
    AssociatedClubLeader = 9007199254740992
    AssociatedClubGatheringMembers = 18014398509481984
    ActorEnsemble = 36028797018963968
    TargetEnsemble = 72057594037927936
    TargetSimPostureTarget = 144115188075855872
    ActorEnsembleSansActor = 288230376151711744
    ActorDiningGroupMembers = 576460752303423488
    TableDiningGroupMembers = 1152921504606846976
    StoredSimOrNameData = 2305843009213693952
    TargetDiningGroupMembers = 4611686018427387904
    LinkedObjects = 9223372036854775808
    RoutingMaster = 18446744073709551616
    RoutingSlaves = 36893488147419103232
    SituationParticipants1 = 73786976294838206464
    SituationParticipants2 = 147573952589676412928
    ObjectCrafter = 295147905179352825856
    MissingPet = 590295810358705651712
    TargetTeleportPortalObjectDestinations = 1180591620717411303424
    ActorFeudTarget = 2361183241434822606848
    TargetFeudTarget = 4722366482869645213696
    ActorSquadMembers = 9444732965739290427392
    TargetSquadMembers = 18889465931478580854784
    AllInstancedSims = 37778931862957161709568
    StoredObjectsOnActor = 75557863725914323419136
    StoredObjectsOnTarget = 151115727451828646838272
    ObjectInventoryOwner = 302231454903657293676544
    LotOwnersOrRenters = 604462909807314587353088
    ActorFiance = 1208925819614629174706176
    TargetFiance = 2417851639229258349412352
    RandomInventoryObject = 4835703278458516698824704
    SituationParticipants3 = 9671406556917033397649408
    Familiar = 19342813113834066795298816
    ObjectProvidingTargetAffordance = 38685626227668133590597632
    StoredSimOnObjectProvidingTargetAffordance = 77371252455336267181195264
    PhotographyTargets = 154742504910672534362390528
    FamiliarOfTarget = 309485009821345068724781056
    PickedStatistic = 618970019642690137449562112
    ActorHousehold = 1237940039285380274899124224
    TargetHousehold = 2475880078570760549798248448
    AllInstancedActiveHouseholdSims = 4951760157141521099596496896
    Street = 9903520314283042199192993792
    VenuePolicyProvider = 19807040628566084398385987584
    ActorLot = 39614081257132168796771975168
    ObjectIngredients = 79228162514264337593543950336
    CreatedObjectIngredients = 158456325028528675187087900672
    StoredCASPartsOnObject = 316912650057057350374175801344
    RoutingOwner = 633825300114114700748351602688
    RoutingTarget = 1267650600228229401496703205376
    CurrentRegion = 2535301200456458802993406410752
    ActorLotLevel = 5070602400912917605986812821504
    ObjectLotLevel = 10141204801825835211973625643008
    TargetHouseholdMembers = 20282409603651670423947251286016
    ObjectAnimalHome = 40564819207303340847894502572032
    AnimalHomeAssignees = 81129638414606681695789005144064
    SituationCraftingItem = 162259276829213363391578010288128
    ObjectRelationshipsComponent = 324518553658426726783156020576256
    ActorHouseholdMembers = 649037107316853453566312041152512
    SavedStoryProgressionSim1 = 1298074214633706907132624082305024
    SavedStoryProgressionSim2 = 2596148429267413814265248164610048
    SavedStoryProgressionZone1 = 5192296858534827628530496329220096
    SavedStoryProgressionZone2 = 10384593717069655257060992658440192
    SavedStoryProgressionString1 = 20769187434139310514121985316880384
    SavedStoryProgressionString2 = 41538374868278621028243970633760768
    SavedStoryProgressionString3 = 83076749736557242056487941267521536
    SavedStoryProgressionString4 = 166153499473114484112975882535043072
    SavedStoryProgressionString5 = 332306998946228968225951765070086144
    ActorClanLeader = 664613997892457936451903530140172288
    TargetClanLeader = 1329227995784915872903807060280344576
    ObjectTrendiOutfitTrend = 2658455991569831745807614120560689152
    ObjectTrendiOutfitTrendTag = 5316911983139663491615228241121378304
    GraduatesCurrent = 10633823966279326983230456482242756608
    GraduatesWaiting = 21267647932558653966460912964485513216
    FashionTrends = 42535295865117307932921825928971026432
    CarryCancellationOriginatorTarget = 85070591730234615865843651857942052864
    TargetSimFrontCarriedSim = 170141183460469231731687303715884105728
    TargetSimBackCarriedSim = 1 << 128
    CarriedSim = 1 << 129
    PurchasedObject = 1 << 130
    StoredSimOrNameDataList = 1 << 131
    StoredSim2 = 1 << 132
    ActorBassinet = 1 << 133
    TargetBassinet = 1 << 134
    ObjectAnimalCost = 1 << 135
    TargetObjectOfJoinedInteraction = 1 << 136
    ObjectAnimalCurrentValue = 1 << 137
    ActorPropertyOwners = 1 << 138
    ActorPropertyOwnerHousehold = 1 << 139
    ActorTenants = 1 << 140
    ActorTenantHouseholds = 1 << 141
    ActorZoneId = 1 << 142
    TargetSimZoneId = 1 << 143
    RandomZoneId = 1 << 144
    AllUnitZoneIds = 1 << 145
    CurrentZoneId = 1 << 146
    PickedZoneHouseholdSims = 1 << 147
    AllSimsInCurrentGame = 1 << 148
    OtherSimsInCurrentGame = 1 << 149
    AllSignificantOthersActor = 1 << 150
    AllSignificantOthersTargetSim = 1 << 151
    HeirloomCreatorSim = 1 << 152
    CurrentlyOpenSmallBusinessOwner = 1 << 153
    SmallBusinessEmployees = 1 << 154
    StoredPickedTattooOnActor = 1 << 155
    StoredPickedTattooOnTarget = 1 << 156


class OmutsuInteractionsService(OmutsuService):
    pass


_INTERACTIONS_SERVICE = OmutsuInteractionsService("interactions")

def get_fire_service() -> OmutsuInteractionsService:
    return _INTERACTIONS_SERVICE
