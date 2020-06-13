echo "starting job in run.sh ..."
export PREFIX_CC3D=../cc3d_420
export PYTHON_INSTALL_PATH=${PREFIX_CC3D}/Python37/bin
export PYTHONPATH=${PREFIX_CC3D}/lib/site-packages
export PATH=$PATH:PYTHON_INSTALL_PATH
export CPP=${PYTHONPATH}/cc3d/cpp
export LD_LIBRARY_PATH=${PREFIX_CC3D}/lib/:${CPP}/lib:${CPP}/CompuCell3DPlugins:${CPP}/CompuCell3DSteppables:$LD_LIBRARY_PATH
python3 run.py
