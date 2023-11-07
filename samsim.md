# Sensitivity of shoreline-trajectory to deposition-events

## Accuracy of inferred signal as function of signal-shape and sample-rate

### Implications for Sequence-Stratigraphy

***

## Summary

Sequo-Strat (Sequence Stratigraphy) is a method that has many applications, the essence of which seems to be: (1) correlate depo-units (deposition units) to depo-units and (2) correlate depo-units to sea-level. These build respectively on following premises: (1) depo-units are laterally continuous and (2) depo-units are sufficiently frequent. For the sake of simplicity, this work focuses solely on the sensitivity of sample-rate on reliability of inferred sea-level from depo-events. It shall consist of three parts: (1) Sea-level signal mimics insolation-curve over $1Ma$; (2) Samples are taken randomly in a wide range ($1-1000$); (3) Ratio of inferred cycles / original cycles is used as measure of fit. This is done for default set of parameter values for insolation, i.e. Period $T$, Amplitude $A$, Period-Modulator $T_m$, Amplitude-Modulator $A_m$, Phase $p$ for Eccentricity $s_E$, Obliquity $s_θ$, Precession $s_ω$: insolation $s$ ($T_E=100ka$, $T_θ=41ka$, $T_ω=26ka$, $A_E=2$, $A_θ=25$, $A_ω=15$, $T_m=5T$, $A_m=1/2A$, $p=0$). The curve of fit (linear scale) against sample-rate (logarithmic scale) matches a logistic curve. The simulation is then performed for all combinations of parameter values within their range. These results provide a spread around the logistic-curve for default values. Samples represent clusters of depo-events. The results do not simulate real processes, they treat the essence of the matter in a conceptual manner. The question is now: if one were to transfer these findings to natural depo-systems, how would they affect the use of Sequo-Strat?

***

## Key words

delta, depo-event, deposition-event, eustatic sea-level, sample, sequence-stratigraphy, sequo-strat, shoreline-trajectory, signal, tectonic subsidence

***

## Introduction

In order to infer signal from samples in general or sea-level from shoreline-trajectory in special one must: (1) Know the shape of the signal and (2) Take sufficient samples from it. This seems quite an ambitious goal for the case of sea-level and depo-events. And it seems to be the exact opposite of what one does in Sequo-Strat, since one infers sea-level from shoreline-trajectory, implicitly assuming that all conditions have been met to reliably do so. Should it not be a requirement to use the method only if all those conditions have explicitly been verified? It is outside the scope of this work to evaluate them all, but for the sake of introduction to the context one shall briefly discuss them. The questions that should always be asked are: (1) Is sea-level curve known? (2) Are depo-events sufficiently frequent?

Relative sea-level can be considered the result of an interplay of three main factors: (1) Tectonic Subsidence, (2) Eustatic Sea-Level, (3) Supply-Rate at the delta-apex. In order to know relative sea-level one must know all three composing factors. Is it safe to assume any of those to be constant and therefore relative sea-level to be governed by only one? Consider a deltaic depo-system, that deposits at the shoreline and therefore records shoreline position. Connect those shorelines and obtain shoreline-trajectory. Is it safe to assume depo-events to be sufficiently frequent and shoreline-trajectory to follow relative sea-level so its shape to be direct reflection of sea-level?

### Tectonic Subsidence Y

Tectonic Subsidence can be considered the result of interplay of four main mechanisms. Their manifestation varies substantially in magnitude and time-scale. Isostatic rebound is notable, because it occurs as result of heating or cooling, but also as result of loading or unloading, both of which occur even on passive margins, particularly where deltaic depo-systems deposit significant amounts of sediment.

$$
Y(t) = f(R,M,σ,q)
$$

- isostasic rebound $R$
- bending moment $M$
- intraplate stress $σ$
- heatflux $q$

### Insolation I

Insolation can be considered the result of interplay of three sine waves, all three related to changes in orbital behaviour of earth around sun. Because their amplitudes vary and because they are not harmonics, the result is an irregular signal, very much different from a single sine wave as is often depicted on Sequo-Strat schematics. To infer such irregular signal from samples requires much more samples than for a single sine wave.

$$
I(t) = f(E,θ,ω)
$$

- eccentricity $E$
- obliquity $θ$
- precession $ω$

### Absolute Sea-level $L$

Absolute Sea-Level fluctuation can be considered to be caused by insolation fluctuations: insolation affects global temperature, which in turn affects global sea-level. But between cause and effect is a long chain of mechanisms. Therefore absolute sea-level can be considered the result of an interplay of all these mechanisms. Is it safe to assume absolute sea-level to mimic the insolation curve? Given the number of mechanisms in that chain, is it safe to assume they would cause no such effects as attenuation, filtering or smoothing?

$$
L(t) = f(T,Ω,Q,P,E)
$$

- temperature $T$
- polar ice $Ω$
- polar transport $Q$
- continent precipitation $P$
- ocean evaporation $E$

### Relative Sea-Level $\tilde{L}$

Relative Sea-Level can be considered the result of an interplay of two factors.

$$
\tilde{L}(t) = f(Y,L_E)
$$

### Deposition D

Deposition can be considered on two spatially distinct scales: (1) Regional Supply-Rate; (2) Local Supply-Rate. First can be considered the result of an interplay of external (allogenic) factors. Second can be considered the result of an interplay of external (allogenic) and internal (autogenic) factors.

#### Regional Supply-Rate

Regional Supply-Rate fluctuations can be considered to be caused by insolation fluctuations: insolation affects global temperature, which in turn affects regional supply-rate. But between cause and effect is a long chain of mechanisms. Therefore regional supply-rate can be considered the result of an interplay of all these mechanisms. Is it safe to assume regional supply-rate to be continuous or at least clusters of depo-events to be sufficiently frequent to adequately sample sea-level curve? Is it safe to assume they would cause no non-linear behaviour of any kind? Is it safe to assume supply-rate to delta-apex to be continuous or at least linearly correlated to global temperature?

$$
D(t) = f(T,P,W,R,Q)
$$

- temperature $T$
- precipitation $P$
- weathering $W$
- erosion $R$
- transport $Q$

#### Local Supply-Rate

Local Supply-Rate fluctuations can be considered to be caused by a host of factors and mechanisms, all of which are very specific to the area and subject to temporal and spatial variation. Deposition and Erosion happen by way of instantaneous events seen on geological time-scale. It is therefore obvious that deposition is not continuous, neither spatially nor temporally. The question is rather how depo-events are spread over space and time. Is it safe to assume them to be equally and densely distributed over time? Or are they more likely to occur in clusters? And should we consider those clusters as samples?

$$
D(t) = f(S,E,D)
$$

- Lobe-Switching $S$
- Erosion $E$
- Deposition $D$

### Shoreline-trajectory X

Shoreline-Trajectory can be considered to mimic Relative Sea-Level-Curve, but only if depo-events (or clusters of depo-events) are sufficiently frequent. But even if they would be, is it safe to assume them to be mirror-images? Even under steady sea-level and constant deposition, shoreline moves out horizontally. One can depict this graphically by using lateral position from delta-apex together with angle-of-climb of subsequent shoreline positions. Maybe one should rather focus on number of cycles in both signals rather than on exact shape.

$$
X(t) = f(L,D)
$$

***

## Simulation

This work shall only focus on the most elementary yet essential of all factors on signal inference, that of sample-rate. The input shall be composite sine wave of three sine waves. The variable shall be sample-rate. The metric shall be number of cycles in original and inferred signal. The immediate goal is to determine sensitivity of signal-inference to sample-rate. Rationale behind this choice is that whatever the shape of the sea-level curve, be it similar to or different from insolation-curve, sample-rate is essential to infer the signal adequately.

### Premises

Premises for this work are in the form of simplifications: (1) Tectonic Subsidence is steady, (2) Absolute Sea-Level mimics Global Temparature, (3) Global Temperature mimics Insolation.

$$
Y'(t) = 0
$$

$$
L(t) = T(t)
$$

$$
T(t) = I(t)
$$

Under those simplifications the following conditions occur: (1) Global Sea-Level mimics Insolation, (2) Relative Sea-Level mimics Global Sea-Level, (3) Relative Sea-Level mimics Insolation.

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

The input-signal is that of Insolation (fig. 1), which is a composite sine-wave of three sine-waves: (1) Eccentricity, (2) Obliquity, (3) Precession. Duration of signal for all simulations is $1Ma$.

$$
L(t) = A_E sin(f_E t + φ_E) + A_θ sin(f_θ t + φ_θ) + A_ω sin(f_ω t + φ_ω)
$$

- Period $T$
- Amplitude $A$
- Period modulator $T_m$
- Amplitude modulator $A_m$
- phase $p$

#### Constant Parameters

Default values for parameters are given in following table. Period is in years, amplitude has no dimension, phase is in radians. These are used for the default-scenario, where sample-rate is the only independent variable (fig. 3).

Table 1. Default paramater values

| | $E$ | $θ$ | $ω$ | |
| :-: |:-: | :-: | :-: | :-: |
| $T$ | $1.0 \cdot 10^5$ | $4.1 \cdot 10^4$ | $2.6 \cdot 10^4$ | $a$ |
| $A$ | $0.2$ | $2.5$ | $1.5$ | - |
| $T_m$ | $5 \cdot T_E$ | $5 \cdot T_θ$ | $5 \cdot T_ω$ | $a$ |
| $A_m$ | $0.5$ | $0.5$ | $0.5$ | - |
| $p$ | 0 | 0 | 0 | rad |

#### Variable Parameters

Ranges of parameter values are given in following table. These are used for all other scenarios, where parameter values are varied within their range (fig. 4).

Table 2. Parameter ranges.

| | $min$ | $max$ | $step$ | |
| :-: |:-: | :-: | :-: | :-: |
| $T$ | $2^2$ | $2^4$ | $1$ | $10^4a$ |
| $A$ | $0$ | $25$ | $5$ | - |
| $T_m$ | $2^0$ | $2^2$ | $1$ | $10^5a$ |
| $A_m$ | $0$ | $12$ | $2.5$ | - |
| $p$ | $2^{-3}$ | $2^{-1}$ | 1 | $π$ |

### Sample

Sample-rate is given as number of samples over duration of signal. A complete run for default scenario consists of following steps: (1) run simulation for constant set of parameter values and constant sample-rate; (2) repeat 10 times; (3) increase sample rate. For the runs with variable parameter these are performed for all permutations of parameter values. Samples are taken at random moments over time. These samples are then evenly distributed over time. This has no effect on number of cycles, but is meant to represent real practice between two known time-lines. Original samples and shifted samples are plotted (fig. 2).

$$
D(t) = f(U)
$$

$$
U \in \{1 \cdot 10^1,1 \cdot 10^3\}/10^5a
$$

- Sample-Rate $U$

### Sensitivity

Plots depict fit against sample-rate. Fit is ratio of number of cycles in sample-signal over number of cycles in original signal.

$$
F = N_D / N_L
$$

***

## Conclusion

### Analysis

Fit against sample-rate on a log-linear scale matches a logistic function (fig. 3). Therefore sample-rate directly determines how many cycles of original signal are captured by sampling. Variations in signal-parameters only cause a spread around the default-scenario (fig. 4). These curves give clear numbers on how many samples are required for specific fit. Fit for 60 samples is only 1/2, fit for 120 samples is 3/4.

### Synthesis

This work addresses the essential element of the signal-inference problem: how many samples are required to capture the signal adequately? For the case of a known single sine-wave with known regular sampling the answer is quite different from that of an unknown signal with unknown irregular sampling. For use of Sequo-Strat it seems that the former is implicitly adopted, whereas the latter should explicitly be adopted. Relative Sea-Level is unknown and is unlikely to mimic Insolation. Tectonic Subsidence is unlikely to be constant. Depo-Events are unlikely to be regular and sufficiently frequent to capture sea-level fluctuations. These factors require careful scrutiny and any study performing correlation of any kind, be it in space-domain or time-domain, should explicitly address all simplifications or assumptions taken and attempt to assess their implications.

***

### Code

The code for this work is written in Jupyter/Python and is available on GitHub (<https://github.com/danmikes/samsim>). Feel free to use and modify it. Maybe this could lead to a collective effort to quantify relevant parameters and assess accuracy of spatial and temporal correlation in depo-systems.

***

### Figure

<!-- ![Insolation](fig1.png) -->
Figure 1. Insolation curve for default parameter values. Red = Eccentricity. Green = Obliquity. Yellow = Precession. Cyan = Insolation.

<!-- ![Simulation](fig2.png) -->
Figure 2. Simulation for default parameter values and sample-rate = 65. Cyan = Insolation. Magenta = Samples. Yellow = Evenly distributed samples.

<!-- ![Constant](fig3.png) -->
Figure 3. Simulation = Simulation for default parameter values and sample-rate = 65. Simulations = Simulation for range of sample-rates and logistic-function matching results. Parameters = Simulation for range of sample-rates and range of Amplitude-values with matching logistic-curve. Lower-Right gives values. Logistic = max, dip, flex for logistic-fit of simulations with default parameter values. Simulation shows minimum, average, maximum sample-rate and fit for simulation with default parameter values. Variable shows minimum, average, maximum sample-rate and fit for simulation with varying amplitude.

<!-- ![Variable](fig4.png) -->
Figure 4. Results for variable parameters (tab.2) with matching logistic-function results. For the ranges chosen Period and Amplitude have most effect, Period modulator and Amplitude modulator have intermediate effect and phase has least effect. Default plot shows results for simulation with default parameter values.
