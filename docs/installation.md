# Installation

## Scope

FourPhonon-Channel has two components:

1. a Fortran patch that instruments an existing FourPhonon calculation; and
2. Python tools that validate and analyze the generated output.

It is not a standalone replacement for FourPhonon or ShengBTE and does not
generate force constants.

## System requirements

Generating channel-resolved rates requires a working official FourPhonon v1.1
build environment. Follow the upstream documentation for the exact versions and
machine-specific flags. In general, users need a supported Fortran compiler,
MPI with a Fortran wrapper, BLAS/LAPACK, spglib, and GNU Make. Configure
`Src/arch.make` locally; this repository intentionally distributes no compiler,
MPI, cluster, or absolute-path configuration.

Some modern gfortran configurations reject legacy logical-comparison syntax in
the unmodified FourPhonon v1.1 `config.f90`. That upstream compatibility issue
occurs before the channel additions are compiled. Use an upstream-supported
compiler configuration or a FourPhonon v1.1 environment already known to build.

For post-processing, use Python 3.9 or newer with NumPy. Matplotlib is required
for plots, while pytest is optional unless running the pytest suite.

## Physical inputs

Start from an input directory that already runs successfully with official
FourPhonon v1.1. It normally contains `CONTROL`, harmonic force constants,
third-order force constants, fourth-order force constants, crystal information,
and any auxiliary data requested by the upstream configuration. Polar
calculations using non-analytic corrections also require the corresponding Born
effective charges and dielectric data.

FourPhonon-Channel does not perform DFT, IFC fitting, SCPH, or force-constant
generation. Input filenames, formats, units, and convergence requirements are
those of official FourPhonon/ShengBTE.

## Patch FourPhonon

```bash
git clone https://github.com/FourPhonon/FourPhonon.git
cd FourPhonon
git checkout v1.1
git apply --check /path/to/FourPhonon-Channel/patches/fourphonon_channel.patch
git apply /path/to/FourPhonon-Channel/patches/fourphonon_channel.patch
cd Src
# Configure arch.make exactly as required by your FourPhonon installation.
make
```

## Install post-processing tools

```bash
cd /path/to/FourPhonon-Channel
python -m pip install .
# For plotting and tests:
python -m pip install '.[plot,test]'
```

No executable or MPI/compiler configuration is distributed here.

## End-to-end use

After compiling, copy or link the patched executable into a new calculation
directory without overwriting prior results. Run FourPhonon in the normal
upstream manner. In addition to the official rate and topology outputs, the
patched executable writes `BTE.Scatt3_*` and `BTE.Scatt4_*` channel files into
the temperature output directory. Validate those files before analysis:

```bash
fourphonon-channel validate /path/to/calculation/T300K
fourphonon-channel plot /path/to/calculation/T300K --output channels.png
```

Version 0.1.0 is validated only for two-atom primitive cells with branches 1–3
acoustic and 4–6 optical.
