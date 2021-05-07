# Estimated R2 maps

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
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

def plot_subplots(scans,scans_names,slices,title,file_name):
    
    slices_names = []
    for i in slices:
        slices_names.append("Slice " + str(i+1))
    
    fig = make_subplots(rows=4, cols=5,horizontal_spacing = 0.01,vertical_spacing = 0.01, 
                    column_titles = slices_names, row_titles = scans_names)

    
    for j in range(len(scans)):
        for i in range(len(slices)):
            current = np.rot90(layers[j][slices[i]],3)
            fig.add_trace(
                go.Heatmap(z = current, 
                           xtype = "scaled", 
                           ytype = "scaled",
                           colorscale = "gray",
                           showscale = False,
                           hoverinfo = "skip"
    #                        colorbar = dict(title = dict(text = "B<sub>0</sub> (Hz)"))
                            ),
                row=(j+1), col=(i+1)
            )


    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    fig.update_layout(height=600, width=800, title_text=title)

    plot(fig, filename = file_name, config = config)

    #display(HTML('fig2.html'))
    

Axial views of estimated in vivo R<sub>2</sub><sup>*</sup> maps. (A), The R<sub>2</sub><sup>*</sup> maps were directly calculated from the spoiled mGRE data by assuming a mono‐exponential signal model neglecting G<sub>z</sub> ( F<sub>z-shim</sub>=1). The other R<sub>2</sub><sup>*</sup> maps were calculated using the proposed signal model for the spoiled mGRE (B), the global z‐shim ( |$\bar{G}$ <sup>+/</sup><sub>c</sub> ) (C), and the proposed slice‐specific approach (D) data. An increase in SNR can be observed from (C) to (D) due to higher signal recovery


scans_path = ["data/mag_echo1_ref_scan.nii","data/mag_echo1_ref_scan.nii","data/mag_echo2_ref_scan.nii","data/mag_echo3_ref_scan.nii"]

n=35

layers = []
for path in scans_path:
    layers.append(load_image(path))

scans_names = ["Prv scan", "Vtor scan", "Tret scan", "Ctvrti scan"]
slices = [2,8,11,14,23]
title = "Axial views of estimated in R\N{SUBSCRIPT TWO} maps"

plot_subplots(layers,scans_names,slices,title,"final.html")
display(HTML('final.html'))