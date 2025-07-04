from iwnbedwetting.enums.base import EnumBase
from sims.outfits.outfit_enums import BodyType
import sims4.log

logger = sims4.log.Logger('IWNBedwettingMain')

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
    FEMININE = 1
    MASCULINE = 2
    CHILD = 3


class DiaperBodyType(EnumBase):
    BOTTOM = BodyType.LOWER_BODY
    ACCESSORY_ADULT = BodyType.INDEX_FINGER_LEFT
    ACCESSORY_CHILD = BodyType.EARRINGS


class DiaperPrintStyle(EnumBase):
    PLAIN = 1
    LANDING_ZONE = 2
    ALL_OVER = 3


class DiaperCASMetadata:
    def __init__(self, creator:str, design_name:str, tape_style:int, frame:int, height:int, body_type:int, print_style:int, cas_id):
        self.creator = creator
        self.design_name = design_name
        self.tape_style = tape_style
        self.height = height
        self.frame = frame
        self.body_type = body_type
        self.print_style = print_style
        self.cas_id = cas_id


class DiaperObjectDefinition(EnumBase):
    ADULT_DIAPER_BAG_PLAIN = 16638570619169569261
    ADULT_DIAPER_ITEM_PLAIN = 13965923130368742748
    ADULT_DIAPER_ITEM_BELLISSIMO = 13965923130368742749
    ADULT_DIAPER_ITEM_SDK = 13965923130368742750
    ADULT_DIAPER_ITEM_BUNNY_HOPPS = 13965923130368742751


class DiaperCC:
    
    _diaper_cc = []

    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,10195004188456681347))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15901019533935666688))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,15261388862686457491))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15863180620097396159))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,9428168299802457337))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,11723233872115429942))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,15880507622158690423))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15119513609445981861))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,11810684646282072503))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,10203310771207522511))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,17416192944310124433))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15067901750559221265))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,9315160533848448694))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,10043094098805179577))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,11301312599355066913))
    _diaper_cc.append(DiaperCASMetadata('ember','bunny',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14529822570535928302))

    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,12038055753906119390))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,13882341130908228455))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,13516959360892489511))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,15402959911057910726))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,11692781661403962981))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,12174830004995219561))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,15395696484973795175))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11952805987498167279))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,15636052488763945153))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11887278681329430061))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,12652172876739024969))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,10971785271352205405))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,9818367281225106513))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,14402379719927751922))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,10828777962635164723))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.HOOK_AND_LOOP,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11377714707345239857))

    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,14400962012846318497))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,14817753706865748494))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,14725808560507840298))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,12723615923680595163))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,14828121630287542581))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,12134976349751938920))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,14081768220370047012))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11798765533300344227))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,13957892856098405122))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,18175719647775004204))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,13128856079699632759))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,13269253604407697180))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,13207486108775125984))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,13903537964114171995))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,13099465542238001347))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11050266238630918155))

    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,14958342929191587069))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,17209114295183730333))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,12452493285954750118))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14457746686525413164))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,10886232791201770012))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14130754783463696206))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,18111581372537224927))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,17192211726903388244))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,12253409016819902919))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14676563098857398606))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,18223001689390402665))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,12409098580593266609))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,10620674236963749782))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,16727274354149623019))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,10518520436121252549))
    _diaper_cc.append(DiaperCASMetadata('ember','nru',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15862920524777542351))

    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,11475566902572188911))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,9358311568702710467))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,11133078861918141011))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,17231554690770013396))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,16957840280945323054))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,17054332893243336036))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,11649414196269637966))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,14847364933606234717))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,12395518647129927303))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,15661513248122902957))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,13130246627993205071))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,12410734985261025785))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,15801089200744424716))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,13838131288253581083))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,17115575128165822309))
    _diaper_cc.append(DiaperCASMetadata('ember','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,12592391533832786983))

    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,17397648718324309626))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,10294754548094293386))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,12351881240003105652))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,12511731984329828297))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,12357393369938480881))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,14210138470179301881))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,10702638174933037029))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,18308005185402329887))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,10608126702256983234))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,11163130419493762065))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,10250677779614694210))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,17929648139096525172))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,16453126801577273791))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,13293234927537261145))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.PLAIN,16477299403392253060))
    _diaper_cc.append(DiaperCASMetadata('ember','plain',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.PLAIN,18109847548095664823))

    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,11687753797074709790))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,11241462963069928728))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,18112578257272953202))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14170645136690908698))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,13930830933397578751))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,10172764427254632969))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,16423671842319494793))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,15858575318118471992))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,12447728614706028788))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.LOW,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,9299821023585529739))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,13140137619929574520))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.MEDIUM,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14406157176776315349))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,10342778039990857114))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.TALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,17550811253687005720))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.ALL_OVER,17109339264598132275))
    _diaper_cc.append(DiaperCASMetadata('ember','crinklz',DiaperTapeStyle.SIMPLE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.ALL_OVER,14530773083303507666))

    _diaper_cc.append(DiaperCASMetadata('lilninthel','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,15174586519016046818))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,9323691022453188679))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,10626761853771937099))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','bellissimo',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,14935196131981263092))

    _diaper_cc.append(DiaperCASMetadata('lilninthel','classico',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,17185900473586388270))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','classico',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.FEMININE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,11276491982480170579))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','classico',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.ACCESSORY_ADULT,DiaperPrintStyle.LANDING_ZONE,15024033459415991799))
    _diaper_cc.append(DiaperCASMetadata('lilninthel','classico',DiaperTapeStyle.LANDING_ZONE,DiaperFrame.MASCULINE,DiaperHeight.WALL,DiaperBodyType.BOTTOM,DiaperPrintStyle.LANDING_ZONE,11509986916541151536))

    @classmethod
    def get_filtered_metadata(cls, creator:str=None, design_name:str=None, tape_style:int=None, frame:int=None, height:int=None, body_type:int=None, print_style:int=None):
        return [x for x in cls._diaper_cc
                if (creator is None or x.creator == creator)
                and (design_name is None or x.design_name == design_name)
                and (tape_style is None or x.tape_style == tape_style)
                and (frame is None or x.frame == frame)
                and (height is None or x.height == height)
                and (body_type is None or x.body_type == body_type)
                and (print_style is None or x.print_style == print_style)
                ]

    @classmethod
    def get_filtered_cas_ids(cls, creator:str=None, design_name:str=None, tape_style:int=None, frame:int=None, height:int=None, body_type:int=None, print_style:int=None):
        return [x.cas_id for x in cls.get_filtered_metadata(creator,design_name,tape_style,frame,height,body_type,print_style)]

    @classmethod
    def get_all_metadata(cls):
        return cls._diaper_cc

    @classmethod
    def get_by_object_definition(cls, object_definition_id:int, frame:int=None, height:int=DiaperHeight.WALL, body_type:int=DiaperBodyType.ACCESSORY_ADULT):
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