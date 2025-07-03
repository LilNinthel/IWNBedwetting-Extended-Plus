from iwnbedwetting.enums.base import EnumBase
from sims.outfits.outfit_enums import BodyType


class DiaperType(EnumBase):
    SIMPLE = 0
    LANDING_ZONE = 1
    HOOK_AND_LOOP = 2


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


class DiaperCC(EnumBase):
    ember_bunny_hook_female_low_accessory = 10195004188456681347
    ember_bunny_hook_female_low_bottom = 15901019533935666688
    ember_bunny_hook_female_medium_accessory = 15261388862686457491
    ember_bunny_hook_female_medium_bottom = 15863180620097396159
    ember_bunny_hook_female_tall_accessory = 9428168299802457337
    ember_bunny_hook_female_tall_bottom = 11723233872115429942
    ember_bunny_hook_female_wall_accessory = 15880507622158690423
    ember_bunny_hook_female_wall_bottom = 15119513609445981861
    ember_bunny_hook_male_low_accessory = 11810684646282072503
    ember_bunny_hook_male_low_bottom = 10203310771207522511
    ember_bunny_hook_male_medium_accessory = 17416192944310124433
    ember_bunny_hook_male_medium_bottom = 15067901750559221265
    ember_bunny_hook_male_tall_accessory = 9315160533848448694
    ember_bunny_hook_male_tall_bottom = 10043094098805179577
    ember_bunny_hook_male_wall_accessory = 11301312599355066913
    ember_bunny_hook_male_wall_bottom = 14529822570535928302

    ember_plain_hook_female_low_accessory = 12038055753906119390
    ember_plain_hook_female_low_bottom = 13882341130908228455
    ember_plain_hook_female_medium_accessory = 13516959360892489511
    ember_plain_hook_female_medium_bottom = 15402959911057910726
    ember_plain_hook_female_tall_accessory = 11692781661403962981
    ember_plain_hook_female_tall_bottom = 12174830004995219561
    ember_plain_hook_female_wall_accessory = 15395696484973795175
    ember_plain_hook_female_wall_bottom = 11377714707345239857
    ember_plain_hook_male_low_accessory = 15636052488763945153
    ember_plain_hook_male_low_bottom = 11887278681329430061
    ember_plain_hook_male_medium_accessory = 12652172876739024969
    ember_plain_hook_male_medium_bottom = 10971785271352205405
    ember_plain_hook_male_tall_accessory = 9818367281225106513
    ember_plain_hook_male_tall_bottom = 14402379719927751922
    ember_plain_hook_male_wall_accessory = 10828777962635164723
    ember_plain_hook_male_wall_bottom = 11377714707345239857

    ember_plain_landing_female_low_accessory = 14400962012846318497
    ember_plain_landing_female_low_bottom = 14817753706865748494
    ember_plain_landing_female_medium_accessory = 14725808560507840298
    ember_plain_landing_female_medium_bottom = 12723615923680595163
    ember_plain_landing_female_tall_accessory = 14828121630287542581
    ember_plain_landing_female_tall_bottom = 12134976349751938920
    ember_plain_landing_female_wall_accessory = 14081768220370047012
    ember_plain_landing_female_wall_bottom = 11798765533300344227
    ember_plain_landing_male_low_accessory = 13957892856098405122
    ember_plain_landing_male_low_bottom = 18175719647775004204
    ember_plain_landing_male_medium_accessory = 13128856079699632759
    ember_plain_landing_male_medium_bottom = 13269253604407697180
    ember_plain_landing_male_tall_accessory = 13207486108775125984
    ember_plain_landing_male_tall_bottom = 13903537964114171995
    ember_plain_landing_male_wall_accessory = 13099465542238001347
    ember_plain_landing_male_wall_bottom = 11050266238630918155

    ember_nru_landing_female_low_accessory = 14958342929191587069
    ember_nru_landing_female_low_bottom = 17209114295183730333
    ember_nru_landing_female_medium_accessory = 12452493285954750118
    ember_nru_landing_female_medium_bottom = 14457746686525413164
    ember_nru_landing_female_tall_accessory = 10886232791201770012
    ember_nru_landing_female_tall_bottom = 14130754783463696206
    ember_nru_landing_female_wall_accessory = 18111581372537224927
    ember_nru_landing_female_wall_bottom = 17192211726903388244
    ember_nru_landing_male_low_accessory = 12253409016819902919
    ember_nru_landing_male_low_bottom = 14676563098857398606
    ember_nru_landing_male_medium_accessory = 18223001689390402665
    ember_nru_landing_male_medium_bottom = 12409098580593266609
    ember_nru_landing_male_tall_accessory = 10620674236963749782
    ember_nru_landing_male_tall_bottom = 16727274354149623019
    ember_nru_landing_male_wall_accessory = 10518520436121252549
    ember_nru_landing_male_wall_bottom = 15862920524777542351

    ember_bellissimo_landing_female_low_accessory = 11475566902572188911
    ember_bellissimo_landing_female_low_bottom = 9358311568702710467
    ember_bellissimo_landing_female_medium_accessory = 11133078861918141011
    ember_bellissimo_landing_female_medium_bottom = 17231554690770013396
    ember_bellissimo_landing_female_tall_accessory = 16957840280945323054
    ember_bellissimo_landing_female_tall_bottom = 17054332893243336036
    ember_bellissimo_landing_female_wall_accessory = 11649414196269637966
    ember_bellissimo_landing_female_wall_bottom = 14847364933606234717
    ember_bellissimo_landing_male_low_accessory = 12395518647129927303
    ember_bellissimo_landing_male_low_bottom = 15661513248122902957
    ember_bellissimo_landing_male_medium_accessory = 13130246627993205071
    ember_bellissimo_landing_male_medium_bottom = 12410734985261025785
    ember_bellissimo_landing_male_tall_accessory = 15801089200744424716
    ember_bellissimo_landing_male_tall_bottom = 13838131288253581083
    ember_bellissimo_landing_male_wall_accessory = 17115575128165822309
    ember_bellissimo_landing_male_wall_bottom = 12592391533832786983

    ember_plain_simple_female_low_accessory = 17397648718324309626
    ember_plain_simple_female_low_bottom = 10294754548094293386
    ember_plain_simple_female_medium_accessory = 12351881240003105652
    ember_plain_simple_female_medium_bottom = 12511731984329828297
    ember_plain_simple_female_tall_accessory = 12357393369938480881
    ember_plain_simple_female_tall_bottom = 14210138470179301881
    ember_plain_simple_female_wall_accessory = 10702638174933037029
    ember_plain_simple_female_wall_bottom = 18308005185402329887
    ember_plain_simple_male_low_accessory = 10608126702256983234
    ember_plain_simple_male_low_bottom = 11163130419493762065
    ember_plain_simple_male_medium_accessory = 10250677779614694210
    ember_plain_simple_male_medium_bottom = 17929648139096525172
    ember_plain_simple_male_tall_accessory = 16453126801577273791
    ember_plain_simple_male_tall_bottom = 13293234927537261145
    ember_plain_simple_male_wall_accessory = 16477299403392253060
    ember_plain_simple_male_wall_bottom = 18109847548095664823

    ember_crinklz_simple_female_low_accessory = 11687753797074709790
    ember_crinklz_simple_female_low_bottom = 11241462963069928728
    ember_crinklz_simple_female_medium_accessory = 18112578257272953202
    ember_crinklz_simple_female_medium_bottom = 14170645136690908698
    ember_crinklz_simple_female_tall_accessory = 13930830933397578751
    ember_crinklz_simple_female_tall_bottom = 10172764427254632969
    ember_crinklz_simple_female_wall_accessory = 16423671842319494793
    ember_crinklz_simple_female_wall_bottom = 15858575318118471992
    ember_crinklz_simple_male_low_accessory = 12447728614706028788
    ember_crinklz_simple_male_low_bottom = 9299821023585529739
    ember_crinklz_simple_male_medium_accessory = 13140137619929574520
    ember_crinklz_simple_male_medium_bottom = 14406157176776315349
    ember_crinklz_simple_male_tall_accessory = 10342778039990857114
    ember_crinklz_simple_male_tall_bottom = 17550811253687005720
    ember_crinklz_simple_male_wall_accessory = 17109339264598132275
    ember_crinklz_simple_male_wall_bottom = 14530773083303507666

    lilninthel_bellissimo_landing_female_wall_accessory = 15174586519016046818
    lilninthel_bellissimo_landing_female_wall_bottom = 9323691022453188679
    lilninthel_bellissimo_landing_male_wall_accessory = 10626761853771937099
    lilninthel_bellissimo_landing_male_wall_bottom = 14935196131981263092

    lilninthel_classico_landing_female_wall_accessory = 17185900473586388270
    lilninthel_classico_landing_female_wall_bottom = 11276491982480170579
    lilninthel_classico_landing_male_wall_accessory = 15024033459415991799
    lilninthel_classico_landing_male_wall_bottom = 11509986916541151536
