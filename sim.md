# Sensitivity of shoreline-trajectory to deposition-events

## Accuracy of inferred signal as function of signal-shape and sample-rate

### Implications for Sequence-Stratigraphy

****

## Summary

Sequo-Strat
correlate depo-units to depo-units in space-domain
correlate depo-units to sea-level in time-domain
sea-level = insolation-curve
deposition uniform and frequent

Delta
Deltaic Depo-System at shore and active
Deltaic clinoform inflection = shoreline
Shoreline-Trajectory = Sealevel-Curve

Condition
to infer signal samples must be sufficiently frequent
deposition events clustered

Simulation
Period $T$, Amplitude $A$, Period-Modulator $T_m$, Amplitude-Modulator $A_m$, Phase $p$
Eccentricity $s_1$, Obliquity $s_2$, Precession $s_3$
insolation $s$ ($T_1=100ka$, $T_2=41ka$, $T_3=26ka$, $A=1$, $T_m=0$, $A_m=\frac{1}{2}$, $p=0$)
duration $d=1Ma$
random samples of insolation curve (sample=cluster)
spread samples evenly
fit (sample-crossings / signal-crossings)
vary sample-rate sam($1$, $100$) => logistic curve ($max_y=1$, $slope=0.4$, $mid_{y,x}=60$)
sample-rate, fit : $(35, \frac{1}{4}) (70, \frac{1}{2}) (140, \frac{3}{4})$
vary parameters $(T, A, T_m, A_m, p)$ for $(s_1, s_2, s_3)$

Question
How affect these findings the use of SequoStrat?

****

## Key words

deposition-event, eustatic sea-level, sample, shoreline-trajectory, signal, tectonic subsidence

****

Choi ...

- Correlation and Stratigraphic Prediction: Sequence stratigraphy helps in correlating and predicting the distribution of sedimentary rock units within a basin. By recognizing and mapping sequences of sedimentary strata, geologists can establish the temporal and spatial relationships of these units.

- Paleogeography Reconstruction: It provides a means to reconstruct the paleogeography of an area at various points in geological history. By understanding how sea levels have changed over time, geologists can infer the position and extent of ancient shorelines and depositional environments.

- Identification of Depositional Environments: It aids in identifying different depositional environments within a basin. By recognizing specific sequence boundaries and stratigraphic surfaces, geologists can infer whether sediments were deposited in a transgressive or regressive setting, nearshore or offshore, etc.

- Hydrocarbon Exploration: In the context of the petroleum industry, sequence stratigraphy is crucial for understanding the distribution and quality of reservoir rocks, seals, and source rocks. It helps in identifying potential hydrocarbon-bearing units within sedimentary basins.

- Understanding Earth History: Sequence stratigraphy provides insights into the Earth's dynamic history, including changes in sea level, tectonic events, and climate variations. It allows geologists to construct a more comprehensive narrative of Earth's geological past.

- Environmental and Resource Management: It can be valuable in assessing the impact of sea-level changes on coastal environments, which is important for coastal management and understanding the response of ecosystems to such changes.

...

## Introduction

- Tectonic Subsidence S
- Insolation H
- Eustatic Sea-level L
- Deposition D
- Shoreline-trajectory X

### Tectonic Subsidence Y

$$
Y(t) = f(R,M)
$$

- isostasic rebound R
- bending moment M
- heatflux q
- intraplate stress σ

### Insolation I

$$
I(t) = f(E,θ,ω)
$$

- eccentricity E
- obliquity θ
- precession ω

### Absolute Sea-level $L$

$$
L(t) = f(T,Ω,Q,P,E)
$$

- temperature T
- polar ice Ω
- polar transport Q
- continent precipitation P
- ocean evaporation E

### Relative Sea-Level $\tilde{L}$

$$
\tilde{L}(t) = f(Y,L_E)
$$

### Deposition D

$$
D(t) = f(T,P,W,R,Q)
$$

- temperature T
- precipitation P
- weathering W
- erosion R
- transport Q

### Shoreline-trajectory X

$$
X(t) = f(L,D)
$$

****

## Simulation

### Premises

- Premise

$$
Y'(t) = 0 \\
$$

$$
L(t) = T(t) \\
$$

$$
T(t) = I(t) \\
$$

- Conclusion

$$
L(t) = I(t)
$$

$$
\tilde{L}(t) = L(t)
$$

$$
\tilde{L}(t) = I(t)
$$

### Signal

$$
L(t) = A_E sin(f_E t + φ_E) + A_θ sin(f_θ t + φ_θ) + A_ω sin(f_ω t + φ_ω)
$$

| | $o$ | $ε$ | $ψ$ | |
:-: |:-: | :-: | :-: | :-:
$T$ | $1.0 \cdot 10^5$ | $4.1 \cdot 10^4$ | $2.6 \cdot 10^4$ | $a$
$A$ | $0.2$ | $2.5$ | $1.5$ | -
$T_m$ | $5$ | $5$ | $5$ | $a$
$A_m$ | $0.5$ | $0.5$ | $0.5$ | -
$p$ | 0 | 0 | 0 | rad

### Sample

$$
D(t) = f(x)
$$

$$
f(x) = (a - 1) x^{-a}
$$

$$
a \in \{?\}
$$

- f(x) = probability density function
- x = sample spacing
- a = scaling exponent

### Sensitivity

- input
  - signal-shape
  - sample-distance

- output
  - fit

****

## Conclusion

### Analysis

?

### Synthesis

?

<!--
Αα (Alpha)
Ββ (Beta)
Γγ (Gamma)
Δδ (Delta)
Εε (Epsilon)
Ζζ (Zeta)
Ηη (Eta)
Θθ (Theta)
Ιι (Iota)
Κκ (Kappa)
Λλ (Lambda)
Μμ (Mu)
Νν (Nu)
Ξξ (Xi)
Οο (Omicron)
Ππ (Pi)
Ρρ (Rho)
Σσ/ς (Sigma)
Ττ (Tau)
Υυ (Upsilon)
Φφ (Phi)
Χχ (Chi)
Ψψ (Psi)
Ωω (Omega)
-->
