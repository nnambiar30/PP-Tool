import json
import pandas as pd

player_dict = {}
final_table_pp = {}
dk_table = {'name': [],
            'line': [],
            'odds': [],
            'o/u':  [],
            'stats': []}
results = { 'name': [],
            'ppline': [],
            'dkline': [],
            'odds': [],
            'o/u': [],
            'stat': []
}
def pp():
    f = open('pp.json')
    data = json.load(f)

    final_table_pp['name'] = []
    final_table_pp['line'] = []
    final_table_pp['stat'] = []
    for i in (data['included']):
        if(i['type'] == 'new_player' and i['attributes']['league'] == 'NBA'):
            player_dict[i['id']] = i['attributes']['name']

    for i in (data['data']):
        if(i['relationships']['league']['data']['id'] == '7' and i['relationships']['stat_type']['data']['id'] == '19'):
            final_table_pp['name'].append(player_dict[i['relationships']['new_player']['data']['id']])
            final_table_pp['line'].append(i['attributes']['line_score'])
            final_table_pp['stat'].append('points')
        
        elif(i['relationships']['league']['data']['id'] == '7' and i['relationships']['stat_type']['data']['id'] == '20'):
            final_table_pp['name'].append(player_dict[i['relationships']['new_player']['data']['id']])
            final_table_pp['line'].append(i['attributes']['line_score'])
            final_table_pp['stat'].append('assists')

        elif(i['relationships']['league']['data']['id'] == '7' and i['relationships']['stat_type']['data']['id'] == '22'):
            final_table_pp['name'].append(player_dict[i['relationships']['new_player']['data']['id']])
            final_table_pp['line'].append(i['attributes']['line_score'])
            final_table_pp['stat'].append('rebounds')

    pp = pd.DataFrame(final_table_pp)
    # print(pp)

    #print(player_dict)
    f.close()
    # print(pp[0])
    return pp

def dk():   
    fp = open('dkpoints.json')
    fr = open('dkreb.json')
    fa = open('dkass.json')
    datar = json.load(fr)
    dataa = json.load(fa)
    datap = json.load(fp)
    for i in datap['eventGroup']['offerCategories']:
        if(i['offerCategoryId'] == 1215):
            for j in i['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']:
                for x in j:
                    for z in x['outcomes']:
                        dk_table['name'].append(z['participant'])
                        dk_table['line'].append(z['line'])
                        dk_table['odds'].append(z['oddsAmerican'])
                        dk_table['o/u'].append(z['label'])
                        dk_table['stats'].append('points')

    for i in datar['eventGroup']['offerCategories']:
        if(i['offerCategoryId'] == 1216):
            for j in i['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']:
                for x in j:
                    for z in x['outcomes']:
                        dk_table['name'].append(z['participant'])
                        dk_table['line'].append(z['line'])
                        dk_table['odds'].append(z['oddsAmerican'])
                        dk_table['o/u'].append(z['label'])
                        dk_table['stats'].append('rebounds')
    for i in dataa['eventGroup']['offerCategories']:
        if(i['offerCategoryId'] == 1217):
            for j in i['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']:
                for x in j:
                    for z in x['outcomes']:
                        dk_table['name'].append(z['participant'])
                        dk_table['line'].append(z['line'])
                        dk_table['odds'].append(z['oddsAmerican'])
                        dk_table['o/u'].append(z['label'])
                        dk_table['stats'].append('assists')
    dx = pd.DataFrame(dk_table)      

    # for i in range(len(dk_table['name'])):
    #     for x in dk_table:
    #         print(dk_table[x][i])
    # print(dx)      
    fa.close()
    fr.close()
    fp.close()
    return dx

def calcFinal():
    for x in range(len(final_table_pp['name'])):
        for y in range(len(dk_table['name'])):
            if final_table_pp['name'][x] == dk_table['name'][y] and final_table_pp['stat'][x] == dk_table['stats'][y] and (abs(final_table_pp['line'][x] - dk_table['line'][y]) <= 0.5) and float(dk_table['odds'][y]) <= -140:
                results['name'].append(final_table_pp['name'][x])
                results['ppline'].append(final_table_pp['line'][x])
                results['dkline'].append(dk_table['line'][y])
                results['odds'].append(dk_table['odds'][y])
                results['o/u'].append(dk_table['o/u'][y])
                results['stat'].append(final_table_pp['stat'][x])
    res = pd.DataFrame(results)
    print(res.sort_values(by=['odds'], ascending=False))  
   # print(res)   

pp()
dk()
calcFinal()