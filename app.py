from flask import Flask, render_template, request
from datetime import datetime, timedelta
import csv

app = Flask("SxS Helper")

@app.route("/")
def index():
    return render_template("index.html")

class_chain = [
    ["Magister", "Destroyer", "Archmage", "Sorcerer", "Mage"],
    ["Prophet", "Dominator", "Arcanist", "Sage", "Mage"],
    ["Ravager", "Conqueror", "Berserker", "Duelist", "Warrior"],
    ["Templar", "Guardian", "Paladin", "Knight", "Warrior"]
]

base_qualities = ["Legendary", "Epic", "Rare"]
quality_order =["Rare", "Epic", "Legendary", "Mythic", "Divine", "Immortal"]
summon_skills = ["Stonechief Summon", "Flame Wolf Summon", "Treantling Summon", "Frenzy Totem", "Waterling Summon", "Rock Rex Summon", "Decoy Clone", "Soulweave", "Thalasson Summon"]

multi_skills = {
    "Frost Guard": {
        "attributes": {
            "Healing Bonus": {
                "Legendary": 2.16,
                "Mythic": 2.36,
                "Divine": 2.7,
                "Immortal": 3.1
            }, "DMG Reduction": {
                "Legendary": 20.80,
                "Mythic": 26.00,
                "Divine": 31.20,
                "Immortal": 36.40
            }
        }
    }
}

today_reset = datetime.now().replace(hour=7, minute=59, second=0, microsecond=0)
default_time = today_reset.strftime("%Y-%m-%dT%H:%M")
if (datetime.now() > today_reset):
    default_time = today_reset.replace(day=today_reset.day + 1).strftime("%Y-%m-%dT%H:%M")

@app.route("/experience-calculator", methods=["GET", "POST"])
def experience_calculator():
    if request.method == 'POST':
        current_level = int(request.form.get('current_level'))
        current_experience = int(request.form['current_experience'])
        exp_per_hour = int(request.form.get('exp_per_hour'))

        boost_count = 1
        today_reset = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)    
        next_reset = today_reset
        if (request.form.get('today_boosted')):
            boost_count = 0
        if (datetime.now() > today_reset):
            next_reset = today_reset.replace(day=today_reset.day + 1)
        boost_diff = (next_reset - datetime.now()).total_seconds() / 3600
        if request.form.get('target_level'):
            target_level = request.form.get('target_level')
        else:
            target_level = current_level + 1
        total_xp_needed = 0 - current_experience
        for level in range(current_level, target_level):
            total_xp_needed += loong_exp[level] * 10000
        hours_left = total_xp_needed / exp_per_hour
        target_boost_count = boost_count
        if hours_left > boost_diff:
            target_boost_count = (hours_left - boost_diff) // 24
        hours_left -= target_boost_count * 2
        target_time = datetime.now() + timedelta(hours=hours_left)
        target_time = target_time.strftime("%Y-%m-%dT%H:%M")
        hours_left = round(max(0, hours_left), 2)


        calculated_level = current_level
        future = datetime.fromisoformat(request.form['time_left'])
        present = datetime.now()
        time_left = (future - present).total_seconds() // 3600
        timed_boost_count = boost_count + ((time_left - boost_diff) // 24)
        total_experience_gained = time_left * exp_per_hour + timed_boost_count * 2 * exp_per_hour
        current_exp_needed = loong_exp[current_level] * 10000 - current_experience
        while total_experience_gained >= current_exp_needed:
            calculated_level += 1
            total_experience_gained -= current_exp_needed
            current_exp_needed = loong_exp[calculated_level] * 10000
        calculated_level += (total_experience_gained / current_exp_needed)
        calculated_level = round(calculated_level, 2)

        return render_template("experience-calculator.html", 
            hours_left=hours_left,
            target_time=target_time,
            calculated_level=calculated_level,
            time_left=request.form.get('time_left'), 
            default_time=default_time,
            current_level=current_level, 
            current_experience=current_experience,
            exp_per_hour=exp_per_hour,  
            target_level=target_level,
            today_boosted=request.form.get('today_boosted'))
    else:
        return render_template("experience-calculator.html", default_time=default_time)

loong_exp = {
    130: 634,
    131: 679,
    132: 734,
    133: 789,
    134: 843,
    135: 894,
    136: 953,
    137: 1006,
    138: 1059,
    139: 1120,
    140: 1128,
    141: 1133,
    142: 1138,
    143: 1144,
    144: 1149,
    145: 1154,
    146: 1159,
    147: 1165,
    148: 1167,
    149: 1173,
    150: 1178,
    151: 1181,
    152: 1183,
    153: 1186,
    154: 1191,
    155: 1197,
    156: 1204,
    157: 1215,
    158: 1220,
    159: 1226,
    160: 1231,
    161: 1239,
    162: 1244,
    163: 1250,
    164: 1250,
    165: 1252,
    166: 1257,
    167: 1263,
    168: 1265,
    169: 1271,
    170: 1276,
    171: 1281,
    172: 1287,
    173: 1295,
    174: 1302,
    175: 1308,
    176: 1313,
    177: 1318,
    178: 1321,
    179: 1326,
    180: 1332,
    181: 1337,
    182: 1339,
    183: 1342,
    184: 1345,
    185: 1347,
    186: 1347,
    187: 1347,
    188: 1347,
    189: 1347,
    190: 1347,
    191: 1347,
    192: 1347,
    193: 1347,
    194: 1347,
    195: 1347,
    196: 1347,
    197: 1347,
    198: 1347,
    199: 1347,
    200: 1347,
    201: 1347,
    202: 1347,
    203: 1347,
    204: 1347,
    205: 1347,
    206: 1347,
    207: 1347,
    208: 1347,
    209: 1347,
    210: 1347,
    211: 1347,
    212: 1347,
    213: 1347,
    214: 1347,
    215: 1347,
    216: 1347,
    217: 1347,
    218: 1347,
    219: 1347,
    220: 1347,
    221: 1347,
    222: 1347,
    223: 1347,
    224: 1347,
    225: 1347,
    226: 1347,
    227: 1347,
    228: 1347,
    229: 1347,
}

@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == 'POST':
        selected_class = request.form.get('selected_class')
        skills_data = get_skills(selected_class)
        return render_template("skills.html", 
            selected_class=selected_class,
            skills_data=skills_data, 
            base_qualities=base_qualities,
            quality_order=quality_order,
            summon_skills=summon_skills,
            multi_skills=multi_skills) 
    else:
        return render_template("skills.html",
            skills_data={},
            base_qualities=base_qualities,
            quality_order=quality_order,
            summon_skills=summon_skills,
            multi_skills=multi_skills)

def get_skills(class_filter):
    skills = []
    classes = get_chain(class_filter)

    with open('s3_skills.csv', newline='') as skills_file:
        reader = csv.DictReader(skills_file)
        for row in reader:
            if row['Class'] in classes:
                skills.append(row)

    organized = {}
    types = ["Technique", "Charm"]
    quality = ["Rare", "Epic", "Legendary"]
    for c in classes:
        organized[c] = {}
        for t in types:
            organized[c][t] = {}
            for q in quality:
                organized[c][t][q] = []


    for skill in skills:
        organized[skill['Class']][skill['Type']][skill['Base']].append(skill)
        
    return organized

def get_chain(chosen_class):
    chains = []
    for chain in class_chain:
        if chosen_class in chain:
            for c in chain:
                if c == chosen_class:
                    chains.append(c)
                elif chosen_class in chains:
                    chains.append(c)
    return chains

@app.route("/cart-calculator", methods=["GET", "POST"])
def cart_calculator():
    season = request.form.get('season')
    season_max = get_cart_max(season)
    cart_data = get_cart(season_max)

    if request.method == 'POST':
        future = datetime.fromisoformat(request.form['time_left'])
        present = datetime.now()
        time_left = (future - present).total_seconds() // 3600
        time_left += (time_left // 24) * 2

        cart_level = {}
        bonus = {}
        priority = [[], [], [], [], [], [], [], []]
        total_output = {}
        for resource in resource_types:
            order = int(request.form.get(f"{resource}_priority"))
            priority[order].append(f"{resource}")
            bonus[f"{resource}_bonus"] = float(request.form.get(f"{resource}_bonus"))
            total_output[f"{resource}_output"] = 0   
            cart_level[f"{resource}_lvl"] = int(request.form.get(f"{resource}_level"))     

        while time_left > 0:
            hourly_update(cart_level, bonus, priority, total_output, cart_data, season_max)
            time_left -= 1

        print(total_output)

        for resource in resource_types:
            total_output[f"{resource}_output"] = int(total_output[f"{resource}_output"])

        return render_template("cart-calculator.html",
                                resource_types=resource_types,
                                cart_level=cart_level,
                                bonus=bonus,
                                total_output=total_output,
                                time_left=future)
    else: 
        cart_level = {}
        bonus = {}
        total_output = {}
        return render_template("cart-calculator.html",
                                resource_types=resource_types,
                                cart_level=cart_level,
                                bonus=bonus,
                                total_output=total_output)

resource_types = ["Rolla", "Wood", "Stone", "Ore", "Essence", "Sand", "Pet"]
resource_display = ["Rolla", "Wood", "Stone", "Raw Ore", "Battle Essence", "Chrono Sand", "Pet Food"]
def get_cart(max_level):
    cart = {}
    with open('cart.csv', newline='') as cart_file:
        reader = csv.DictReader(cart_file)
        for row in reader:
            level = row['Lvl']
            cart[level] = row
    return cart

def get_cart_max(season):
    if season == "2":
        return 108
    else:
        return 152

def hourly_update(cart_level, bonus, priority, total_output, cart_data, season_max):
    for resource in resource_types:
        current_bonus = float(bonus[f"{resource}_bonus"]) / 100 + 1
        output = int(cart_data[str(cart_level[f"{resource}_lvl"])][f"{resource} Output"])
        hourly_output = current_bonus * output
        total_output[f"{resource}_output"] = int(total_output[f"{resource}_output"]) + hourly_output

    for order in range(1, len(priority)):
        if priority[order]:
            if max_leveled(priority, order, cart_level, season_max) == False:
                if equal_levels(priority, order, cart_level):
                    for resource in priority[order]:
                        upgrade_cart(resource, total_output, cart_data, cart_level, season_max)
                else: 
                    resource = get_lowest_level(priority, order, cart_level, season_max)
                    upgrade_cart(resource, total_output, cart_data, cart_level, season_max)
                break


def max_leveled(priority, order, cart_level, season_max):
    for resource in priority[order]:
        if (int(cart_level[f"{resource}_lvl"] != season_max)):
            return False
    return True


def equal_levels(priority, order, cart_level):
    levels = []
    for resource in priority[order]:
        levels.append(cart_level[f"{resource}_lvl"])

    if len(levels) == 1:
        return True
    else:
        for resource in range(1, len(levels)):
            if (levels[resource] != levels[resource - 1]):
                return False
        return True

def upgrade_cart(resource, total_output, cart_data, cart_level, season_max):
    current_wood = int(total_output["Wood_output"])
    current_stone = int(total_output["Stone_output"])
    level = str(cart_level[f"{resource}_lvl"])
    stone_cost = int(cart_data[level][f"{resource} Stone Cost"])
    wood_cost = int(cart_data[level][f"{resource} Wood Cost"])
    if current_wood > wood_cost and current_stone > stone_cost:
        if int(level) < season_max:
            total_output["Wood_output"] -= wood_cost
            total_output["Stone_output"] -= stone_cost
            cart_level[f"{resource}_lvl"] = cart_level[f"{resource}_lvl"] + 1

def get_lowest_level(priority, order, cart_level, season_max):
    levels = []
    resources = []
    for resource in priority[order]:
        levels.append(cart_level[f"{resource}_lvl"])
        resources.append(resource)

    length = len(levels)
    min = levels[0]
    index = 0
    if length == 1:
        return resources[index]
    else:
        for x in range(1, length):
            if levels[x] < min and levels[x] < season_max:
                min = levels[x]
                index = x
    return resources[index]
