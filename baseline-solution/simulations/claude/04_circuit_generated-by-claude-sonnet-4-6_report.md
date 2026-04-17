# Schematic Conversion Report (claude-sonnet-4-6)

- **Source image:** `/home/daniel/git/electroai-hackathon/baseline-solution/images/04_circuit.png`
- **Model:** `claude-sonnet-4-6`
- **Circuit name:** Voltage Doubler / Clamper-Rectifier Circuit
- **Falstad URL:** https://www.falstad.com/circuit/circuitjs.html#eNpdTkkOwzAIvOcVHHqthbHB4TlVkp4qVaq6fL-Q4KSqt5FnhoETZMCEvhgyJkKk1gqOJKoNGIHXZznnPLxBBQpWBztotWKPaGrIQq0aZTvxMAHhuLpLWLcmOfS5Cw6eSDAv18vr9jykOqLDoUydcvCi_9QHcFtLHTZDdn34xMQxVBDu2J1GRXpkONOn2xv-cNoL7yAg3quiqjX0odi-ZLd8AUhFQ_w

## Summary

This circuit is an AC voltage doubler using a clamper stage followed by a peak detector. In the first half-cycle, D1 conducts and charges C1 to the peak AC voltage, clamping the waveform. In the second half-cycle, D2 conducts and the clamped voltage (approximately 2× peak) charges C2, which filters the output across load RL. The resulting DC output voltage Vo is approximately twice the peak AC input voltage.

## Components

| Reference | Type | Value | Connections |
|-----------|------|-------|-------------|
| V1 | AC Voltage Source | assumed 120V RMS, 60Hz | positive, negative |
| C1 | Capacitor | assumed 10uF | pin1, pin2 |
| D1 | Diode | assumed 1N4007 | anode, cathode |
| D2 | Diode | assumed 1N4007 | anode, cathode |
| C2 | Capacitor | assumed 10uF | pin1, pin2 |
| RL | Resistor (Load) | assumed 10kohm | pin1, pin2 |

## Assumptions

- AC source assumed to be 120V RMS at 60Hz (values not labeled in schematic)
- C1 capacitance assumed to be 10uF (value not shown)
- C2 capacitance assumed to be 10uF (value not shown)
- D1 and D2 assumed to be standard rectifier diodes 1N4007
- RL load resistance assumed to be 10kohm (value not shown)
- Ground reference is taken at node B (bottom rail)
- D1 anode is connected to B (bottom rail) and cathode to node_mid based on diode orientation shown pointing upward

## Missing Information

- AC source voltage and frequency not labeled
- C1 capacitance value not shown
- C2 capacitance value not shown
- RL load resistance value not shown
- Diode part numbers not specified
- Output voltage polarity marker Vo is shown but no numerical value given

## Inconsistencies

- D1 orientation in schematic shows cathode pointing upward toward node_mid and anode toward bottom rail B — this is consistent with a negative clamper; however, the resulting output Vo would be positive, which is consistent with the arrow direction shown for Vo
- No explicit ground symbol is shown; node B is inferred as the circuit common/return

## Validation

- Components in analysis absent from LTSpice netlist: C1, C2, D1, D2, RL, V1
