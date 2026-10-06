# MgTe example

MgTe has a two-atom primitive cell and six phonon branches:

- branches 1–3: acoustic;
- branches 4–6: optical.

The compact reference fixture is derived from a validated 0 GPa, 300 K calculation. It is sufficient to run closure tests and produce plots; it is not a complete FourPhonon calculation and contains no force constants.

```bash
fourphonon-channel validate ../../tests/reference
fourphonon-channel plot ../../tests/reference --output figures/mgte_channels.png
```

The pressure-comparison figures use separately validated 0 and 5 GPa channel calculations. No pressure mode matching is implied: each pressure is plotted against its own target frequency.

`input/README.md` documents which upstream inputs a user needs but intentionally does not distribute production inputs.
