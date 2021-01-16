# singularity box definition file
# contains cc3d package (offscreen mode) in the base conda environment

Bootstrap: library
From: ubuntu:focal

%post -c /bin/bash
# use an unmounted folder
  cd /opt

# get the good sources
  echo "deb http://archive.ubuntu.com/ubuntu focal-backports main universe multiverse restricted" >> /etc/apt/sources.list

# refresh
  apt-get update
  apt-get dist-upgrade -y

# install required packages
  apt-get install -y wget git g++ make libosmesa-dev libgl-dev

# build miniconda from source
  wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  bash Miniconda3-latest-Linux-x86_64.sh -bfp /usr/local
  conda config --append channels compucell3d
  conda config --prepend channels conda-forge
  conda config --set channel_priority false

# install dependencies
  conda install python=3.7
  conda install -c conda-forge pandas jinja2 pyqt pyqtgraph deprecated qscintilla2 chardet imageio matplotlib seaborn swig=3 cmake=3.13.4
  conda install -c conda-forge/label/vtk_dev vtk=9.0.0.rc3=with_osmesa_py37h43e0876_0
  conda install -c compucell3d tbb_full_dev
  pip install webcolors libroadrunner antimony

# build cc3d from (custom) sources
  git clone https://github.com/gabroo/CompuCell3D.git
  git clone https://github.com/gabroo/cc3d_build_scripts.git
  mkdir cc3d_build && cd cc3d_build
  cmake \
    -G Unix\ Makefiles \
    -DCMAKE_BUILD_TYPE:STRING=Release \
    -DNO_OPENCL:BOOLEAN=ON \
    -DCMAKE_INSTALL_PREFIX:PATH=/opt/cc3d \
    -DPYTHON_EXECUTABLE=/usr/local/bin/python3 \
    -DPython_EXECUTABLE=/usr/local/bin/python3 \
    -DPYTHON_INCLUDE_DIR=/usr/local/include/python3.7m \
    -DPython_INCLUDE_DIRS=/usr/local/include/python3.7m \
    -DPYTHON_LIBRARY=/usr/local/lib/libpython3.7m.so \
    -DPython_LIBRARIES=/usr/local/lib/libpython3.7m.so \
    -DPython_LIBRARY_RELEASE=/usr/local/lib/libpython3.7m.so \
    -DVTK_DIR=/usr/local/lib/cmake/vtk-9.0 \
    -DVTK_INCLUDE_DIRS=/usr/local/include/vtk-9.0 \
    /opt/CompuCell3D/CompuCell3D
  make -j8
  make install
  
# symbolic links
  ln -s /opt/cc3d/lib/site-packages/cc3d /usr/local/lib/python3.7/site-packages/cc3d
  ln -s $(find /opt/cc3d | grep "\.so$") /usr/local/lib
  
%test
# make sure we can do VTK offscreen
  cd /opt
  python3 CompuCell3D/cc3d/experimental/offscreen-test.py
