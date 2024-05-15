#!/bin/bash

# Create conda environment and activate it
conda create --name Gpu python=3.10 -y

# Activate the environment and execute the commands within a subshell
(
    eval "$(conda shell.bash hook)"
    conda activate tf_gpu_conda

    pip install --upgrade pip
    pip install tensorflow[and-cuda]
    pip install jupyterlab pandas matplotlib scikit-learn seaborn xarray netCDF4 h5netcdf xgboost streamlit holoviews bokeh plotly folium streamlit-folium statsmodels gradio pydot graphviz prophet jupyterlab-nvdashboard shap ipywidgets

    # Verify installation
    python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
)

