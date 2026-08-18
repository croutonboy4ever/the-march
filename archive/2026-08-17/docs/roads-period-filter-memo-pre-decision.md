# Memo: Roman roads on march-period maps, display or filter

2026-08-17. For Tony. Decision filed Open in the March Decision Log; this memo
is the options brief behind it. Nothing here is decided.

## The question

The corridor road layer comes from the AWMC Barrington roads data. Hannibal
crossed in 218 BC, before Rome built roads in Transalpine Gaul. Every render so
far draws the roads with the legend line "Roman road (AWMC)". Should
march-period scenes keep showing them, and under what label?

## What the data says

Inspection of `processed/awmc-roads-corridor.geojson` (137 features), 2026-08-17:

| Attribute finding | Count |
|---|---|
| `timeperiod` = RL (Roman and Late Antique) | 62 |
| `timeperiod` = RL? (as above, queried) | 30 |
| `timeperiod` = R (Roman only) | 4 |
| `timeperiod` empty | 41 |
| Named vias (Via Domitia, Via Aurelia, Via Iulia Augusta), all in the empty-field group | 4 of the 41 |

The Barrington time-period codes slice antiquity as: A Archaic, C Classical,
H Hellenistic (330 to 30 BC), R Roman (30 BC to AD 300), L Late Antique. The
march year 218 BC falls in the Hellenistic slice. **No corridor road feature
carries an H code.** Every dated feature in the corridor is attested for
periods beginning 30 BC at the earliest, more than a century after the march.
The 41 undated features assert no period at all. (The full 3,166-feature raw
file does contain H-coded roads elsewhere in the ancient world, so the absence
of H here is a statement by the source, not a gap in its vocabulary.)

Two honesty caveats the experience must carry with any choice:

1. The codes are attestation slices from the Barrington map compilation, not
   construction dates. The Via Domitia is conventionally dated to about 118 BC,
   which is Hellenistic-slice years, yet its segments here carry no code. A
   filter on `timeperiod` is a filter on what the atlas asserts, nothing more.
2. Absence of Roman roads does not mean absence of routes. The army moved on
   existing Gallic and Alpine paths. No attested pre-Roman road linework
   exists in the AWMC set for this corridor, and conventions section 6 forbids
   inventing one. If a march-period scene shows no roads, that is the honest
   rendering of the sources we hold.

## Options

**A. Keep the roads, relabel them as later context.** Legend and captions
change to something like "Roman roads (AWMC Barrington; the network postdates
the march)". Cheap, immediate, keeps the wayfinding value of the road lines,
and turns the layer into an explicit anachronism instead of a silent one.
Cost: a 218 BC scene still shows infrastructure that was not there, and a
label has to work hard against a strong visual impression.

**B. Period-filter march-period scenes.** Where a scene sits in 218 BC, drop
the road layer. Given the data above, filtering "where dating allows" removes
all 96 dated features as post-march; the 41 undated features assert nothing
and would be dropped with them rather than promoted to march-period by
silence. Effect: no roads on march-period maps at all. Roads return, fully
labeled, in later-period content (the war's aftermath, the Long Shadow
chapter, any modern-context view). Cost: the corridor map loses familiar
reference lines that help a newcomer orient.

These compose rather than exclude: A is a labeling treatment, B is a
per-scene visibility rule.

## Recommendation

Both, staged. Now, while everything rendered is exploratory: apply A, change
the legend line in the render scripts to name the roads as later than the
march (one-line edits, no data change). For the shipped Crossing chapter:
apply B as the default for march-period scenes, with the labeled road layer
available as explicit later-Roman context (for example a toggle or an
aside), never as silent background. This follows conventions sections 3 and 6:
the map asserts only what the sources put there in 218 BC, and the Roman
network enters as the labeled later layer it is.

The call is yours; the Decision Log row stays Open until you make it.
