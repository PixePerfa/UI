# Use TensorFlow's official GPU-enabled Jupyter image as the base
FROM tensorflow/tensorflow:latest-gpu-jupyter

# Set the working directory
WORKDIR /app

# Upgrade pip and install required Python packages
RUN pip install --upgrade pip && \
    pip install tensorflow[and-cuda] jupyterlab pandas matplotlib scikit-learn seaborn xarray netCDF4 h5netcdf xgboost streamlit holoviews bokeh plotly folium streamlit-folium statsmodels gradio pydot graphviz prophet jupyterlab-nvdashboard shap ipywidgets nvidia-cuda-toolkit torch torchaudio transformers huggingface_hub fastapi uvicorn ray dask optuna hyperopt loguru "ray[all]"


    
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.1-1_all.deb && \
    apt-get install apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release && \
    apt-get install curl && \
    apt-get install wget && \
    dpkg -i cuda-keyring_1.1-1_all.deb && \
    apt install software-properties-common && \
    add-apt-repository contrib && \
    apt-get update  && \
    apt-get -y install cudnn-cuda-12
    apt-get -y install cuda-toolkit-12-4



# Install monitoring and debugging tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    nvidia-smi \
    htop \
    ipdb \
    pdbpp \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh 

RUN pip install 'litellm[proxy]'

# Create a custom entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Make port 8888 available to the world outside this container
EXPOSE 8888

# Make port 8501 available for Streamlit
EXPOSE 8501

# Make port litellm available for Streamlit
EXPOSE 4000

# Make port litellm available for Streamlit
EXPOSE 8000
# Make port ray 
EXPOSE 8265

# Run Jupyter Lab on container start
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--port=8888", "--no-install", "--no-browser"]
