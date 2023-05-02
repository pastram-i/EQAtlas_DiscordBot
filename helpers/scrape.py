import json, os, requests, sys

from bs4 import BeautifulSoup
import aiosqlite

from database.models import Zone, Connection, Link

def get_zones():
    if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/../../database/zones.json"):
        sys.exit("'zones.json' not found! Please add it and try again.")
    else:
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/../../database/zones.json") as file:
            return json.load(file)
        
def update_zones(update_link=False, update_db=False):
    #zone named needs to be manually added to zones.json, link will be generated
    j = get_zones()
    if update_link:
        ZONES_url = 'https://wiki.project1999.com/Zones'
        ZONES_page = requests.get(ZONES_url, verify=False)
        ZONES_soup = BeautifulSoup(ZONES_page.content, 'html.parser')

    for c in j:
        for t in c['zones']:
            for z in t['zones']:
                if update_link:
                    f = zone_link(z, ZONES_soup) if z['name'] != 'Beholder\'s Maze (Gorge of King Xorbb)' else '/Beholder%27s_Maze'
                    z['link'] = f"https://wiki.project1999.com{f}"
                if update_db:
                    parsed = parse_zone(c['continent'], t['type'], z['name'], z['link'])


    with open(f"{os.path.realpath(os.path.dirname(__file__))}/../../database/zones.json", 'w') as outfile:
        json.dump(j, outfile)

def zone_link(z, soup):
    by_title = soup.find('a', title=z['name'], href=True)['href']
    return by_title or soup.find('a', string=z['name'], href=True)['href']

def parse_zone(continent, type, name, url):
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    zone = Zone()
    connections = []
    links = []

    zone.name = name
    zone.continent = continent
    zone.type = type

    top_table_rows = soup.select('table.zoneTopTable tr')
    for r in top_table_rows:
        k = r.find('th').text.strip().lower().replace(':', '')
        if k == 'level_of_monsters':
            zone.level_of_monsters = r.find('td').text.strip()
        elif k == 'types of monsters':
            v = r.find('td').text.strip().split(',')
            for m in v:
                links.append(Link(
                    zone=zone,
                    value=m,
                    type='monster',
                    url=f"https://wiki.project1999.com/{m}"
                ))
        elif k == 'notable npcs':
            v = r.find('td').text.strip().split(',')
            for m in v:
                links.append(Link(
                    zone=zone,
                    value=m,
                    type='npc',
                    url=f"https://wiki.project1999.com/{m}"
                ))
        elif k == 'unique items':
            v = r.find('td').text.strip().split(',')
            for m in v:
                links.append(Link(
                    zone=zone,
                    value=m,
                    type='item',
                    url=f"https://wiki.project1999.com/{m}"
                ))
        elif k == 'related quests':
            v = r.find('td').text.strip().split(',')
            for m in v:
                links.append(Link(
                    zone=zone,
                    value=m,
                    type='quest',
                    url=f"https://wiki.project1999.com/{m}"
                ))
        elif k == 'adjacent zones':
            v = r.find('td').text.strip().split(',')
            for m in v:
                connections.append(Connection(
                    zone=zone,
                    connected_to=m,
                    ocean_connection=None,
                    one_way_connection=None,
                ))
        elif k == 'name in who':
            zone.name_in_who = r.find('td').text.strip()
        elif k == 'zone spawn timer':
            zone.zone_spawn_timer = r.find('td').text.strip()
        elif k == 'succorevacuate':
            zone.succor_evac = r.find('td').text.strip()
        elif k == 'zem  value':
            zone.zem_value = r.find('td').text.strip()
        elif k == 'minimum player level':
            zone.above_45 = True
        elif k == 'player guides':
            v = r.find('td').text.strip().split(',')
            for m in v:
                links.append(Link(
                    zone=zone,
                    value=m,
                    type='guide',
                    url=f"https://wiki.project1999.com/{m}"
                ))
        elif k == 'guilds':
            v = r.find('td').text.strip().split(',')
            for m in v:
                links.append(Link(
                    zone=zone,
                    value=m,
                    type='guild',
                    url=f"https://wiki.project1999.com/{m}"
                ))
        elif k == 'city races':
            v = r.find('td').text.strip().split(',')
            for m in v:
                links.append(Link(
                    zone=zone,
                    value=m,
                    type='city race',
                    url=f"https://wiki.project1999.com/{m}"
                ))
        elif k == 'tradeskill facilities':
            v = r.find('td').text.strip().split(',')
            for m in v:
                links.append(Link(
                    zone=zone,
                    value=m,
                    type='tradeskikll facility',
                    url=f"https://wiki.project1999.com/{m}"
                ))
        else:
            pass



    zone.url_name
    zone.friendly_name
    zone.url

    zone.key_required
    zone.firepot_port
    zone.shaman_port
    zone.druid_port
    zone.wizard_port

    return zone