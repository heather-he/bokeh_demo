{}# import pacakges
import networkx as nx

import pandas as pd
import numpy as np
import datetime as dt
from scipy.stats import spearmanr
import math

from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool, ResetTool, BoxZoomTool, LabelSet, CDSView, ColumnDataSource, PanTool, Legend, Slider, RadioGroup
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Blues4
from bokeh.plotting import figure
from bokeh.models.widgets import CheckboxGroup,Select, Button, Div, MultiSelect, DataTable, TableColumn, TextInput
from bokeh.models.annotations import LabelSet, Span
from bokeh.io import curdoc
from bokeh.layouts import layout, column, row
from bokeh.events import Tap


########################################################################################################################
########################################################################################################################
# import provider data
df_trna_p1 = pd.read_csv('trna_provider.csv')
df_trna_p1['fre_all'] = df_trna_p1['fre_all']/1000
df_trna_p1['fre_tyt'] = df_trna_p1['fre_tyt']/1000

#import topic and region data
df_trna_p2p3 = pd.read_csv('trna_topic_reg.csv')
for col in ['topic_all','topic_tyt','reg_all','reg_tyt']:
    df_trna_p2p3[col] = df_trna_p2p3[col]/1000

###news provider
trna_p1_cds = ColumnDataSource(data = {'y':df_trna_p1['fre_all_factor'],
                                    'right':df_trna_p1['fre_all']})
###main topics
trna_p2_cds = ColumnDataSource(data = {'y':df_trna_p2p3['topic_all_factor'],
                                    'right':df_trna_p2p3['topic_all']})

trna_p3_cds = ColumnDataSource(data = {'y':df_trna_p2p3['reg_all_factor'],
                                    'right':df_trna_p2p3['reg_all']})

def create_figure_trna():
    kw = {}
    if multi_select_indicator.value == ['provider']:
        if multi_select_scope.value ==['all']:
            trna_p1_cds.data['y'] = df_trna_p1['fre_all_factor']
            trna_p1_cds.data['right'] = df_trna_p1['fre_all']
            kw['y_range'] = df_trna_p1['fre_all_factor']
            trna = figure(**kw)
            trna.title.text = 'Main news provider for TRNA'


        elif multi_select_scope.value ==['tyt']:
            trna_p1_cds.data['y'] = df_trna_p1['fre_tyt_factor']
            trna_p1_cds.data['right'] = df_trna_p1['fre_tyt']
            kw['y_range'] = df_trna_p1['fre_tyt_factor']
            trna = figure(**kw)
            trna.title.text = 'Main news provider for Toyota news'

        trna.hbar(y = 'y', height= 0.5, right = 'right',source = trna_p1_cds)
        trna.xaxis.axis_label = 'Total number of news items provided (k)'


    elif multi_select_indicator.value == ['topic']:
        if multi_select_scope.value ==['all']:
            trna_p2_cds.data['y'] = df_trna_p2p3['topic_all_factor']
            trna_p2_cds.data['right'] = df_trna_p2p3['topic_all']
            kw['y_range'] = df_trna_p2p3['topic_all_factor']
            trna = figure(**kw)
            trna.title.text = 'Most frequently reported topics in TRNA'


        elif multi_select_scope.value ==['tyt']:
            trna_p2_cds.data['y'] = df_trna_p2p3['topic_tyt_factor']
            trna_p2_cds.data['right'] = df_trna_p2p3['topic_tyt']
            kw['y_range'] = df_trna_p2p3['topic_tyt_factor']
            trna = figure(**kw)
            trna.title.text = 'Most frequently reported topics in Toyota news'

        trna.hbar(y = 'y', height= 0.5, right = 'right',source = trna_p2_cds)
        trna.xaxis.axis_label = 'Frequency of each topics being reported (k)'

    elif multi_select_indicator.value == ['reg']:
        if multi_select_scope.value ==['all']:
            trna_p3_cds.data['y'] = df_trna_p2p3['reg_all_factor']
            trna_p3_cds.data['right'] = df_trna_p2p3['reg_all']
            kw['y_range'] = df_trna_p2p3['reg_all_factor']
            trna = figure(**kw)
            trna.title.text = 'Most frequently reported regions in TRNA'

        elif multi_select_scope.value ==['tyt']:
            trna_p3_cds.data['y'] = df_trna_p2p3['reg_tyt_factor']
            trna_p3_cds.data['right'] = df_trna_p2p3['reg_tyt']
            kw['y_range'] = df_trna_p2p3['reg_tyt_factor']
            trna = figure(**kw)
            trna.title.text = 'Most frequently reported regions in Toyota news'

        trna.hbar(y = 'y', height= 0.5, right = 'right',source = trna_p3_cds)
        trna.xaxis.axis_label = 'Frequency of each regions being reported (k)'


    trna.height = 500
    trna.width = 500

    trna.title.text_font_size = '15px'
    trna.xaxis.axis_label_text_font_size = '15px'

    trna.toolbar.logo = None
    trna.tools = [PanTool(),ResetTool()]

    return trna

def update_trna():
    layout_trna.children[-1] = create_figure_trna()

multi_select_scope = MultiSelect(title='Select news scope',
                           value=["all"],
                           options=[("all","All news in TRNA"),
                                    ("tyt", "News related to Toyota")])

multi_select_indicator = MultiSelect(title = 'Select indictor',
                                    value = ["provider"],
                                    options = [("provider","Main news provider"),
                                                ("topic","Most frequently reported topics"),
                                                ("reg","Most frequently reported regions")])
button = Button(label = 'Confirm Select',width = 600)

button.on_click(update_trna)


pre_trna = Div(text =
'''
<h2> Summary on Thomas Reuters News Analytics Data</h2>
<p>
Thomas Reuters News Analytics (TRNA) is a system which can read and interpret news automatically.
It tracks more than 25,000 equities and nearly 40 commodities and energy topics.
</p>
<p>
In the figure below, you will see:1) the main news provider; 2) the most-frequently reported topics; 3) the most-frequently reported regions in TRNA, and also for Toyota-related news.
</p>
''',
width = 1400, height = 120)


control_trna=row([multi_select_scope,multi_select_indicator])
layout_trna = column([pre_trna,control_trna,button,create_figure_trna()])

#################################################################################
#################################################################################

df_nx = pd.read_csv('TotalNX_raw.csv')
df_mktcap = pd.read_csv('TotalNX_mktcap.csv')

dict_edgess = {}
dict_edgess['start'] = []
dict_edgess['stop'] = []
dict_edgess['level'] = []
dict_edgess['color'] = []
for key,label in df_nx.iterrows():
    node1 = label['Target']
    for com in label['Competitors'].split(', '):
        node2 = com
        dict_edgess['start'].append(node1)
        dict_edgess['stop'] .append(node2)
        dict_edgess['level'].append('com')
        dict_edgess['color'].append('orange')
    for col in label['Collaborators'].split(', '):
        node2 = col
        dict_edgess['start'].append(node1)
        dict_edgess['stop'] .append(node2)
        dict_edgess['level'].append('col')
        dict_edgess['color'].append(Blues4[1])
df_edges = pd.DataFrame.from_dict(dict_edgess, orient= 'columns')

G = nx.convert_matrix.from_pandas_edgelist(df_edges,source='start',target='stop',edge_attr=True )

# add attributes (coms/cols to nodes)
node_attr = {}
for u in list(G.nodes()):
    com_str = ''
    col_str = ''
    mkt_cap = round(df_mktcap[df_mktcap.Company == u]['MktCapMilUSD']/1000,2)
    size = math.pow(mkt_cap*10,0.5)
    for v in list(G.neighbors(u)):
        if G.edges[u, v]['level'] == 'com':
            if com_str == '':
                com_str = v
            else:
                com_str = com_str+', '+v
        else:
            if col_str == '':
                col_str = v
            else:
                col_str = col_str+', '+v
    node_attr[u] = {'competitors':com_str, 'collaborators': col_str,'marketcap':mkt_cap,'size':size}

nx.set_node_attributes(G,node_attr)

# add pre-processed attr to edges

edge_attr = {('Toyota', 'Daimler'): {'link': 1197.0, 'width': 8.383555526381897},
 ('Toyota', 'BMW'): {'link': 3646.0, 'width': 11.709679255337296},
 ('Toyota', 'Ford'): {'link': 8425.0, 'width': 15.054660733864615},
 ('Toyota', 'Honda'): {'link': 8517.0, 'width': 15.103791930831333},
 ('Toyota', 'Nissan'): {'link': 7298.0, 'width': 14.419863778394722},
 ('Toyota', 'Tesla'): {'link': 587.0, 'width': 6.7700430507310205},
 ('Toyota', 'Volkswagen'): {'link': 4356.0, 'width': 12.351689374987615},
 ('Toyota', 'Hyundai'): {'link': 2484.0, 'width': 10.43627411183484},
 ('Toyota', 'General Motor'): {'link': 6404.0, 'width': 13.865495587870672},
 ('Toyota', 'Peugeot'): {'link': 1124.0, 'width': 8.226780185306504},
 ('Toyota', 'Renault'): {'link': 1020.0, 'width': 7.990612154170351},
 ('Toyota', 'SAIC'): {'link': 117.0, 'width': 4.1730708532587215},
 ('Toyota', 'Geely'): {'link': 107.0, 'width': 4.062703547247622},
 ('Toyota', 'Audi'): {'link': 1089.0, 'width': 8.14907592085283},
 ('Toyota', 'Toyota Industries'): {'link': 36.0, 'width': 2.930156051583521},
 ('Toyota', 'JTEKT'): {'link': 24.0, 'width': 2.594557933960465},
 ('Toyota', 'Toyota Tsusho'): {'link': 72.0, 'width': 3.6074452531358503},
 ('Toyota', 'Aisin Seiki'): {'link': 44.0, 'width': 3.1119728754884552},
 ('Toyota', 'Toyoda Gosei'): {'link': 25.0, 'width': 2.626527804403767},
 ('Toyota', 'DENSO'): {'link': 275.0, 'width': 5.392619876708788},
 ('Toyota', 'Toyota Boshoku'): {'link': 28.0, 'width': 2.7173614464666307},
 ('Toyota', 'Isuzu'): {'link': 299.0, 'width': 5.529697276636928},
 ('Toyota', 'Yamaha Motor Corporation'): {'link': 99.0,
  'width': 3.969086450680869},
 ('Toyota', 'Panasonic'): {'link': 1185.0, 'width': 8.358252850417093},
 ('Toyota', 'Suzuki'): {'link': 886.0, 'width': 7.660023756983168},
 ('Daimler', 'General Motor'): {'link': 1404.0, 'width': 8.794479326665492},
 ('Daimler', 'Volkswagen'): {'link': 1986.0, 'width': 9.758740582119596},
 ('Daimler', 'BMW'): {'link': 2210.0, 'width': 10.076684988383805},
 ('Daimler', 'Ferrari'): {'link': 6.0, 'width': 1.711769859409705},
 ('Daimler', 'Ford'): {'link': 1099.0, 'width': 8.171453388018401},
 ('Daimler', 'Tata'): {'link': 286.0, 'width': 5.456445351652516},
 ('Daimler', 'Geely'): {'link': 33.0, 'width': 2.8546586347325023},
 ('Daimler', 'FCA'): {'link': 742.0, 'width': 7.2630857498532615},
 ('Daimler', 'Tesla'): {'link': 256.0, 'width': 5.278031643091578},
 ('Daimler', 'Audi'): {'link': 571.0, 'width': 6.714146798776599},
 ('Daimler', 'Porsche'): {'link': 424.0, 'width': 6.1405851355603245},
 ('Daimler', 'Thyssenkrupp'): {'link': 104.0, 'width': 4.028190508306193},
 ('Daimler', 'Eagle Ottawa'): {'link': 6.0, 'width': 1.711769859409705},
 ('Daimler', 'Inteva Products'): {'link': 6.0, 'width': 1.711769859409705},
 ('Daimler', 'Nemak'): {'link': 6.0, 'width': 1.711769859409705},
 ('Daimler', 'Johnson Electric'): {'link': 6.0, 'width': 1.711769859409705},
 ('Daimler', 'ZF Lenksysteme'): {'link': 6.0, 'width': 1.711769859409705},
 ('Daimler', 'Honda'): {'link': 614.0, 'width': 6.8619968023628495},
 ('Daimler', 'SAIC'): {'link': 42.0, 'width': 3.068843822095698},
 ('Daimler', 'Isuzu'): {'link': 66.0, 'width': 3.5144970301577456},
 ('BMW', 'General Motor'): {'link': 2927.0, 'width': 10.962934433948192},
 ('BMW', 'Volkswagen'): {'link': 3819.0, 'width': 11.873667892654328},
 ('BMW', 'Tata'): {'link': 297.0, 'width': 5.518574817074292},
 ('BMW', 'Geely'): {'link': 85.0, 'width': 3.791627615651737},
 ('BMW', 'Honda'): {'link': 2639.0, 'width': 10.627517213377699},
 ('BMW', 'Hyundai'): {'link': 951.0, 'width': 7.824456043197678},
 ('BMW', 'FCA'): {'link': 1201.0, 'width': 8.391950281995028},
 ('BMW', 'Audi'): {'link': 1921.0, 'width': 9.661803696225665},
 ('BMW', 'Porsche'): {'link': 1771.0, 'width': 9.428998537103112},
 ('BMW', 'Brembo'): {'link': 27.0, 'width': 2.6878753795222865},
 ('BMW', 'Thyssenkrupp'): {'link': 116.0, 'width': 4.162338506563337},
 ('BMW', 'BorgWarner'): {'link': 90.0, 'width': 3.8572052822268215},
 ('BMW', 'Elringklinger'): {'link': 19.0, 'width': 2.4189454814875875},
 ('BMW', 'Bridgestone'): {'link': 165.0, 'width': 4.626421347685184},
 ('BMW', 'Mahle'): {'link': 12.0, 'width': 2.1074358993444706},
 ('BMW', 'Tesla'): {'link': 164.0, 'width': 4.617991768029603},
 ('Ford', 'General Motor'): {'link': 11191.0, 'width': 16.393084168453125},
 ('Ford', 'Volkswagen'): {'link': 4524.0, 'width': 12.49271346035393},
 ('Ford', 'Hyundai'): {'link': 2353.0, 'width': 10.26801697927448},
 ('Ford', 'Tata'): {'link': 577.0, 'width': 6.735234854151509},
 ('Ford', 'Honda'): {'link': 6057.0, 'width': 13.635694799990336},
 ('Ford', 'Tesla'): {'link': 531.0, 'width': 6.569440088225624},
 ('Ford', 'Renault'): {'link': 1236.0, 'width': 8.464582481114899},
 ('Ford', 'FCA'): {'link': 3047.0, 'width': 11.09587961663363},
 ('Ford', 'Nissan'): {'link': 5349.0, 'width': 13.136563799357676},
 ('Ford', 'Peugeot'): {'link': 1427.0, 'width': 8.837454522521941},
 ('Ford', 'Geely'): {'link': 181.0, 'width': 4.756676020942042},
 ('Ford', 'Suzuki'): {'link': 599.0, 'width': 6.811269224912827},
 ('Ford', 'NHK Spring'): {'link': 61.0, 'width': 3.4324083555054865},
 ('Ford', 'SAIC'): {'link': 141.0, 'width': 4.41332320594846},
 ('Ford', 'Audi'): {'link': 1041.0, 'width': 8.039614389892176},
 ('Ford', 'Isuzu'): {'link': 288.0, 'width': 5.4678645329573055},
 ('Ford', 'Yamaha Motor Corporation'): {'link': 67.0,
  'width': 3.5303880208226968},
 ('Honda', 'General Motor'): {'link': 4235.0, 'width': 12.247741861060948},
 ('Honda', 'Volkswagen'): {'link': 2881.0, 'width': 10.910960347887551},
 ('Honda', 'Hyundai'): {'link': 2034.0, 'width': 9.828908329257011},
 ('Honda', 'Nissan'): {'link': 5398.0, 'width': 13.172550252815595},
 ('Honda', 'FCA'): {'link': 1149.0, 'width': 8.281252154517615},
 ('Honda', 'Mitsubishi Motor'): {'link': 275.0, 'width': 5.392619876708788},
 ('Honda', 'Suzuki'): {'link': 982.0, 'width': 7.900115601809375},
 ('Honda', 'Tata'): {'link': 324.0, 'width': 5.664525067769412},
 ('Honda', 'Isuzu'): {'link': 150.0, 'width': 4.496011130479918},
 ('Honda', 'Tesla'): {'link': 170.0, 'width': 4.668041156493942},
 ('Honda', 'Peugeot'): {'link': 536.0, 'width': 6.587936992707819},
 ('Honda', 'Renault'): {'link': 662.0, 'width': 7.018711588426945},
 ('Honda', 'SAIC'): {'link': 78.0, 'width': 3.6951185877797474},
 ('Honda', 'Geely'): {'link': 83.0, 'width': 3.764639786125727},
 ('Honda', 'Audi'): {'link': 687.0, 'width': 7.097199628102596},
 ('Honda', 'Yamaha Motor Corporation'): {'link': 131.0,
  'width': 4.3169934398356835},
 ('Nissan', 'General Motor'): {'link': 3716.0, 'width': 11.776675584870901},
 ('Nissan', 'Volkswagen'): {'link': 2893.0, 'width': 10.92457448512156},
 ('Nissan', 'Hyundai'): {'link': 1873.0, 'width': 9.588735371815519},
 ('Nissan', 'Mitsubishi Motor'): {'link': 271.0, 'width': 5.368967650924707},
 ('Nissan', 'Renault'): {'link': 1724.0, 'width': 9.353220620367958},
 ('Nissan', 'Tesla'): {'link': 401.0, 'width': 6.0386980144698},
 ('Nissan', 'Suzuki'): {'link': 706.0, 'width': 7.1555234663517435},
 ('Nissan', 'Peugeot'): {'link': 768.0, 'width': 7.338518037139213},
 ('Nissan', 'SAIC'): {'link': 101.0, 'width': 3.9929733546852777},
 ('Nissan', 'Geely'): {'link': 87.0, 'width': 3.8181745258867683},
 ('Nissan', 'Audi'): {'link': 575.0, 'width': 6.728222630300609},
 ('Nissan', 'Yamaha Motor Corporation'): {'link': 41.0,
  'width': 3.0467383348995827},
 ('Tesla', 'General Motor'): {'link': 546.0, 'width': 6.624571514496293},
 ('Tesla', 'Hyundai'): {'link': 50.0, 'width': 3.233635032886787},
 ('Tesla', 'Volkswagen'): {'link': 82.0, 'width': 3.7509748799354137},
 ('Tesla', 'Kia'): {'link': 32.0, 'width': 2.82842712474619},
 ('Tesla', 'Tata'): {'link': 40.0, 'width': 3.0242521453322184},
 ('Tesla', 'Kandi Technologies'): {'link': 20.0, 'width': 2.4564560522315806},
 ('Tesla', 'Navistar'): {'link': 10.0, 'width': 1.9952623149688795},
 ('Tesla', 'Oshkosh'): {'link': 14.0, 'width': 2.2071833466585677},
 ('Tesla', 'Paccar'): {'link': 7.0, 'width': 1.7927899625209969},
 ('Tesla', 'Spartan'): {'link': 6.0, 'width': 1.711769859409705},
 ('Tesla', 'Wabco'): {'link': 6.0, 'width': 1.711769859409705},
 ('Tesla', 'Brembo'): {'link': 6.0, 'width': 1.711769859409705},
 ('Tesla', 'Inteva Products'): {'link': 6.0, 'width': 1.711769859409705},
 ('Tesla', 'Modine Manufacturing'): {'link': 7.0, 'width': 1.7927899625209969},
 ('Tesla', 'Sika'): {'link': 6.0, 'width': 1.711769859409705},
 ('Tesla', 'Stabilus'): {'link': 6.0, 'width': 1.711769859409705},
 ('Tesla', 'ZF Lenksysteme'): {'link': 6.0, 'width': 1.711769859409705},
 ('Tesla', 'Panasonic'): {'link': 32.0, 'width': 2.82842712474619},
 ('Volkswagen', 'General Motor'): {'link': 4544.0,
  'width': 12.509256473251348},
 ('Volkswagen', 'Hyundai'): {'link': 1814.0, 'width': 9.497103802223686},
 ('Volkswagen', 'Renault'): {'link': 1409.0, 'width': 8.803863450185993},
 ('Volkswagen', 'Tata'): {'link': 339.0, 'width': 5.741956651022271},
 ('Volkswagen', 'Subaru'): {'link': 25.0, 'width': 2.626527804403767},
 ('Volkswagen', 'Kia'): {'link': 1365.0, 'width': 8.720468053022428},
 ('Volkswagen', 'Suzuki'): {'link': 362.0, 'width': 5.856155109274522},
 ('Volkswagen', 'Audi'): {'link': 1598.0, 'width': 9.142669749061096},
 ('Volkswagen', 'Porsche'): {'link': 2112.0, 'width': 9.940498729938096},
 ('Volkswagen', 'Microsoft'): {'link': 316.0, 'width': 5.622197850610044},
 ('Volkswagen', 'Peugeot'): {'link': 1804.0, 'width': 9.481367056918364},
 ('Volkswagen', 'SAIC'): {'link': 195.0, 'width': 4.8641883518579165},
 ('Volkswagen', 'Geely'): {'link': 91.0, 'width': 3.8700129448363705},
 ('Volkswagen', 'Isuzu'): {'link': 98.0, 'width': 3.9570161493329823},
 ('Volkswagen', 'Yamaha Motor Corporation'): {'link': 29.0,
  'width': 2.7461192933624785},
 ('Hyundai', 'General Motor'): {'link': 1932.0, 'width': 9.678368119995476},
 ('Hyundai', 'FCA'): {'link': 754.0, 'width': 7.298126784789853},
 ('Hyundai', 'Renault'): {'link': 559.0, 'width': 6.671500798886764},
 ('Hyundai', 'Geely'): {'link': 12.0, 'width': 2.1074358993444706},
 ('Hyundai', 'Peugeot'): {'link': 584.0, 'width': 6.7596444657544845},
 ('Hyundai', 'Mazda'): {'link': 436.0, 'width': 6.1922138550463295},
 ('Hyundai', 'Suzuki'): {'link': 314.0, 'width': 5.611499058942004},
 ('Hyundai', 'Tata'): {'link': 311.0, 'width': 5.595361067573949},
 ('Hyundai', 'Audi'): {'link': 341.0, 'width': 5.752098490995028},
 ('Hyundai', 'SAIC'): {'link': 54.0, 'width': 3.309162757266209},
 ('Hyundai', 'Yamaha Motor Corporation'): {'link': 6.0,
  'width': 1.711769859409705},
 ('General Motor', 'Peugeot'): {'link': 2088.0, 'width': 9.90647500938525},
 ('General Motor', 'Suzuki'): {'link': 430.0, 'width': 6.1665255699532375},
 ('General Motor', 'Renault'): {'link': 1197.0, 'width': 8.383555526381897},
 ('General Motor', 'FCA'): {'link': 2895.0, 'width': 10.9268396628969},
 ('General Motor', 'SAIC'): {'link': 427.0, 'width': 6.153587247023441},
 ('General Motor', 'Tata'): {'link': 695.0, 'width': 7.121892948696807},
 ('General Motor', 'NGK Spark Plug'): {'link': 31.0,
  'width': 2.801615349437184},
 ('General Motor', 'Mold Masters'): {'link': 31.0, 'width': 2.801615349437184},
 ('General Motor', 'Bosch'): {'link': 31.0, 'width': 2.801615349437184},
 ('General Motor', 'Mitsubishi Electric'): {'link': 83.0,
  'width': 3.764639786125727},
 ('General Motor', 'Geely'): {'link': 180.0, 'width': 4.748776734338052},
 ('General Motor', 'Audi'): {'link': 963.0, 'width': 7.8539455514196845},
 ('Peugeot', 'FCA'): {'link': 1447.0, 'width': 8.874431864008676},
 ('Peugeot', 'Mitsubishi Motor'): {'link': 83.0, 'width': 3.764639786125727},
 ('Renault', 'Suzuki'): {'link': 182.0, 'width': 4.764544816607805},
 ('Renault', 'Tata'): {'link': 104.0, 'width': 4.028190508306193},
 ('SAIC', 'Mazda'): {'link': 41.0, 'width': 3.0467383348995827},
 ('SAIC', 'Geely'): {'link': 58.0, 'width': 3.380869426401905},
 ('Geely', 'Suzuki'): {'link': 3.0, 'width': 1.3903891703159093},
 ('Geely', 'Tata'): {'link': 48.0, 'width': 3.194275505495155},
 ('Geely', 'FCA'): {'link': 37.0, 'width': 2.954340289925338},
 ('Geely', 'Shell'): {'link': 0.5, 'width': 0.5},
 ('Geely', 'Audi'): {'link': 27.0, 'width': 2.6878753795222865},
 ('Audi', 'Tata'): {'link': 104.0, 'width': 4.028190508306193},
 ('Audi', 'Porsche'): {'link': 878.0, 'width': 7.639208345346838},
 ('Audi', 'Aston Martin'): {'link': 4.0, 'width': 1.515716566510398},
 ('Audi', 'Ferrari'): {'link': 4.0, 'width': 1.515716566510398},
 ('Audi', 'Alibaba'): {'link': 4.0, 'width': 1.515716566510398},
 ('Audi', 'Baidu'): {'link': 7.0, 'width': 1.7927899625209969},
 ('Audi', 'Tencent'): {'link': 4.0, 'width': 1.515716566510398},
 ('Toyota Industries', 'Kion Group'): {'link': 0.5, 'width': 0.5},
 ('Toyota Industries', 'Whiting'): {'link': 0.5, 'width': 0.5},
 ('Toyota Industries', 'Godrej Consumer Products'): {'link': 0.5,
  'width': 0.5},
 ('Toyota Industries', 'Unilever'): {'link': 0.5, 'width': 0.5},
 ('Toyota Industries', 'P&G'): {'link': 8.0, 'width': 1.8660659830736148},
 ('Toyota Industries', 'Sisscohoist'): {'link': 0.5, 'width': 0.5},
 ('Toyota Industries', 'Engliftsystems'): {'link': 0.5, 'width': 0.5},
 ('Toyota Industries', "L'Oreal"): {'link': 0.5, 'width': 0.5},
 ('Toyota Industries', 'S.C. Johnson'): {'link': 0.5, 'width': 0.5},
 ('Toyota Industries', 'DENSO'): {'link': 8.0, 'width': 1.8660659830736148},
 ('Toyota Industries', 'Mazda'): {'link': 4.0, 'width': 1.515716566510398},
 ('JTEKT', 'Hoover Precision Products'): {'link': 0.5, 'width': 0.5},
 ('JTEKT', 'NSK'): {'link': 29.0, 'width': 2.7461192933624785},
 ('JTEKT', 'TimKen'): {'link': 12.0, 'width': 2.1074358993444706},
 ('JTEKT', 'SKF'): {'link': 0.5, 'width': 0.5},
 ('JTEKT', 'Nbc Bearings'): {'link': 0.5, 'width': 0.5},
 ('JTEKT', 'Schaeffler'): {'link': 1.0, 'width': 1.0},
 ('JTEKT', 'Minebea'): {'link': 12.0, 'width': 2.1074358993444706},
 ('JTEKT', 'NTN'): {'link': 0.5, 'width': 0.5},
 ('Toyota Tsusho', 'Mitsubishi Corp'): {'link': 74.0,
  'width': 3.63721954306138},
 ('Toyota Tsusho', 'ITOCHU'): {'link': 12.0, 'width': 2.1074358993444706},
 ('Toyota Tsusho', 'Marubeni'): {'link': 14.0, 'width': 2.2071833466585677},
 ('Toyota Tsusho', 'Sumitomo'): {'link': 5.0, 'width': 1.6206565966927624},
 ('Toyota Tsusho', 'CFAO'): {'link': 0.5, 'width': 0.5},
 ('Aisin Seiki', 'Valeo'): {'link': 19.0, 'width': 2.4189454814875875},
 ('Aisin Seiki', 'Delphi'): {'link': 8.0, 'width': 1.8660659830736148},
 ('Aisin Seiki', 'Bosch'): {'link': 0.5, 'width': 0.5},
 ('Aisin Seiki', 'GETRAG'): {'link': 0.5, 'width': 0.5},
 ('Aisin Seiki', 'Calsonic kansei'): {'link': 0.5, 'width': 0.5},
 ('Aisin Seiki', 'Keihin'): {'link': 0.5, 'width': 0.5},
 ('Aisin Seiki', 'DENSO'): {'link': 34.0, 'width': 2.8803394661274377},
 ('Aisin Seiki', 'Nathan'): {'link': 0.5, 'width': 0.5},
 ('Aisin Seiki', 'Johnson Controls'): {'link': 13.0,
  'width': 2.1586538444215795},
 ('Toyoda Gosei', 'Delphi'): {'link': 1.0, 'width': 1.0},
 ('Toyoda Gosei', 'Valeo'): {'link': 0.5, 'width': 0.5},
 ('Toyoda Gosei', 'Magneti Marelli'): {'link': 0.5, 'width': 0.5},
 ('Toyoda Gosei', 'Johnson Controls'): {'link': 0.5, 'width': 0.5},
 ('Toyoda Gosei', 'Bosch'): {'link': 0.5, 'width': 0.5},
 ('Toyoda Gosei', 'ZF TRW'): {'link': 0.5, 'width': 0.5},
 ('Toyoda Gosei', 'Honeywell'): {'link': 5.0, 'width': 1.6206565966927624},
 ('Toyoda Gosei', 'Takata'): {'link': 0.5, 'width': 0.5},
 ('Toyoda Gosei', 'Lear'): {'link': 6.0, 'width': 1.711769859409705},
 ('DENSO', 'Delphi'): {'link': 123.0, 'width': 4.236151985630706},
 ('DENSO', 'Valeo'): {'link': 89.0, 'width': 3.844297613276208},
 ('DENSO', 'Honeywell'): {'link': 50.0, 'width': 3.233635032886787},
 ('DENSO', 'Johnson Controls'): {'link': 48.0, 'width': 3.194275505495155},
 ('DENSO', 'Bosch'): {'link': 0.5, 'width': 0.5},
 ('DENSO', 'Makita'): {'link': 0.5, 'width': 0.5},
 ('DENSO', 'United Technologies'): {'link': 0.5, 'width': 0.5},
 ('DENSO', 'Harman Embedded Audio'): {'link': 0.5, 'width': 0.5},
 ('DENSO', 'ZF TRW'): {'link': 0.5, 'width': 0.5},
 ('DENSO', 'Siemens'): {'link': 37.0, 'width': 2.954340289925338},
 ('Toyota Boshoku', 'Siemens'): {'link': 19.0, 'width': 2.4189454814875875},
 ('Toyota Boshoku', 'Honeywell'): {'link': 5.0, 'width': 1.6206565966927624},
 ('Toyota Boshoku', 'Johnson Controls'): {'link': 5.0,
  'width': 1.6206565966927624},
 ('Toyota Boshoku', 'Magna'): {'link': 0.5, 'width': 0.5},
 ('Toyota Boshoku', 'Faurecia'): {'link': 5.0, 'width': 1.6206565966927624},
 ('Toyota Boshoku', 'Adient'): {'link': 0.5, 'width': 0.5},
 ('Toyota Boshoku', 'Grupo Antolin'): {'link': 0.5, 'width': 0.5},
 ('Toyota Boshoku', 'Benteler'): {'link': 0.5, 'width': 0.5},
 ('Toyota Boshoku', 'SRG Global'): {'link': 0.5, 'width': 0.5},
 ('Toyota Boshoku', 'Lear'): {'link': 11.0, 'width': 2.053136413658844},
 ('Isuzu', 'Paccar'): {'link': 40.0, 'width': 3.0242521453322184},
 ('Isuzu', 'Navistar'): {'link': 48.0, 'width': 3.194275505495155},
 ('Isuzu', 'Oshkosh'): {'link': 7.0, 'width': 1.7927899625209969},
 ('Isuzu', 'Scania'): {'link': 3.0, 'width': 1.3903891703159093},
 ('Isuzu', 'Cummins'): {'link': 27.0, 'width': 2.6878753795222865},
 ('Yamaha Motor Corporation', 'Hero Motor'): {'link': 28.0,
  'width': 2.7173614464666307},
 ('Yamaha Motor Corporation', 'Suzuki'): {'link': 52.0,
  'width': 3.271907393351148},
 ('Yamaha Motor Corporation', 'Bajaj Auto'): {'link': 7.0,
  'width': 1.7927899625209969},
 ('Yamaha Motor Corporation', 'TVS'): {'link': 5.0,
  'width': 1.6206565966927624},
 ('Yamaha Motor Corporation', 'NVIDIA'): {'link': 6.0,
  'width': 1.711769859409705},
 ('Panasonic', 'Sony'): {'link': 4718.0, 'width': 12.651073560183999},
 ('Panasonic', 'OSRAM'): {'link': 3.0, 'width': 1.3903891703159093},
 ('Panasonic', 'Nikon'): {'link': 432.0, 'width': 6.175116053788563},
 ('Panasonic', 'HTC'): {'link': 360.0, 'width': 5.8464299467026075},
 ('Panasonic', 'BenQ'): {'link': 4.0, 'width': 1.515716566510398},
 ('Panasonic', 'Philips'): {'link': 446.0, 'width': 6.234483180286312},
 ('Panasonic', 'Samsung'): {'link': 3959.0, 'width': 12.002608775656242},
 ('Panasonic', 'Microsoft'): {'link': 953.0, 'width': 7.829388979204495},
 ('Panasonic', 'HUAWEI'): {'link': 3.0, 'width': 1.3903891703159093},
 ('Panasonic', 'Dell'): {'link': 3.0, 'width': 1.3903891703159093},
 ('Suzuki', 'FCA'): {'link': 289.0, 'width': 5.473553316918489},
 ('Suzuki', 'Mitsubishi Motor'): {'link': 76.0, 'width': 3.666435739776208},
 ('Suzuki', 'Tata'): {'link': 189.0, 'width': 4.818796000914871}}
nx.set_edge_attributes(G, edge_attr)

nx_renderer = from_networkx(G, nx.kamada_kawai_layout)

# Convert: NetworkX node attributes -> ColumnDataSource
node_dict = {}
node_dict['index'] = list(G.nodes())

node_attr_keys = [attr_key for node in list(G.nodes(data=True)) for attr_key in node[1].keys() ]
node_attr_keys = list(set(node_attr_keys))

for attr_key in node_attr_keys:
    node_dict[attr_key] = [node_attr[attr_key] if attr_key in node_attr.keys() else None
                           for node_key, node_attr in list(G.nodes(data=True))]
node_source = ColumnDataSource(node_dict)

# Set node attribute to Bokeh DataSource
nx_renderer.node_renderer.data_source = node_source
nx_renderer.node_renderer.view = CDSView(source=node_source)

# Convert: NetworkX edge attributes -> ColumnDataSource
edge_dict = {}
edge_dict['start'] = [x[0] for x in G.edges(data=True)]
edge_dict['end'] = [x[1] for x in G.edges(data=True)]

edge_attr_keys = [attr_key for edge in list(G.edges(data=True)) for attr_key in edge[2].keys() ]
edge_attr_keys = list(set(edge_attr_keys))

for attr_key in edge_attr_keys:
    edge_dict[attr_key] = [edge_attr[attr_key] if attr_key in edge_attr.keys() else None
                           for _, _, edge_attr in list(G.edges(data=True))]
edge_source = ColumnDataSource(edge_dict)

# Set edge attribute to Bokeh DataSource
nx_renderer.edge_renderer.data_source = edge_source
nx_renderer.edge_renderer.view = CDSView(source=edge_source)

# generate graphs
nx = Plot(plot_width=1400, plot_height=800,
            x_range=Range1d(-1.2,1.2), y_range=Range1d(-1.2,1.2))
nx.title.text = "Competitive and Collaborative Network for Toyota"
nx.add_tools(TapTool(),BoxZoomTool(), ResetTool())
nx_renderer.node_renderer.glyph = Circle(size='size', fill_color=Blues4[2], line_color = Blues4[2], line_width = 0.5)

nx_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Blues4[0], line_color = Blues4[0])
nx_renderer.node_renderer.hover_glyph = Circle(size=10, fill_color=Blues4[0])

nx_renderer.edge_renderer.glyph = MultiLine(line_color="color", line_alpha=0.3, line_width='width')


nx_tooltips = """
<div>
    <div>
    <span style="font-size: 10px">Competitors:@competitors</span>
    </div>
    <div>
    <span style="font-size: 10px">Collaborators: @collaborators</span>
    </div>
    <div>
    <span style="font-size: 10px">Market Capitalization (Bililion$): @marketcap</span>
    </div>
</div>
"""
node_hover = HoverTool(tooltips=nx_tooltips)
nx.add_tools(node_hover)

x, y = zip(*nx_renderer.layout_provider.graph_layout.values())
label_source = ColumnDataSource({'x': x, 'y': y, 'company_name': [n for n in list(G.nodes())]})
labels = LabelSet(x='x', y='y', text = 'company_name', source=label_source, text_font_size="7pt",text_font_style='bold')


nx.renderers.append(nx_renderer)
nx.renderers.append(labels)

link_raw = pd.read_csv('TotalNX_link.csv')
data_table_nxlink = {'Target': np.array(link_raw[link_raw.Start =='Toyota']['Start']),
                'Neighbour': np.array(link_raw[link_raw.Start =='Toyota']['Stop']),
                'Relationship': np.array(link_raw[link_raw.Start == 'Toyota']['Level']),
                'Relevance': np.array(link_raw[link_raw.Start =='Toyota']['Link'])}
cds_table_nxlink = ColumnDataSource(data_table_nxlink)

columns_table_nxlink = [
    TableColumn(field='Target', title='Target'),
    TableColumn(field='Neighbour', title='Neighbour'),
    TableColumn(field = 'Relationship', title = 'Relationship'),
    TableColumn(field='Relevance', title='Relevance')
    ]
table_nxlink = DataTable(source=cds_table_nxlink, columns=columns_table_nxlink, width=1200, height=280)

title_table_nxlink = Div(text = '''<b>Relevance between target company and its competitors/collaborators</b>''')
note_table_nxlink =  Div(text='''
<b>Notes:</b>
<p>
The relevance is measured by the number of times that the two companies (the target company and its competitors/collaborators) are reported in the same news item.
Two companies are suggested to be more relevant when they are frequently reported in the same news.
</p>

''', width=1400)

taptool = nx.select(type=TapTool)

def update_linkage():
    selected_index = nx_renderer.node_renderer.data_source.selected.indices
    try:
        selected = list(G.nodes())[selected_index[0]]
    except:
        selected = 'Toyota'

    if link_raw[link_raw.Start ==selected].shape[0] != 0:
        cds_table_nxlink.data = {'Target': np.array(link_raw[link_raw.Start ==selected]['Start']),
                                 'Neighbour': np.array(link_raw[link_raw.Start ==selected]['Stop']),
                                 'Relationship':np.array(link_raw[link_raw.Start ==selected]['Level']),
                                 'Relevance': np.array(link_raw[link_raw.Start ==selected]['Link'])}
    else:
        cds_table_nxlink.data = {'Target': np.array(link_raw[link_raw.Stop ==selected]['Stop']),
                                 'Neighbour': np.array(link_raw[link_raw.Stop ==selected]['Start']),
                                 'Relationship':np.array(link_raw[link_raw.Stop ==selected]['Level']),
                                 'Relevance': np.array(link_raw[link_raw.Stop ==selected]['Link'])}

nx.on_event(Tap, update_linkage)


note_nx =  Div(text='''
<b>Notes:</b>
<p>
The GRI data for <b>Toyota, BMW, Daimler, Ford, General Motor, Tesla</b> has been pre-loaded for test.
Simply tap on the circle (the selected circle will turn dark blue), and the corresponding GRIs can be accessed in the GRI generator below.
GRIs for other companies are currently un-avaiable.
</p>

''', width=1400)

pre_nx = Div(text=
               '''
               <h2> Network Graph for Toyota </h2>
               <p>
               The figure below presents a two-tier competitor-and-collaborator network for Toyota.
               Competitors are connected with orange lines and collaborators with blue lines.
               </p>

               ''',
               width=1400)

layout_nx= column(pre_nx, nx, note_nx, title_table_nxlink, table_nxlink, note_table_nxlink)


#################################################################################
#################################################################################
df_mcgg = pd.read_csv('Toyota.csv')
df_mcgg['Date'] = pd.to_datetime(df_mcgg['Date']).apply(dt.datetime.date)
cds_mcgg = ColumnDataSource(df_mcgg)

taptool = nx.select(type=TapTool)

def update_cds_mcgg():
    if index_radiogroup_mcgg.active == 5:
        selected_index = nx_renderer.node_renderer.data_source.selected.indices
        try:
            selected = list(G.nodes())[selected_index[0]]
        except:
            selected = 'Toyota'
        if datasource_radiogroup_mcgg.active == 0:
            url = '{}.csv'.format(selected)
        elif datasource_radiogroup_mcgg.active == 1:
            url = '{}_unscaled.csv'.format(selected)

        df_mcgg = pd.read_csv(url)
        df_mcgg['Date'] = df_mcgg['Date'].astype('str')
        cds_mcgg.data = {col: np.array(df_mcgg[col]) for col in df_mcgg.columns}
        dd = [dt.datetime.strptime(d, '%Y-%m-%d') for d in cds_mcgg.data['Date']]
        cds_mcgg.data['Date'] = np.array([dt.datetime.date(d) for d in dd])

    else:
        selected = index_radiogroup_mcgg.labels[index_radiogroup_mcgg.active]
        if datasource_radiogroup_mcgg.active == 0:
            url = '{}.csv'.format(selected)
        elif datasource_radiogroup_mcgg.active == 1:
            url = '{}_unscaled.csv'.format(selected)
        df_mcgg = pd.read_csv(url)
        df_mcgg['Date'] = df_mcgg['Date'].astype('str')
        cds_mcgg.data = {col: np.array(df_mcgg[col]) for col in df_mcgg.columns}
        dd = [dt.datetime.strptime(d, '%Y-%m-%d') for d in cds_mcgg.data['Date']]
        cds_mcgg.data['Date'] = np.array([dt.datetime.date(d) for d in dd])

def create_figure_mcgg(cds_main_mcgg,cds_label_optim,cds_label_pessi):

    kw = {}

    kw['y_range'] = Range1d(start=min(cds_main_mcgg.data["y2"])-0.5, end=max(cds_main_mcgg.data["y1"])+0.5)
    kw['x_axis_type'] = 'datetime'
    mcgg = figure(**kw)

    mcgg.add_tools(hover)
    mcgg.toolbar.logo = None

    # style backgound
    mcgg.height = 600
    mcgg.width = 1400

    # style Axes
    mcgg.xaxis.axis_label = 'Date'
    mcgg.yaxis.axis_label = 'GRI'

    # style title
    mcgg.title.text = "News Sentiment Index"
    mcgg.title.text_font_size = "15px"
    mcgg.title.align = "center"

    # add span
    span_zero_mcgg = Span(location=0, dimension='width', line_color='black', line_width=2)
    mcgg.add_layout(span_zero_mcgg)

    ###create second layer: dynamic figure
    # create line plot
    mcgg.varea(x="date", y1='Bottom', y2="y1",
               fill_color='red', fill_alpha=0.1,
               legend='optimistic index',
               source=cds_main_mcgg)
    mcgg.varea(x="date", y1='Bottom', y2="y2",
               fill_color='green', fill_alpha=0.1,
               legend='pessimistic index',
               source=cds_main_mcgg)

    mcgg.line(x="date", y="y1",
              line_color='red', line_alpha=0.8,
              legend='optimistic index',
              source=cds_main_mcgg)
    mcgg.line(x="date", y="y2",
              line_color='green', line_alpha=0.8,
              legend='pessimistic index',
              source=cds_main_mcgg)


    mcgg.circle(x="date", y="y1", size=6, color='red',
                source=cds_label_optim)

    mcgg.circle(x="date", y="y2", size=6, color='green',
                source=cds_label_pessi)

    labels_optim = LabelSet(x='date', y="y1", text='label_optim', source=cds_label_optim,
                            render_mode='css',
                            text_font_size='10px',
                            border_line_color='black', border_line_alpha=0.8,
                            background_fill_color='white', background_fill_alpha=0.7)
    labels_pessi = LabelSet(x='date', y="y2", text='label_pessi', source=cds_label_pessi,
                            render_mode='css',
                            text_font_size='10px',
                            border_line_color='black', border_line_alpha=0.8,
                            background_fill_color='white', background_fill_alpha=0.7)

    mcgg.legend.location = "top_right"
    mcgg.legend.click_policy="hide"

    mcgg.add_layout(labels_optim)
    mcgg.add_layout(labels_pessi)

    return mcgg


###create first layer
hover = HoverTool(tooltips=[("Date", "@date{%F}"),
                            ("Optimistic index", "@y1"),
                            ("Pessimistic index", "@y2")],
                  formatters={"date": "datetime"})

title_index_radiogroup_mcgg = Div(text = 'Select Market Index or Company Levels',width = 300)
index_radiogroup_mcgg = RadioGroup(
        labels=['FTSE 100',
                'Dow Jones Industrial Average',
                'NASDAQ 100',
                'S&P 500',
                'Nikkei 225',
                'None'],
                width=300,
                height=110)

multi_select_level_mcgg = MultiSelect(value=["tar_"],
                                      options=[("tar_", "Target Company"),
                                               ("com_", "Competitors"),
                                               ("col_", "Collaborators"),
                                               ("none", "None")],
                                      width=300,
                                      height=70)

multi_select_region_mcgg = MultiSelect(title="Select region",
                                       value=["NAM_"],
                                       options=[("NAM_", "North America"),
                                                ("EU_", "Europe"),
                                                ("EA_", "East Asia"),
                                                ("JP_", "Japan"),
                                                ("ME_", "Middle East")],
                                       width=300,
                                       height=215)

multi_select_risk_mcgg = MultiSelect(title="Select risk factor",
                                     value=['econ'],
                                     options=[("econ", "Economic"),
                                              ("pol", "Political"),
                                              ("dis", "Natural disasters and accidents"),
                                              ("cyb", "Cyber Risk")],
                                     width=300,
                                     height=215)
title_datasource_radiogroup_mcgg = Div(text = 'Select Data Source', width = 300)
datasource_radiogroup_mcgg = RadioGroup(
        labels=['Scaled',
                'Unscalde'],
        active=0)

slider_num_label_mcgg = Slider(title="Number of major events to show for each GRI", value=5, start=1, end=30, step=1, width = 300)

button_mcgg = Button(label='Generator sentiment indicators', width=1400)

cds_main_mcgg = ColumnDataSource(data={"date": cds_mcgg.data['Date'],
                                     "y1": cds_mcgg.data["tar_NAM_econ"],
                                     "y2": cds_mcgg.data["tar_NAM_econ_pessi"],
                                     "Bottom": cds_mcgg.data["Bottom"]})

df_label_begin_optim = pd.read_csv('tyt_NAM_econ_label.csv')
df_label_begin_optim["Date"] = pd.to_datetime(df_label_begin_optim["Date"]).apply(dt.datetime.date)
df_label_begin_pessi = pd.read_csv('tyt_NAM_econ_pessi_label.csv')
df_label_begin_pessi["Date"] = pd.to_datetime(df_label_begin_pessi["Date"]).apply(dt.datetime.date)

cds_label_optim = ColumnDataSource(data={"date":df_label_begin_optim["Date"],
                                    "y1":df_label_begin_optim["tar_NAM_econ"],
                                    "y2":df_label_begin_optim["tar_NAM_econ_pessi"],
                                    "label_optim":df_label_begin_optim["tar_NAM_econ_label"]})

cds_label_pessi = ColumnDataSource(data={"date":df_label_begin_pessi["Date"],
                                    "y1":df_label_begin_pessi["tar_NAM_econ"],
                                    "y2":df_label_begin_pessi["tar_NAM_econ_pessi"],
                                    "label_pessi":df_label_begin_pessi["tar_NAM_econ_label"]})

def update_mcgg():

    if index_radiogroup_mcgg.active == 5:
        num_label = slider_num_label_mcgg.value

        cds_main_mcgg.data["y1"] = cds_main_mcgg.data['Bottom']
        cds_main_mcgg.data["y2"] = cds_main_mcgg.data['Bottom']

        optim_label_data = {'date':[],'label_optim':[]}
        pessi_label_data = {'date':[],'label_pessi':[]}

        for level in multi_select_level_mcgg.value:
            for region in multi_select_region_mcgg.value:
                for risk in multi_select_risk_mcgg.value:

                    key_optim = level+region+risk
                    key_pessi = key_optim+'_pessi'
                    key_label = key_optim+'_label'

                    cds_main_mcgg.data["y1"] = cds_main_mcgg.data["y1"]+cds_mcgg.data[key_optim]
                    cds_main_mcgg.data["y2"] = cds_main_mcgg.data["y2"]+cds_mcgg.data[key_pessi]

                    optim_label_data['date'] = optim_label_data['date']+[cds_mcgg.data['Date'][i] for i in np.argsort(cds_mcgg.data[key_optim])[num_label*(-1):]]
                    optim_label_data['label_optim'] = optim_label_data['label_optim']+[cds_mcgg.data[key_label][i] for i in np.argsort(cds_mcgg.data[key_optim])[num_label*(-1):]]

                    pessi_label_data['date'] = pessi_label_data['date']+[cds_mcgg.data['Date'][i] for i in np.argsort(cds_mcgg.data[key_pessi])[:num_label]]
                    pessi_label_data['label_pessi'] = pessi_label_data['label_pessi']+[cds_mcgg.data[key_label][i] for i in np.argsort(cds_mcgg.data[key_pessi])[:num_label]]


        cds_label_optim.data = {'date':np.array(optim_label_data['date']),
                                'y1':[cds_main_mcgg.data["y1"][i] for i in [np.where(cds_main_mcgg.data['date']==item)[0][0] for item in optim_label_data['date']]],
                                'y2':[cds_main_mcgg.data["y2"][i] for i in [np.where(cds_main_mcgg.data['date']==item)[0][0] for item in optim_label_data['date']]],
                                'label_optim': np.array(optim_label_data["label_optim"])}

        cds_label_pessi.data = {'date':np.array(pessi_label_data['date']),
                                'y1':[cds_main_mcgg.data["y1"][i] for i in [np.where(cds_main_mcgg.data['date']==item)[0][0] for item in pessi_label_data['date']]],
                                'y2':[cds_main_mcgg.data["y2"][i] for i in [np.where(cds_main_mcgg.data['date']==item)[0][0] for item in pessi_label_data['date']]],
                                'label_pessi':np.array(pessi_label_data['label_pessi'])}



        layout_mcgg.children[1] = create_figure_mcgg(cds_main_mcgg=cds_main_mcgg,
                                                     cds_label_optim=cds_label_optim,
                                                     cds_label_pessi=cds_label_pessi)

    else:
        num_label = slider_num_label_mcgg.value

        cds_main_mcgg.data["y1"] = cds_main_mcgg.data['Bottom']
        cds_main_mcgg.data["y2"] = cds_main_mcgg.data['Bottom']

        optim_label_data = {'date':[],'label_optim':[]}
        pessi_label_data = {'date':[],'label_pessi':[]}

        for region in multi_select_region_mcgg.value:
            for risk in multi_select_risk_mcgg.value:

                key_optim = 'idx_'+region+risk
                key_pessi = key_optim+'_pessi'
                key_label = key_optim+'_label'

                cds_main_mcgg.data["y1"] = cds_main_mcgg.data["y1"]+cds_mcgg.data[key_optim]
                cds_main_mcgg.data["y2"] = cds_main_mcgg.data["y2"]+cds_mcgg.data[key_pessi]

                optim_label_data['date'] = optim_label_data['date']+[cds_mcgg.data['Date'][i] for i in np.argsort(cds_mcgg.data[key_optim])[num_label*(-1):]]
                optim_label_data['label_optim'] = optim_label_data['label_optim']+[cds_mcgg.data[key_label][i] for i in np.argsort(cds_mcgg.data[key_optim])[num_label*(-1):]]

                pessi_label_data['date'] = pessi_label_data['date']+[cds_mcgg.data['Date'][i] for i in np.argsort(cds_mcgg.data[key_pessi])[:num_label]]
                pessi_label_data['label_pessi'] = pessi_label_data['label_pessi']+[cds_mcgg.data[key_label][i] for i in np.argsort(cds_mcgg.data[key_pessi])[:num_label]]


        cds_label_optim.data = {'date':np.array(optim_label_data['date']),
                                'y1':[cds_main_mcgg.data["y1"][i] for i in [np.where(cds_main_mcgg.data['date']==item)[0][0] for item in optim_label_data['date']]],
                                'y2':[cds_main_mcgg.data["y2"][i] for i in [np.where(cds_main_mcgg.data['date']==item)[0][0] for item in optim_label_data['date']]],
                                'label_optim': np.array(optim_label_data["label_optim"])}

        cds_label_pessi.data = {'date':np.array(pessi_label_data['date']),
                                'y1':[cds_main_mcgg.data["y1"][i] for i in [np.where(cds_main_mcgg.data['date']==item)[0][0] for item in pessi_label_data['date']]],
                                'y2':[cds_main_mcgg.data["y2"][i] for i in [np.where(cds_main_mcgg.data['date']==item)[0][0] for item in pessi_label_data['date']]],
                                'label_pessi':np.array(pessi_label_data['label_pessi'])}


        layout_mcgg.children[1] = create_figure_mcgg(cds_main_mcgg=cds_main_mcgg,
                                                     cds_label_optim=cds_label_optim,
                                                     cds_label_pessi=cds_label_pessi)


button_mcgg.on_click(update_cds_mcgg)
button_mcgg.on_click(update_mcgg)


pre_mcgg = Div(text=
               '''
               <h2> GRIs Generator </h2>
               <p>
               In the figure below, you can generate the optimistic and pessimistic GRIs of various levels for the company you selected in the network.
               Alternatively, you can select one of the market indexes and generate the corresponding GRIs.
               </p>
               <p>
               Multi-select is enabled (i.e. more than one level/region/risk factors can be selected). When multiple GRIs are selected, the GRI generator will show the sum of all GRIs.
               </p>
               <p>
               GRIs can be presented in a scaled format where GRIs are scaled to the interval of [-1,1]; or in its original format, which is the aggregated news sentiment scores.
               N.B.For both format, multi-select is allowed, but the sum of scaled GRIs can be difficult to intepret.
               </p>
               <p>
               The slider is used for controlling the number of major events to show for each GRI.
               </p>
               You can also click on the legend to mute the corresponding GRI.
               </p>

               ''',
               width=1400)





pre_all = Div(text='''
<p>
<h1>Construct Geolocation Risk-factor Indicators with News Sentiment</h1>
</p>
<p>
<b>
In this page, a method to construct geo-risk factor indicators (GRIs) by using publicly available information – news is presented. GRIs can capture various risk types in different regions faced by individual companies comprehensively. GRIs can be employed by companies to measure their own risk exposures and to support the business operational and strategical decision-making, or be adopted by other stakeholders to capture the risks faced by the company and make predictions about the company’s performance in the market and communities.
</p>
<p>
Toyota Motor Corporation is chosen as an example to demonstrate the implication of GRIs, since the business operation of this company is spread globally, the need for developing an integrated risk measurement system can be urgent.
<p>
You will first see a brief summary about the news data used to construct GRIs, then a competitor-and-collaborator network for Toyota, you can then select the company from the network graph and see corresponding GRIs in the generator at the end of this page.
</p>
</b>
</p>''', width=1400)



control_mcgg = [column(title_index_radiogroup_mcgg,index_radiogroup_mcgg, multi_select_level_mcgg),
                multi_select_region_mcgg,
                multi_select_risk_mcgg,
                column([slider_num_label_mcgg, title_datasource_radiogroup_mcgg, datasource_radiogroup_mcgg])]


layout_mcgg = column(
    [pre_mcgg,
     create_figure_mcgg(cds_main_mcgg=cds_main_mcgg,
                        cds_label_optim=cds_label_optim,
                        cds_label_pessi=cds_label_pessi),
     row(control_mcgg),
     button_mcgg])

layout_all = column([pre_all,layout_trna,layout_nx,layout_mcgg])
curdoc().add_root(layout_all)
