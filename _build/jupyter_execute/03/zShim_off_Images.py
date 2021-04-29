# zShim_off Images

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
        for slice in range(number_of_slices):
                layers.append(nii_data[:,:,slice,frame])

    return layers

def mapp(list_value, range_1,range_2):
    m = interp1d(range_1,range_2)
    return m(list_value)

def visualise_slices(volume, nb_frames, title,file_name):
    r, c = volume[0].shape

    fig = go.Figure(frames=[go.Frame(data=go.Surface(
        z=(nb_frames/10 - k * 0.1) * np.ones((r, c)),
        surfacecolor=np.flipud(volume[nb_frames - k]),
        cmin=0, cmax=250
        ),
        name=str(k) # you need to name the frame for the animation to behave properly
        )
        for k in range(1,nb_frames)])

    # Add data to be displayed before animation starts
    fig.add_trace(go.Surface(
        z=nb_frames/10 * np.ones((r, c)),
        surfacecolor=np.flipud(volume[nb_frames]),
        colorscale='Gray',
        cmin=0, cmax=250,
        colorbar=dict(thickness=20, ticklen=4)
        ))


    def frame_args(duration):
        return {
                "frame": {"duration": duration},
                "mode": "immediate",
                "fromcurrent": True,
                "transition": {"duration": duration, "easing": "linear"},
            }

    sliders = [
                {
                    "pad": {"b": 10, "t": 60},
                    "len": 0.9,
                    "x": 0.1,
                    "y": 0,
                    "steps": [
                        {
                            "args": [[f.name], frame_args(0)],
                            "label": str(k),
                            "method": "animate",
                        }
                        for k, f in enumerate(fig.frames)
                    ],
                }
            ]

    # Layout
    fig.update_layout(
             title=title,
             width=600,
             height=600,
             scene=dict(
                        zaxis=dict(range=[-0.1, nb_frames/10 ], autorange=False),
                        aspectratio=dict(x=1, y=1, z=1),
                        ),
             updatemenus = [
                {
                    "buttons": [
                        {
                            "args": [None, frame_args(50)],
                            "label": "&#9654;", # play symbol
                            "method": "animate",
                        },
                        {
                            "args": [[None], frame_args(0)],
                            "label": "&#9724;", # pause symbol
                            "method": "animate",
                        },
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 70},
                    "type": "buttons",
                    "x": 0.1,
                    "y": 0,
                }
             ],
             sliders=sliders
    )
    plot(fig, filename = file_name, config = config)

    #display(HTML('fig.html'))


raw_images_path = ["data/mag_echo3_ref_scan.nii","data/mag_echo3_zShim_Gc_220_alpha_60deg.nii",
                                  "data/mag_echo3_zShim_Gc_split_alpha_60deg.nii","data/mag_echo3_zShim_off_alpha_60deg.nii"]
raw_images_titles = ["mag_echo3_ref_scan","mag_echo3_zShim_Gc_220_alpha_60deg","mag_echo3_zShim_Gc_split_alpha_60deg","mag_echo3_zShim_off_alpha_60deg"]


n=20

raw_images_layers = []
for path in raw_images_path:
    raw_images_layers.append(load_image(path))

# for layers in raw_images_layers:
#     tmp1=[]
#     tmp2=[]
#     for array in layers:
#         for a in array:
#             tmp1.append(max(a))
#             tmp2.append(min(a))
#     print(max(tmp1))
#     print(min(tmp2))

mapp_raw_images_layers = []
for layers in raw_images_layers[1:4]:
    mapp_layers=[]
    for i in range(n+1):
        mapp_layers.append(mapp(layers[i],[0,31],[0,255]))
    mapp_raw_images_layers.append(mapp_layers)

mapp_layers=[]
for i in range(n+1):
     mapp_layers.append(mapp(raw_images_layers[0][i],[0,520],[0,255]))
mapp_raw_images_layers.append(mapp_layers)

visualise_slices(mapp_raw_images_layers[3], n, raw_images_titles[3],"fig34.html")
display(HTML('fig34.html'))