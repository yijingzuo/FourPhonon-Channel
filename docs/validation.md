# Reproducibility and validation

Reference system: MgTe, 0 GPa, 300 K, two-atom primitive cell, 282 irreducible target modes.

Internal per-mode closure:

- three-phonon maximum absolute residual: `1.94289e-16 THz`
- four-phonon maximum absolute residual: `2.22045e-16 THz`

Three-way validation compared, mode by mode:

```text
total scattering rate
= official topology decomposition
= new A/O decomposition
```

All 282 modes passed with zero failures. Upstream `BTE.w_*` files print fewer digits than the new channel files; therefore text-level residuals are approximately `1e-10 THz`, while internal closure reaches approximately `1e-16 THz`.

The tests use `atol=2e-9`, `rtol=2e-9`, and treat scales at or below `1e-12` with the absolute tolerance. For acoustic target modes, `OOO` and `OOOO` are structural zeros. `AOOO` is not asserted as a universal zero.
