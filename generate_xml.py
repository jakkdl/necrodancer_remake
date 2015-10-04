import shutil
import xml.etree.ElementTree as ET



def getProp(item, attrib):
    if attrib in item.attrib:
        return item.attrib[attrib]
    return None

def prettyFly(name):
    if name == None:
        return None
    return name.split('|')[2].lower()


def listChances(xmlfile, rarities):
    items = {}

    tree = ET.parse(xmlfile)
    root = tree.getroot()

    def getRarity(item):
        for rarity_name, rarity_values in rarities.items():
            found = True
            for key, val in rarity_values.items():
                if getProp(item, key) != val:
                    found = False
                    break
            if found:
                return rarity_name
        return None

    for item in root[0]:
        rarity = getRarity(item)
        if rarity == None:
            continue
        if rarity not in items:
            items[rarity] = [item]
        else:
            items[rarity].append(item)
        #items.get(getRarity(item), []).append(item)

    for rarity, items_ in items.items():
        print(rarity, ":")
        sorted_items = sorted(prettyFly(getProp(i, 'flyaway')) for i in items_)
        for i in sorted_items:
            print(" "*10, i)


def sortOrder(rarity):
    if rarity == 'never':      return 0
    if rarity == 'common':     return 1
    if rarity == 'normal':     return 2
    if rarity == 'normal+urn': return 3
    if rarity == 'rare':       return 4
    if rarity == 'urnOnly':    return 5
    print('unkwnown rarity:', rarity)
    return None

def sort_print(item, rarity):
    print(sortOrder(rarity),
            (rarity + ":").ljust(11),
            prettyFly(item.attrib['flyaway']))

def vals(item, rarity):
    for key, val in rarity.items():
        item.attrib[key] = str(val)




def adjustChances(xmlfile, rarities):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    for item in root[0]:
        slot = getProp(item, 'slot')

        if slot == "spell":
            vals(item, rarities['rare'])

        elif slot == "ring":
            if     ('phasing' in item.tag or
                    'wonder' in item.tag):
                vals(item, rarities['never'])
            elif 'luck' in item.tag:
                item.attrib['hint'] = item.attrib['hint'].replace('FIND BETTER ITEMS', 'BAT IMMUNITY')
            elif   ('protection' in item.tag or
                    'shadows' in item.tag or
                    'charisma' in item.tag or
                    'gold' in item.tag or
                    'might' in item.tag or
                    'becoming' in item.tag):
                vals(item, rarities['normal'])

            elif   ('war' in item.tag or
                    'peace' in item.tag or
                    'mana' in item.tag or
                    'regeneration' in item.tag or
                    'shielding' in item.tag or
                    'courage' in item.tag):
                vals(item, rarities['rare'])
            else:
                print("unknown ring:", item.tag)

        #charms
        elif slot == 'misc':
            if ('key' in item.tag or
                    'magnet' in item.tag or
                    'potion' in item.tag):
                vals(item, rarities['never'])
            elif 'luck' in item.tag:
                #disable lucky charm
                item.attrib['hint'] = item.attrib['hint'].replace('FIND BETTER ITEMS', 'BAT IMMUNITY')
            else:
                vals(item, rarities['rare'])

        elif slot == 'action':
            if 'lord' in item.tag:
                vals(item, rarities['never'])
            elif getProp(item, 'isScroll'):
                vals(item, rarities['normal'])
            elif getProp(item, 'isFood'):
                if '1' in item.tag:   #apple
                    vals(item, rarities['common'])
                elif '2' in item.tag: #cheese
                    vals(item, rarities['common'])
                elif '3' in item.tag: #drumstick
                    vals(item, rarities['normal'])
                elif '4' in item.tag: #ham
                    vals(item, rarities['rare'])
            else:
                vals(item, rarities['normal'])

        elif slot == 'head':
            if 'ninja' in item.tag or 'crown_of_greed' in item.tag:
                vals(item, rarities['never'])
            else:
                vals(item, rarities['normal'])

        elif slot == 'shovel':
            if 'crystal' in item.tag:
                vals(item, rarities['urnOnly'])
            elif 'shard' in item.tag:
                vals(item, rarities['never'])
            else:
                vals(item, rarities['normal'])

        elif slot == 'torch':
            if '1' in item.tag:
                vals(item, rarities['common'])
            elif '2' in item.tag:
                vals(item, rarities['normal'])
            elif '3' in item.tag:
                vals(item, rarities['rare'])
            else:
                vals(item, rarities['normal'])
            
        elif slot == 'feet':
            if 'speed' in item.tag:
                vals(item, rarities['never'])
            vals(item, rarities['normal'])

        elif slot == 'bomb':
            if '3' in item.tag:
                vals(item, rarities['normal'])
            else:
                vals(item, rarities['common'])
        elif slot == 'hud':
            if 'backpack' in item.tag:
                vals(item, rarities['common'])
            elif 'holster' in item.tag:
                vals(item, rarities['common'])
            elif 'holding' in item.tag:
                vals(item, rarities['rare'])

        elif getProp(item, 'consumable'):
            if 'empty2' in item.tag:  #2 empty heart containers
                vals(item, rarities['normal'])
            elif 'empty' in item.tag: #1 empty heart container
                vals(item, rarities['common'])
            elif '2' in item.tag:     #2 full heart containers
                vals(item, rarities['rare'])
            else:                     #1 full heart container
                vals(item, rarities['normal'])

        elif slot == "body":
            if 'dorian' in item.tag:
                vals(item, rarities['never'])
            elif 'leather' in item.tag:
                vals(item, rarities['common'])
            elif 'chainmail' in item.tag:
                vals(item, rarities['normal'])
            elif 'armor_platemail' in item.tag:
                vals(item, rarities['normal'])
            elif 'heavyplate' in item.tag:
                vals(item, rarities['rare'])
            else:
                vals(item, rarities['normal'])

        elif slot == "weapon":
            if 'dagger_jeweled' in item.tag:
                vals(item, rarities['normal'])
            elif ('weapon_flower' in item.tag or
                    'golden_lute' in item.tag or
                    'weapon_dagger' == item.tag or
                    'dagger_shard' in item.tag):
                vals(item, rarities['never'])
            elif 'dagger' in item.tag:
                vals(item, rarities['common'])
            elif ('blunderbuss' in item.tag or
                    'rifle' in item.tag):
                vals(item, rarities['rare'])
            elif getProp(item, 'isFrost'):
                vals(item, rarities['normal'])
            elif getProp(item, 'isPhasing'):
                vals(item, rarities['normal'])
            elif getProp(item, 'isBlood'):
                vals(item, rarities['common'])
            elif getProp(item, 'isTitanium'):
                vals(item, rarities['normal'])
            elif getProp(item, 'isGlass'):
                vals(item, rarities['rare'])
            elif getProp(item, 'isObsidian'):
                vals(item, rarities['rare'])




    tree.write(xmlfile)

def goldToFrost(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    for item in root[0]:
        if 'dagger_frost' in item.tag:
            #remove piercing from frost dagger
            item.attrib['flyaway'] = item.attrib['flyaway'].replace('DAGGER OF FROST', 'FROST DAGGER')
            item.attrib['hint'] = item.attrib['hint'].replace(', PIERCING','')
            item.attrib['isPiercing'] = 'false'
        elif getProp(item, 'slot') == "weapon" and getProp(item, 'isGold'):
            if 'dagger' in item.tag:
                #add piercing to gold dagger
                item.attrib['isPiercing'] = 'true'
                item.attrib['hint'] = item.attrib['hint'][:-1] + ', PIERCING|'
                continue
            item.attrib['isGold'] = 'false'
            item.attrib['isFrost'] = 'true'
            item.attrib['hint'] = item.attrib['hint'].replace('HIGH DMG AFTER GOLD PICKUP', 'FREEZE ENEMIES, KILL FROZEN ENEMIES')
            item.attrib['flyaway'] = item.attrib['flyaway'].replace('GOLDEN', 'FROST')



    tree.write(xmlfile)

def baseToPhasing(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    for item in root[0]:
        if 'dagger_phasing' in item.tag:
            item.attrib['flyaway'] = item.attrib['flyaway'].replace('DAGGER OF PHASING', 'TITANIUM DAGGER')
            item.attrib['hint'] = item.attrib['hint'].replace(', 2 DMG','')
            item.attrib['isPhasing'] = 'false'
        elif 'titanium_dagger' in item.tag:
            item.attrib['flyaway'] = item.attrib['flyaway'].replace('TITANIUM DAGGER', 'PHASING DAGGER')
            item.attrib['isPhasing'] = 'true'
            item.attrib['hint'] = item.attrib['hint'].replace('2', 'PHASING')

        elif (getProp(item, 'slot') == "weapon" and
                'titanium' not in item.tag and
                'obsidian' not in item.tag and
                'golden' not in item.tag and
                'blood' not in item.tag and
                'glass' not in item.tag and
                'dagger' not in item.tag and
                'rifle' not in item.tag and
                'blunderbuss' not in item.tag and
                'flower' not in item.tag):
            #item.attrib['isGold'] = 'false'
            item.attrib['isPhasing'] = 'true'
            item.attrib['hint'] = item.attrib['hint'][:-1] + ', PHASING|'
            flyaway = item.attrib['flyaway'].split('|')
            flyaway[2] = 'PHASING ' + flyaway[2]
            item.attrib['flyaway'] = '|'.join(flyaway)



    tree.write(xmlfile)


fromxml = 'original.xml'
toxml = 'necrodancer.xml'


rarities = {
        'common': {
            'shopChance'       : '5000',
            'chestChance'      : '50',
            'lockedChestChance': '50',
            'lockedShopChance' : '0',
            'urnChance'        : '0'
            },

        'normal': {
            'shopChance'       : '100',
            'chestChance'      : '100',
            'lockedChestChance': '100',
            'lockedShopChance' : '100',
            'urnChance'        : '0'
            },

        'normal+urn': {
            'shopChance'       : '100',
            'chestChance'      : '100',
            'lockedChestChance': '100',
            'lockedShopChance' : '100',
            'urnChance'        : '100'
            },

        'rare': {
            'shopChance'       : '40',
            'chestChance'      : '40',
            'lockedChestChance': '40',
            'lockedShopChance' : '40',
            'urnChance'        : '100'
            },

        'urnOnly': {
            'shopChance'       : '0',
            'chestChance'      : '0',
            'lockedChestChance': '0',
            'lockedShopChance' : '0',
            'urnChance'        : '100'
            },

        'never': {
            'shopChance'       : '0',
            'chestChance'      : '0',
            'lockedChestChance': '0',
            'lockedShopChance' : '0',
            'urnChance'        : '0'
            }
        }

#xmlEnemyShuffle(todir + 'necrodancer.xml')
#listItems(todir + 'necrodancer.xml')
shutil.copyfile(fromxml, toxml)
goldToFrost(toxml)
baseToPhasing(toxml)
adjustChances(toxml, rarities)
listChances(toxml, rarities)
