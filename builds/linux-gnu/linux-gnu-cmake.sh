#!/bin/sh

# cmake configuration script that works on the Linux box in Matt's office (blueskies) with GCC
# Others will need to modify the Netcdf path.
# This config script is setup to perform a parallel build with Trilinos.
#
# BUILD OPTIONS:
# The call to cmake below includes several input ON/OFF switch parameters, to
# provide a simple way to select different build options.  These are:
# CISM_BUILD_CISM_DRIVER -- ON by default, set to OFF to only build the CISM libraries.
# CISM_ENABLE_BISICLES -- OFF by default, set to ON to build a BISICLES-capable cism_driver.
# CISM_ENABLE_FELIX -- OFF by default, set to ON to build a FELIX-capable cism_driver.
# CISM_USE_TRILINOS -- OFF by default, set to on for builds with Trilinos.
# CISM_MPI_MODE -- ON by default, only set to OFF for serial builds.
# CISM_SERIAL_MODE -- OFF by default, set to ON for serial builds.
# CISM_USE_GPTL_INSTRUMENTATION -- ON by default, set to OFF to not use GPTL instrumentation.
# CISM_COUPLED -- OFF by default, set to ON to build with CESM.

# After this executes, do:
#   make -j 8

# Set path to top cism directory
# Note, this is an easy way to build out of source.
# In directory you want to build in, run:
#   $ source $CISM/builds/linux-gnu-cism/linux-gnu-cism-cmake $CISM
# where $CISM is the path to the top level cism directory.
if [ $# -eq 0 ]
then
    cism_top="../.." 
else
    cism_top=${1%/}
fi


echo CISM: "${cism_top}"

echo
echo Run this script by typing: source linux-gnu-cism-cmake
echo
echo Set CISM_TRILINOS_DIR to your Trilinos installation directory.
echo

# remove old build data:
rm -f ./CMakeCache.txt
rm -rf ./CMakeFiles

echo
echo "Doing CMake Configuration step"

cmake \
  -D CISM_BUILD_CISM_DRIVER:BOOL=ON \
  -D CISM_ENABLE_BISICLES=OFF \
  -D CISM_ENABLE_FELIX=OFF \
\
  -D CISM_USE_TRILINOS:BOOL="${CISM_USE_TRILINOS:=OFF}" \
  -D CISM_MPI_MODE:BOOL=ON \
  -D CISM_SERIAL_MODE:BOOL=OFF \
\
  -D CISM_USE_GPTL_INSTRUMENTATION:BOOL=OFF \
  -D CISM_COUPLED:BOOL=OFF \
\
  -D CISM_TRILINOS_DIR="$CISM_TRILINOS_DIR" \
  -D CISM_NETCDF_DIR="/usr/local/netcdf-parallel" \
  -D CISM_NETCDF_LIBS="netcdff" \
\
  -D CMAKE_Fortran_FLAGS="-g -O2 -ffree-line-length-none -fPIC -fno-range-check" \
\
  -D CMAKE_CXX_COMPILER=mpicxx \
  -D CMAKE_C_COMPILER=mpicc \
  -D CMAKE_Fortran_COMPILER=mpif90 \
\
  -D CISM_EXTRA_LIBS:STRING="-lblas" \
\
  -D CISM_MPI_INC_DIR=/usr/include/x86_64-linux-gnu/mpich \
  -D CISM_MPI_LIB_DIR=/usr/lib/x86_64-linux-gnu \
\
  -D CMAKE_VERBOSE_MAKEFILE=OFF \
  "${cism_top}"

