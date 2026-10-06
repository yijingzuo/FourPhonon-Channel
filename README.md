# FourPhonon-Channel

Channel-resolved three- and four-phonon scattering analysis based on acoustic/optical branch composition.

> **Independent extension:** This project is an extension/analysis tool for [FourPhonon](https://github.com/FourPhonon/FourPhonon) and is not the official FourPhonon distribution.

## Features

- Three-phonon composition channels: `AAA`, `AAO`, `AOO`, `OOO`.
- Four-phonon composition channels: `AAAA`, `AAAO`, `AAOO`, `AOOO`, `OOOO`.
- Per-target-mode output in the same scattering-rate units as FourPhonon.
- Per-mode closure diagnostics and independent three-way validation.
- Python commands to validate, summarize, compare pressures, and plot channels.
- A compact, real MgTe reference fixture with automated tests.

This classification complements rather than replaces the upstream topology decomposition:

- 3ph topology: absorption/combination `+` and emission/splitting `-`;
- 4ph topology: combination `++`, redistribution `+-`, and splitting `--`.

**A/O composition** identifies which phonon sectors participate. **Topology** identifies how the scattering process occurs.

## Supported scope in v0.1.0

Version 0.1.0 preserves the validated reference implementation:

```text
branches 1–3 = acoustic
branches 4–6 = optical
```

It is validated for two-atom primitive cells (`Nbands=6`). The scientific concept generalizes to branches 4 through `3*Natoms`, but that generalization has not been introduced into the validated Fortran patch. Do not use the patch for larger primitive cells without extending and independently validating the branch classifier.

## Theory

For each target mode,

\[
\Gamma_{3\mathrm{ph}}=\Gamma_{AAA}+\Gamma_{AAO}+\Gamma_{AOO}+\Gamma_{OOO},
\]

\[
\Gamma_{4\mathrm{ph}}=\Gamma_{AAAA}+\Gamma_{AAAO}+\Gamma_{AAOO}+\Gamma_{AOOO}+\Gamma_{OOOO}.
\]

Bookkeeping uses the **same event contribution** accumulated by upstream FourPhonon, including its occupation factors, matrix elements, energy-conservation treatment, symmetry and prefactors. The 3ph minus channel inherits the upstream `1/2` double-counting correction. No scattering physics is reimplemented by the Python tools.

See [theory.md](docs/theory.md).

## What this repository is—and is not

FourPhonon-Channel is not a standalone phonon-scattering solver. The Fortran
part is a source patch for official FourPhonon/ShengBTE; the Python part only
reads, validates, summarizes, compares, and plots scattering outputs. It does
not run DFT, fit interatomic force constants, perform SCPH calculations, or
recompute scattering physics.

The complete workflow is:

```text
DFT / force-constant generation
        -> valid FourPhonon input directory
        -> FourPhonon v1.1 patched with FourPhonon-Channel
        -> official totals/topologies plus A/O channel files
        -> FourPhonon-Channel Python validation and plotting
```

## Prerequisites

To generate new channel-resolved scattering rates, users first need a working
official FourPhonon v1.1 installation and its ShengBTE dependencies. A typical
build requires:

- a Fortran compiler supported by the upstream source;
- an MPI implementation and MPI Fortran wrapper;
- BLAS and LAPACK;
- spglib as required by the upstream build;
- GNU Make and an upstream-compatible `Src/arch.make`.

The exact compiler and library flags are machine dependent and are not shipped
by this repository. Official FourPhonon v1.1 also contains legacy Fortran syntax
that may be rejected by some recent gfortran configurations; follow the
upstream-supported toolchain or an already validated local build. This project
does not include compiler-specific modifications.

The post-processing package requires Python 3.9 or newer and NumPy. Matplotlib
is needed for plotting, and pytest is optional for the developer test suite.

## Required calculation inputs

The patched executable consumes the same physical inputs as an ordinary
FourPhonon calculation. Before applying this extension, users must already have
a calculation directory that runs correctly with official FourPhonon. Depending
on the material and upstream configuration, this normally includes:

- `CONTROL`, containing the crystal, q mesh, temperature, isotope and run settings;
- harmonic/second-order force constants;
- third-order force constants for 3ph scattering;
- fourth-order force constants for 4ph scattering;
- Born effective charges and dielectric data when non-analytic corrections are
  enabled for a polar material;
- any other structure or auxiliary files required by the selected upstream
  FourPhonon/ShengBTE workflow.

File naming and formatting must follow official FourPhonon v1.1. No production
force constants or private first-principles inputs are distributed here.

## Installation

Obtain the compatible upstream source and apply the patch:

```bash
git clone https://github.com/FourPhonon/FourPhonon.git
cd FourPhonon
git checkout v1.1
git apply --check /path/to/FourPhonon-Channel/patches/fourphonon_channel.patch
git apply /path/to/FourPhonon-Channel/patches/fourphonon_channel.patch
cd Src
# Configure upstream arch.make for your compiler, MPI, BLAS/LAPACK, and spglib.
make
```

Install the optional post-processing CLI:

```bash
cd /path/to/FourPhonon-Channel
python -m pip install '.[plot,test]'
```

Full details: [installation.md](docs/installation.md).

## Usage

1. Prepare and run FourPhonon normally with a supported two-atom primitive cell.
2. Use the patched executable. It writes A/O channel files alongside upstream `BTE.w_*` outputs in each temperature directory.
3. Validate before analysis:

```bash
fourphonon-channel validate /path/to/calculation/T300K
```

4. Summarize acoustic target modes:

```bash
fourphonon-channel summarize /path/to/calculation/T300K --acoustic-targets
```

5. Plot one calculation or compare two pressures:

```bash
fourphonon-channel plot /path/to/calculation/T300K --output channels.png
fourphonon-channel compare /path/to/0GPa/T300K /path/to/5GPa/T300K --output comparison.csv
```

The direct scripts remain available:

```bash
python src/postprocess/validate_channels.py PATH
python src/postprocess/plot_channels.py PATH --output channels.png
python src/postprocess/compare_pressure.py PATH0 PATH5 --output comparison.csv
```

## Output files

```text
BTE.Scatt3_AAA   BTE.Scatt3_AAO   BTE.Scatt3_AOO   BTE.Scatt3_OOO
BTE.Scatt4_AAAA  BTE.Scatt4_AAAO  BTE.Scatt4_AAOO  BTE.Scatt4_AOOO  BTE.Scatt4_OOOO
```

Columns:

```text
mode_index  q_index  branch  omega(rad/ps)  scattering_rate(THz)
```

Ordinary frequency is `omega/(2*pi)` in THz. Numerically, `1 THz = 1 ps^-1`. See [output_format.md](docs/output_format.md).

## Validation

MgTe at 0 GPa and 300 K, 282 target modes:

- internal 3ph maximum absolute closure residual: `1.94289e-16 THz`;
- internal 4ph maximum absolute closure residual: `2.22045e-16 THz`;
- three-way comparison: `original total = official topology sum = A/O sum`;
- failed modes: `0 / 282`.

Because official `BTE.w_*` text output has fewer printed digits, text-level residuals are around `1e-10 THz`; internal closure is around `1e-16 THz`. See [validation.md](docs/validation.md).

Run the packaged checks:

```bash
python tests/run_tests.py
# Optional, when pytest is installed:
python -m pytest -q
fourphonon-channel validate tests/reference
```

## Example

The [MgTe example](examples/MgTe/README.md) contains compact reference data and figures only. It intentionally excludes force constants, production outputs, executables, and private calculation inputs.

## License and upstream attribution

FourPhonon v1.1 is licensed under GNU GPL v3. This patch-based distribution is provided under `GPL-3.0-only`; modified material is marked and the upstream copyright/license requirements remain applicable. Users must obtain FourPhonon from its official repository.

When publishing results, cite the upstream FourPhonon and ShengBTE papers listed in [CITATION.cff](CITATION.cff), plus this software record. The repository URL remains a placeholder until a public repository is created.
