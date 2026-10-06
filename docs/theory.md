# Theory and classification

FourPhonon-Channel adds a label to the same event contribution already accumulated by FourPhonon. It does not recalculate matrix elements, populations, energy conservation, prefactors, symmetry multiplicities, or topology.

For three-phonon events, the unordered acoustic/optical composition gives

\[
\Gamma_{3\mathrm{ph}}=\Gamma_{AAA}+\Gamma_{AAO}+\Gamma_{AOO}+\Gamma_{OOO}.
\]

For four-phonon events,

\[
\Gamma_{4\mathrm{ph}}=\Gamma_{AAAA}+\Gamma_{AAAO}+\Gamma_{AAOO}+\Gamma_{AOOO}+\Gamma_{OOOO}.
\]

Composition and topology are orthogonal labels. Composition answers which phonon sectors participate. The upstream `+/-` and `++/+-/--` decomposition describes how a process occurs.

## Branch convention in v0.1.0

The validated reference implementation uses branches 1–3 as acoustic and 4–6 as optical. This is appropriate for a two-atom primitive cell. Although the conceptual rule extends to branches 4 through `3*Natoms`, v0.1.0 deliberately preserves the validated Fortran implementation and does not claim validation for cells with more than two atoms.
