# import pacakges
import networkx as nx

import pandas as pd
import numpy as np
import datetime as dt
from scipy.stats import spearmanr

from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool, ResetTool, BoxZoomTool, LabelSet, CDSView, ColumnDataSource, PanTool, Legend
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Blues4
from bokeh.plotting import figure
from bokeh.models.widgets import Select, Button, Div, MultiSelect, DataTable, TableColumn, TextInput
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
    kw = dict()
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
width = 1200, height = 120)


control_trna=row([multi_select_scope,multi_select_indicator])
layout_trna = column([pre_trna,control_trna,button,create_figure_trna()])

#################################################################################
#################################################################################

df = pd.read_csv('CC_Network_Toyota.csv')

dict_edgess = {}
dict_edgess['start'] = []
dict_edgess['stop'] = []
dict_edgess['level'] = []
dict_edgess['color'] = []
for key,label in df.iterrows():
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
node_attr = dict()
for u in list(G.nodes()):
    com_str=''
    col_str=''
    for v in list(G.neighbors(u)):
        if G.edges[u, v]['level'] == 'com':
            if com_str=='':
                com_str=v
            else:
                com_str=com_str+', '+v
        else:
            if col_str=='':
                col_str=v
            else:
                col_str=col_str+', '+v
    node_attr[u] = {'competitors':com_str, 'collaborators': col_str}
nx.set_node_attributes(G,node_attr)

nx_renderer = from_networkx(G, nx.kamada_kawai_layout)

# Convert: NetworkX node attributes -> ColumnDataSource
node_dict = dict()
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
edge_dict = dict()
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
nx = Plot(plot_width=1200, plot_height=800,
            x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))
nx.title.text = "Competitive and Collaborative Network for Toyota"
nx.add_tools(TapTool(),BoxZoomTool(), ResetTool())
nx_renderer.node_renderer.glyph = Circle(size=15, fill_color=Blues4[2], line_color = Blues4[2], line_width = 0.5)
nx_renderer.node_renderer.selection_glyph = Circle(size=10, fill_color=Blues4[0], line_color = Blues4[0])
nx_renderer.node_renderer.hover_glyph = Circle(size=10, fill_color=Blues4[0])

nx_renderer.edge_renderer.glyph = MultiLine(line_color="color", line_alpha=0.3, line_width=1)


TOOLTIPS = """
<div>
    <div>
    <span style="font-size: 10px">Competitors:@competitors</span>
    </div>
    <div>
    <span style="font-size: 10px">Collaborators: @collaborators</span>
    </div>
</div>
"""
node_hover = HoverTool(tooltips=TOOLTIPS)
nx.add_tools(node_hover)

x, y = zip(*nx_renderer.layout_provider.graph_layout.values())
label_source = ColumnDataSource({'x': x, 'y': y, 'company_name': [n for n in list(G.nodes())]})
labels = LabelSet(x='x', y='y', text = 'company_name', source=label_source, text_font_size="7pt",text_font_style='bold')


nx.renderers.append(nx_renderer)
nx.renderers.append(labels)



note_nx =  Div(text='''
<b>Notes:</b>

<p>
The GFI data for <b>Toyota, BMW, Daimler, Ford, General Motor, Tesla</b> has been pre-loaded for test.
Simply tap on the circle (the selected circle will turn dark blue), and the corresponding GFIs can be accessed in the GFI generator below.
GFIs for other companies are currently un-avaiable.
</p>

''', width=1200)

pre_nx = Div(text=
               '''
               <h2> Network Graph for Toyota </h2>
               <p>
               The figure below presents a two-tier competitor-and-collaborator network for Toyota.
               Competitors are connected with orange lines and collaborators with blue lines.
               </p>

               ''',
               width=1200)

layout_nx= column(pre_nx, nx, note_nx)




#################################################################################
#################################################################################


df_mcgg = pd.read_csv('Toyota.csv')
df_mcgg['Date'] = pd.to_datetime(df_mcgg['Date']).apply(dt.datetime.date)
cds_mcgg = ColumnDataSource(df_mcgg)

taptool = nx.select(type=TapTool)

def update_cds_mcgg():
    selected_index = nx_renderer.node_renderer.data_source.selected.indices
    selected = list(G.nodes())[selected_index[0]]
    url = '{}.csv'.format(selected)
    df_mcgg = pd.read_csv(url)
    df_mcgg['Date'] = df_mcgg['Date'].astype('str')
    cds_mcgg.data = {col: np.array(df_mcgg[col]) for col in df_mcgg.columns}
    dd = [dt.datetime.strptime(d, '%Y-%m-%d') for d in cds_mcgg.data['Date']]
    cds_mcgg.data['Date'] = np.array([dt.datetime.date(d) for d in dd])

nx.on_event(Tap, update_cds_mcgg)

def create_figure_mcgg(source_mcgg,cds_label_optim,cds_label_pessi):


    kw = dict()

    kw['y_range'] = Range1d(start=min(source_mcgg.data["y2"])-0.5, end=max(source_mcgg.data["y1"])+0.5)
    kw['x_axis_type'] = 'datetime'
    mcgg = figure(**kw)

    mcgg.add_tools(hover)
    mcgg.toolbar.logo = None

    # style backgound
    mcgg.height = 600
    mcgg.width = 1200

    # style Axes
    mcgg.xaxis.axis_label = 'Date'
    mcgg.yaxis.axis_label = 'GFI'

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
               source=source_mcgg)
    mcgg.varea(x="date", y1='Bottom', y2="y2",
               fill_color='green', fill_alpha=0.1,
               legend='pessimistic index',
               source=source_mcgg)

    mcgg.line(x="date", y="y1",
              line_color='red', line_alpha=0.8,
              legend='optimistic index',
              source=source_mcgg)
    mcgg.line(x="date", y="y2",
              line_color='green', line_alpha=0.8,
              legend='pessimistic index',
              source=source_mcgg)



    mcgg.circle(x="date", y="y1", size=6, color='red',
                source=cds_label_optim)

    mcgg.circle(x="date", y="y2", size=6, color='green',
                source=cds_label_pessi)

    labels_optim = LabelSet(x='date', y="y1", text='label', source=cds_label_optim,
                            render_mode='css',
                            text_font_size='10px',
                            border_line_color='black', border_line_alpha=0.8,
                            background_fill_color='white', background_fill_alpha=0.7)
    labels_pessi = LabelSet(x='date', y="y2", text='label', source=cds_label_pessi,
                            render_mode='css',
                            text_font_size='10px',
                            border_line_color='black', border_line_alpha=0.8,
                            background_fill_color='white', background_fill_alpha=0.7)

    mcgg.legend.location = "top_right"
    mcgg.legend.click_policy="mute"

    mcgg.add_layout(labels_optim)
    mcgg.add_layout(labels_pessi)

    return mcgg


###create first layer
hover = HoverTool(tooltips=[("Date", "@date{%F}"),
                            ("Optimistic index", "@y1"),
                            ("Pessimistic index", "@y2")],
                  formatters={"date": "datetime"})


multi_select_level_mcgg = MultiSelect(title="Select level",
                                      value=["tar_"],
                                      options=[("tar_", "Target Company"),
                                               ("com_", "Competitors"),
                                               ("col_", "Collaborators"),
                                               ("all_", "All Levels")],
                                      width=290,
                                      height=130)

multi_select_region_mcgg = MultiSelect(title="Select region",
                                       value=["NAM_"],
                                       options=[("NAM_", "North America"),
                                                ("EU_", "Europe"),
                                                ("EA_", "East Asia"),
                                                ("JP_", "Japan"),
                                                ("ME_", "Middle East"),
                                                ('GLO_', 'Global')],
                                       width=290,
                                       height=130)

multi_select_risk_mcgg = MultiSelect(title="Select risk factor",
                                     value=['econ'],
                                     options=[("econ", "Economic"),
                                              ("pol", "Political"),
                                              ("dis", "Natural disasters and accidents"),
                                              ("cyb", "Cyber Risk")],
                                     width=290,
                                     height=130)

button_mcgg = Button(label='Generator sentiment indicators', width=1200)

source_mcgg = ColumnDataSource(data={"date": cds_mcgg.data['Date'],
                                     "y1": cds_mcgg.data["tar_NAM_econ"],
                                     "y2": cds_mcgg.data["tar_NAM_econ_pessi"],
                                     "Bottom": cds_mcgg.data["Bottom"]})

df_label_begin_optim = pd.read_csv('label.csv')
df_label_begin_optim["Date"] = pd.to_datetime(df_label_begin_optim["Date"]).apply(dt.datetime.date)
df_label_begin_pessi = pd.read_csv('pessi_label.csv')
df_label_begin_pessi["Date"] = pd.to_datetime(df_label_begin_pessi["Date"]).apply(dt.datetime.date)

cds_label_optim = ColumnDataSource(data={"date":df_label_begin_optim["Date"],
                                    "y1":df_label_begin_optim["tar_NAM_econ"],
                                    "y2":df_label_begin_optim["tar_NAM_econ_pessi"],
                                    "label":df_label_begin_optim["tar_NAM_econ_label"]})

cds_label_pessi = ColumnDataSource(data={"date":df_label_begin_pessi["Date"],
                                    "y1":df_label_begin_pessi["tar_NAM_econ"],
                                    "y2":df_label_begin_pessi["tar_NAM_econ_pessi"],
                                    "label":df_label_begin_pessi["tar_NAM_econ_label"]})

def update_mcgg():
    key_optim = multi_select_level_mcgg.value[0] + multi_select_region_mcgg.value[0] + multi_select_risk_mcgg.value[0]
    key_pessi = key_optim + "_pessi"
    key_label = key_optim + "_label"
    source_mcgg.data["y1"] = cds_mcgg.data[key_optim]
    source_mcgg.data["y2"] = cds_mcgg.data[key_pessi]

    cds_label_optim.data['date'] = [cds_mcgg.data['Date'][i] for i in np.argsort(cds_mcgg.data[key_optim])[-5:]]
    cds_label_optim.data["y1"] = [cds_mcgg.data[key_optim][i] for i in np.argsort(cds_mcgg.data[key_optim])[-5:]]
    cds_label_optim.data["y2"] = [cds_mcgg.data[key_pessi][i] for i in np.argsort(cds_mcgg.data[key_optim])[-5:]]
    cds_label_optim.data["label"] = [cds_mcgg.data[key_label][i] for i in np.argsort(cds_mcgg.data[key_optim])[-5:]]

    cds_label_pessi.data['date'] = [cds_mcgg.data['Date'][i] for i in np.argsort(cds_mcgg.data[key_pessi])[:5]]
    cds_label_pessi.data["y1"] = [cds_mcgg.data[key_optim][i] for i in np.argsort(cds_mcgg.data[key_pessi])[:5]]
    cds_label_pessi.data["y2"] = [cds_mcgg.data[key_pessi][i] for i in np.argsort(cds_mcgg.data[key_pessi])[:5]]
    cds_label_pessi.data["label"] = [cds_mcgg.data[key_label][i] for i in np.argsort(cds_mcgg.data[key_pessi])[:5]]

    layout_mcgg.children[-3] = create_figure_mcgg(source_mcgg=source_mcgg,
                                                 cds_label_optim=cds_label_optim,
                                                 cds_label_pessi=cds_label_pessi)

button_mcgg.on_click(update_mcgg)

pre_mcgg = Div(text=
               '''
               <h2> GFIs Generator </h2>
               <p>
               In the figure below, you can generate the optimistic and pessimistic GFIs for the company you selected in the network (companies listed after 2012 or non-listed companies are not available).
               You can also click on the legend to mute the corresponding GFI.
               </p>

               ''',
               width=1200)

pre_all = Div(text='''
<p>
<h1>Construct Geolocation Risk-factor Indicators with News Sentiment</h1>
</p>
<p>
<b>
In this page, a method to construct geo-risk factor indicators (GFIs) by using publicly available information – news is presented. GFIs can capture various risk types in different regions faced by individual companies comprehensively. GFIs can be employed by companies to measure their own risk exposures and to support the business operational and strategical decision-making, or be adopted by other stakeholders to capture the risks faced by the company and make predictions about the company’s performance in the market and communities.
</p>
<p>
Toyota Motor Corporation is chosen as an example to demonstrate the implication of GFIs, since the business operation of this company is spread globally, the need for developing an integrated risk measurement system can be urgent.
<p>
You will first see a brief summary about the news data used to construct GFIs, then a competitor-and-collaborator network for Toyota, you can then select the company from the network graph and see corresponding GFIs in the generator at the end of this page.
</p>
<p>
At the end of this page, a more flexible GFI generator is provided, through which you can generate the GFIs for the company you are interested in.
</p>
</b>
</p>''', width=1200)



control_mcgg = row([multi_select_level_mcgg, multi_select_region_mcgg, multi_select_risk_mcgg])
layout_mcgg = column(
    [pre_mcgg,
     create_figure_mcgg(source_mcgg=source_mcgg,
                        cds_label_optim=cds_label_optim,
                        cds_label_pessi=cds_label_pessi),
     control_mcgg,button_mcgg])

#################################################################################
#################################################################################
layout_all = column([pre_all,layout_trna,layout_nx,layout_mcgg])
curdoc().add_root(layout_all)
