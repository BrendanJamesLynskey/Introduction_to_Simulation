# 🧮 Introduction to Simulation

An interactive Reveal.js presentation on simulation as engineers practise it, from field solvers to cloud systems: why engineers simulate (and when they should not), six levels (physics, circuits, digital logic, architecture, systems, software virtual platforms), the methods they share (time-stepping and events, stiffness and step control, randomness, co-simulation, digital twins, verification and validation), and how to choose a level. Every level ends with links into the decks and simulators on this GitHub that go deeper.

## ▶ [Open the Presentation](https://brendanjameslynskey.github.io/Introduction_to_Simulation/)

## 📄 [Markdown Version](presentation.md)

---

## Contents

| # | Part | Topic | Description |
|---|------|-------|-------------|
| 01 | | Title | Fields → circuits → logic → architecture → systems → software |
| 02 | | Topics | The two parts at a glance; how the links work |
| 03 | | What a Simulation Is | State, rules, inputs, solver, observers; analysis vs simulation vs emulation vs prototype |
| 04 | | Why Simulate? | Eight motivations, each with an example from the deck; the payoff in cost, schedule and risk |
| 05 | | Motivation, Level and Tool | For each motivation: the usual levels, typical tools, and where this GitHub goes deeper |
| 06 | | When Simulation Is the Wrong Tool | When an analytical answer, a measurement or a prototype is the better choice |
| 07 | | The Levels at a Glance | Six levels: what is solved, how time advances, units, methods |
| 08 | I | Part I: The Levels | Divider |
| 09 | I | Level 1: Physics and Numerical Methods | FDM, FVM, FEM; meshing and refinement studies |
| 10 | I | Field Solvers: FDTD, FEM and MoM | Yee grid, the CFL condition, a worked FDTD cost estimate; the SI series' field solver |
| 11 | I | CFD, TCAD and Multiphysics | Turbulence models, process and device simulation, coupled fields, hand-over models |
| 12 | I | Level 2: Circuits, and What SPICE Does | MNA, Newton–Raphson, implicit integration, timestep control and breakpoints |
| 13 | I | Switching and Behavioural Models | PWL (SIMPLIS-style) and averaged models; Verilog-A, IBIS, IBIS-AMI |
| 14 | I | Level 3: Digital Logic, Event-Driven and Cycle-Based | Delta cycles; Icarus against [Verilator](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-verilator), measured on the same RTL (131×) |
| 15 | I | Gate Level, Emulation and FPGA Prototypes | SDF back-annotation; orders of magnitude in speed |
| 16 | I | Level 4: Architecture, Analytical and Discrete-Event | [Roofline](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-roofline), DES, cost models, correlation |
| 17 | I | Architecture: Transaction-Level and Cycle-Level | SystemC TLM (LT/AT, quantum), gem5-class models, trace- vs execution-driven, sampling |
| 18 | I | Level 5: System, Network and Cloud | DES at scale (a SimPy serving simulator, measured), queueing, ns-3-class and agent-based models |
| 19 | I | Monte Carlo and Variance Reduction | σ/√N; antithetic, control variates, [common random numbers](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-crn), importance sampling, quasi-MC |
| 20 | I | Level 6: Software Virtual Platforms | Instruction-set simulators, QEMU's dynamic translation, virtual prototypes |
| 21 | I | One Accelerator, Every Level | The FHE accelerator modelled at five levels on this GitHub; a SerDes thread |
| 22 | II | Part II: Cross-Cutting Methods | Divider |
| 23 | II | Time-Stepping and Event-Driven | Fixed and adaptive steps, event queues, hybrid systems; SVG diagram |
| 24 | II | Stiffness, Stability and Step Control | Explicit vs implicit, h < 2τ, embedded error estimates, breakpoints |
| 25 | II | Interactive: One Circuit, Four Solvers | An RC circuit by forward Euler, backward Euler, adaptive Dormand–Prince (with and without breakpoints) and an event-driven exact solver |
| 26 | II | Deterministic and Stochastic | Reproducibility, seeds and streams, [replications, confidence intervals](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-warmup), [batch means](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-batchmeans) |
| 27 | II | Co-Simulation and Hardware-in-the-Loop | FMI/FMU, mixed-signal, cocotb and golden models, HIL |
| 28 | II | Digital Twins, Defined Carefully | The National Academies definition; model vs monitor vs twin |
| 29 | II | Verification, Validation and Calibration | Three questions, model credibility, a ladder of evidence |
| 30 | II | Speed, Accuracy and Effort | Every level on one log-scale chart of simulated seconds per wall-clock second |
| 31 | II | How to Choose a Level | Questions to ask, and a decision table |
| 32 | II | Takeaways | Summary and next steps |
| 33 | II | Where to Go Next | Every series on this GitHub, by level |

---

## Demo code and measurements

[`demo/`](demo/) holds the code behind the interactive slide and every measured number in the deck. Each script writes a `results.json` and a `results.md`; `index.html` and `presentation.md` were rendered from those files, not typed.

| Path | What it does | Result |
|------|--------------|--------|
| [`demo/rc_solvers.py`](demo/rc_solvers.py) | The four-solver RC demo in Python; the slide's JavaScript is a line-for-line port, checked against [`results.json`](demo/results.json) for all 37 settings in a headless browser | [`demo/results.md`](demo/results.md) |
| [`demo/rtl_speed/`](demo/rtl_speed/) | Times `ntt_core` from [RTL_CoSim_NTT](https://github.com/BrendanJamesLynskey/RTL_CoSim_NTT) in Icarus Verilog and Verilator; the testbench checks every output word against the golden NTT | Icarus 6,416, Verilator 837,883 clock cycles per second ([results](demo/rtl_speed/results.md)) |
| [`demo/des_speed/`](demo/des_speed/) | Times [Disaggregated_Inference_Sim](https://github.com/BrendanJamesLynskey/Disaggregated_Inference_Sim) serving 3,000 requests, counting SimPy events | 835× real time, 1,566× with the exact fast path ([results](demo/des_speed/results.md)) |

All measurements were taken on one Intel i7-3770 PC; expect different absolute numbers elsewhere.

**Illustrative, not measured:** the speed bands on the "Speed, Accuracy and Effort" chart are orders of magnitude (rules of thumb from [InfSim 01](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-03), labelled indicative), apart from the QEMU band (cited from Bellard, 2005) and the FDTD band (a worked estimate whose assumptions are on the field-solver slide). Speed statements marked "indicative" on the slides are likewise rules of thumb.

---

## Slide Controls

| Action | Key |
|--------|-----|
| Next / Previous | `→` `←` or swipe |
| Overview | `Esc` |
| Fullscreen | `F` |
| Export to PDF | Append `?print-pdf` to URL, then print |

## Technology

[Reveal.js 4.6](https://revealjs.com) · [highlight.js](https://highlightjs.org) · Bricolage Grotesque + Instrument Sans + Geist Mono

Single self-contained `index.html` (the demo is plain JavaScript inside it) — no build step, no npm, no dependencies to install.

## See also

- [LLM Inference Simulators](https://github.com/BrendanJamesLynskey/LLM_Hub_Inference_Simulators) — the chip-design fidelity ladder in depth, a SimPy simulator tutorial, and LLM serving simulation (InfSim 01 links back here).
- [FHE Accelerator Simulators](https://github.com/BrendanJamesLynskey/FHE_Hub_Accelerator_Simulators) — one accelerator taken from workload to design-space results.
- [Simulation Engineering Toolkit](https://github.com/BrendanJamesLynskey/SimEng_Hub_Toolkit) — the engineering around a simulator: Rust and SystemC models, verification, CI, specifications, measurement, PPA.
- [Signal Integrity](https://github.com/BrendanJamesLynskey/Signal_Integrity) — seventeen decks computed by a 2-D field solver and circuit models.
- [SystemVerilog_Simulators](https://github.com/BrendanJamesLynskey/SystemVerilog_Simulators) — what actually runs in the free RTL simulators.
- [DCDC_Control_Techniques](https://github.com/BrendanJamesLynskey/DCDC_Control_Techniques) — the power converters whose simulation the circuit slides discuss.
- [Interview_Simulation](https://github.com/BrendanJamesLynskey/Interview_Simulation) — interview questions with worked answers, tested coding challenges and quizzes on simulation and performance modelling; its answers link back to these slides.
- Indexes: [Hardware](https://github.com/BrendanJamesLynskey/Hardware) · [Software](https://github.com/BrendanJamesLynskey/Software) · [Mathematics](https://github.com/BrendanJamesLynskey/Mathematics).

## References

K. S. Yee, [*IEEE Trans. Antennas Propag.* 14(3), 1966](https://doi.org/10.1109/TAP.1966.1138693) · R. Courant, K. Friedrichs, H. Lewy, [*Math. Annalen* 100, 1928](https://doi.org/10.1007/BF01448839) · L. W. Nagel, [SPICE2, UC Berkeley ERL M520, 1975](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1975/9602.html) · C.-W. Ho, A. Ruehli, P. Brennan, [The modified nodal approach to network analysis, 1975](https://doi.org/10.1109/TCS.1975.1084079) · J. R. Dormand, P. J. Prince, [A family of embedded Runge–Kutta formulae, 1980](https://doi.org/10.1016/0771-050X%2880%2990013-3) · E. Hairer, G. Wanner, [*Solving Ordinary Differential Equations II*](https://doi.org/10.1007/978-3-642-05221-7) · N. Binkert et al., [The gem5 simulator, 2011](https://doi.org/10.1145/2024716.2024718) · J. Lowe-Power et al., [The gem5 Simulator: Version 20.0+](https://arxiv.org/abs/2007.03152) · A. Akram, L. Sawalha, [A Survey of Computer Architecture Simulation Techniques and Tools, 2019](https://doi.org/10.1109/ACCESS.2019.2917698) · G. F. Riley, T. R. Henderson, [The ns-3 Network Simulator, 2010](https://doi.org/10.1007/978-3-642-12331-3_2) · C. M. Macal, M. J. North, [Tutorial on agent-based modelling and simulation, 2010](https://doi.org/10.1057/jos.2010.3) · N. Metropolis, S. Ulam, [The Monte Carlo Method, 1949](https://doi.org/10.1080/01621459.1949.10483310) · F. Bellard, [QEMU, a Fast and Portable Dynamic Translator, 2005](https://www.usenix.org/legacy/event/usenix05/tech/freenix/full_papers/bellard/bellard.pdf) · T. Blochwitz et al., [The Functional Mockup Interface, 2011](https://doi.org/10.3384/ecp11063105) · R. G. Sargent, [Verification and validation of simulation models, 2013](https://doi.org/10.1057/jos.2012.20) · National Academies, [Foundational Research Gaps and Future Directions for Digital Twins, 2024](https://doi.org/10.17226/26894) · NIST, [The Economic Impacts of Inadequate Infrastructure for Software Testing, Planning Report 02-3, 2002](https://www.nist.gov/system/files/documents/director/planning/report02-3.pdf) · NASA, [NASA-STD-7009, Standard for Models and Simulations](https://standards.nasa.gov/standard/NASA/NASA-STD-7009)

## License

Educational use. Code examples provided as-is.
