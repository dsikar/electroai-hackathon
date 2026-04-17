# Schematic Conversion Report (claude-sonnet-4-6)

- **Source image:** `/home/daniel/git/electroai-hackathon/baseline-solution/data/schematics/images/15-triac-timer.png`
- **Model:** `claude-sonnet-4-6`
- **Circuit name:** Touch/Push-ON Latching AC Load Controller with Triac
- **Falstad URL:** https://www.falstad.com/circuit/circuitjs.html#eNp1ks1OhDAQx-99iknwoIcl01I-zq7eDCHGF6hQd0lQCGXd6NM7U1rcTZTQzPCb4T-daW9AAqbITw4SU4WQ0ws6g9zupBQJ7M1k2n7pPy1M49nO4E7TNHyJGTLUUKE3skBAEkAUbeSaVsVYpcruSnIw1aKLnA3_pkDWGrEU3xtiq7QPKXHeCsQwEospHGOLIS-yTDE7bD5bqkIsgebkjvB6WpbxA8xHB4NZ2iM874Xz8nH5vSO8mcFZ6jag0BxVV35s1C_X9J3odaEfqfR7imIxh1n0t8EFdt1PAvf7XJdQN_W_s142kBVVDMAO04K3oDiJ50KxP7TzEpq6Ie2rseOFeAS51t5Kf1sKLrCJc-z6cBJ4enzwgz2YxcJsXe-WcaZCXkevetlvoWED3hbr3KM4fxcqcBJ_mXvTwu372NnBdmAcuHNPB3hH-ZxXXaaviGuWGA6H9sF-dYFCKwEHEb497PKt8ZYzfwAZY6bF

## Summary

This circuit is a latching AC mains load controller triggered by a momentary push button. A BC547 NPN transistor is used as a latch driver, biased through a 2M2 resistor and a 1000uF capacitor that holds the base charge after the button is released. The BC547 drives a BC557 PNP transistor which in turn triggers a BT36 Triac via an LED optocoupler-style gate drive (1K resistor + LED to Triac gate), switching an AC mains load. The 1N4007 diode and 12V Zener with 0.22uF/400V capacitor form a simple capacitive power supply to derive low-voltage DC from the 220V AC mains for the control circuit.

## Components

| Reference | Type | Value | Connections |
|-----------|------|-------|-------------|
| SW1 | Pushbutton (momentary NO) | PUSH TO ON | pin1, pin2 |
| R1 | Resistor | 1K | pin1, pin2 |
| R2 | Resistor | 2M2 | pin1, pin2 |
| C1 | Electrolytic Capacitor | 1000uF | positive, negative |
| Q1 | NPN BJT | BC547 | base, collector, emitter |
| R3 | Resistor | 1K | pin1, pin2 |
| Q2 | PNP BJT | BC557 | base, collector, emitter |
| D1 | Rectifier Diode | 1N4007 | anode, cathode |
| ZD1 | Zener Diode | 12V | cathode, anode |
| C2 | Capacitor (X-rated / film) | 0.22uF/400V | pin1, pin2 |
| LED1 | LED | Red LED | anode, cathode |
| R4 | Resistor | 1K | pin1, pin2 |
| TRIAC1 | Triac | BT36 | MT1, MT2, gate |
| LOAD1 | AC Load | LOAD (unspecified) | pin1, pin2 |

## Assumptions

- The 2M2 resistor connects the push button output to BC547 base to provide a slow charge path for C1 (1000uF), creating a latch effect.
- The 1K resistor (R1) labeled near top-left connects VCC_DC to BC547 base as pull-up or initial drive.
- BC547 collector connects to BC557 base through R3 (1K) — when BC547 is ON it pulls BC557 base low, turning ON the PNP BC557.
- The LED and 1K resistor in series drive the Triac gate directly (no opto-isolator IC visible — LED may serve as visual indicator and gate current limiter).
- The capacitive power supply (C2=0.22uF/400V, D1=1N4007, ZD1=12V zener) provides approximately 12V DC rail (VCC_DC) referenced to AC neutral/GND.
- GND in the low-voltage section is tied to AC neutral (floating mains — as warned in schematic).
- The push button connects between VCC_DC rail and the 2M2/C1 node to charge capacitor when pressed.
- BT36 Triac gate current flows from MT1 through gate via R4 and LED1 from BC557 collector.
- The 1K resistor near BC547 base (top-left) is a base current limiting resistor from VCC to base.
- DC supply voltage assumed to be 12V based on Zener voltage.

## Missing Information

- Exact wiring of the push button — which terminal connects to VCC and which to the 2M2 resistor is not fully clear.
- Whether LED1 is purely a status indicator or forms part of an opto-triac drive (no opto IC part number visible).
- The exact nature of the LOAD (resistive, inductive, power rating).
- No current limiting resistor visible between D1 cathode and Zener — possible omission or it is implied by C2 reactance.
- The connection point of R4 bottom terminal to Triac gate vs MT1 is ambiguous.
- BC547 collector connection path to BC557 base is not explicitly traced with net labels.
- Whether the 1K top-left resistor connects to BC547 base or collector.

## Inconsistencies

- The circuit warning states 'Floating Mains AC' — the low-voltage DC ground is referenced to mains AC neutral, making the entire control circuit live and dangerous without isolation.
- The LED appears to directly interface with the Triac gate without an opto-isolator, meaning the gate drive circuit is also at mains potential — this is consistent with the floating mains warning but is a safety concern.
- A 0.22uF/400V capacitor used as a current-limiting dropper with only a 1N4007 diode and 12V Zener may not supply sufficient current for reliable Triac latching depending on load.
- The latch mechanism using only 1000uF capacitor and 2M2 resistor may have variable hold time depending on supply voltage and leakage.

## Validation

- Components in analysis absent from LTSpice netlist: C1, C2, D1, LED1, LOAD1, Q1, Q2, R1, R2, R3, R4, SW1, TRIAC1, ZD1
