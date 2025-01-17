# zShim_Gc_split Images

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math
import nibabel as nib
import matplotlib.pyplot as plt
from math import ceil
from scipy.interpolate import interp1d
import time
from ipywidgets import interactive, HBox, widgets, interact
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from IPython.core.display import display, HTML
init_notebook_mode(connected=True)
config={'showLink': False, 'displayModeBar': False}

def load_image(path):
    nii_img = nib.load(path)
    nii_data = nii_img.get_fdata()

    number_of_slices = nii_data.shape[2]
    number_of_frames = nii_data.shape[3]

    layers = []

    for frame in range(number_of_frames):
        for s in range(number_of_slices):
                layers.append(nii_data[:,:,s,frame])
    
    return layers

def mapp(list_value, range_1,range_2):
    m = interp1d(range_1,range_2)
    return m(list_value)

def compare_scans(scans,nb_frames,file_name):
    newmap = np.concatenate((scans[0],scans[1],scans[2]), axis=1)
    new_title = "Echo1\t\t\tEcho2\t\t\tEcho3"
    
    data = []
    for i in range(nb_frames):
        current = np.rot90(newmap[i],3)
        data_c = go.Heatmap(z = current, 
                            visible = False,
                            xtype = "scaled", 
                            ytype = "scaled",
                            colorscale = "gray",
                            showscale = False,
                            hoverinfo = "skip"
                            #colorbar = dict(title = dict(text = "B<sub>0</sub> (Hz)"))
                           )
        data.append(data_c)
    data[0]['visible'] = True

    # Create steps and slider
    steps = []
    for i in range(nb_frames):
        step = dict(
            method = 'restyle',  
            args = ['visible', [False]*n],
            label = str(i+1)
        )
        step['args'][1][i] = True # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active = 0,
        currentvalue = {'prefix':"Current slice is: <b>"},
        pad = {"t": 50, "b": 10},
        steps = steps
    )]

    # Setup the layout of the figure
    layout = go.Layout(
        title = new_title, 
        width=800,
        height=500,
        margin=go.layout.Margin(
            l=50,
            r=50,
            b=60,
            t=35,
        ),
        showlegend = False,
        autosize = False,
        sliders=sliders,
        xaxis = dict(showgrid = False,
                     showticklabels= False),
        yaxis = dict(showgrid = False,
                     showticklabels = False),
        font = dict(family="Courier New, monospace",
                    size=14),
    )
    

    # Plot function saves as html or with ipplot
    fig = dict(data=data, layout=layout)
    plot(fig, filename = file_name, config = config)

    #display(HTML('fig2.html'))
    

raw_images_path = ["data/mag_echo1_zShim_Gc_split_alpha_60deg.nii","data/mag_echo2_zShim_Gc_split_alpha_60deg.nii","data/mag_echo3_zShim_Gc_split_alpha_60deg.nii"]

n=35

layers = []
for path in raw_images_path:
    layers.append(load_image(path))

# for layer in layers:
#     tmp1=[]
#     tmp2=[]
#     for array in layer:
#         for a in array:
#             tmp1.append(max(a))
#             tmp2.append(min(a))
#     print(max(tmp1))
#     print(min(tmp2))

mapp_layers = []
mapp_layer=[]
n=n-1
for i in range(n+1):
    mapp_layer.append(mapp(layers[0][i],[0,35],[0,255]))
mapp_layers.append(mapp_layer)

mapp_layer=[]
for i in range(n+1):
     mapp_layer.append(mapp(layers[1][i],[0,35],[0,255]))
mapp_layers.append(mapp_layer)

mapp_layer=[]
for i in range(n+1):
     mapp_layer.append(mapp(layers[2][i],[0,35],[0,255]))
mapp_layers.append(mapp_layer)

compare_scans(mapp_layers,n,"fig33.html")
display(HTML('fig33.html'))