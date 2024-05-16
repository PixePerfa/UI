# Use a smaller base image
FROM tensorflow/tensorflow:nightly-gpu-jupyter

# Set the working directory
WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cuda-toolkit \
    && rm -rf /var/lib/apt/lists/*

# Install Nvidia container toolkit
RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
    && apt-get update \
    && apt-get install -y nvidia-container-toolkit \
    && rm -rf /var/lib/apt/lists/*

# Install LocalLLM Providers
RUN curl -fsSL https://ollama.com/install.sh | sh \
    && pip install 'litellm[proxy]'

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tensorflow[and-cuda] jupyterlab pandas matplotlib

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir tensorflow[and-cuda] jupyterlab pandas matplotlib scikit-learn seaborn xarray netCDF4 h5netcdf xgboost streamlit holoviews bokeh plotly folium streamlit-folium statsmodels gradio pydot graphviz prophet jupyterlab-nvdashboard shap torch torchaudio transformers huggingface_hub fastapi uvicorn ray dask hyperopt loguru "ray[all]"


ENV TF_FORCE_GPU_ALLOW_GROWTH=true


# Expose the necessary ports
EXPOSE 8888 8501 4000 8000 8265 11434 

# Run Jupyter Lab on container start
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--port=8888", "--no-browser"]
