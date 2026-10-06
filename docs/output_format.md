# Output format

The patched executable writes:

- `BTE.Scatt3_AAA`, `BTE.Scatt3_AAO`, `BTE.Scatt3_AOO`, `BTE.Scatt3_OOO`
- `BTE.Scatt4_AAAA`, `BTE.Scatt4_AAAO`, `BTE.Scatt4_AAOO`, `BTE.Scatt4_AOOO`, `BTE.Scatt4_OOOO`
- `BTE.Scatt3_closure`, `BTE.Scatt4_closure`, `BTE.Scatt_AO_closure_summary`

Each channel file contains:

```text
mode_index  q_index  branch  omega(rad/ps)  scattering_rate(THz)
```

The line ordering matches the upstream branch-major `BTE.w_*` ordering. Convert angular frequency using

\[
f(\mathrm{THz})=\omega(\mathrm{rad/ps})/(2\pi).
\]

Numerically, `1 THz = 1 ps^-1`, so scattering rates labelled THz may also be plotted as ps⁻¹.
