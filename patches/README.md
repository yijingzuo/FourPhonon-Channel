# FourPhonon patch

`fourphonon_channel.patch` targets the official FourPhonon **v1.1** tag.

Apply from the root of a clean upstream checkout:

```bash
git checkout v1.1
git apply --check /path/to/fourphonon_channel.patch
git apply /path/to/fourphonon_channel.patch
cd Src
make
```

The patch contains only A/O bookkeeping, MPI reduction, output, and closure diagnostics in `Src/processes.f90` and `Src/ShengBTE.f90`. It contains no compiler configuration, scheduler settings, force constants, executable, or machine-specific path.

The reference implementation defines branches 1–3 as acoustic and branches 4–6 as optical. Version 0.1.0 is validated for two-atom primitive cells (`Nbands=6`). See the top-level README before applying it to another system.
