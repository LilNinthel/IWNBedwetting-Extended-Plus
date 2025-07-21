from iwnbedwetting.enums.base import EnumBase
from sims.outfits.outfit_enums import BodyType
import sims4.log

logger = sims4.log.Logger('IWNBedwettingMain')


class DefaultDiaperType(EnumBase):
    UNSPECIFIED = 0
    PULLUP = 1
    DISCREET = 2
    MEDICAL = 3
    PREMIUM_MEDICAL = 4
    ABDL = 5
    PREMIUM_ABDL = 6
    MAGIC = 7


class DiaperTapeStyle(EnumBase):
    SIMPLE = 0
    LANDING_ZONE = 1
    HOOK_AND_LOOP = 2
    PULL_UP = 3


class DiaperHeight(EnumBase):
    LOW = 1
    MEDIUM = 2
    TALL = 3
    WALL = 4


class DiaperFrame(EnumBase):
    INVALID = 0
    FEMININE = 1
    MASCULINE = 2
    CHILD = 3


class DiaperBodyType(EnumBase):
    BOTTOM = BodyType.LOWER_BODY
    ACCESSORY = BodyType.INDEX_FINGER_LEFT


class DiaperPrintStyle(EnumBase):
    PLAIN = 1
    LANDING_ZONE = 2
    ALL_OVER = 3


class DiaperCASMetadata:
    def __init__(self, creator:str, design_name:str, tape_style:int, frame:int, height:int, body_type:int, print_style:int, cas_id, diaper_types):
        self.creator = creator
        self.design_name = design_name
        self.tape_style = tape_style
        self.height = height
        self.frame = frame
        self.body_type = body_type
        self.print_style = print_style
        self.cas_id = cas_id
        self.diaper_types = frozenset([DefaultDiaperType.UNSPECIFIED])
        if diaper_types is not None:
            self.diaper_types = frozenset(list(diaper_types))


class DiaperObjectDefinition(EnumBase):
    ADULT_DIAPER_BAG_PLAIN = 16638570619169569261
    ADULT_DIAPER_ITEM_PLAIN = 13965923130368742748
    ADULT_DIAPER_ITEM_BELLISSIMO = 13965923130368742749
    ADULT_DIAPER_ITEM_SDK = 13965923130368742750
    ADULT_DIAPER_ITEM_BUNNY_HOPPS = 13965923130368742751


class DiaperCC:
    
    _diaper_cc = []

    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,10195004188456681347,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15901019533935666688,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,15261388862686457491,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15863180620097396159,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,9428168299802457337,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,11723233872115429942,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,15880507622158690423,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15119513609445981861,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,11810684646282072503,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,10203310771207522511,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,17416192944310124433,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15067901750559221265,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,9315160533848448694,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,10043094098805179577,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,11301312599355066913,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14529822570535928302,[DefaultDiaperType.PREMIUM_ABDL]))

    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,12038055753906119390,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,13882341130908228455,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,13516959360892489511,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,15402959911057910726,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,11692781661403962981,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,12174830004995219561,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,15395696484973795175,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11952805987498167279,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,15636052488763945153,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11887278681329430061,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,12652172876739024969,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,10971785271352205405,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,9818367281225106513,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,14402379719927751922,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,10828777962635164723,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11377714707345239857,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))

    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,14400962012846318497,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,14817753706865748494,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,14725808560507840298,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,12723615923680595163,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,14828121630287542581,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,12134976349751938920,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,14081768220370047012,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11798765533300344227,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,13957892856098405122,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,18175719647775004204,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,13128856079699632759,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,13269253604407697180,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,13207486108775125984,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,13903537964114171995,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,13099465542238001347,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11050266238630918155,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))

    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,14958342929191587069,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,17209114295183730333,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,12452493285954750118,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14457746686525413164,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,10886232791201770012,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14130754783463696206,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,18111581372537224927,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,17192211726903388244,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,12253409016819902919,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14676563098857398606,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,18223001689390402665,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,12409098580593266609,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,10620674236963749782,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,16727274354149623019,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,10518520436121252549,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15862920524777542351,[DefaultDiaperType.ABDL]))

    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,11475566902572188911,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,9358311568702710467,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,11133078861918141011,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,17231554690770013396,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,16957840280945323054,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,17054332893243336036,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,11649414196269637966,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,14847364933606234717,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,12395518647129927303,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,15661513248122902957,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,13130246627993205071,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,12410734985261025785,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,15801089200744424716,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,13838131288253581083,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,17115575128165822309,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,12592391533832786983,[DefaultDiaperType.PREMIUM_ABDL]))

    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,17397648718324309626,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,10294754548094293386,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,12351881240003105652,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,12511731984329828297,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,12357393369938480881,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,14210138470179301881,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,10702638174933037029,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,18308005185402329887,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,10608126702256983234,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11163130419493762065,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,10250677779614694210,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,17929648139096525172,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,16453126801577273791,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,13293234927537261145,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.PLAIN,16477299403392253060,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,18109847548095664823,[DefaultDiaperType.MEDICAL,DefaultDiaperType.PREMIUM_MEDICAL]))

    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,11687753797074709790,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,11241462963069928728,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,18112578257272953202,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14170645136690908698,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,13930830933397578751,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,10172764427254632969,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,16423671842319494793,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15858575318118471992,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,12447728614706028788,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,9299821023585529739,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,13140137619929574520,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14406157176776315349,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,10342778039990857114,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,17550811253687005720,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.ALL_OVER,17109339264598132275,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14530773083303507666,[DefaultDiaperType.ABDL]))

    _diaper_cc.append(DiaperCASMetadata('lilninthel','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,15174586519016046818,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,9323691022453188679,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,10626761853771937099,[DefaultDiaperType.PREMIUM_ABDL]))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,14935196131981263092,[DefaultDiaperType.PREMIUM_ABDL]))

    _diaper_cc.append(DiaperCASMetadata('lilninthel','classico',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,17185900473586388270,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','classico',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,11276491982480170579,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','classico',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY,DiaperPrintStyle.LANDING_ZONE,15024033459415991799,[DefaultDiaperType.ABDL]))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','classico',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,11509986916541151536,[DefaultDiaperType.ABDL]))

    @classmethod
    def get_filtered_metadata(cls, creator:str=None, design_name:str=None, tape_style:int=None, frame:int=None, height:int=None, body_type:int=None, print_style:int=None, diaper_type:int=DefaultDiaperType.UNSPECIFIED):
        return [x for x in cls._diaper_cc
                if (creator is None or x.creator == creator)
                and (design_name is None or x.design_name == design_name)
                and (tape_style is None or x.tape_style == tape_style)
                and (frame is None or x.frame == frame)
                and (height is None or x.height == height)
                and (body_type is None or x.body_type == body_type)
                and (print_style is None or x.print_style == print_style)
                and (diaper_type is None or diaper_type == DefaultDiaperType.UNSPECIFIED or diaper_type in x.diaper_types)
                ]

    @classmethod
    def get_filtered_cas_ids(cls, creator:str=None, design_name:str=None, tape_style:int=None, frame:int=None, height:int=None, body_type:int=None, print_style:int=None, diaper_type:int=DefaultDiaperType.UNSPECIFIED):
        return [x.cas_id for x in cls.get_filtered_metadata(creator,design_name,tape_style,frame,height,body_type,print_style,diaper_type)]

    @classmethod
    def get_all_metadata(cls):
        return cls._diaper_cc

    @classmethod
    def get_by_object_definition(cls, object_definition_id:int, frame:int=None, height:int=DiaperHeight.WALL, body_type:int=DiaperBodyType.ACCESSORY):
        logger.info("get_by_object_definition {}".format(object_definition_id))
        if object_definition_id == DiaperObjectDefinition.ADULT_DIAPER_BAG_PLAIN or object_definition_id == DiaperObjectDefinition.ADULT_DIAPER_ITEM_PLAIN:
            return cls.get_filtered_cas_ids(tape_style=DiaperTapeStyle.LANDING_ZONE,frame=frame,height=height,body_type=body_type,print_style=DiaperPrintStyle.PLAIN)
        if object_definition_id == DiaperObjectDefinition.ADULT_DIAPER_ITEM_BELLISSIMO:
            return cls.get_filtered_cas_ids(design_name='bellissimo',frame=frame,height=height,body_type=body_type)
        if object_definition_id == DiaperObjectDefinition.ADULT_DIAPER_ITEM_SDK:
            return cls.get_filtered_cas_ids(tape_style=DiaperTapeStyle.LANDING_ZONE,frame=frame,height=height,body_type=body_type,print_style=DiaperPrintStyle.LANDING_ZONE)
        if object_definition_id == DiaperObjectDefinition.ADULT_DIAPER_ITEM_BUNNY_HOPPS:
            return cls.get_filtered_cas_ids(design_name='bunny', frame=frame, height=height, body_type=body_type)
        logger.info("No suitable diapers found")
        return []