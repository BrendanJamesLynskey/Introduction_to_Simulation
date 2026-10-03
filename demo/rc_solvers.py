#!/usr/bin/env python3
"""Reference implementation of the deck's interactive demo: one RC low-pass filter driven by a
square wave, solved four ways. The JavaScript on the "Interactive: One Circuit, Four Solvers"
slide is a line-for-line port; the browser check compares its readouts with results.json.

    dv/dt = (u(t) - v) / tau,   v(0) = 0,   u(t) = 1 V for the first half of each period, else 0

Times are in units of tau = RC (1 ms on the slide). The square wave has period PERIOD and the
run lasts T_END. Methods:

  fe    forward Euler, fixed step h            (explicit: unstable for h > 2 tau)
  be    backward Euler, fixed step h           (implicit: stable for any h, but damped)
  rk45  Dormand-Prince 5(4), adaptive steps    (finds each edge by rejecting steps)
  event exact solution between switching events (piecewise-exponential, like a
        piecewise-linear switching simulator: one "step" per edge)

    python3 rc_solvers.py            # writes results.json and results.md next to this file
"""

import json
import math
from pathlib import Path

TAU = 1.0
PERIOD = 4.0
HALF = PERIOD / 2
T_END = 5 * PERIOD


def u(t):
    return 1.0 if (t % PERIOD) < HALF else 0.0


def u_left(t):
    """The input just before t: the value held over a step that ends at t (edges are breakpoints)."""
    ph = t % PERIOD
    if ph == 0:
        return 1.0 if t == 0 else 0.0
    return 1.0 if ph <= HALF else 0.0


def exact(t):
    """Closed form: v relaxes towards u(t) between edges, v_k at each edge t_k = k * HALF."""
    k = min(int(t / HALF), int(T_END / HALF) - 1)
    v = 0.0
    decay = math.exp(-HALF / TAU)
    for i in range(k):
        ui = 1.0 if i % 2 == 0 else 0.0
        v = ui + (v - ui) * decay
    uk = 1.0 if k % 2 == 0 else 0.0
    return uk + (v - uk) * math.exp(-(t - k * HALF) / TAU)


def f(t, v):
    return (u(t) - v) / TAU


def fixed(method, h):
    ts, vs = [0.0], [0.0]
    n = 0
    t, v = 0.0, 0.0
    evals = 0
    while t < T_END:
        n += 1
        t1 = min(n * h, T_END)
        dt = t1 - t
        if method == "fe":
            v = v + dt * f(t, v)
        else:  # backward Euler: f(t1, v1) with the input held over the step; linear in v1, so solved exactly
            v = (v + dt * u_left(t1) / TAU) / (1 + dt / TAU)
        evals += 1
        t = t1
        ts.append(t)
        vs.append(v)
    return dict(ts=ts, vs=vs, steps=n, rejected=0, evals=evals)


# Dormand-Prince 5(4) tableau
C = [0, 1 / 5, 3 / 10, 4 / 5, 8 / 9, 1, 1]
A = [[],
     [1 / 5],
     [3 / 40, 9 / 40],
     [44 / 45, -56 / 15, 32 / 9],
     [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729],
     [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656],
     [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84]]
B5 = [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0]
B4 = [5179 / 57600, 0, 7571 / 16695, 393 / 640, -92097 / 339200, 187 / 2100, 1 / 40]


def rk45(tol, breakpoints=False):
    """Adaptive Dormand-Prince. With breakpoints, no step crosses an edge and the input is held
    at its value for the step (what a circuit simulator does at a PULSE source's corners)."""
    ts, vs = [0.0], [0.0]
    t, v, h = 0.0, 0.0, 0.1
    steps = rejected = evals = 0
    while t < T_END:
        h = min(h, T_END - t)
        t1 = t + h
        if breakpoints:
            nxt = (math.floor(t / HALF) + 1) * HALF   # t is always snapped onto an edge it reaches
            if nxt <= t1:
                h, t1 = nxt - t, nxt
            uh = u(t)
        k = []
        for i in range(7):
            vi = v
            for j in range(i):
                vi = vi + h * A[i][j] * k[j]
            k.append((uh - vi) / TAU if breakpoints else f(t + C[i] * h, vi))
        evals += 7
        v5 = v
        v4 = v
        for i in range(7):
            v5 = v5 + h * B5[i] * k[i]
            v4 = v4 + h * B4[i] * k[i]
        scale = tol + tol * max(abs(v), abs(v5))
        err = abs(v5 - v4) / scale
        if err <= 1.0:
            t = t1
            v = v5
            steps += 1
            ts.append(t)
            vs.append(v)
        else:
            rejected += 1
        fac = 5.0 if err == 0 else min(5.0, max(0.2, 0.9 * err ** -0.2))
        h = h * fac
    return dict(ts=ts, vs=vs, steps=steps, rejected=rejected, evals=evals)


def event():
    ts, vs = [0.0], [0.0]
    v = 0.0
    decay = math.exp(-HALF / TAU)
    n = int(T_END / HALF)
    for i in range(n):
        ui = 1.0 if i % 2 == 0 else 0.0
        v = ui + (v - ui) * decay
        ts.append((i + 1) * HALF)
        vs.append(v)
    return dict(ts=ts, vs=vs, steps=n, rejected=0, evals=n)


def max_error(r):
    return max(abs(v - exact(t)) for t, v in zip(r["ts"], r["vs"]))


def run(method, x=None):
    r = (fixed(method, x) if method in ("fe", "be") else rk45(x) if method == "rk45" else
         rk45(x, breakpoints=True) if method == "rk45bp" else event())
    return dict(method=method, param=x, steps=r["steps"], rejected=r["rejected"], evals=r["evals"],
                max_error=max_error(r))


H_LIST = (0.05, 0.1, 0.2, 0.25, 0.5, 1.0, 1.5, 1.9, 2.0, 2.2, 2.5)   # the slide's step slider
TOL_LIST = (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8)                 # the slide's tolerance slider
CASES = ([("fe", h) for h in H_LIST] + [("be", h) for h in H_LIST] +
         [("rk45", tol) for tol in TOL_LIST] + [("rk45bp", tol) for tol in TOL_LIST] + [("event", None)])

NAMES = {"fe": "Forward Euler", "be": "Backward Euler", "rk45": "Dormand–Prince 5(4)", "rk45bp": "Dormand–Prince 5(4), edges as breakpoints", "event": "Event-driven (exact)"}

if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    rows = [run(m, x) for m, x in CASES]
    (here / "results.json").write_text(json.dumps(rows, indent=1) + "\n")
    out = ["# RC demo: reference results", "",
           "Generated by `python3 rc_solvers.py`. RC low-pass, tau = 1, square wave of period 4 tau",
           "(0 to 1 V), 20 tau simulated (10 edges). Errors are the largest |v - v_exact| at the solver's own",
           "time points. The deck's JavaScript reproduces every row (checked in the browser).", "",
           "| Method | Step h / tol | Accepted steps | Rejected | RHS evaluations | Max error (V) |",
           "|---|---|---|---|---|---|"]
    for r in rows:
        p = "" if r["param"] is None else (f"h = {r['param']:g} tau" if r["method"] in ("fe", "be") else f"tol = {r['param']:.0e}")
        out.append(f"| {NAMES[r['method']]} | {p} | {r['steps']} | {r['rejected']} | {r['evals']} | {r['max_error']:.3g} |")
    (here / "results.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
