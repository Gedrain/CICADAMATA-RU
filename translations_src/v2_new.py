# v2: strings that v1 left in English (names excluded).
# SCRIPT: string constants patched into compiled scripts (.gdc).
# CAT: translation catalog entries (scene texts, animation finals, texts that
#      scripts put on labels by themselves, including Russian-keyed entries for
#      labels whose text is built from an already translated prefix).

MODES = {"NORMAL": "ОБЫЧНЫЙ", "CICADADEATH": "СМЕРТЬЦИКАДЫ", "ESPERIA": "ЭСПЕРИЯ", "STARSHOT": "ЗВЁЗДНЫЙ ВЫСТРЕЛ"}

TITLES = {
"NAMELESS": "БЕЗЫМЯННАЯ", "INITIATE": "ПОСВЯЩЁННАЯ", "FIRST STEP": "ПЕРВЫЙ ШАГ", "BOTTOMFEEDER": "ПАДАЛЬЩИЦА",
"ENTRY": "НОВЕНЬКАЯ", "PROSPECT": "ПЕРСПЕКТИВНАЯ", "BIRDBRAIN": "КУРИНЫЕ МОЗГИ", "WHISPER": "ШЁПОТ",
"EMERGENT": "ПРОБУДИВШАЯСЯ", "SIGNAL": "СИГНАЛ", "STRIDER": "ШАГАЮЩАЯ", "AFTERIMAGE": "ОСТАТОЧНЫЙ ОБРАЗ",
"DISSONANT": "ДИССОНАНС", "SHELL": "ОБОЛОЧКА", "PARALLAX": "ПАРАЛЛАКС", "FORMLESS": "БЕСФОРМЕННАЯ",
"ELEGY": "ЭЛЕГИЯ", "OMEN": "ЗНАМЕНИЕ", "TRAUMATA": "ТРАВМАТА", "BROKEN RECORD": "ЗАЕВШАЯ ПЛАСТИНКА",
"KILL SCREEN": "ЭКРАН СМЕРТИ", "CICATRICE": "РУБЕЦ", "METAMATERIAL": "МЕТАМАТЕРИАЛ", "EMBLEMATA": "ЭМБЛЕМАТА",
"QUAD MACHINE": "КВАДРОМАШИНА", "CINDER": "ПЕПЕЛ", "MEMORA": "МЕМОРА", "FREE BIRD": "ВОЛЬНАЯ ПТИЦА",
"WONDERCHILD": "ЧУДО-ДИТЯ", "OUT OF LINE": "ВНЕ ПРАВИЛ", "RISKRUNNER": "РИСКОВАЯ", "DIGIMAIDEN": "ЦИФРОДЕВА",
"MATA PHENOMENA": "ФЕНОМЕН MATA", "BITTER SNARE": "ГОРЬКИЙ СИЛОК", "THE JUDGE": "СУДЬЯ", "ALEPH": "АЛЕФ",
"MIND KILLER": "УБИЙЦА РАЗУМА", "DEMIURGE": "ДЕМИУРГ", "GONER": "ОБРЕЧЁННАЯ", "CRISIS ACTOR": "КРИЗИСНАЯ АКТРИСА",
"EXECUTOR": "ПАЛАЧ", "MAGICICADA": "МАГИЦИКАДА", "BASTARD OF HEAVEN": "НЕБЕСНОЕ ОТРОДЬЕ", "LIGHTLESS": "БЕССВЕТНАЯ",
"CICADA ULTRA": "ЦИКАДА УЛЬТРА", "BLACK SWAN": "ЧЁРНЫЙ ЛЕБЕДЬ", "SUPERSTAR": "СУПЕРЗВЕЗДА", "AUTOMATA": "АВТОМАТА",
"WHITE RABBIT": "БЕЛЫЙ КРОЛИК",
}
WORLDS = {"EMERGENCE": "ПРОБУЖДЕНИЕ", "ICEBOX": "МОРОЗИЛКА", "DEEPDIVE": "ГЛУБИНА", "VERDANT": "ЗЕЛЕНЬ",
          "DEAD ZONE": "МЁРТВАЯ ЗОНА", "ENCORE": "НА БИС", "SUNSET": "ЗАКАТ", "BONUS": "БОНУС"}
LEVELS = {
"CUBES": "КУБЫ", "AENSLAND": "ЭНСЛЕНД", "MANDALA": "МАНДАЛА", "REVERIE": "ГРЁЗЫ", "GLACIER": "ЛЕДНИК",
"ALSEIA": "АЛСЕЯ", "RABBIT HOLE": "КРОЛИЧЬЯ НОРА", "CASCADE": "КАСКАД", "RUNOFF": "СТОК", "ESTUARY": "УСТЬЕ",
"MEADOW": "ЛУГ", "HARE": "ЗАЯЦ", "RIBBON": "ЛЕНТА", "SLINGSHOT": "РОГАТКА", "PEREGRINE": "САПСАН",
"MARATHON": "МАРАФОН", "ONEMORE": "ЕЩЁРАЗОК", "HALCYON": "БЕЗМЯТЕЖНОСТЬ", "JETPOD": "РЕАКТИВНАЯ КАПСУЛА",
"LOCKUP": "КАТАЛАЖКА", "KITSCH": "КИТЧ", "HAILSTONE": "ГРАДИНА", "SKEWER": "ВЕРТЕЛ", "SQUARE UP": "ВЫХОДИ НА БОЙ",
"CHESS": "ШАХМАТЫ", "IMMERSE": "ПОГРУЖЕНИЕ", "GRASSFIELD": "ТРАВЯНОЕ ПОЛЕ", "BIG SHOT": "БОЛЬШАЯ ШИШКА",
"MIST": "ТУМАН", "CASHOUT": "ОБНАЛИЧКА",
}
PRETITLES = {"SPHERE DEBUG": "СФЕРА ОТЛАДКА", "FIN": "КОНЕЦ"}
for w in range(1, 7):
    for l in range(1, 4):
        PRETITLES["SPHERE %d-%d" % (w, l)] = "СФЕРА %d-%d" % (w, l)
for p in ("1-1", "1-2", "1-3", "1-4", "2-1", "2-2", "2-3", "3-1", "4-1"):
    PRETITLES["PROTO " + p] = "ПРОТО " + p
for b in (1, 2, 3):
    PRETITLES["BONUS %d" % b] = "БОНУС %d" % b
ENEMIES = {"SHOOTER": "СТРЕЛОК", "CRAB": "КРАБ", "SPIDER": "ПАУК", "BIRD": "ПТИЦА", "ESPER": "ЭСПЕР",
           "BOUNCER": "ПОПРЫГУН", "FLOWER": "ЦВЕТОК"}
EVENTS = {
"FALLEN": "ПАДЕНИЕ", "LAUNCHER": "КАТАПУЛЬТА", "SEE YOU STARSIDE": "УВИДИМСЯ СРЕДИ ЗВЁЗД", "TRAMPOLINE": "БАТУТ",
"THRASHER": "МОЛОТИЛКА", "STARCROSSED": "НЕ СУДЬБА", "SQUISHER": "ДАВИЛКА", "LAWNMOWER": "ГАЗОНОКОСИЛКА",
"THE ORIGINAL": "ОРИГИНАЛ", "DISPATCHED": "УСТРАНЕНИЕ", "MELTDOWN": "РАСПЛАВЛЕНИЕ", "BLACKOUT": "ЗАТМЕНИЕ",
"CHAIN": "ЦЕПНАЯ", "IMPACT": "УДАР", "ZAPPER": "РАЗРЯД", "CUT DOWN": "ПОДКОШЕНА", "REPAIR": "РЕМОНТ",
"INCINERATED": "ИСПЕПЕЛЕНА", "HURDLE": "БАРЬЕР", "IMPALED": "НАСАЖЕНА", "STARSTRUCK": "ЗВЕЗДОУДАР",
"WIPEOUT": "ЗАЧИСТКА", "CORE GET": "ЯДРО ВЗЯТО", "EXPLODED": "ВЗОРВАНА",
}
for base in ("TRAMPOLINE", "THRASHER", "HURDLE"):
    for n in (1, 2, 3):
        EVENTS["%s+%d" % (base, n)] = "%s+%d" % (EVENTS[base], n)

SCRIPT = {}
SCRIPT.update(TITLES); SCRIPT.update(WORLDS); SCRIPT.update(LEVELS); SCRIPT.update(PRETITLES)
SCRIPT.update({'"%s"' % k: '"%s"' % v for k, v in ENEMIES.items()})
SCRIPT.update({k: v for k, v in EVENTS.items() if k != "CORE GET"})
SCRIPT.update({
# level_transition / deploy_screen: prefixes stripped from translated pretitles
"SPHERE ": "СФЕРА ", "PROTO ": "ПРОТО ", "BONUS ": "БОНУС ", "PROTO": "ПРОТО", "MUSEUM": "МУЗЕЙ",
# hints (header texts)
"DEPLOYMENTS": "ВЫСАДКИ", "ASCENT": "ПОДЪЁМ", "OVERHEAT": "ПЕРЕГРЕВ", "FUNCTION: DASH": "ФУНКЦИЯ: РЫВОК",
"FUNCTION: STOMP": "ФУНКЦИЯ: УДАР ВНИЗ", "IN THE ZONE": "В ПОТОКЕ",
# HUD jump counter / player state
"FLR": "ЗМЛ", "DSC": "СПК", "SLD": "СКЛ",
"SLIDE": "СКОЛЬЖЕНИЕ", "SPRNG": "ПРУЖИНА", "FALL": "ПАДЕНИЕ", "LAND": "ПРИЗЕМЛЕНИЕ", "RUN": "БЕГ", "IDLE": "ПОКОЙ",
# JOYEUSE lines / notifications / Steam timeline
"MY LIGHT IN DARK": "МОЙ СВЕТ ВО ТЬМЕ", "MY WHITE RABBIT": "МОЙ БЕЛЫЙ КРОЛИК", "RUST/CORRODE": "РЖАВЕЙ/РАЗЪЕДАЙ",
"_ERR": "_ОШБ", "ZONED": "В ПОТОКЕ", "LEVEL COMPLETE": "УРОВЕНЬ ПРОЙДЕН", "TOTAL POINTS": "ВСЕГО ОЧКОВ",
"TOTAL TIME": "ОБЩЕЕ ВРЕМЯ", "FIRST CLEAR!": "ПЕРВОЕ ПРОХОЖДЕНИЕ!", "NEW PERSONAL BEST!": "НОВЫЙ ЛИЧНЫЙ РЕКОРД!",
"SUCCESSFUL DEPLOYMENT": "УСПЕШНАЯ ВЫСАДКА", "LEVEL": "УРОВЕНЬ", "RUSH": "ЗАБЕГ", " COMPLETE": " ПРОЙДЕН",
"SPHERE RUSH + ": "ЗАБЕГ ПО СФЕРАМ + ", "> SPHERE RUSH + ": "> ЗАБЕГ ПО СФЕРАМ + ", "SPHERE RUSH": "ЗАБЕГ ПО СФЕРАМ",
# Discord status
"INTRO": "ВСТУПЛЕНИЕ", "INIT": "ЗАПУСК", "SPHERE RUSH: ": "ЗАБЕГ ПО СФЕРАМ: ", "CCID + [CI": "ЦКИД + [CI",
"LEVEL ": "УРОВЕНЬ ", "PB: ": "РЕКОРД: ", "somewhere above the earth...": "где-то над землёй...", "FIRST LAUNCH": "ПЕРВЫЙ ЗАПУСК",
# ids / dates / places
" + / CSCD +": " + / КСКД +", "+ CICADA_DEMO.ONR": "+ ЦИКАДА_ДЕМО.ОНР",
"CCDAMTA_DM": "CCDAMTA_ДМ", "+ CASCADE / ONAEIRE, 7AS": "+ КАСКАД / ОНЭЙР, 7ПС", '"CICADA"': '"ЦИКАДА"',
"; ST. SANVEI / ONAEIRE, 7AS": "; СЕНТ-САНВЕЙ / ОНЭЙР, 7ПС", '"ANGEL"': '"АНГЕЛ"', "UNK_M_(%d)": "НЕИЗВ_М_(%d)",
"MMB": "СКМ", "MWHEEL UP": "КОЛЕСО ВВЕРХ", "MWHEEL DOWN": "КОЛЕСО ВНИЗ",
# stats blocks
"\n\texfils + ": "\n\tэвакуаций + ", "\n\tfunction: dash + ": "\n\tфункция: рывок + ",
"\n\tfunction: stomp + ": "\n\tфункция: удар вниз + ", "\n\tzoned\" + ": "\n\tв потоке\" + ",
"\n\tstarstruck + ": "\n\tзвездоудар + ", "\n\t\tZONED + ": "\n\t\tВ ПОТОКЕ + ", "XP / ": "ОП / ", "XP/": "ОП/",
# cosmetics
"CLASSIC": "КЛАССИКА", "DEMO": "ДЕМО", "CICADA KILLER": "УБИЙЦА ЦИКАД",
# deploy screen / misc UI
"DROPSHIP": "ДЕСАНТНИК", "POST-EXFIL": "ПОСЛЕ ЭВАКУАЦИИ", "THANK\nYOU": "СПАСИБО\nТЕБЕ",
'"SPEEDISKEY"': '"СКОРОСТЬРЕШАЕТ"', '"SUCKERFORPUNISHMENT"': '"ЛЮБЛЮСТРАДАТЬ"', '"DELUSIONINME"': '"БРЕДВОМНЕ"',
'"INTOTHESTARS"': '"КЗВЁЗДАМ"',
"> INITIATION, CASCADE": "> ИНИЦИАЦИЯ, КАСКАД", "> MU ARAE, CASCADE": "> МЮ ЖЕРТВЕННИКА, КАСКАД",
"> EPSILON II, CASCADE": "> ЭПСИЛОН II, КАСКАД", "> CASSIOPEIA/Y, CASCADE": "> КАССИОПЕЯ/Y, КАСКАД",
"> LOWER CIRCINUS, CASCADE": "> НИЖНИЙ ЦИРКУЛЬ, КАСКАД", "> ABOVE ALL ELSE, CASCADE": "> ПРЕВЫШЕ ВСЕГО, КАСКАД",
"> WR_LIVE, CASCADE": "> БК_ЭФИР, КАСКАД", "> ST. SANVEI, ONAEIRE": "> СЕНТ-САНВЕЙ, ОНЭЙР",
"CCDAMTA / VER. ": "CCDAMTA / ВЕР. ", "%.1f MB": "%.1f МБ", "+ TIME: ": "+ ВРЕМЯ: ", "\n\t\t+ CPU: ": "\n\t\t+ ЦП: ",
"\n\t\t+ GPU: ": "\n\t\t+ ГП: ", "ERR": "ОШБ",
# terminals
"+ SPHERES.ONR": "+ СФЕРЫ.ОНР", "+ ENTRY_LOG.ONR": "+ ЖУРНАЛ_ВХОДА.ОНР", "+ SILICA.ONR": "+ КРЕМНЕЗЁМ.ОНР",
"+ LUCKY_CAT.ONR": "+ КОТ_ВЕЗУНЧИК.ОНР", "+ HARVEST.ONR": "+ ЖАТВА.ОНР", "+ CREVASSE.ONR": "+ РАСЩЕЛИНА.ОНР",
"+ UNTITLED.ONR": "+ БЕЗ_НАЗВАНИЯ.ОНР", "+ JOYEUSE.ONR": "+ JOYEUSE.ОНР", "+ CONNECTION.ONR": "+ СВЯЗЬ.ОНР",
"+ RED_VEIL.ONR": "+ КРАСНАЯ_ВУАЛЬ.ОНР", "+ AEGIS.ONR": "+ AEGIS.ОНР", "+ ST_SANVEI.ONR": "+ ST_SANVEI.ОНР",
"+ MESSENGER.ONR": "+ ВЕСТНИК.ОНР", "+ VALENTINE.ONR": "+ VALENTINE.ОНР", "+ UNTITLED_2.ONR": "+ БЕЗ_НАЗВАНИЯ_2.ОНР",
"+ SOL.ONR": "+ SOL.ОНР", "+ OVERFLOW.ONR": "+ ПЕРЕПОЛНЕНИЕ.ОНР", "+ JOY_BEFORE.ONR": "+ JOY_ПРЕЖДЕ.ОНР",
"+ MNDKLLR.ONR": "+ УБЦРЗМ.ОНР", "+ LOVEYOU.ONR": "+ ЛЮБЛЮТЕБЯ.ОНР",
})
for d in ("04_APR", "05_APR", "06_APR", "08_APR", "09_APR", "11_APR", "14_APR", "17_APR", "19_APR", "22_APR",
          "23_APR", "25_APR", "28_APR", "29_APR", "09_MAY", "13_MAY", "17_MAY"):
    SCRIPT[d + "_7AS"] = d.replace("APR", "АПР").replace("MAY", "МАЙ") + "_7ПС"

CAT = {}
# labels showing a single value set by scripts
CAT.update(MODES); CAT.update(TITLES); CAT.update(WORLDS); CAT.update(LEVELS); CAT.update(PRETITLES)
CAT.update({k: v for k, v in EVENTS.items()})
CAT.update({"BRNZ": "БРНЗ", "SLVR": "СРБР", "GOLD": "ЗЛТО", "DMND": "АЛМЗ", "CCDA": "ЦКДА",
            "STOMP": "УДАР ВНИЗ", "DASH": "РЫВОК", "JUMP": "ПРЫЖОК"})
for en, ru in MODES.items():
    CAT['"%s"' % en] = '"%s"' % ru
    CAT["ЗАБЕГ ПО СФЕРАМ + " + en] = "ЗАБЕГ ПО СФЕРАМ + " + ru
    CAT["> ЗАБЕГ ПО СФЕРАМ + " + en] = "> ЗАБЕГ ПО СФЕРАМ + " + ru
    CAT["SPHERE RUSH + " + en] = "ЗАБЕГ ПО СФЕРАМ + " + ru
    CAT["> SPHERE RUSH + " + en] = "> ЗАБЕГ ПО СФЕРАМ + " + ru
CAT.update({
# static scene texts
"CICADAMATA\" Original Sound Collection": "CICADAMATA\" — оригинальный саундтрек",
"TO BECOME A CICADA\nIS TO SPLIT YOUR SKIN\nAND LEAVE THE OLD SHAPE\nCLINGING TO A TREE": "СТАТЬ ЦИКАДОЙ —\nЗНАЧИТ СБРОСИТЬ КОЖУ\nИ ОСТАВИТЬ ПРЕЖНИЙ ОБЛИК\nЦЕПЛЯТЬСЯ ЗА ДЕРЕВО",
"+ runtime>00:03:17:00": "+ длительность>00:03:17:00",
"\"BIRD\"": "\"ПТИЦА\"",
"+ DECEMBER-C1 \"PATCHWORK\"\n\n+ [wave amp=15.0 freq=5.0 connected=1][pulse freq=2.0 color=yellow ease=2.0]FAWN-A2 \"WHITE RABBIT\"[/pulse][/wave]\n\n+ JACK-L3 \"SILICA\"\n\n+ ROWAN-K4 \"EMERGENT\"\n\n+ MIYA-H5 \"LITANY\"\n\n+ GALWAY-O6 \"SKINCAST\"\n\n+ TAINA-I7 \"STRIKER\"":
    "+ DECEMBER-C1 \"ЛОСКУТЫ\"\n\n+ [wave amp=15.0 freq=5.0 connected=1][pulse freq=2.0 color=yellow ease=2.0]FAWN-A2 \"БЕЛЫЙ КРОЛИК\"[/pulse][/wave]\n\n+ JACK-L3 \"КРЕМНЕЗЁМ\"\n\n+ ROWAN-K4 \"ПРОБУДИВШАЯСЯ\"\n\n+ MIYA-H5 \"ЛИТАНИЯ\"\n\n+ GALWAY-O6 \"СБРОШЕННАЯ КОЖА\"\n\n+ TAINA-I7 \"УДАРНИЦА\"",
"     + DECEMBER-C1 \"MESSENGER\"\n\n": "     + DECEMBER-C1 \"ВЕСТНИК\"\n\n",
"     + [wave amp=15.0 freq=5.0 connected=1][pulse freq=2.0 color=C42B47 ease=2.0]FAWN-A2 \"WHITE RABBIT\"[/pulse][/wave]\n\n":
    "     + [wave amp=15.0 freq=5.0 connected=1][pulse freq=2.0 color=C42B47 ease=2.0]FAWN-A2 \"БЕЛЫЙ КРОЛИК\"[/pulse][/wave]\n\n",
"     + SABLE-L3 \"SILICA\"\n\n": "     + SABLE-L3 \"КРЕМНЕЗЁМ\"\n\n",
"     + ROWAN-K4 \"MAD HATTER\"\n\n": "     + ROWAN-K4 \"БЕЗУМНЫЙ ШЛЯПНИК\"\n\n",
"     + MIYA-H5 \"LUCKY CAT\"\n\n": "     + MIYA-H5 \"КОТ-ВЕЗУНЧИК\"\n\n",
"     + HALCA-O6 \"SNOWDROP\"\n\n": "     + HALCA-O6 \"ПОДСНЕЖНИК\"\n\n",
"     + TAINA-I7 \"RED QUEEN\"\n\n": "     + TAINA-I7 \"ЧЕРВОННАЯ КОРОЛЕВА\"\n\n",
"IN7_01": "ИН7_01", "SPHERE 5-3 + EMOTICORE NULLHEART": "СФЕРА 5-3 + ЭМОЦИЯДРО НУЛЬ-СЕРДЦЕ",
"\"RABBIT HOLE\"": "\"КРОЛИЧЬЯ НОРА\"", "SPHERE RUSH": "ЗАБЕГ ПО СФЕРАМ", "_INFO01": "_ИНФО01", "ERR": "ОШБ",
"FAWN-A2 + \"WHITE RABBIT\"": "FAWN-A2 + \"БЕЛЫЙ КРОЛИК\"",
"+ 00:00.000 + / CSCD +": "+ 00:00.000 + / КСКД +", "+ 00:00.000 + / CSDC +": "+ 00:00.000 + / КСКД +",
"DECEMBER-A1\nFAWN-A2 \"WHITE RABBIT\"\n": "DECEMBER-A1\nFAWN-A2 \"БЕЛЫЙ КРОЛИК\"\n",
"PREPA": "ПОДГО", "/7AS": "/7ПС", "CICADAMATA\" PRERELEASE": "CICADAMATA\" ПРЕДРЕЛИЗ", "FLR": "ЗМЛ",
"\"TIMEELAPSE\"": "\"ПРОШЛОВРЕМЕНИ\"", "\"SUCKERFORPUNISHMENT\"": "\"ЛЮБЛЮСТРАДАТЬ\"",
"+ March, MATA\" Inherent +": "+ March, изначальная MATA\" +", "STRATA 1-1": "СТРАТА 1-1", "DREAMSTREAK": "ПОЛОСА СНОВ",
"+ FAWN-A2 \"WHITE RABBIT\"": "+ FAWN-A2 \"БЕЛЫЙ КРОЛИК\"", "7AS/CI000002": "7ПС/CI000002",
"I KNEW I COULD COUNT ON YOU": "Я ЗНАЛА, ЧТО НА ТЕБЯ МОЖНО ПОЛОЖИТЬСЯ", "ST_FALL": "СТ_ПАДЕНИЕ", "MATA\"STATE": "СОСТОЯНИЕMATA\"",
"\"RECEIVEINPUT\"": "\"ПРИЁМВВОДА\"", "\"DASH\"": "\"РЫВОК\"", "\"STOMP\"": "\"УДАРВНИЗ\"", "\"JUMPREADY\"": "\"ПРЫЖОКГОТОВ\"",
"\"JUMPAMNT\"": "\"ЧИСЛОПРЫЖКОВ\"", "\"VERTVEL\"": "\"ВЕРТСКОР\"", "\"ENERGY\"": "\"ЭНЕРГИЯ\"",
"\"COREREMAIN\"": "\"ОСТАЛОСЬЯДЕР\"", "\"TOTALSCORE\"": "\"ОБЩИЙСЧЁТ\"",
"0.725S       1.0X       5600K      100MP\n93-21-27 [REC] + 45/100\n": "0.725С       1.0X       5600К      100МП\n93-21-27 [ЗАП] + 45/100\n",
"ERR! UNKN_": "ОШБ! НЕИЗВ_",
"FLWRGRDN01 | PROJECT CICADA ★ 2025-2026\n": "FLWRGRDN01 | ПРОЕКТ ЦИКАДА ★ 2025-2026\n",
"FLWRGRDN01 | PROJECT CICADA ★ 2025-2026": "FLWRGRDN01 | ПРОЕКТ ЦИКАДА ★ 2025-2026",
"the CASCADE \"loveless initiation\"": "КАСКАД: \"инициация без любви\"", "BONUS": "БОНУС", "7AS": "7ПС",
"+ CICADA.ONR": "+ ЦИКАДА.ОНР", " ; ANGEL.ONR": " ; АНГЕЛ.ОНР", "\"CICADA\"": "\"ЦИКАДА\"",
"+ CASCADE / ONAEIRE, 7AS": "+ КАСКАД / ОНЭЙР, 7ПС",
"threats dispatched + 000000\ncores collected + 000000\ndeployments + 000000\nexfils + 000000\nmata\" energy depletions + 000000\nfunction: dash + 000000\nfunction: stomp + 000000\nzoned\" + 000000\nstarstruck + 000000\n":
    "устранено угроз + 000000\nсобрано ядер + 000000\nвысадок + 000000\nэвакуаций + 000000\nистощений энергии mata\" + 000000\nфункция: рывок + 000000\nфункция: удар вниз + 000000\nв потоке\" + 000000\nзвездоудар + 000000\n",
"CLASSIC": "КЛАССИКА", "CUSTOM": "СВОЙ ЗАБЕГ",
"STRATA PERFORMANCE: 19200 / 00:00.000": "РЕЗУЛЬТАТ СТРАТЫ: 19200 / 00:00.000", "STRATA 3": "СТРАТА 3",
"STRATA 1-3": "СТРАТА 1-3", "STRATA 3-1": "СТРАТА 3-1", "NXT": "ДАЛ", "+ FawnStSv.onr - XX/04/7AS": "+ FawnСтСв.онр - XX/04/7ПС",
"SEE YOU SOON": "ДО СКОРОЙ ВСТРЕЧИ", "MUSEUM": "МУЗЕЙ",
"\"CASCADE_FIRST_ENTRY\"": "\"КАСКАД_ПЕРВЫЙ_ВХОД\"", "PLAY": "ИГРАТЬ", "HOLD TO SKIP": "УДЕРЖИВАЙ, ЧТОБЫ ПРОПУСТИТЬ",
"+ DASH": "+ РЫВОК", "+ STOMP": "+ УДАР ВНИЗ", "CLEARANCE_": "ДОПУСК_", "_CMPLT": "_ПРЙДН",
"PERSONAL BEST: 24124": "ЛИЧНЫЙ РЕКОРД: 24124", "99999XP/99999XP": "99999ОП/99999ОП",
"+ FAWN-A2 \"WHITE RABBIT\" - CARGO: 4C +": "+ FAWN-A2 \"БЕЛЫЙ КРОЛИК\" - ГРУЗ: 4Я +", "EX\nFL": "ЭВ\nАК",
"EMOTICORE NULLHEART": "ЭМОЦИЯДРО НУЛЬ-СЕРДЦЕ", "LOCATION, CASCADE": "МЕСТО, КАСКАД", "SPHERE": "СФЕРА",
"a clever fake\nis just as good as the real thing": "хорошая подделка\nничем не хуже оригинала",
"CCDAMTA / VER. TEST5": "CCDAMTA / ВЕР. TEST5", "+ DEMO_EXPIRY": "+ ДЕМО_ИСТЕКАЕТ", "_IN7": "_ИН7",
"ELAPSED TIME: 00.00.000\nCORES COLLECTED: 04\nTHREATS DISPATCHED: 12\nJUMPS PERFORMED: 2": "ПРОШЛО ВРЕМЕНИ: 00.00.000\nСОБРАНО ЯДЕР: 04\nУСТРАНЕНО УГРОЗ: 12\nСДЕЛАНО ПРЫЖКОВ: 2",
"_VIEWED": "_ПРОСМОТРЕН", "SPHERE 1-1 + RABBIT HOLE ": "СФЕРА 1-1 + КРОЛИЧЬЯ НОРА ", "BONUS SPHERES": "БОНУСНЫЕ СФЕРЫ",
"INITIATE CICADA": "ПОСВЯЩЁННАЯ ЦИКАДА", "2000000XP": "2000000ОП", "DEMO INITIATE": "ДЕМО-ПОСВЯЩЁННАЯ",
"+ CONCEIVER": "+ ЗАМЫСЛИВШАЯ", "CICADA KILLER": "УБИЙЦА ЦИКАД",
"JANUARY\nTIME SPENT + 00:00.000\nTHREATS DISPATCHED + 33333\n": "JANUARY\nВРЕМЯ В ИГРЕ + 00:00.000\nУСТРАНЕНО УГРОЗ + 33333\n",
"CORES COLLECTED + 44444\nDEPLOYMENTS + 32451\nZONED + 319381\n": "СОБРАНО ЯДЕР + 44444\nВЫСАДОК + 32451\nВ ПОТОКЕ + 319381\n",
"+ TEST_FILE.ONR": "+ ТЕСТ_ФАЙЛ.ОНР", "04_APR_7AS": "04_АПР_7ПС",
# animation finals
"CORE": "ЯДРО", "CORES": "ЯДРА", "EXIT": "ВЫХОД", "COMMENCING MATA\" TRANSFER...": "НАЧИНАЮ ПЕРЕНОС MATA\"...",
"JOY_RAIL_CHARGE\nL_R_MERGE\nWARMING_UP_55Y\nCONCRETIZING_IV": "JOY_ЗАРЯД_РЕЛЬСЫ\nL_R_СЛИЯНИЕ\nПРОГРЕВ_55Y\nКОНКРЕТИЗАЦИЯ_IV",
"ST_SV\nSAVE_US": "СТ_СВ\nСПАСИ_НАС", "IAM\nJOYEUSE": "Я\nJOYEUSE", "CHK...": "ПРВ...",
"FILE SELECT": "ВЫБОР ФАЙЛА", "+ Link Found +": "+ Связь найдена +", "+ Connecting... +": "+ Подключение... +",
"+ ERR: TIMEOUT +": "+ ОШБ: ТАЙМ-АУТ +", "+ INF_RDVL +": "+ ИНФ_КРВЛ +", "DIA: ATTEMPTING_CONNECTION": "ДИА: ПОПЫТКА_ПОДКЛЮЧЕНИЯ",
"+ Access Denied +": "+ Доступ запрещён +", "VANITY": "ОБЛИК", "Thank You\nFor Playing": "Спасибо\nЗа Игру",
"WHOAMI": "КТОЯ", "IAMJOYE\nUSE": "ЯJOYE\nUSE", "FOURCORES": "ЧЕТЫРЕЯДРА",
# decorative cipher-font labels (N4NOOSE; Cyrillic mapped onto the same cipher glyphs)
"IAMJOYEUSE": "ЯJOYEUSE", "ALERT": "ТРЕВОГА", "FIRSTDEPLOYMENT": "ПЕРВАЯВЫСАДКА", "SPHINFO": "СФИНФО",
"SPHRUSH": "СФЗБГ", "CR": "ЯД", "TRMNL": "ТРМНЛ", "HNT": "ПДСК", "SPHSLCT ": "ВБРСФ ", "CSCD": "КСКД",
"PTSEARN": "ОЧКПЛЧ", "TIMEBON": "БОНВРМ", "MATALVL": "УРВMATA", "LVLRUSH": "ЗБГУРВ", "MATASPEC": "ХАРMATA",
"QTNG": "ВХД", "CICADAFAWNA2IAMJOYEUSE\n": "ЦИКАДАFAWNA2ЯJOYEUSE\n", "THREAT": "УГРОЗА", "CCDA\n": "ЦКДА\n",
"IAMDEAD": "ЯМЕРТВА", "LDRBRDS": "ТБЛЛДР", "CNGRTS": "ПЗДРВЛ", "SRY": "ПРСТ", "OPTN": "НСТР", "EVENT": "СОБЫТИЕ",
"CCDARANK\n": "ЦКДАРАНГ\n", "GTFONOW": "ВАЛИСКОРЕЕ", "CH": "ПР",
"+ Lin +": "+ Св +", "+ Link Fo +": "+ Связь на +", "+ Con +": "+ Под +", "+ Connect +": "+ Подключ +",
"+ Connecting. +": "+ Подключение. +", "+ Connecting.. +": "+ Подключение.. +", "IAMJOYEUSELISTENT": "ЯJOYEUSEСЛУШАЙ",
})
