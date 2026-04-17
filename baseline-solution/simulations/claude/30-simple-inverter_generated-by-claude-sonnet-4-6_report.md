# Schematic Conversion Report (claude-sonnet-4-6)

- **Source image:** `/home/daniel/git/electroai-hackathon/baseline-solution/data/schematics/images/30-simple-inverter.png`
- **Model:** `claude-sonnet-4-6`
- **Circuit name:** 12V DC to 120V/220V AC Inverter (Push-Pull)
- **Falstad URL:** https://www.falstad.com/circuit/circuitjs.html#eNptkU0SgjAMhfc9RRZu6SRtUttrOF7ABbpxJY5c36aQTh2BxXs8vkJ-TkCAHvUSIPQpckhniSVTEhEQBAGOIPNE5D5ACYERN80IenN9DM2hF7f-MDHU1C3dqwZWluB-ey7zzmsWkbd37tW9avsGpFxjLqnFqj1-d0pV_4wwEUzic60o1LawMnZE9ZhZ-_mm2l3NjG-6Z9b9yJkfOfNWtnHWwpZd_zNg3UqOMep-qi-lDPXZhMf6Elv26LWoShsTukufc1M82N0Xn_pg5A

## Summary

This is a simple push-pull inverter circuit that converts 12V DC battery power to AC voltage suitable for powering AC outlet loads. The circuit uses two MJ2955 PNP power transistors driven in alternating fashion through a center-tapped transformer. The transistors alternately conduct, driving current through each half of the transformer primary winding to produce a quasi-square wave AC output. A switch S1 controls power from the 12V battery B1.

## Components

| Reference | Type | Value | Connections |
|-----------|------|-------|-------------|
| B1 | DC Voltage Source (Battery) | 12V | positive, negative |
| S1 | SPST Switch | on-off | pin1, pin2 |
| T1 | Center-Tapped Transformer | Primary: 2x12V CT, Secondary: 120V/220V | primary_tap1, primary_CT, primary_tap2, secondary_live, secondary_neutral |
| R1 | Resistor | 68Ω | pin1, pin2 |
| R2 | Resistor | 68Ω | pin1, pin2 |
| Q1 | PNP BJT Power Transistor | MJ2955 | base, collector, emitter |
| Q2 | PNP BJT Power Transistor | MJ2955 | base, collector, emitter |

## Assumptions

- MJ2955 is a PNP power transistor (standard part); pinout assumed as Base, Collector, Emitter per TO-3 package standard.
- The transformer primary is a center-tapped winding with each half rated for 12V, and the secondary outputs 120V or 220V depending on configuration.
- The circuit oscillates due to transformer feedback (not explicitly shown); this is a self-oscillating inverter relying on magnetic coupling feedback between the two transistors.
- The base resistors R1 and R2 (68Ω each) provide initial bias; the transformer's feedback winding (implied) drives the bases alternately — the schematic may be simplified and omit explicit feedback windings.
- Battery negative (B1 minus) connects to ground/common node.
- The switch S1 is in series with the positive terminal of B1 and the center tap of the transformer.
- No explicit feedback winding is shown; it is assumed the cross-coupled collector-to-base feedback occurs through the transformer leakage or an implicit winding.
- Output frequency is assumed ~60Hz (or 50Hz depending on transformer design); no timing components are visible.
- The AC outlet secondary winding provides 120V/220V output.

## Missing Information

- No explicit oscillation feedback mechanism is shown (feedback winding or cross-coupling network between Q1 collector to Q2 base and vice versa).
- Transformer part number or detailed specifications (turns ratio, power rating, frequency) are not labeled.
- No output frequency specification or timing components visible.
- Power rating of the circuit is not indicated.
- No fuse or protection components are shown for the battery input or AC output.
- The exact wiring of Q1 and Q2 bases to collector cross-feedback is unclear from the image — the schematic appears simplified.
- Secondary winding tap configuration (for 120V vs 220V selection) is not detailed.

## Inconsistencies

- Without a cross-coupling or feedback network between the transistors, the circuit cannot self-oscillate — typical push-pull inverters require either feedback windings on the transformer or an external oscillator driving the bases. The schematic appears to show only resistors R1 and R2 connecting the supply to the bases, which alone would not produce oscillation.
- Both MJ2955 transistors appear to have their emitters connected to the same supply rail (center tap / switched positive), which is correct for PNP push-pull, but simultaneous base bias via R1 and R2 from the same rail would turn both on simultaneously rather than alternately — suggesting missing cross-coupling is a significant omission.
- The image label shows '12V' on both sides of the transformer CT, which is consistent with a 0-12-24V or 12-0-12 center-tapped winding, but the exact configuration is ambiguous.

## Validation

- Components in analysis absent from LTSpice netlist: B1, Q1, Q2, R1, R2, S1, T1
