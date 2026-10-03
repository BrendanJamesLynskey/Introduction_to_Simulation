# Introduction to Simulation

**How engineers simulate, from field solvers to cloud systems**

*Six levels of simulation, the methods they share, and how to choose between them, with a link at every level into working simulators and decks on this GitHub*

```
Fields -> Circuits -> Logic -> Architecture -> Systems -> Software
```

Model  |  Solve  |  Measure  |  Validate

---

## Table of Contents

- [01 · Topics](#slide-01--topics)
- [02 · What a Simulation Is](#slide-02--what-a-simulation-is)
- [03 · The Levels at a Glance](#slide-03--the-levels-at-a-glance)
- **[Part I — The Levels](#part-i--the-levels)**
- [04 · Level 1: Physics and Numerical Methods](#slide-04--level-1-physics-and-numerical-methods)
- [05 · Field Solvers: FDTD, FEM and MoM](#slide-05--field-solvers-fdtd-fem-and-mom)
- [06 · CFD, TCAD and Multiphysics](#slide-06--cfd-tcad-and-multiphysics)
- [07 · Level 2: Circuits, and What SPICE Does](#slide-07--level-2-circuits-and-what-spice-does)
- [08 · Switching and Behavioural Models](#slide-08--switching-and-behavioural-models)
- [09 · Level 3: Digital Logic, Event-Driven and Cycle-Based](#slide-09--level-3-digital-logic-event-driven-and-cycle-based)
- [10 · Gate Level, Emulation and FPGA Prototypes](#slide-10--gate-level-emulation-and-fpga-prototypes)
- [11 · Level 4: Architecture, Analytical and Discrete-Event](#slide-11--level-4-architecture-analytical-and-discrete-event)
- [12 · Architecture: Transaction-Level and Cycle-Level](#slide-12--architecture-transaction-level-and-cycle-level)
- [13 · Level 5: System, Network and Cloud](#slide-13--level-5-system-network-and-cloud)
- [14 · Monte Carlo and Variance Reduction](#slide-14--monte-carlo-and-variance-reduction)
- [15 · Level 6: Software Virtual Platforms](#slide-15--level-6-software-virtual-platforms)
- [16 · One Accelerator, Every Level](#slide-16--one-accelerator-every-level)
- **[Part II — Cross-Cutting Methods](#part-ii--cross-cutting-methods)**
- [17 · Time-Stepping and Event-Driven](#slide-17--time-stepping-and-event-driven)
- [18 · Stiffness, Stability and Step Control](#slide-18--stiffness-stability-and-step-control)
- [19 · Interactive: One Circuit, Four Solvers](#slide-19--interactive-one-circuit-four-solvers)
- [20 · Deterministic and Stochastic](#slide-20--deterministic-and-stochastic)
- [21 · Co-Simulation and Hardware-in-the-Loop](#slide-21--co-simulation-and-hardware-in-the-loop)
- [22 · Digital Twins, Defined Carefully](#slide-22--digital-twins-defined-carefully)
- [23 · Verification, Validation and Calibration](#slide-23--verification-validation-and-calibration)
- [24 · Speed, Accuracy and Effort](#slide-24--speed-accuracy-and-effort)
- [25 · How to Choose a Level](#slide-25--how-to-choose-a-level)
- [26 · Takeaways](#slide-26--takeaways)
- [27 · Where to Go Next](#slide-27--where-to-go-next)

---

## Slide 01 — Topics

### Part I: the levels

- What a simulation is; the levels at a glance
- Level 1: physics and numerical methods (FEM, FDTD, MoM, CFD, TCAD)
- Level 2: circuits (SPICE, switching simulators, IBIS and IBIS-AMI)
- Level 3: digital logic (event-driven, cycle-based, gate level, emulation, FPGA prototypes)
- Level 4: architecture (analytical, discrete-event, transaction-level, cycle-level)
- Level 5: system, network and cloud (DES at scale, queueing, Monte Carlo)
- Level 6: software virtual platforms (ISS, QEMU, virtual prototypes)
- One accelerator, every level

### Part II: cross-cutting methods

- Time-stepping and event-driven
- Stiffness, stability and step control
- Interactive: one circuit, four solvers
- Deterministic and stochastic; seeds and [replications](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-warmup)
- Co-simulation and hardware-in-the-loop
- Digital twins, defined carefully
- Verification, validation and calibration
- Speed, accuracy and effort; how to choose a level

### How to read it

Each level stands on its own, then ends with an **On this GitHub** box that links the decks and code going deeper. Concepts the simulation series already explain link to their glossary entries in the [LLM Inference Simulators](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#glossary), [FHE Accelerator Simulators](https://brendanjameslynskey.github.io/FHE_Hub_Accelerator_Simulators/#glossary) and [Simulation Engineering Toolkit](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#glossary) hubs; the rest are explained on the slide.

---

## Slide 02 — What a Simulation Is

### A model, run forward

A simulation advances a model of a system through time, or across many parameter settings, to predict behaviour that you cannot measure, or would rather not. Every simulator has the same parts:

- **State**: node voltages, field values, register contents, queue lengths
- **Rules** for how the state changes: differential equations, logic, or event handlers
- **Inputs**: stimulus, a workload, random arrivals
- A **solver** or kernel that advances time
- **Observers** that turn the run into metrics

### Why simulate

- The thing does not exist yet: a chip is designed years before silicon ([InfSim 01, the pre-silicon problem](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-01))
- Testing it is too slow, costly or dangerous
- You cannot see inside it: the current in a via, the occupancy of a queue
- You want a thousand what-ifs, not one

### Four words that get confused

- **Analysis**: a closed-form or static answer with no time evolution: a DC operating point, a [roofline](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-roofline), static timing analysis
- **Simulation**: a model advanced through time or events in software
- **Emulation**: the design, or a functional equivalent, executing on other hardware: a hardware emulator running RTL, QEMU running another CPU's binaries
- **Prototype**: the real design in a different implementation, such as RTL on FPGAs

### Three questions every simulator answers

1. What is the state, and how much detail does it keep? (Part I)
2. How does time advance: fixed steps, adaptive steps, or events?
3. How do you know the answer is right: verification and validation?

Questions 2 and 3 are the same at every level, which is why Part II exists.

---

## Slide 03 — The Levels at a Glance

| Level | What is solved | How time advances | Unit of time · unit of data | Typical methods |
|---|---|---|---|---|
| 1 Physics | Partial differential equations over a mesh: Maxwell, Navier–Stokes, heat, drift–diffusion | Fixed steps (stability-limited), or one solve per frequency | fs to ms · mesh cells | FDTD, FEM, MoM, CFD, TCAD |
| 2 Circuit | Kirchhoff's laws plus device models: differential-algebraic equations | Adaptive implicit steps; breakpoints at source corners | ps to ms · node voltages | SPICE, switching (PWL) simulators, IBIS, IBIS-AMI |
| 3 Digital logic | Boolean or four-state logic, with or without delays | Events (signal changes) or one evaluation per clock | ps or cycles · signals | RTL and gate-level simulation, emulation, FPGA prototypes |
| 4 Architecture | Pipelines, caches, memories, interconnect, accelerators | Cycles, transactions or events; or no time at all | cycles to µs · transactions | [Roofline](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-roofline), discrete-event, SystemC TLM, cycle-level |
| 5 System | Requests, packets, jobs, agents, failures | Events; random sampling | µs to hours · requests | DES, queueing networks, network simulators, Monte Carlo, agent-based |
| 6 Software | Instructions on a modelled CPU with its peripherals | Instructions, in blocks or time quanta | instructions · architectural state | Instruction-set simulators, QEMU, virtual prototypes |

### Going up the table

Each level throws away detail that the level below keeps, and gains speed and reach in exchange: a field solver can afford nanoseconds of a connector; a system simulator can afford hours of a data centre. The hand-over between levels is a reduced model: S-parameters, a compact device model, a cycle count, a cost model.

### On this GitHub

- [InfSim 01: The Fidelity Ladder](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-03) zooms into levels 3–4 for chip design (glossary: [the fidelity ladder](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-fidelity))
- [InfSim 01: What Each Level Throws Away](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-04)

---

## Part I — The Levels

Six levels, from fields on a mesh to software on a modelled CPU. For each: what is solved, how time advances, the tools, speed and accuracy, what it is validated against, and where this GitHub goes deeper.

---

## Slide 04 — Level 1: Physics and Numerical Methods

### What is solved

Partial differential equations over space and time: Maxwell's equations (electromagnetics), Navier–Stokes (fluids), heat conduction, elasticity, Poisson plus drift–diffusion (semiconductors). Space is cut into a **mesh**, and the equations become a large system of algebraic ones:

- **Finite differences (FDM)**: derivatives replaced by differences on a structured grid. Simple and fast; awkward on curved geometry
- **Finite volumes (FVM)**: fluxes balanced cell by cell, so mass and energy are conserved exactly. The workhorse of CFD
- **Finite elements (FEM)**: the solution approximated by basis functions on elements of any shape; the weak form becomes a large sparse linear system. Fits any geometry; meshes refine where the field changes fast

### The mesh is part of the model

A result is credible only after a **refinement study**: shrink the cells until the quantity you care about stops changing, and use the trend (Richardson extrapolation) to estimate the error that remains. Mesh error, model error (the physics left out) and data error (material properties) are different things and need different checks.

### Speed, accuracy, validation

- 3-D problems take hours to days per run; 2-D cross-sections take seconds
- Accuracy is limited by geometry, material data and the mesh, rarely by arithmetic
- Validated against closed-form cases, published benchmark problems, and measurement: a vector network analyser, a wind tunnel, a thermocouple

### On this GitHub

- [Numerical Methods visualiser](https://brendanjameslynskey.github.io/Numerical_Methods/): Euler and RK4 ODE solvers, animated step by step
- [Differential Equations Explorer](https://brendanjameslynskey.github.io/Differential_Equations_Explorer/): wave and heat equations, Green's functions
- [Wilmott 14: the (S, t) grid, explicit, implicit and Crank–Nicolson](https://brendanjameslynskey.github.io/Wilmott_QF_14_Numerical_Methods/#slide-02): a PDE solved by finite differences
- Field solvers for signal integrity: next slide

---

## Slide 05 — Field Solvers: FDTD, FEM and MoM

### Three ways to solve Maxwell's equations

- **FDTD** (time domain): electric and magnetic fields on two interleaved grids (Yee, 1966), updated in a leapfrog. One pulse-excited run gives the whole frequency response. Explicit, so the step has a hard limit
- **FEM** (usually frequency domain): one sparse solve per frequency on a tetrahedral mesh that follows any 3-D shape: packages, connectors, antennas
- **MoM** (method of moments, integral equations): mesh only the conductor surfaces; dense matrices; suited to open radiating structures and layered (2.5-D) boards
- **Quasi-static 2-D solvers**: a cross-section gives per-unit-length L, C, R and G for a transmission line in seconds

### The CFL condition

```
Δt ≤ Δx / (c·√3)     (3-D Yee grid, cubic cells)
```

An explicit scheme is stable only if a wave crosses no more than about one cell per step (Courant, Friedrichs and Lewy, 1928). Small cells force small steps: halving the cell size in 3-D multiplies the work by 16.

### Worked estimate (illustrative)

0.1 mm cells in air give Δt ≤ 0.19 ps. Assume 10⁷ cells and 10⁸ cell updates per second on a multi-core CPU: each step takes 0.1 s, so one wall-clock second simulates about 1.9 &times; 10<sup>&minus;12</sup> s. A nanosecond of a connector takes about 9 minutes. Redo the arithmetic with your own assumptions.

### Tools and sources

Open source: [openEMS](https://www.openems.de/), [Meep](https://meep.readthedocs.io/) (FDTD), [Elmer](https://github.com/ElmerCSC/elmerfem) (FEM); commercial suites from the EDA and CAE vendors.

K. S. Yee, [IEEE Trans. Antennas Propag., 1966](https://doi.org/10.1109/TAP.1966.1138693) · R. Courant, K. Friedrichs, H. Lewy, [Math. Annalen, 1928](https://doi.org/10.1007/BF01448839)

### On this GitHub

- [Signal Integrity 01: Where Fifty Ohms Comes From](https://brendanjameslynskey.github.io/Signal_Integrity/01-transmission-lines/#slide-04) (interactive, from a field solve)
- [Signal Integrity 02: Checking the Profile Against a Field Solve](https://brendanjameslynskey.github.io/Signal_Integrity/02-return-paths/#slide-03)
- [fdm2d.py](https://github.com/BrendanJamesLynskey/Matrix_Articles/blob/main/si_models/fdm2d.py): the 2-D electrostatic solver behind the series (finite differences, red–black SOR)
- [Physical Audio companion, chapter 9](https://brendanjameslynskey.github.io/Companion_JOS_Physical_Audio_Signal_Processing/#ch9): FDTD on a vibrating membrane

---

## Slide 06 — CFD, TCAD and Multiphysics

### Computational fluid dynamics

Navier–Stokes solved by finite volumes. Turbulence is usually *modelled* (Reynolds-averaged or large-eddy models) rather than resolved, which only direct numerical simulation does, at enormous cost. Engineers use it for airflow through a server, cooling of a heat sink, aerodynamics. Validated against wind-tunnel and thermal-chamber measurements. Open source: [OpenFOAM](https://www.openfoam.com/).

### Technology CAD (TCAD)

**Process** simulation predicts the shapes and doping that implant, diffusion and etch steps leave behind. **Device** simulation solves Poisson's equation with drift–diffusion for electrons and holes on the device's mesh, giving I–V and C–V curves. Those curves are fitted by compact models, which are what SPICE uses. Commercial suites dominate; [DEVSIM](https://devsim.org/) is an open-source device simulator.

### Multiphysics

Real problems couple fields: current heats a conductor and heat raises its resistance (electro-thermal); temperature bends a package (thermo-mechanical); air carries heat away (fluid-thermal). Solvers couple either **monolithically** (one large system) or by **partitioning**, where each solver runs its own physics and they exchange boundary values, which is co-simulation (Part II).

### Where the levels hand over

- TCAD → compact device model → SPICE
- EM field solver → S-parameters → circuit and channel simulation
- CFD → thermal boundary conditions → power and reliability models

Each hand-over is a reduced-order model: the level above never sees the mesh, so the reduction must keep what it needs, such as causality and passivity for S-parameters.

### On this GitHub

- [Signal Integrity 03: What the Kramers–Kronig Test Says About Both](https://brendanjameslynskey.github.io/Signal_Integrity/03-materials-and-loss/#slide-09): material models that must stay causal
- [Matrix Methods: Passivity Is the Hard Part](https://brendanjameslynskey.github.io/Matrix_Methods_Network_Parameters/#slide-13)
- [Kramers–Kronig Relations](https://github.com/BrendanJamesLynskey/Kramers_Kronig_Relations): the causality constraint on every fitted model

---

## Slide 07 — Level 2: Circuits, and What SPICE Does

### Inside a SPICE transient run

- **Modified nodal analysis (MNA)**: the unknowns are node voltages plus the currents through voltage sources and inductors. Each element *stamps* a few entries into one sparse system (Ho, Ruehli and Brennan, 1975)
- **Newton–Raphson** for nonlinear devices: each iteration replaces every diode and transistor by its linearisation (a conductance and a current source), solves the sparse system by LU factorisation, and repeats until the voltages settle
- **Implicit integration**: backward Euler, trapezoidal or Gear (BDF) turns each capacitor and inductor into a similar companion model for the step
- **Timestep control**: the step is chosen from an estimate of the local truncation error, and forced to land on the corners of pulse and piecewise-linear sources (**breakpoints**). If Newton fails to converge, the step is cut and retried

```
[ G  B ; C  D ] · [ v ; i ] = [ i_s ; v_s ]     (the MNA system, re-solved every iteration)
```

Also: DC operating point (Newton, no time), AC small-signal (one complex solve per frequency), noise. The [interactive demo](#slide-19--interactive-one-circuit-four-solvers) is a one-node transient problem, solved four ways.

### Speed, accuracy, validation

- Accuracy is set by the **device models** (compact models fitted to silicon by the foundry) and by parasitics extracted from layout
- Thousands of transistors: nanoseconds to microseconds of circuit time per minute (indicative). Fast-SPICE tools partition and simplify to go larger
- Validated against silicon measurements and the foundry's process corners

### Tools

Open source: [ngspice](https://ngspice.sourceforge.io/), [Xyce](https://xyce.sandia.gov/). Commercial SPICE and fast-SPICE simulators from the EDA vendors, and free vendor-supplied SPICE tools for board-level power design.

L. W. Nagel, [SPICE2, UC Berkeley ERL M520, 1975](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1975/9602.html) · C.-W. Ho, A. Ruehli, P. Brennan, [IEEE Trans. Circuits Syst., 1975](https://doi.org/10.1109/TCS.1975.1084079)

### On this GitHub

- [DC-DC Control Techniques: References & Resources](https://brendanjameslynskey.github.io/DCDC_Control_Techniques/#/27) (vendor SPICE models and simulators)
- [Interview_Power_Supply_Design](https://github.com/BrendanJamesLynskey/Interview_Power_Supply_Design)

---

## Slide 08 — Switching and Behavioural Models

### Power converters break SPICE's budget

A buck converter switches every microsecond or so, a load-transient study needs milliseconds, and SPICE spends its steps on the edges. Two remedies:

- **Piecewise-linear (PWL) switching simulators**, in the style of SIMPLIS: each switch and device is a few linear segments, each linear topology is solved exactly between switching events, and the simulator only has to find when the next switching event happens. It can also search for the periodic steady state directly
- **Averaged models**: replace the switching by its average over a cycle, for loop design and stability

The event-driven solver in the [demo](#slide-19--interactive-one-circuit-four-solvers) uses the same idea on an RC circuit.

### Behavioural models

- **Verilog-A / Verilog-AMS**: equations describing a block, simulated inside a circuit simulator
- **IBIS**: an I/O buffer as I/V and V/t tables, so a board can be simulated without the vendor's transistor netlist
- **IBIS-AMI**: SerDes transmit and receive equalisation as executable algorithmic models that a channel simulator calls, statistically or bit by bit, to predict eyes and bit error ratios

### On this GitHub

- [DC-DC Control Techniques: Interactive Load Transient Response](https://brendanjameslynskey.github.io/DCDC_Control_Techniques/#/17) and [COT Timing](https://brendanjameslynskey.github.io/DCDC_Control_Techniques/#/14)
- [COT_DCDC_Simulink](https://github.com/BrendanJamesLynskey/COT_DCDC_Simulink): a constant on-time converter in MATLAB/Simulink
- [SerDes Equalisation: From S-Parameters to a Pulse Response](https://brendanjameslynskey.github.io/SerDes_Equalisation/#slide-05) and [the whole equaliser chain](https://brendanjameslynskey.github.io/SerDes_Equalisation/#slide-07)
- [Matrix Methods: Where This Shows Up](https://brendanjameslynskey.github.io/Matrix_Methods_Network_Parameters/#slide-18) (SPICE and IBIS-AMI macromodels)
- [Signal Integrity 17: What Is Implemented Here, and What Is Not](https://brendanjameslynskey.github.io/Signal_Integrity/17-com-and-compliance/#slide-02) (channel operating margin)

### Speed, accuracy, validation

- PWL: much faster than SPICE on converters (indicative), exact for its own PWL model; accuracy rests on how well the segments fit the devices
- IBIS: validated against the vendor's transistor-level simulation and lab measurements

### Sources

[IBIS Open Forum](https://ibis.org/) (IBIS and IBIS-AMI specifications) · [Verilog-AMS (Accellera)](https://www.accellera.org/downloads/standards/v-ams) · [SIMetrix/SIMPLIS](https://www.simetrix.co.uk/) (commercial PWL simulator; see its documentation)

---

## Slide 09 — Level 3: Digital Logic, Event-Driven and Cycle-Based

### Event-driven

Every signal change is an event in a **time wheel**; only logic that reads a changed signal is re-evaluated. Four-state values (0, 1, X, Z), arbitrary `#` delays and any testbench construct. Updates within one time step happen in ordered zero-time iterations: **delta cycles** in VHDL and SystemC ([glossary: the SystemC kernel and delta cycles](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-sckernel)), the active and non-blocking-assignment regions of a SystemVerilog time slot. Icarus Verilog, GHDL and the commercial simulators work this way.

### Cycle-based

Evaluate the whole design once per clock edge as compiled code. Assumes synchronous logic, usually two-state, no timing inside a cycle. [Verilator](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-verilator) compiles SystemVerilog into a C++ model this way; since version 5 it also accepts timing constructs (`--timing`). Fast regressions, weaker on X-propagation and testbench features.

### Measured: the same RTL in both

| Simulator | Style | Compile | Clock cycles per second |
|---|---|---|---|
| Icarus Verilog version 12.0 (stable) | event-driven, interpreted | 0.03 s | 6,416 |
| Verilator 5.020 | cycle-based, compiled C++ | 4.38 s | 837,883 |

Verilator ran **131×** more cycles per second and paid for it in compile time. Design: `ntt_core` from RTL_CoSim_NTT (50-bit words, N = 1024, 4 lanes), every output word checked against the golden NTT. Script and results: [demo/rtl_speed](demo/rtl_speed) (i7-3770). A small core: a large SoC runs orders of magnitude slower in both simulators, and the ratio varies with the design and the testbench.

### Speed, accuracy, validation

RTL simulation is exact for the logic, because it *is* the design. What it needs validating against is the specification: tests, assertions, coverage, and a golden model checking every output. Large SoCs simulate at tens to thousands of cycles per second (indicative).

[Icarus Verilog](https://steveicarus.github.io/iverilog/) · [Verilator guide](https://verilator.org/guide/latest/) · [GHDL](https://ghdl.github.io/ghdl/)

### On this GitHub

- [Free SystemVerilog Simulators: the support matrix](https://brendanjameslynskey.github.io/SystemVerilog_Simulators/#s4) (Icarus, Verilator, xsim, Questa Starter, slang)
- [SimEng 05: Verilator, Icarus and CI for RTL](https://brendanjameslynskey.github.io/SimEng_05_Verification_Bridge_cocotb/#slide-10)
- [RTL_CoSim_NTT](https://github.com/BrendanJamesLynskey/RTL_CoSim_NTT): the design timed above

---

## Slide 10 — Gate Level, Emulation and FPGA Prototypes

### Gate-level simulation

After synthesis, the design is a netlist of library cells. **SDF** (Standard Delay Format) back-annotation gives each cell and wire the delays computed by static timing analysis or extraction, and setup and hold checks fire during simulation. Used for reset and X-propagation, power-up sequences and checking timing constraints; far slower than RTL, so run sparingly. Timing sign-off itself is static timing analysis, not simulation.

### Hardware emulation

RTL compiled onto special-purpose hardware (processor-based or FPGA-based emulators). Around a megahertz, with full signal visibility: fast enough to boot an operating system and run real software before silicon, at a high price per seat.

### FPGA prototyping

The RTL on one or more FPGAs, partitioned when it does not fit. Tens of megahertz and real I/O, but little visibility and long compile times. Mostly for software teams and system validation.

### Orders of magnitude (indicative, large SoC)

| Platform | Design clock reached | An hour of simulation covers |
|---|---|---|
| RTL simulation | 10 Hz to 10 kHz | under a second of chip time |
| Gate level with SDF | slower than RTL | less than RTL does |
| Emulation | ~1 MHz | an OS boot |
| FPGA prototype | 10 to 100 MHz | real workloads, slowly |
| Silicon | GHz | everything, too late to change |

Rules of thumb from [InfSim 01's fidelity ladder](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-03); they vary hugely with design size and modelling style.

### On this GitHub

- [RISC-V SoC](https://github.com/BrendanJamesLynskey/RISCV_SoC) and its [5-stage RV32IMC core](https://github.com/BrendanJamesLynskey/RISCV_RV32IMC_5stage): RTL with self-checking testbenches
- [Transformer decoder RTL](https://github.com/BrendanJamesLynskey/LLM_Transformer_Decoder_RTL) and [AI matrix-multiply units](https://github.com/BrendanJamesLynskey/AI_MMUL_Unit) (SystemVerilog plus cocotb)
- [InfSim 01: Software-Level Simulators and RTL Simulation](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-06)
- [Interview_FPGA](https://github.com/BrendanJamesLynskey/Interview_FPGA): FPGA design and prototyping questions

---

## Slide 11 — Level 4: Architecture, Analytical and Discrete-Event

### Analytical models

Closed-form performance: the [roofline](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-roofline) (attainable throughput = the smaller of peak compute and bandwidth × arithmetic intensity), queueing formulas, a spreadsheet of FLOPs and bytes. Microseconds per answer, so whole design spaces can be swept; blind to contention, queueing and transients.

### Discrete-event simulation (DES)

The machine as components exchanging timed events (a kernel starts, a DMA finishes, a memory request returns), and the clock jumps from one event to the next. Contention and queueing emerge rather than being assumed. Each event's duration comes from a [cost model](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-costmodel). ([Glossary: discrete-event simulation](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-des).)

### Validated against

[Hardware counters](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-hwcounters) and timings on an existing chip, RTL cycle counts for new blocks, and published results; the gap is reported as a [calibration and correlation](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-correlation) figure, not hidden.

### Speed

Analytical: microseconds per design point. DES: about 10⁵ to 10⁷ events per second in a compiled kernel, fewer in Python (indicative; [InfSim 01](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-03)). The number of events, set by the abstraction, matters more than the language: see [InfSim 08: Fewer Events](https://brendanjameslynskey.github.io/InfSim_08_Accelerating_Simulators/#slide-03).

### On this GitHub

- [InfSim 03: Put a Batch on the Roofline](https://brendanjameslynskey.github.io/InfSim_03_LLM_Inference_Workloads/#slide-05) (interactive)
- [InfSim 02: A Kernel in 30 Lines](https://brendanjameslynskey.github.io/InfSim_02_Simulator_Development_Tutorial/#slide-02), then the whole tutorial
- [FHESim 03: The SimPy Engine](https://brendanjameslynskey.github.io/FHESim_03_Simulating_an_FHE_Accelerator/#slide-05) and its [live simulator](https://brendanjameslynskey.github.io/FHESim_03_Simulating_an_FHE_Accelerator/#slide-09)
- [FHE_Accelerator_Sim](https://github.com/BrendanJamesLynskey/FHE_Accelerator_Sim) and [Disaggregated_Inference_Sim](https://github.com/BrendanJamesLynskey/Disaggregated_Inference_Sim): two SimPy simulators with tests and bit-exact JavaScript ports
- [SimEng 05: Feeding the RTL Back Into the Simulator](https://brendanjameslynskey.github.io/SimEng_05_Verification_Bridge_cocotb/#slide-12)

---

## Slide 12 — Architecture: Transaction-Level and Cycle-Level

### Transaction-level modelling (SystemC TLM-2.0)

A bus transfer is a function call that carries a payload and an annotated delay, not a sequence of pin wiggles.

- [Loosely timed (LT)](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-ltstyle): each initiator runs ahead of global time by up to a [quantum](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-quantum) (temporal decoupling). Fast enough to boot an operating system
- [Approximately timed (AT)](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-atstyle): a four-phase protocol per transfer, so contention and pipelining are modelled; slower

### Cycle-level simulation

Pipelines, caches and queues updated every cycle, as in gem5's detailed CPU models or GPU simulators. About 10⁴ to 10⁶ cycles per second (indicative). More detail is not more accuracy unless it is calibrated against the real machine.

N. Binkert et al., [The gem5 simulator, 2011](https://doi.org/10.1145/2024716.2024718) · J. Lowe-Power et al., [The gem5 Simulator: Version 20.0+, 2020](https://arxiv.org/abs/2007.03152) · A. Akram, L. Sawalha, [A Survey of Computer Architecture Simulation Techniques and Tools, 2019](https://doi.org/10.1109/ACCESS.2019.2917698)

### Trace-driven or execution-driven

- **Trace-driven**: replay a recorded stream of instructions, memory accesses or kernels. Fast and repeatable, but the program cannot react when the timing changes
- **Execution-driven**: run the program on the model, so timing-dependent behaviour (spinning on a lock, adaptive batching) is captured. Slower
- **Sampling**: simulate representative intervals in detail and fast-forward the rest ([glossary: sampling, checkpoints and mode switching](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-sampling))

### On this GitHub

- [SimEng 03: The Quantum Trade-Off](https://brendanjameslynskey.github.io/SimEng_03_SystemC_TLM_Models/#slide-10) (interactive) and [SystemC_Accelerator_Model](https://github.com/BrendanJamesLynskey/SystemC_Accelerator_Model)
- [SimEng 04: Why "Bandwidth × Efficiency" Fails](https://brendanjameslynskey.github.io/SimEng_04_Memory_Systems_DRAM_HBM/#slide-01) and [Memory_System_Sim](https://github.com/BrendanJamesLynskey/Memory_System_Sim), a command-level DRAM model
- [InfSim 04: System, Network and Micro-Architecture Simulators](https://brendanjameslynskey.github.io/InfSim_04_Simulator_Landscape/#slide-05)
- [InfSim 08: Sampling, Checkpoints and Mode Switching](https://brendanjameslynskey.github.io/InfSim_08_Accelerating_Simulators/#slide-11)

---

## Slide 13 — Level 5: System, Network and Cloud

### DES at system scale

The events are now requests, batches, transfers and failures, across thousands of components and hours of traffic. Measured on this PC: [Disaggregated_Inference_Sim](https://github.com/BrendanJamesLynskey/Disaggregated_Inference_Sim) (SimPy) serves 3,000 LLM requests, 770.9 s of simulated time, with 90,766 events in 0.923 s: **835×** faster than real time, or 1,566× with its exact fast path. Script: [demo/des_speed](demo/des_speed).

### Queueing networks

Servers and queues with arrival and service distributions. Closed forms such as [Little's law](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-little) (L = λW) and the [M/M/1 queue](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-queueing) give instant answers for simple cases, and double as unit tests for a simulator: a correct DES must reproduce them.

### Network simulators and agent-based models

**Packet-level** simulators ([ns-3](https://www.nsnam.org/), [OMNeT++](https://omnetpp.org/)) model protocols and topologies packet by packet; flow-level models trade packet detail for speed. **Agent-based** models give many autonomous agents simple local rules (people, vehicles, traders) and let the aggregate behaviour emerge.

G. F. Riley, T. R. Henderson, [The ns-3 Network Simulator, 2010](https://doi.org/10.1007/978-3-642-12331-3_2) · C. M. Macal, M. J. North, [Tutorial on agent-based modelling and simulation, 2010](https://doi.org/10.1057/jos.2010.3)

### Speed, accuracy, validation

- Speed depends on events per simulated second: macro-stepping and coarser events buy orders of magnitude
- Accuracy rests on the workload model (arrival process, request mix) at least as much as on the component models
- Validated against production traces and against the queueing closed forms above

### On this GitHub

- [InfSim 05: Run the Simulator](https://brendanjameslynskey.github.io/InfSim_05_Disaggregated_Inference/#slide-06) (the same model, in the browser)
- [InfSim 02: A Queue, Checked Against Theory](https://brendanjameslynskey.github.io/InfSim_02_Simulator_Development_Tutorial/#slide-03)
- [Rust_DES_Kernel](https://github.com/BrendanJamesLynskey/Rust_DES_Kernel): a bit-exact Rust port of the serving simulator
- [InfSim 04: Serving-Level Simulators](https://brendanjameslynskey.github.io/InfSim_04_Simulator_Landscape/#slide-02)
- [Markov Chain Visualisation](https://brendanjameslynskey.github.io/Markov_Chain_Visualisation/): a stochastic model simulated step by step

---

## Slide 14 — Monte Carlo and Variance Reduction

### The method

Estimate an expectation by averaging random samples of the model. The standard error falls only as the square root of the number of samples, so each extra decimal digit costs a hundred times more runs.

```
standard error = σ / √N
```

Engineering uses: manufacturing yield under process variation (Monte Carlo SPICE), reliability and failure rates, risk and option prices, and the randomness inside every stochastic DES.

N. Metropolis, S. Ulam, [The Monte Carlo Method, JASA, 1949](https://doi.org/10.1080/01621459.1949.10483310)

### Variance reduction: shrink σ, not just grow N

- **Antithetic variates**: pair each random draw with its mirror image, so their errors partly cancel
- **Control variates**: subtract a correlated quantity whose mean is known exactly
- **[Common random numbers](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-crn)**: compare two designs on the same random stream, so the difference is not swamped by noise
- **Importance sampling**: draw more samples from the rare region that matters and reweight them. Essential for bit error ratios of 10⁻¹² or for failure probabilities
- **Quasi-Monte Carlo**: low-discrepancy points (Sobol, Halton) fill the space more evenly than random ones

### Reporting it

A Monte Carlo answer is an estimate with an error bar: report the [confidence interval](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-warmup) and the number of samples, and check that it shrinks as expected when N grows.

### On this GitHub

- [Wilmott 14: Monte Carlo Simulation](https://brendanjameslynskey.github.io/Wilmott_QF_14_Numerical_Methods/#slide-06), [antithetic and control variates](https://brendanjameslynskey.github.io/Wilmott_QF_14_Numerical_Methods/#slide-07), [low-discrepancy sequences](https://brendanjameslynskey.github.io/Wilmott_QF_14_Numerical_Methods/#slide-09)
- [Wilmott 09: barrier-option Monte Carlo](https://brendanjameslynskey.github.io/Wilmott_QF_09_Exotic_Options/#slide-10) (interactive)
- [InfSim 06: Replications, Confidence Intervals and Common Random Numbers](https://brendanjameslynskey.github.io/InfSim_06_Metrics_Hotspots_Validation/#slide-07) (interactive)
- [Random Walk Visualisation](https://github.com/BrendanJamesLynskey/Random_Walk_Visualisation) and [Central Limit Theorem](https://github.com/BrendanJamesLynskey/Central_Limit_Theorem)

---

## Slide 15 — Level 6: Software Virtual Platforms

### Instruction-set simulators (ISS)

Fetch, decode and execute one instruction at a time against modelled registers and memory. Simple, and exact at the level of the instruction set. [Spike](https://github.com/riscv-software-src/riscv-isa-sim), the RISC-V reference ISS, is used as the golden model when verifying processor RTL.

### Dynamic binary translation: QEMU

QEMU's code generator ([TCG](https://www.qemu.org/docs/master/devel/tcg.html)) translates each block of guest instructions into host code once and caches it. In the original paper, user-mode emulation was about 4× slower than native on integer code and 10× on floating point, with a further factor of 2 for the software MMU in full-system mode (QEMU 0.4.2; today's figures depend on the guest, host and workload).

F. Bellard, [QEMU, a Fast and Portable Dynamic Translator, USENIX 2005](https://www.usenix.org/legacy/event/usenix05/tech/freenix/full_papers/bellard/bellard.pdf)

### Virtual prototypes

A whole platform (CPUs, bus, memory map, peripherals) as fast functional models, often SystemC TLM loosely timed, so firmware, drivers and operating systems run before silicon. Register-accurate, not cycle-accurate: right for software bring-up, wrong for performance. Open source: [Renode](https://renode.io/); CPU vendors and EDA vendors sell their own.

### Speed, accuracy, validation

- Interpretive ISS: tens of millions of instructions per second at most; translated (QEMU) and LT platforms: hundreds of millions to billions (indicative)
- Functionally exact if the models are right; no timing to speak of
- Validated by running the same software on the platform and on silicon or an FPGA, and by architecture compliance test suites

### On this GitHub

- [RISC-V: Mini RISC-V Stepper](https://brendanjameslynskey.github.io/RISC_V/#/21), an instruction-set simulator in the browser, running Fibonacci
- [Interview_RISC_V: simulation with Spike and QEMU](https://github.com/BrendanJamesLynskey/Interview_RISC_V/blob/main/05_ecosystem/simulation_spike_qemu.md)
- [InfSim 01: Four Jobs a Simulator Does](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-02) (software bring-up is one)
- [SimEng 03: Loosely Timed, Temporal Decoupling and the Quantum](https://brendanjameslynskey.github.io/SimEng_03_SystemC_TLM_Models/#slide-07)

---

## Slide 16 — One Accelerator, Every Level

The FHE accelerator work on this GitHub models one design at five levels, and each level checks or feeds another. It is a compact example of how the levels work together on a real project.

| Level | Model | What it answers | Explained in |
|---|---|---|---|
| Analytical | Roofline and the NTT-, MAC-, memory- and power-bound tests | Which resource limits bootstrapping? | [FHESim 05: NTT-Bound Against Memory-Bound](https://brendanjameslynskey.github.io/FHESim_05_Results_and_Design_Space/#slide-03) |
| Discrete-event | [FHE_Accelerator_Sim](https://github.com/BrendanJamesLynskey/FHE_Accelerator_Sim) (SimPy, bit-exact JS port) | Latency, energy and hot-spots for a trace | [FHESim 03: The SimPy Engine](https://brendanjameslynskey.github.io/FHESim_03_Simulating_an_FHE_Accelerator/#slide-05) |
| Memory system | [Memory_System_Sim](https://github.com/BrendanJamesLynskey/Memory_System_Sim) (command-level DRAM/HBM) | Replaces "bandwidth × efficiency" | [SimEng 04: Plugging It Into the FHE Simulator](https://brendanjameslynskey.github.io/SimEng_04_Memory_Systems_DRAM_HBM/#slide-12) |
| Transaction-level | [SystemC_Accelerator_Model](https://github.com/BrendanJamesLynskey/SystemC_Accelerator_Model) (TLM-2.0, AT and LT) | Does a C++ model agree op by op? | [SimEng 03: Checked Against the SimPy Model](https://brendanjameslynskey.github.io/SimEng_03_SystemC_TLM_Models/#slide-09) |
| RTL | [RTL_CoSim_NTT](https://github.com/BrendanJamesLynskey/RTL_CoSim_NTT) (cocotb on [Verilator](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-verilator)) | Real NTT cycle counts | [SimEng 05: Feeding the RTL Back Into the Simulator](https://brendanjameslynskey.github.io/SimEng_05_Verification_Bridge_cocotb/#slide-12) |
| Area and cost | The calibrated area, yield and cost model | Is a design worth its silicon? | [SimEng 13: PPA Explorer](https://brendanjameslynskey.github.io/SimEng_13_PPA_Tradeoffs/#slide-09) ([glossary: PPA](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-ppa)) |

### The flows between levels

- RTL cycle counts calibrate the NTT throughput the DES assumes
- The DES's traces drive the SystemC model, which must agree with it
- The DRAM model replaces a fixed efficiency factor with scheduled commands

### A second thread: one SerDes link

Field solver ([Signal Integrity 01–04](https://brendanjameslynskey.github.io/Signal_Integrity/)) → S-parameters ([Matrix Methods](https://brendanjameslynskey.github.io/Matrix_Methods_Network_Parameters/)) → pulse response and equalisers ([SerDes Equalisation](https://brendanjameslynskey.github.io/SerDes_Equalisation/)) → a compliance verdict ([Signal Integrity 17](https://brendanjameslynskey.github.io/Signal_Integrity/17-com-and-compliance/)).

---

## Part II — Cross-Cutting Methods

The questions every level shares: how time advances, how the step is chosen, how randomness is handled, how simulators are joined together, how a model earns trust, and how to choose a level in the first place.

---

## Slide 17 — Time-Stepping and Event-Driven

*(Diagram: fixed steps, adaptive steps crowding at the input edges, and irregular events popped from an event queue.)*

### Time-stepping

For continuous state (voltages, fields, temperatures): advance by a step h and evaluate the derivatives. Fixed steps are simple and suit real-time use; adaptive steps follow the dynamics and save work where little happens.

### Event-driven

For state that changes only at instants (a packet arrives, a signal toggles): keep a priority queue of future events, pop the earliest, run its handler, which may schedule more. Simultaneous events need a [deterministic tie-break](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-tiebreak). ([Glossary: DES](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-des).)

### Hybrid

Continuous dynamics with discrete events (a switch opens, a thermostat fires): integrate, detect the zero crossing, locate it, then restart from it. SPICE breakpoints, switching simulators and FMI's event mode all do this.

### On this GitHub

- [InfSim 02: Step Through the Event List](https://brendanjameslynskey.github.io/InfSim_02_Simulator_Development_Tutorial/#slide-04) (interactive) · [SimEng 01: The Event List: BinaryHeap and Reverse](https://brendanjameslynskey.github.io/SimEng_01_Rust_for_Simulation_Engineers/#slide-02) · [SimEng 01: The Event Queue's Ordering Rule](https://brendanjameslynskey.github.io/SimEng_01_Rust_for_Simulation_Engineers/#slide-04) (interactive)

---

## Slide 18 — Stiffness, Stability and Step Control

### Explicit and implicit

- **Forward Euler** (explicit): v<sub>n+1</sub> = v<sub>n</sub> + h·f(t<sub>n</sub>, v<sub>n</sub>). Cheap per step, but on dv/dt = −v/τ each step multiplies the error by (1 − h/τ)
- **Backward Euler, trapezoidal, BDF** (implicit): f evaluated at the new point, so each step needs a solve (Newton, for a nonlinear circuit), but decaying modes stay stable for any h

```
|1 − h/τ| < 1  ⇔  0 < h < 2τ     (forward Euler on dv/dt = −v/τ)
```

### Stiffness

A system is stiff when it mixes very different time constants: picosecond parasitics with millisecond thermal drift, fast and slow chemistry. An explicit method's step is capped by the *fastest* mode even after that mode has died away; an implicit one can let the step follow the slow behaviour you care about. That is why SPICE integrates implicitly.

### Error control

**Embedded pairs** such as Dormand–Prince 5(4) compute two solutions of different order from the same stages; their difference estimates the local error, and the step grows or shrinks to keep it under a tolerance. The estimate assumes the solution is smooth. At a discontinuity (a square-wave edge, a switch closing) the solver rejects step after step until it has pinned the edge down, unless it is told where the edges are: **breakpoints**.

### Try it next

On the RC circuit of the next slide, forward Euler at h = 2.2τ ends 25.8 V off a 1 V signal; backward Euler at the same step stays within 0.708 V. Adaptive Dormand–Prince at a tolerance of 10⁻⁶ needs 2,660 evaluations and rejects 218 steps; told where the edges are, it needs 560 and its error falls from 2.4 &times; 10<sup>&minus;4</sup> V to 2.5 &times; 10<sup>&minus;7</sup> V.

J. R. Dormand, P. J. Prince, [A family of embedded Runge–Kutta formulae, 1980](https://doi.org/10.1016/0771-050X(80)90013-3) · E. Hairer, G. Wanner, [Solving Ordinary Differential Equations II: Stiff and Differential-Algebraic Problems](https://doi.org/10.1007/978-3-642-05221-7)

### On this GitHub

- [Numerical Methods visualiser](https://brendanjameslynskey.github.io/Numerical_Methods/): Euler against RK4, step by step
- [Wilmott 14: Explicit FD for the Black–Scholes PDE](https://brendanjameslynskey.github.io/Wilmott_QF_14_Numerical_Methods/#slide-04), where the explicit scheme's stability limit appears again

---

## Slide 19 — Interactive: One Circuit, Four Solvers

An RC low-pass filter (τ = RC = 1 ms) driven by a 0–1 V square wave of period 4τ, simulated for 20τ (10 edges). Error is the largest |v − v<sub>exact</sub>| at the solver's own time points. In the deck, sliders pick the fixed step h and the tolerance, and a plot shows the chosen solver against the exact answer. The reference implementation is [demo/rc_solvers.py](demo/rc_solvers.py); its full table is [demo/results.md](demo/results.md). Some rows:

| Method | Setting | Accepted steps | Rejected | RHS evaluations | Max error (V) |
|---|---|---|---|---|---|
| Forward Euler | h = 0.1 τ | 200 | 0 | 200 | 0.0192 |
| Forward Euler | h = 2.2 τ (unstable) | 10 | 0 | 10 | 25.8 |
| Backward Euler | h = 2.2 τ | 10 | 0 | 10 | 0.708 |
| Dormand–Prince 5(4) | tol = 1e-6 | 162 | 218 | 2,660 | 2.4 &times; 10<sup>&minus;4</sup> |
| D–P, edges as breakpoints | tol = 1e-6 | 71 | 9 | 560 | 2.5 &times; 10<sup>&minus;7</sup> |
| Event-driven (exact) | 10 edges | 10 | 0 | 10 | 5.6 &times; 10<sup>&minus;17</sup> |

Try: forward Euler at h = 2.2τ (unstable) against backward Euler at the same step (stable, but smeared); Dormand–Prince with and without breakpoints at the same tolerance; the event-driven solver, exact to rounding in 10 events, because the input is constant between edges, as in a piecewise-linear switching simulator.

---

## Slide 20 — Deterministic and Stochastic

### Deterministic models still need reproducibility

Same inputs, same outputs, on every run and every machine. That takes deliberate work: a fixed rule for simultaneous events, ordered floating-point reductions, no dependence on hash order or thread timing ([glossary: determinism, tie-breaking and RNG streams](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-determinism)). Ports to another language can even be [bit-exact](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-bitexact).

### Stochastic models

- Random arrivals, request sizes, failures, process variation
- Seed every random stream explicitly and record the seed; give each source its own stream, so changing one does not shift the others
- One run is one sample. Run independent [replications](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-warmup), discard the warm-up transient, and report a mean with a confidence interval; within one long run, use [batch means](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-batchmeans)

### Pitfalls

- Reporting a single run as the answer
- Confidence intervals computed from correlated observations, such as consecutive request latencies
- Comparing two designs on different random streams, so noise swamps the difference (use [common random numbers](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-crn))
- Tail percentiles: a p99 needs far more samples than a mean

### On this GitHub

- [InfSim 06: Statistics That Survive Review](https://brendanjameslynskey.github.io/InfSim_06_Metrics_Hotspots_Validation/#slide-06) and [its interactive](https://brendanjameslynskey.github.io/InfSim_06_Metrics_Hotspots_Validation/#slide-07)
- [SimEng 12: Statistics of Simulation Output](https://brendanjameslynskey.github.io/SimEng_12_Measurement_Tools_and_Methods/#slide-14)
- [InfSim 02: Time, Ordering and Determinism Pitfalls](https://brendanjameslynskey.github.io/InfSim_02_Simulator_Development_Tutorial/#slide-10)
- [SimEng 02: Reproducing Python's Random Numbers](https://brendanjameslynskey.github.io/SimEng_02_Rust_Python_PyO3/#slide-07) in Rust

---

## Slide 21 — Co-Simulation and Hardware-in-the-Loop

### Co-simulation and FMI

Two or more simulators, each with its own solver, exchange values at agreed communication points. The [Functional Mock-up Interface (FMI)](https://fmi-standard.org/) packages a model as an FMU: an XML description plus C code or binaries. In **model exchange** the host integrates the FMU's equations; in **co-simulation** the FMU brings its own solver, and a master algorithm steps every FMU and passes signals between them at each macro step. The step size trades accuracy and stability against speed.

T. Blochwitz et al., [The Functional Mockup Interface for Tool independent Exchange of Simulation Models, Modelica 2011](https://doi.org/10.3384/ecp11063105)

### Mixed-signal and HW/SW

- **Mixed-signal**: a time-stepping analogue solver and an event-driven digital kernel, synchronised at the boundary signals; real-number models of the analogue blocks speed it up
- **Hardware and software**: Python drives RTL through [cocotb](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-cocotb) while a [golden model](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-goldenmodel) checks outputs; or compiled RTL sits inside a C++ or SystemC platform ([glossary: co-simulation](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-cosim))

### Hardware-in-the-loop (HIL)

The controller under test is real hardware (an engine control unit, a motor drive's controller board), wired to a **real-time** simulation of the plant it controls. The simulator must finish every step before its deadline, so plant models are simplified until they do. The cheaper stages come first: model-in-the-loop, software-in-the-loop (the controller code on a PC), processor-in-the-loop (on the target processor).

### On this GitHub

- [SimEng 05: cocotb in One Page](https://brendanjameslynskey.github.io/SimEng_05_Verification_Bridge_cocotb/#slide-03) and [Two Golden Models and a Scoreboard](https://brendanjameslynskey.github.io/SimEng_05_Verification_Bridge_cocotb/#slide-04)
- [InfSim 01: Co-Simulation in Practice](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-08)
- [RTL_CoSim_NTT](https://github.com/BrendanJamesLynskey/RTL_CoSim_NTT): Python golden model against RTL
- [Control Theory explorer](https://brendanjameslynskey.github.io/Control_Theory/): a controller and plant simulated in a loop

---

## Slide 22 — Digital Twins, Defined Carefully

### A definition worth using

> "A digital twin is a set of virtual information constructs that mimics the structure, context, and behavior of a natural, engineered, or social system (or system-of-systems), is dynamically updated with data from its physical twin, has a predictive capability, and informs decisions that realize value. The bidirectional interaction between the virtual and the physical is central to the digital twin."

US National Academies, [Foundational Research Gaps and Future Directions for Digital Twins](https://doi.org/10.17226/26894) (2024), adapting a 2020 AIAA definition

### Model, monitor or twin?

| What you have | Live data | Predicts | Feeds decisions back | Call it |
|---|---|---|---|---|
| A CAD or simulation model | no | yes | no | a model |
| A dashboard of sensor data | yes | no | maybe | monitoring |
| A model kept in step with live data | yes | yes | no | sometimes a "digital shadow" |
| All of these, with decisions acted on | yes | yes | yes | a digital twin |

### What a real twin needs

- A model fast enough to keep up with the asset: usually a reduced-order model from the levels in Part I
- Continual calibration from data (data assimilation), with its uncertainty quantified
- Verification and validation of the whole loop, not just the model

The term is used loosely in marketing: ask which of the four properties actually hold. Nothing on this GitHub is a twin in this strict sense; the nearest ingredient is calibration, such as [calibrating a simulator against OpenFHE](https://brendanjameslynskey.github.io/FHE_Hub_Accelerator_Simulators/#g-calibration).

---

## Slide 23 — Verification, Validation and Calibration

### Three different questions

- **Verification**: did we build the model right? The code matches the intended model: unit tests, analytic cases, convergence studies, [differential testing](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-differential) against an independent implementation
- **Validation**: did we build the right model? Its output matches the real system to the accuracy the decision needs, over the range of conditions it will be used for
- **Calibration**: tuning parameters until the model matches data. Calibrate on one data set and validate on another, or the validation proves nothing

R. G. Sargent, [Verification and validation of simulation models, J. Simulation, 2013](https://doi.org/10.1057/jos.2012.20)

### Model credibility

- State the intended use and the domain the model covers
- Document assumptions and what each level leaves out
- Report validation results with the conditions they cover, and their uncertainty
- Keep [golden runs](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-golden) in CI, so a change that moves an answer is noticed

### A ladder of evidence

1. Closed-form cases the model must reproduce
2. Convergence as the mesh or step is refined
3. Agreement with another simulator
4. Agreement with measurement, out of sample

([Glossary: the verification ladder](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-ladder).)

### On this GitHub

- [InfSim 06: The Verification Ladder](https://brendanjameslynskey.github.io/InfSim_06_Metrics_Hotspots_Validation/#slide-08)
- [SimEng 09: The V-Model](https://brendanjameslynskey.github.io/SimEng_09_Specs_Requirements_Test_Plans/#slide-07) ([glossary](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-vmodel))
- [SimEng 12: Agreement as a Measurement](https://brendanjameslynskey.github.io/SimEng_12_Measurement_Tools_and_Methods/#slide-15)
- [FHESim 02: Checked Against a Real OpenFHE Bootstrap](https://brendanjameslynskey.github.io/FHESim_02_Anatomy_of_Bootstrapping/#slide-12)
- [Signal Integrity 16: What Correlation Honestly Means](https://brendanjameslynskey.github.io/Signal_Integrity/16-measurement-and-correlation/#slide-09)
- [Signal Integrity 01: Checking the Model Against a Published Example](https://brendanjameslynskey.github.io/Signal_Integrity/01-transmission-lines/#slide-11)

---

## Slide 24 — Speed, Accuracy and Effort

*(Chart: simulated seconds per wall-clock second, log scale, one row per method from most physical detail to least; indicative bands, one cited band, one worked estimate, and measured points.)*

| Method | Level | Simulated s per wall s | Basis |
|---|---|---|---|
| 3-D full-wave EM (FDTD) | 1 | about 1.9 &times; 10<sup>&minus;12</sup> | worked estimate (slide 05) |
| SPICE, transistor level | 2 | 10⁻¹⁰ to 10⁻⁶ | indicative |
| Gate level + SDF timing | 3 | 10⁻¹⁰ to 10⁻⁷ | indicative |
| RTL simulation | 3 | 10⁻⁸ to 10⁻⁵ | indicative (large SoC at 1 GHz); measured on a small core: Icarus 6,416 and Verilator 837,883 cycles/s |
| Cycle-level architecture | 4 | 10⁻⁵ to 10⁻³ | indicative |
| Hardware emulation | 3 | about 10⁻³ | indicative |
| FPGA prototype | 3 | 10⁻² to 10⁻¹ | indicative |
| TLM virtual platform (LT) | 4/6 | 10⁻² to 10⁻¹ | indicative |
| QEMU dynamic translation | 6 | 1/20 to 1/4 | cited: Bellard (2005) |
| System DES (LLM serving) | 5 | 10 to 10⁴ | indicative; measured: 835 and 1,566 |
| Analytical models | 4/5 | 10⁴ to 10⁹ | indicative |

### Reading it

Rows run from most physical detail (top) to least. Bands are orders of magnitude and each spans decades, because model size matters as much as the level. Indicative bands follow [InfSim 01's ladder](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-03) (large SoC, 1 GHz); QEMU is from Bellard (2005); FDTD is the worked estimate on the field-solver slide.

### Measured here

Icarus and [Verilator](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-verilator) on a small NTT core sit at and beyond the fast end of the RTL band, because the core is small; the SimPy serving simulator runs 835× to 1,566× faster than real time. Scripts in [demo/](demo/).

### Effort

Detail costs model-building time and calibration data: a [roofline](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-roofline) takes an afternoon; a validated cycle-level or meshed 3-D model takes weeks; RTL arrives late. The trade-off is named in [SimEng 13: The Other Trade-offs](https://brendanjameslynskey.github.io/SimEng_13_PPA_Tradeoffs/#slide-12); feel the spread in [InfSim 01's calculator](https://brendanjameslynskey.github.io/InfSim_01_Why_Simulate/#slide-05).

---

## Slide 25 — How to Choose a Level

### Questions to ask first

1. Which decision will the answer change, and how accurate must it be to change it?
2. What is the smallest unit of time and data that affects the answer?
3. How much simulated time, or how many samples, do you need? A p99 needs hours of traffic; a reflection needs nanoseconds
4. What can you calibrate and validate against?
5. When do you need it, and who will maintain it?

### The rule of thumb

Use the highest level that can answer the question, and drop to a lower level only for the part that needs it, through a hand-over model or co-simulation. Detail you cannot calibrate is not accuracy.

| Question | Level and method | Why |
|---|---|---|
| Impedance of a new board stack-up | 1: 2-D field solver | Geometry and materials set it |
| Eye opening at 28 GBd through a backplane | 1–2: S-parameters, then channel simulation with IBIS-AMI | Nanoseconds of waveform; statistical BER |
| Will the converter ring on a load step? | 2: averaged model, then PWL switching simulation | Milliseconds of switching |
| Does the RTL meet its specification? | 3: RTL simulation against a golden model | Exact logic; regressions in a compiled simulator |
| How big should the on-chip SRAM be? | 4: analytical sweep, then DES | Hundreds of design points |
| p99 time-to-first-token under bursty traffic | 5: system DES with [replications](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-warmup) | Hours of traffic, many seeds |
| Will the driver boot before silicon? | 6: virtual platform | Billions of instructions, no timing |
| Yield of a large die under process variation | Analytical yield model, then Monte Carlo | Closed forms, then the variation |

Worked versions: [InfSim 04: Which Question, Which Level?](https://brendanjameslynskey.github.io/InfSim_04_Simulator_Landscape/#slide-01) · [Build or Reuse?](https://brendanjameslynskey.github.io/InfSim_04_Simulator_Landscape/#slide-08) · [SimEng 13: Dies per Wafer and Yield](https://brendanjameslynskey.github.io/SimEng_13_PPA_Tradeoffs/#slide-06)

---

## Slide 26 — Takeaways

### What to remember

- Six levels, from fields on a mesh to software on a modelled CPU; each trades detail for speed and reach, and hands a reduced model to the level above
- Two ways to advance time: steps for continuous state, events for discrete changes; real simulators mix them
- Explicit methods are limited by stability (CFL, h < 2τ); implicit methods by the cost of a solve per step. Stiff problems need implicit methods
- Adaptive steps need help at discontinuities: breakpoints, or event-driven segments
- Stochastic answers need seeds, [replications and confidence intervals](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/#g-warmup); deterministic ones need reproducibility
- Verification, validation and calibration are different jobs, and calibration data must not double as validation data
- Choose the highest level that answers the question

### Next steps

1. Run the four-solver demo until the stability limit and the breakpoint effect are obvious
2. Build a discrete-event kernel in 30 lines: [InfSim 02](https://brendanjameslynskey.github.io/InfSim_02_Simulator_Development_Tutorial/)
3. Time Icarus against [Verilator](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/#g-verilator) on a design of your own with [demo/rtl_speed](demo/rtl_speed)
4. Pick a level you rarely use and read its "On this GitHub" links

### Further reading

Law, *Simulation Modeling and Analysis* (discrete-event) · Hairer & Wanner, *Solving ODEs II* (stiff problems) · Taflove & Hagness, *Computational Electrodynamics: The FDTD Method* · Sargent (2013) on V&V · the reading lists in [InfSim 10](https://brendanjameslynskey.github.io/InfSim_10_Further_Learning/)

---

## Slide 27 — Where to Go Next

| Level | Start here | Then |
|---|---|---|
| 1 Physics | [Signal Integrity series](https://brendanjameslynskey.github.io/Signal_Integrity/) (17 decks; computed by a field solver) | [Matrix Methods in Network Parameters](https://brendanjameslynskey.github.io/Matrix_Methods_Network_Parameters/) · [Matrix Articles models](https://github.com/BrendanJamesLynskey/Matrix_Articles) · [Numerical Methods](https://brendanjameslynskey.github.io/Numerical_Methods/) |
| 2 Circuit | [DC-DC Control Techniques](https://brendanjameslynskey.github.io/DCDC_Control_Techniques/) | [SerDes Equalisation](https://brendanjameslynskey.github.io/SerDes_Equalisation/) · [Matrix Concepts in Digital Filters](https://brendanjameslynskey.github.io/Matrix_Concepts_Digital_Filters/) |
| 3 Digital logic | [Free SystemVerilog Simulators](https://brendanjameslynskey.github.io/SystemVerilog_Simulators/) | [SimEng 05: verification bridge](https://brendanjameslynskey.github.io/SimEng_05_Verification_Bridge_cocotb/) · [RTL_CoSim_NTT](https://github.com/BrendanJamesLynskey/RTL_CoSim_NTT) · [Hardware index](https://github.com/BrendanJamesLynskey/Hardware) (RTL repos) |
| 4 Architecture | [LLM Inference Simulators](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/) (InfSim 01–11) | [FHE Accelerator Simulators](https://brendanjameslynskey.github.io/FHE_Hub_Accelerator_Simulators/) · [SimEng 03: SystemC TLM](https://brendanjameslynskey.github.io/SimEng_03_SystemC_TLM_Models/) · [SimEng 04: memory systems](https://brendanjameslynskey.github.io/SimEng_04_Memory_Systems_DRAM_HBM/) · [SimEng 13: PPA](https://brendanjameslynskey.github.io/SimEng_13_PPA_Tradeoffs/) |
| 5 System | [InfSim 05: Disaggregated Inference](https://brendanjameslynskey.github.io/InfSim_05_Disaggregated_Inference/) | [InfSim 06: metrics and validation](https://brendanjameslynskey.github.io/InfSim_06_Metrics_Hotspots_Validation/) · [Wilmott 14: Monte Carlo](https://brendanjameslynskey.github.io/Wilmott_QF_14_Numerical_Methods/) · [Markov chains](https://brendanjameslynskey.github.io/Markov_Chain_Visualisation/) |
| 6 Software | [RISC-V deck](https://brendanjameslynskey.github.io/RISC_V/) (instruction stepper) | [Interview_RISC_V](https://github.com/BrendanJamesLynskey/Interview_RISC_V) · [Cortex-M series](https://brendanjameslynskey.github.io/Cortex_M/) |
| Engineering a simulator | [Simulation Engineering Toolkit](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/) (13 decks) | Rust and PyO3 ports, testing, Jenkins, specifications, performance analysis, measurement tools |

### The three simulation series

[LLM Inference Simulators](https://brendanjameslynskey.github.io/LLM_Hub_Inference_Simulators/) (why and how to simulate inference hardware) · [FHE Accelerator Simulators](https://brendanjameslynskey.github.io/FHE_Hub_Accelerator_Simulators/) (one accelerator, end to end) · [Simulation Engineering Toolkit](https://brendanjameslynskey.github.io/SimEng_Hub_Toolkit/) (the engineering around a simulator). Each hub has a glossary linking every concept to the slides that explain it.

### Indexes

[Hardware](https://github.com/BrendanJamesLynskey/Hardware) · [Software](https://github.com/BrendanJamesLynskey/Software) · [Mathematics](https://github.com/BrendanJamesLynskey/Mathematics)
