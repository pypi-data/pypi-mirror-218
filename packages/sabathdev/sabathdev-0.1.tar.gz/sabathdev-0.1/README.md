# sabathdev installation

This repository is built using the template from [horovod-gpu-data-science-project](https://github.com/KAUST-Academy/horovod-gpu-data-science-project). Sabathdev repository contains scientific machine learning benchmarks (from [SciML-Bench](https://github.com/stfc-sciml/sciml-bench.git)) that uses distributed, multi-gpu training with [Horovod](https://github.com/horovod/horovod) together with one of [TensorFlow](https://www.tensorflow.org/), [PyTorch](https://pytorch.org/), or [MXNET](https://mxnet.apache.org/). 

## Getting Started

Pre-requisite Anaconda Installation:
```
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh

bash Anaconda3-2022.10-Linux-x86_64.sh

# Go through installation process (initialize with conda init with yes when prompted)

exec bash
```

To use sabath just clone this repository, cd to sabathdev directory and run the following commands.
```
git clone git@github.com:icl-utk-edu/sabathdev.git

cd sabathdev

# To run miniWeatherML

conda env create -f envs/miniWeatherML.yml

conda activate miniWeatherML

src/miniWeatherML_scripts/miniWeatherML.sh 
```

## Usage (Deprecated)
To run the benchmarks, use the following command (assuming conda environment is activated):

```
python3 sabathdev.py <dataset_name> <benchmark_name>
```
For Example:
```
python3 sabathdev.py MNIST MNIST_tf_keras
```

## Sciml Datasets and Benchmarks

### Benchmarks

<TABLE style="width:100%>"
<TR>
<TH>Benchmark</TH>
<TH>Dataset </TH>
<TH>Title </TH>
<TH>Info </TH>
<TH>Dependencies </TH>
</TR>
<TR>
<TD>MNIST_tf_keras</TD>
<TD>MNIST</TD>
<TD>Classifying MNIST with CNN using Tensorflow Keras.</TD>
<TD>Demonstrates how to build a benchmark into SciML-Bench.</TD>
<TD>tensorflow</TD>
</TR>
<TR>
<TD>MNIST_torch</TD>
<TD>MNIST</TD>
<TD>Classifying MNIST with CNN using Pytorch and Horovod for distributed learning.</TD>
<TD>Demonstrates how to build a benchmark into SciML-Bench.</TD>
<TD>torch, horovod (with HOROVOD_WITH_PYTORCH=1)</TD>
</TR>
<TR>
<TD>em_denoise</TD>
<TD>em_graphene_sim</TD>
<TD>Denoising electron microscopy (EM) images of graphene using an autoencoder.</TD>
<TD>Here the datasets are simulated datasets.</TD>
<TD>mxnet</TD>
</TR>
<TR>
<TD>dms_structure</TD>
<TD>dms_sim</TD>
<TD>Classifying crystal structures based on the DMS pattern.</TD>
<TD>Diffuse multiple scattering patterns simulated for Tetragonal and Rhombohedral crystal strcutures mimics data collecet at Diamond Light Source.</TD>
<TD>torch</TD>
</TR>
<TR>
<TD>slstr_cloud</TD>
<TD>slstr_cloud_ds1</TD>
<TD>Cloud segmentation in Sentinel-3 SLSTR images</TD>
<TD>Classifying pixels as either cloudy or clear using images from the SLSTR instrument onboard Sentinel-3 using a U-Net style architecture.</TD>
<TD>tensorflow, horovod (with HOROVOD_WITH_TENSORFLOW=1), scikit-learn</TD>
</TR>
</TABLE>

### Datasets

<TABLE style="width:100%>"
<TR>
<TH>Dataset</TH>
<TH>Size (approx) </TH>
<TH>Title </TH>
<TH>Info </TH>
<TH>Data server </TH>
</TR>
<TR>
<TD>MNIST</TD>
<TD>12 MB</TD>
<TD>The MNIST database of handwritten digits.</TD>
<TD>Demonstrates how to add a dataset to SciML-Bench.</TD>
<TD>By contributors</TD>
</TR>
<TR>
<TD>em_graphene_sim</TD>
<TD>28 GB</TD>
<TD>Simulated electron microscopy (EM) images of graphene.</TD>
<TD>Each image has a clean and a noisy version.</TD>
<TD>By contributors</TD>
</TR>
<TR>
<TD>dms_sim</TD>
<TD>7 GB</TD>
<TD>Simulated diffuse multiple scattering (DMS) patterns.</TD>
<TD>The patterns are labelled by the azimuthal angles.</TD>
<TD>By contributors</TD>
</TR>
<TR>
<TD>slstr_cloud_ds1</TD>
<TD>180 GB</TD>
<TD>Sentinel-3 SLSTR satellite image data.</TD>
<TD>The ground truth of a pixel as either cloudy or clear is provided.</TD>
<TD>By contributors</TD>
</TR>
</TABLE>

## Dependencies

### environment.yml

```
name: null

channels:
- pytorch
- nvidia
- conda-forge
- defaults

dependencies:
- bokeh=1.4
- cmake=3.16 # insures that Gloo library extensions will be built
- cudatoolkit=10.1
- cudnn=7.6
- cupti=10.1
- cxx-compiler=1.0 # insures C and C++ compilers are available
- jupyterlab=1.2
- mpi4py=3.0 # installs cuda-aware openmpi
- nccl=2.5
- nodejs=13
- nvcc_linux-64=10.1 # configures environment to be "cuda-aware"
- pip=20.0
- pip:
    - mxnet-cu101mkl==1.6.* # MXNET is installed prior to horovod
- python=3.7
- pytorch=1.5
- tensorboard=2.1
- tensorflow-gpu=2.1
- torchvision=0.6
```
### requirements.txt

```
py-cpuinfo
gputil
tabulate
aws-shell
matplotlib
scikit-learn
h5py==2.10.0
horovod==0.19.*
jupyterlab-nvdashboard==0.2.*
jupyter-tensorboard==0.2.*

# make sure horovod is re-compiled if environment is re-built
--no-binary=horovod
```

## Citation
<a name="citation"></a>

If you use this code or the data in your research, please cite the following GitHub repository:

```bibtex
@misc{scimlbench:2021,
    title  = {SciMLBench: A Benchmarking Suite for AI for Science},
    author = {Jeyan Thiyagalingam, Kuangdai Leng, Samuel Jackson,  Juri Papay, Mallikarjun Shankar, Geoffrey Fox,  Tony Hey},
    url    = {https://github.com/stfc-sciml/sciml-bench},
    year   = {2021}
}
```

