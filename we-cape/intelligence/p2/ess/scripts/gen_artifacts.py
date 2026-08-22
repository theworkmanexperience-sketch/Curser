#!/usr/bin/env python3
"""WECAPE-AR2-SPRINT3A artifact generator.
Emits: STEP0_TIMING_CLOSURE.md · VISUAL_EVENT_REGISTRY.yaml ·
EDITORIAL_SYNCHRONIZATION.yaml · CONDUCTOR_SCORE.yaml ·
ESS_VALIDATION_REPORT.md · PRODUCTION_INTELLIGENCE_SEED.yaml ·
CAPTION_REGISTRY.yaml (enriched)."""
import json, os, re, numpy as np, datetime

OUT="/home/claude/work/ess"
os.makedirs(OUT, exist_ok=True)
U="/mnt/user-data/uploads/WE_CAPE_OUTPUT/AlphaRoundUp_2026/SPRINT3A_WORK/"
W="/home/claude/work/out/"

RUN_ID="WECAPE-AR2-SPRINT3A-20260822-114028"
REGEN_RUN_ID="WECAPE-AR2-ESS004-REGEN-20260822-174500"
RULING = dict(
  id="ESS-004-RULING",
  date="2026-08-22",
  authority="Executive Producer",
  session="ELS-001",
  definition=("MANDATORY_SILENCE prohibits WE CAPE-ADDED NON-DIEGETIC SCORE only. Existing production "
              "audio - speech, ambience, engine noise, wind, and any source audio captured as part of "
              "the documentary record - remains permissible unless otherwise directed by an Executive PDR."),
  test=("PROVENANCE, not acoustics. An element breaches a silence zone if and only if WE CAPE added it "
        "as score. Read from the FCPXML asset media-rep path: /Soundtrack/ = WE CAPE-added score; "
        "Original Media or CONTRIBUTED = documentary record. No listening judgement is required, and "
        "none is permitted as the basis of a compliance verdict."),
  finding=("ELS-001: the span is a composite production soundscape - music/vocals, engine rumble, wind, "
           "speech. The proxy does not conclusively distinguish the provenance of the musical content, "
           "and that distinction is NOT required under this ruling."))
SHA=dict(
 mp4="a53655fc673945a0d99dde3d5b60c9a126d8b41e4e44a7c7eedeb058ba0f47e8",
 fcpxml="2bf0685373d6963bc151b982fd8b16b072d47ca88bb36f3c4dcd4cf5563858e7",
 srt="89d61f965aa17e4d3dade14173869b34efb0c09d689b1c347d3c9c8f6eca1c6b",
 etc="e91318a6719c81e448e6c57267dff7a807076cb9aded822a459fb6353e80010d")
LOCK=4846.625
GIT="ff0c45f77b2fb612606e1d5b8ef86641822e5e4a"

tl=json.load(open(W+"timeline_resolved.json"))
off=json.load(open(W+"step0_offset.json"))
anch=json.load(open(W+"step0_anchors.json"))
obs=json.load(open(W+"die_v_observables.json"))
cams=json.load(open(W+"camera_runs.json"))
els=tl['elements']

def tc(s, frames=True):
    if s is None: return "NULL"
    h=int(s//3600); m=int(s%3600//60); sec=s%60
    return f"{h:02d}:{m:02d}:{sec:06.3f}"
def mmss(s):
    return f"{int(s//60):02d}:{int(s%60):02d}"

titles_d1=sorted([x for x in els if x['tag']=='title' and x['depth']==1],key=lambda y:y['abs_in_s'])
titles_d2=sorted([x for x in els if x['tag']=='title' and x['depth']>=2],key=lambda y:y['abs_in_s'])
audio16=sorted([x for x in els if x['tag']=='asset-clip' and x['lane'] and x['lane'].startswith('-')],
               key=lambda y:y['abs_in_s'])
spine=[x for x in els if x['depth']==0 and x['tag']!='transition']

# ---- audio element provenance (from FCPXML asset media-rep src) ----
AUD_SRC={
 "KICKSTANDS UP v1 (Remastered)":("/AlphaRoundUp_2026/Soundtrack/KICKSTANDS UP v1.wav","SCORE_ASSET"),
 "NOTOR1OUS_CARAVAN_2_":("/Volumes/10TB/.../CONTRIBUTED/Videos_Alpha RoundUp/NOTOR1OUS_CARAVAN_2_.mp4","CONTRIBUTED_VIDEO_AUDIO"),
}
def aud_class(name):
    if name in AUD_SRC: return AUD_SRC[name][1]
    return "PRODUCTION_ORIGINAL_MEDIA_AUDIO"
def aud_src(name):
    if name in AUD_SRC: return AUD_SRC[name][0]
    return "/AlphaRoundUp_2026/AlphaRoundUp_2026.fcpbundle/P2_CHRONO_SETS/Original Media/%s.wav"%name

SEG=[("S01",0,73,"cold_open",None,[]),("S02",73,111,"host_day_brief",None,["host"]),
 ("S03",111,1622,"interview_gauntlet_1","L03-staging",["R01-R45"]),
 ("S04",1622,1643,"ride_brief","L03",[]),("S05",1660,1750,"escort_ride",None,[]),
 ("S06",1903,1953,"librarian_speech","L04",["C01"]),("S07",1965,2030,"council_profile",None,["C02"]),
 ("S08",2031,2156,"town_proclamation",None,["C03-mayor"]),("S09",2163,2190,"first_ride_moment",None,[]),
 ("S10",2219,2332,"state_proclamation",None,["C04","C05"]),
 ("S11",2335,3120,"interview_gauntlet_2","L04",["R46-R67"]),
 ("S12",3124,3236,"organizer_honors_and_silence",None,[]),("S13",3230,3275,"group_photo",None,[]),
 ("S14",3276,3324,"service_wrap_preview",None,[]),("S15",3370,3523,"riding_music_passage",None,[]),
 ("S16",3523,3985,"bike_night_arrivals",None,["R68-R75"]),("S17",3985,4008,"audience_cta",None,[]),
 ("S18",4165,4780,"bike_night_ambience",None,[]),("S19",4784,4846,"friday_wrap_part3_tease",None,[])]

# ============================ VISUAL EVENTS ============================
def ev(i, s, e, cls, conf, note, refs, dev=None):
    return dict(id=f"VE-{i:03d}", span=dict(start_s=round(s,3), end_s=round(e,3),
                start_tc=tc(s), end_tc=tc(e)),
                event_class=cls,
                source=dict(artifact="Filmage_Editor.mp4", sha256=SHA['mp4']),
                evidence_ref=refs, confidence=conf, observation=note,
                derivation=dev or "MODEL_MEDIATED_FRAME_OBSERVATION",
                enrichment=dict(nie={}, mie={}, pie={}))

E=[]; n=1
def add(s,e,cls,conf,note,refs,dev=None):
    global n
    E.append(ev(n,s,e,cls,conf,note,refs,dev)); n+=1

# --- measured, instrument-derived ---
add(0.0,31.0,"ILLUMINATION_DAY_OR_LIT_INTERIOR","HIGH",
    "mean luma 116.6 (grid 2 fps, 64x36 luma)","measured:2fps-luma-series","INSTRUMENT_DERIVED_LUMA")
add(31.0,69.5,"ILLUMINATION_LOW_LIGHT_NIGHT","HIGH",
    "sustained luma <70 for 38.5 s; night material inside the cold-open montage",
    "measured:2fps-luma-series; frames 00:00:33,36,...,00:01:06","INSTRUMENT_DERIVED_LUMA")
add(69.5,3984.5,"ILLUMINATION_DAY_OR_LIT_INTERIOR","HIGH",
    "mean luma 118.5; continuous day / lit-interior block spanning 65 min",
    "measured:2fps-luma-series","INSTRUMENT_DERIVED_LUMA")
add(3984.5,4846.5,"ILLUMINATION_LOW_LIGHT_NIGHT","HIGH",
    "sustained luma <70 to end of runtime; mean luma 47.2; warm ratio R/B 1.32 "
    "(artificial amber street/venue lighting, NOT golden hour)",
    "measured:2fps-luma-series; frame 01:06:24 is first night sample, 01:06:21 still day",
    "INSTRUMENT_DERIVED_LUMA")
# --- observed, from contact sheets / probe sheets ---
add(0.0,73.0,"COLD_OPEN_MONTAGE","HIGH",
    "Rapid montage: club back-patch inserts; highway riding formation; marked police vehicle; "
    "massed motorcycles in a lot; interior ceremony with US flag and standards; night street/venue "
    "material. Shot-change density 25.5 cuts/min (highest in the film).",
    "frames 00:00:00,03,06,...,00:01:12 (sheet_000)")
add(69.375,76.417,"MAIN_TITLE_CARD","HIGH",
    "On-screen title 'ALPHA ROUNDUP II'; ETC title element in/out reproduced in picture.",
    "ETC title[1]; frames 00:01:09,00:01:12")
add(111.0,1622.0,"INTERVIEW_STAGING_AREA_STATIC_DAY","HIGH",
    "Hotel parking lot, overcast sky, wet pavement, densely parked touring motorcycles, "
    "one or two subjects addressing camera. Camera is body/stick-mounted, near-static with slow reframes. "
    "Crowd density band: MODERATE (individuals distinguishable, lot not full-frame packed).",
    "frames sampled 00:01:51 .. 00:27:00 at 3.000 s (sheets 001-018); sheets read: 001,005,010,015")
add(111.333,335.695,"QUESTION_CARD_SEQUENCE_1","HIGH",
    "Recurring on-screen question cards (Who You Rid'n Wit? / Initiated? / Why Do You Ride? / "
    "What's Your Name / What RU Rid'n?) plus 'One Question... Many Answers'. 22 ETC title elements.",
    "ETC titles[2..22]; picture-verified at 00:01:51 and 00:02:00")
add(380.750,537.557,"KINETIC_TEXT_CARD_SEQUENCE_1","HIGH",
    "Nested (compound-clip) kinetic text cards: 'One Question... Many Answers', "
    "'W i n d T h e r a p h y', 'T h r o t t l e h e r a p h y'. Not counted in the ETC 40-title census.",
    "ETC nested titles; picture-verified at 00:07:39 and 00:08:57")
add(1620.0,1660.0,"MOUNT_UP_STAGING_AREA","HIGH",
    "Riders returning to machines, helmets on, column forming in the staging lot.",
    "frames 00:27:00 .. 00:27:39 (sheet_018)")
add(1630.0,1644.6,"MAP_TRAVEL_GRAPHIC_INSERT","HIGH",
    "Picture-in-picture route-map animation (origin to Smyrna Event Center) visible in frame; "
    "co-located with ETC audio element 'Map traavel to Smyrna Event Center-7' (27:10.000-27:24.610).",
    "frames 00:27:12,00:27:15,00:27:18,00:27:21")
add(1660.0,1695.0,"ESCORT_DEPARTURE_COLUMN","HIGH",
    "Machines leaving the lot in single/double column onto the public road. PROBE-1 window.",
    "probe P1 frames 00:27:40 .. 00:28:15 at 1.000 s")
add(1695.0,1990.0,"MASS_RIDE_PUBLIC_ROAD","HIGH",
    "Continuous mass ride on public roads in two-abreast formation, POV from within the column. "
    "Uninterrupted from 00:28:15 to approx 00:33:00. Crowd/vehicle density band: HIGH (column fills frame).",
    "probe P1 frames 00:28:15..00:29:09; frames 00:28:30..00:33:00 (sheets 019-022)")
add(1746.0,1851.0,"LAW_ENFORCEMENT_ESCORT_PRESENCE","HIGH",
    "Marked police vehicles and an officer positioned at road intersections along the route "
    "(observed at 00:29:06, 00:30:03, 00:30:21, 00:30:51, 00:31:33, 00:31:48).",
    "probe P1 frame 00:29:06; frames 00:30:03,00:30:21,00:30:51,00:31:33,00:31:48")
add(1974.0,1980.0,"CARTOGRAPHIC_REVEAL","HIGH",
    "Full-frame map graphic: state outline labelled TENNESSEE with NASHVILLE and SMYRNA placed.",
    "frames 00:32:54,00:32:57")
add(1980.0,1990.0,"AERIAL_OR_ELEVATED_ESTABLISHING_VIEW","MEDIUM",
    "High-angle wide view of the town/venue approach with an emblem overlay. "
    "UNCERTAIN whether captured from an aerial platform or an elevated position: at 320x180 the "
    "parallax cue is not resolvable, and camera-device family in the ETC does not establish capture mode.",
    "frame 00:33:00")
add(1987.250,1994.958,"VENUE_IDENTIFICATION_CARD","HIGH",
    "On-screen card 'Smyrna Event Center / 100 Sam Ridley Parkway East, Smyrna, TN 37167'.",
    "ETC title[23]; picture-verified at 00:33:06,00:33:09,00:33:12")
add(1995.0,2100.0,"VENUE_ARRIVAL_PROCESSION","HIGH",
    "Machines arriving at the venue frontage in procession; riders raising fists; "
    "civic speech carried as a picture-in-picture inset over the arrival picture rather than full frame.",
    "frames 00:33:15 .. 00:35:00 (sheets 022-023)")
add(2022.458,2331.542,"CIVIC_LOWER_THIRD_SEQUENCE","HIGH",
    "Named civic lower-thirds: Racquel Peebles (Council Member), Mayor Mary Esther Reed, "
    "David Santucci (Town Manager), Jerome Dempsey (Council Member). 9 ETC title elements. "
    "Person linkage deferred to human confirmation against ORGANIZATION/RIDER registries; "
    "no biometric identification performed - text was read from the title elements, not from faces.",
    "ETC titles[24..31]; picture-verified at 00:33:45,00:35:18,00:37:00,00:37:12")
add(2106.0,2109.0,"OBSERVED_BLACK_FRAME","MEDIUM",
    "A fully black sampled frame at 00:35:06 between two picture-bearing samples. "
    "Classified as OBSERVED, not diagnosed: at a 3.000 s sampling grid a dip-to-black transition and a "
    "black-frame defect are indistinguishable. Requires human inspection of 00:35:04-00:35:09.",
    "frame 00:35:06")
add(2116.333,2133.958,"PROCLAMATION_DOCUMENT_INSERT_TOWN","HIGH",
    "'OFFICE OF THE MAYOR / Proclamation' document shown full-height beside a speaker inset.",
    "frames 00:35:18,00:35:21,00:35:24,00:35:27,00:35:30")
add(2190.0,2220.0,"INTERIOR_PRESENTATION_FULL_FRAME","HIGH",
    "Interior presentation: podium area, US flag and a second standard, presenter with microphone, "
    "club members receiving. Camera near-static. Crowd density band: LOW-to-MODERATE in frame.",
    "frames 00:36:33 .. 00:36:57")
add(2277.0,2325.0,"PROCLAMATION_DOCUMENT_INSERT_STATE","HIGH",
    "'STATE OF TENNESSEE / PROCLAMATION' document shown full-height with two officials as inset, "
    "over parking-lot picture.",
    "frames 00:37:57 .. 00:38:45")
add(2335.0,3120.0,"INTERVIEW_STAGING_AREA_STATIC_DAY_2","HIGH",
    "Second interview gauntlet, visibly a different location from the first: venue parking lot with a "
    "low brick building behind, dry pavement, denser machine parking. Crowd density band: HIGH.",
    "frames 00:38:57 .. 00:52:00 at 3.000 s (sheets 025-034); sheets read: 025,026")
add(2337.708,2382.583,"QUESTION_CARD_SEQUENCE_2","HIGH",
    "Question cards resume for the second gauntlet (5 ETC title elements) inside the R46 carve-out window.",
    "ETC titles[32..36]; picture-verified at 00:38:57,00:39:06,00:39:18,00:39:33,00:39:39")
add(2566.917,3120.042,"KINETIC_TEXT_CARD_SEQUENCE_2","HIGH",
    "Nested kinetic text cards: 'For My P E A C E', 'TEN YEARS WE RIDE AS ONE BROTHERHOOD!', "
    "'Be Alone, In My T h o u g h t s', 'I Love R i d i n g', 'For the B r o t h e r h o o d', "
    "'The Ride Is Only The Beginning', 'Brotherhood Beyond The Miles', 'The Journey Reveals The Why'.",
    "ETC nested titles 00:42:46 .. 00:52:00")
add(3124.0,3210.0,"INTERIOR_HONORS_CEREMONY","HIGH",
    "Interior hall: podium with venue plate, US flag and standards, framed plaques presented and raised, "
    "line of recipients holding awards. Camera near-static, low frame-difference energy. PROBE-2 window.",
    "probe P2 frames 00:52:04 .. 00:53:30 at 1.000 s")
add(3210.0,3232.0,"BANQUET_ROOM_WIDE_HIGH_DENSITY","HIGH",
    "Wide views of a seated banquet room, round tables fully occupied. Crowd density band: HIGH.",
    "probe P2 frames 00:53:30 .. 00:53:48")
add(3240.0,3262.0,"VENUE_EGRESS_WALKOUT","HIGH",
    "Members walking out through interior corridors and lobby to the exterior.",
    "frames 00:54:00 .. 00:54:21")
add(3264.0,3282.0,"MASS_GROUP_PHOTOGRAPH_EXTERIOR","HIGH",
    "Several hundred members assembled in ranks under the venue portico for a group photograph, "
    "shot from across the lawn. Crowd density band: VERY HIGH.",
    "frames 00:54:24,00:54:27,00:54:30,00:54:33,00:54:36")
add(3285.0,3330.0,"MOUNT_UP_VENUE_LOT","HIGH",
    "Mass mount-up in the venue lot; machines packed nose-in across the frame.",
    "frames 00:54:45 .. 00:55:27")
add(3328.0,3520.0,"ROAD_RIDE_DAY_CLEAR_SKY","HIGH",
    "Sustained multi-lane road riding in formation under clear blue sky - a visibly different sky state "
    "from the overcast staging block earlier in the day.",
    "frames 00:55:30 .. 00:58:27 (sheets 037-038)")
add(3520.0,3984.5,"DAYLIGHT_LOT_GATHERING_AND_INTERVIEWS","HIGH",
    "Hotel parking lot in bright daylight with blue sky: arrivals, machines being parked, "
    "individual riders addressing camera. Measured mean luma 130.7. "
    "This span carries the registry label 'bike_night_arrivals'; the picture in this span is daylight. "
    "Recorded as an observation only - the registry value remains authoritative.",
    "frames 00:58:30 .. 01:06:21 (sheets 039-044); sheets read: 039,041,044")
add(3984.5,4100.0,"NIGHT_RIDE_DEPARTURE","HIGH",
    "Transition to night within one sampling interval: 01:06:21 is daylight, 01:06:24 is night. "
    "Instrument cross-check places the sustained night onset at 3984.5 s. Night ride departure follows, "
    "handlebar/dashboard POV with headlamps and tail lights.",
    "frames 01:06:21,01:06:24,01:06:27 .. 01:08:00; measured 2 fps luma series")
add(4140.0,4400.0,"NIGHT_VENUE_LOT_GATHERING","HIGH",
    "Night venue lot: machines parked with coloured accent lighting, people moving between them, "
    "storefront frontage lit behind. Crowd density band: MODERATE-to-HIGH.",
    "frames 01:09:00 .. 01:13:20 (sheets 046-048); sheet read: 046")
add(4410.0,4490.0,"INTERIOR_NIGHT_VENUE_CROWD","HIGH",
    "Interior of a night venue: multiple screens, string lighting, standing and seated crowd. "
    "Crowd density band: HIGH.",
    "frames 01:13:30 .. 01:14:18 (sheet_049)")
add(4490.0,4780.0,"NIGHT_ROAD_RIDING","HIGH",
    "Night road and highway riding in formation; lowest measured frame-difference energy of the film "
    "(mean 12.6) and lowest shot-change density (0.56 cuts/min) - long unbroken takes.",
    "frames 01:14:21 .. 01:19:40 (sheets 049-053); sheets read: 049,052")
add(4784.0,4846.5,"NIGHT_RIDE_CLOSE","HIGH",
    "Final night ride into a lit portico arrival, then the closing card run. PROBE-3 window.",
    "probe P3 frames 01:19:44 .. 01:20:46 at 1.000 s")
add(4827.750,4846.042,"CLOSING_CARD_SEQUENCE","HIGH",
    "Closing question cards (Why Do You Ride? / What RU Rid'n? / Who You Rid'n Wit? / How Long You Been "
    "Rid'n) then the sign-off card \"..and that's what's good!\". Every card's ETC in/out reproduced in "
    "picture to within the 1.000 s probe grid - this is the frame-accuracy evidence for Step 0.",
    "probe P3 frames 01:20:27 .. 01:20:46 at 1.000 s; ETC titles[37..40] + nested closing title")

# explicit NOT-OBSERVED declarations (absence recorded, never silently omitted)
NOT_OBSERVED=[
 dict(event_class="GOLDEN_HOUR_LIGHT", status="NOT_OBSERVED",
      basis="No span in the runtime shows the low-sun warm daylight signature. The two warm-ratio "
            "excursions (R/B 1.31 and 1.32) are the cold-open night montage and the sustained night block, "
            "both artificial amber lighting. Warm ratio never exceeds 1.10 during any daylight span."),
 dict(event_class="FLAG_DETAIL_BEYOND_PRESENCE", status="OBSERVED_AS_PRESENCE_ONLY",
      basis="A US flag and one or more additional standards are visible at the interior ceremony and "
            "honors spans. Identification of the additional standards is not resolvable at 320x180 and is "
            "recorded as UNCERTAIN rather than named."),
 dict(event_class="PERSON_IDENTITY", status="NOT_PERFORMED",
      basis="Prohibited by ADR-009 and WET-SPEC-DIE-001 §11. No face recognition or biometric "
            "identification was run. The only person names in this registry are text read from ETC title "
            "elements, and they are carried as caption text, not as identifications."),
 dict(event_class="CAMERA_MOTION_CLASS", status="RECORDED_AS_FRAME_DIFFERENCE_ENERGY_ONLY",
      basis="At 320x180 with a 0.5 s observation grid, camera motion cannot be separated from subject "
            "motion or from shot changes. The instrument series is published as FRAME_DIFFERENCE_ENERGY "
            "bands; camera-motion class per se is UNCERTAIN except where a sheet shows it directly."),
 dict(event_class="INTERVIEW_COUNT_BY_VISION", status="NOT_ATTEMPTED",
      basis="Interview counts remain the registry's (TIMELINE_REGISTRY interview_count, RIDER_REGISTRY). "
            "Counting subjects visually would duplicate a governed registry value with a weaker method."),
]

# ============================ DELTA LEDGER ============================
def D(i,cat,desc,val,disp):
    return dict(id=f"D-{i:02d}",category=cat,description=desc,magnitude=val,disposition=disp)
seg_cov=sum(e-s for _,s,e,_,_,_ in SEG)
seg_gaps=[]
prev=0.0
for _,s,e,act,_,_ in SEG:
    if s>prev+0.001: seg_gaps.append((prev,s))
    prev=max(prev,e)
if prev<LOCK: seg_gaps.append((prev,LOCK))
gap_total=sum(b-a for a,b in seg_gaps)

CUES=[("CUE-01",0,73),("CUE-02a",111,630),("CUE-02b",630,1125),("CUE-02c",1125,1622),
      ("CUE-03",1660,1750),("SIL-01",1903,2332),("CUE-04",2335,3120),("SIL-02",3124,3229),
      ("CUE-05",3230,3275),("CUE-06",3276,3324),("CUE-07",3370,3523),("CUE-08",3523,4008),
      ("CUE-09a",4165,4470),("CUE-09b",4470,4780),("CUE-10",4784,4846)]
cue_cov=sum(e-s for _,s,e in CUES)
cue_gaps=[];prev=0.0
for _,s,e in CUES:
    if s>prev+0.001: cue_gaps.append((prev,s))
    prev=max(prev,e)
if prev<LOCK: cue_gaps.append((prev,LOCK))
cue_gap_total=sum(b-a for a,b in cue_gaps)

LEDGER=[
 D(1,"NON_SPEECH_TAIL","Lock runtime 4846.625 s vs last lock-SRT cue end 4841.208 s. The tail is the "
   "closing card over the final shot; no speech exists to transcribe.","+5.417 s","CLOSED"),
 D(2,"NON_SPEECH_HEAD","First lock-SRT cue starts at 0.333 s, not 0.000 s.","+0.333 s","CLOSED"),
 D(3,"PRE_LOCK_VS_LOCK_SRT_REVISION","Founding fixture (WET-SPEC-DIE-001 App. A) records 2,290 cues "
   "ending 01:20:40; the lock SRT carries 2,291 cues ending 01:20:41.208. The pre-lock SRT is not among "
   "this run's four authoritative inputs, so the single added cue cannot be identified here.",
   "+1 cue / +1.208 s","CLOSED-AS-BOUNDED (pre-lock SRT out of scope of this run's inputs)"),
 D(4,"REGISTRY_NOTE_ARITHMETIC","TIMELINE_REGISTRY.delta_note states the pre-lock/lock delta as +6.025 s. "
   "Lock runtime minus the fixture's stated 01:20:40 end is +6.625 s.","0.600 s","CLOSED-AS-NOTED "
   "(registry text unchanged by this run; flagged for registry maintenance)"),
 D(5,"PROXY_CONTAINER_ROUNDING","Filmage_Editor.mp4 video stream duration 4846.633 s and container "
   "duration 4846.747 s vs sequence 4846.625 s.","+0.008 s video / +0.122 s container","CLOSED"),
 D(6,"ETC_CENSUS_EXCLUDES_TRANSITIONS","FCPXML top-level spine carries 214 story elements; the ETC "
   "spine census is 191. The 23-element difference is exactly the transition elements.","23 elements","CLOSED"),
 D(7,"NESTED_TITLES_NOT_IN_ETC_CENSUS","FCPXML contains 57 title elements; 40 sit on connected lanes at "
   "depth 1 (the ETC census) and 17 are nested inside compound clips.","17 titles","CLOSED - the 17 are "
   "enrolled into CAPTION_REGISTRY by this run"),
 D(8,"ETC_CONNECTED_OFFSETS_NULL","Every connected element in P2_LOCK_timing.json carries "
   "timeline_offset_s: null; only rel_offset_s is present, and parent references are by non-unique name.",
   "404 elements","CLOSED - absolute offsets resolved from FCPXML nesting; resolver validated 191/191 "
   "against the ETC spine offsets"),
 D(9,"SYNC_CLIP_INTERNAL_MEDIA","18 resolved elements fall outside [0, 4846.625]. All are video/gap/audio "
   "components inside synchronized clips using the offset==start idiom; they are media plumbing, not "
   "timeline story elements.","18 elements","CLOSED - excluded from the timeline census by rule"),
 D(10,"CORRELATION_INDETERMINATE_SPANS","12 of 19 registry segments cannot yield an independent offset "
   "estimate from envelope correlation.","1968 s of runtime","CLOSED - each carries a categorized reason "
   "(segment shorter than the lag-search window, or SRT speech coverage below 30%)"),
 D(11,"SATURATED_SPEECH_MASK","S08 and S10 initially returned apparent lags of -6.75 s and -3.25 s. In "
   "both spans the ASR emits back-to-back cues with a median inter-cue gap of 0.042 s (one frame at 24 "
   "fps), so the speech mask is effectively constant and the correlation surface is a plateau, not a peak.",
   "2 segments / 238 s","CLOSED - measurement artefact, not a timebase shift; a genuine mid-film shift "
   "bounded by zero-offset neighbours on both sides is editorially impossible"),
 D(12,"EDITORIAL_CARD_LAG_CONSTANT","Across 11 semantic anchors spanning 97.4% of runtime, title cards "
   "land a median +0.708 s after the matching spoken phrase begins (sd 0.784 s).","+0.708 s median",
   "CLOSED - a constant editorial design lag, not a timebase offset"),
 D(13,"NO_RATE_MISMATCH","Regression of anchor delta on time gives a drift of +0.684 s over the full "
   "runtime, 95% CI [-0.541, +1.909] s, which contains zero. A 23.976/24 pulldown error would be -4.85 s.",
   "0 s within CI","CLOSED"),
 D(14,"CUE_BOUNDARY_VS_EXISTING_ELEMENT","CUE-01 is specified 00:00-01:13; the existing score element "
   "KICKSTANDS UP v1 occupies 00:00:00.000-00:01:16.417.","+3.417 s","OPEN-TO-PDR (cue in/out binds to "
   "the closed ETC; reconciliation verdict is a human decision)"),
 D(15,"OBSERVED_ACTIVITY_EXCEEDS_CUE_SPAN","CUE-03 ESCORT_ANTHEM is specified 00:27:40-00:29:10 (90 s). "
   "The mass ride is observed continuously in picture from 00:28:15 to approximately 00:33:00.",
   "approx +150 s of unscored ride","OPEN-TO-PDR (registry and cue sheet remain authoritative; recorded "
   "as CONFLICTED observation)"),
 D(16,"REGISTRY_LABEL_VS_OBSERVATION","TIMELINE_REGISTRY S16 (00:58:43-01:06:25) carries the label "
   "'bike_night_arrivals'. Measured mean luma over that span is 130.7 and the picture is bright daylight "
   "with blue sky throughout.","462 s","CONFLICTED - registry value retained as authoritative; observation "
   "recorded and raised as a PDR candidate"),
 D(17,"AGREEMENT_WITHIN_SAMPLING","Registry S16/S17 boundary at 3985 s vs instrument-measured sustained "
   "night onset at 3984.5 s.","0.5 s","CLOSED - agreement within the 0.5 s observation grid"),
 D(18,"SILENCE_LAW_OVERLAP_CANDIDATE","Audio-lane element NOTOR1OUS_CARAVAN_2_ occupies "
   "00:33:37.708-00:34:39.667, entirely inside SIL-01 (00:31:43-00:38:52). Its source is a contributed "
   "video's audio, not a score asset. Whether its content is musical was NOT determined by this run.",
   "61.958 s inside a mandatory-silence window","OPEN-TO-PDR - classified UNCERTAIN; escalated rather "
   "than resolved"),
 D(19,"CUE_SHEET_COVERAGE_GAPS","Spans carrying neither a cue nor a mandatory silence.",
   f"{cue_gap_total:.3f} s across {len(cue_gaps)} spans","CLOSED-AS-ENUMERATED (each span listed in "
   "CONDUCTOR_SCORE.uncovered_spans)"),
 D(20,"REGISTRY_SEGMENT_GAPS","Runtime not covered by TIMELINE_REGISTRY segments S01-S19.",
   f"{gap_total:.3f} s across {len(seg_gaps)} spans","CLOSED-AS-ENUMERATED (each span listed in "
   "EDITORIAL_SYNCHRONIZATION.unsegmented_spans)"),
 D(21,"TITLE_TEXT_LETTER_SPACING","Title text extracted from FCPXML carries kinetic letter-spacing "
   "(for example 'W i n d T h e r a p h y'). Style runs within one text block were concatenated; residual "
   "spacing is the designed on-screen treatment and was not normalised.","cosmetic","CLOSED - verbatim "
   "preserved per DIE-X rule X-2 (zero interpretation at extraction)"),
 D(22,"OFFLINE_MEDIA_REFERENCE","FCPXML asset r95 (NOTOR1OUS_CARAVAN_2_) resolves to /Volumes/10TB/..., "
   "a volume not mounted for this run.","1 asset","CLOSED-AS-NOTED - affects content inspection only, not timing. It was the stated reason "
   "D-18 could not be resolved in RE-001; the ESS-004 ruling retired that dependency by making the "
   "test provenance rather than content, so the offline volume no longer blocks any decision"),
 D(23,"DIE_V_SAMPLING_UNCERTAINTY","Contact-sheet evidence timestamps sit on a 3.000 s grid and probe "
   "sheets on a 1.000 s grid.","+/-0.5 sample","CLOSED - frame-accuracy claims rest on the ETC and on the "
   "1.000 s probe grid, never on the 3.000 s survey grid"),
 D(24,"PROXY_RESOLUTION_CEILING","The visual ground truth supplied is a 320x180 proxy carrying a "
   "'Filmage Editor' trial watermark. Formation geometry, flag identification, and camera-motion class "
   "are limited by this.","320x180 vs 3840x2160 master","CLOSED-AS-DECLARED - every affected observation "
   "is capped at MEDIUM or UNCERTAIN; no observation claims detail the proxy cannot carry"),
 D(26,"YAML_SEXAGESIMAL_TIMECODE","Bare timecode values (start_tc / end_tc) are parsed by YAML 1.1 "
   "loaders as sexagesimal numbers - 00:31:43.000 loads as the float 1903.0 - silently converting a "
   "human-readable string field into a number. Present in every YAML artifact of the RE-001 baseline; "
   "found during the ESS-004 regeneration.","4 artifacts, all *_tc fields",
   "FIXED in the regeneration - all timecodes are now quoted at write time and load as strings. The "
   "RE-001 archived copies retain the defect by design (immutable); RE-002 will carry the fix"),
 D(25,"DIE_V_SHEET_SAMPLING","54 survey contact sheets were generated at 3.000 s cadence covering 100% "
   "of runtime; 20 sheets were read frame-by-frame in full, chosen to cover every non-gauntlet span "
   "completely and the two homogeneous interview gauntlets by systematic sample.",
   "20 of 54 sheets read in full","CLOSED-AS-DECLARED - gauntlet spans carry span-level classifications "
   "only, never per-event claims outside a read sheet"),
]

_TC_RE = re.compile(r'((?:start_tc|end_tc):\s*)(\d{2}:\d{2}:\d{2}\.\d{3})(?=[,}\s])')
def yamlsafe(text):
    """Quote bare timecodes. YAML 1.1 parses 00:31:43.000 as sexagesimal (=1903.0),
    silently turning a human-readable string field into a float. Found during the
    ESS-004 regeneration; fixed here rather than left in the new baseline."""
    return _TC_RE.sub(r'\1"\2"', text)

def y(s):
    """Always quote scalars - YAML indicator characters (? : - # etc) are common
    in caption text and cue names, and selective quoting is a silent-failure trap."""
    s=str(s)
    return '"'+s.replace('\\','\\\\').replace('"','\\"').replace('\n',' ')+'"' 
def blk(text, indent):
    pad=" "*indent
    return "\n".join(pad+l for l in re.sub(r'\s+',' ',text).strip().split("\n"))

HDR=f"""# ============================================================================
# RUN_ID: {RUN_ID}
# Sprint: G3-ESS-001 Rev A (Sprint 3A) - governed production run
# Generated by: intelligence/p2/ess/scripts (see EXECUTION_LOG.md)
# Authoritative inputs (SHA-256):
#   Filmage_Editor.mp4                     {SHA['mp4']}
#   Alpha RoudUp Part 2.fcpxmld/Info.fcpxml {SHA['fcpxml']}
#   Alpha RoudUp Part 2_SRT__SRT 2_...srt   {SHA['srt']}
#   P2_LOCK_timing.json                     {SHA['etc']}
# Editorial lock: 4846.625 s (01:20:46:14 @ 24 fps, NDF) - offset model: ZERO
# REGENERATED WECAPE-AR2-ESS004-REGEN-20260822-174500 under Executive Ruling ESS-004 (2026-08-22, session ELS-001):
#   MANDATORY_SILENCE prohibits WE CAPE-added non-diegetic score ONLY.
#   Supersedes the pre-ruling state archived at RE-001. Regenerate, never patch (DOC-002).
# Repository commit at launch: {GIT}
# ============================================================================
"""

# ---------------------------------------------------------------- STEP 0 ----
per=off['per_segment']
L=[]
L.append(f"# STEP0_TIMING_CLOSURE.md")
L.append(f"## Editorial Timing Closure - {RUN_ID}\n")
L.append("**Status: CLOSED.** The +/-6 s tolerance carried by TIMELINE_REGISTRY since Sprint 2 is "
         "discharged. Every delta between the lock SRT, the Editorial Timing Contract, the locked "
         "FCPXML and the master proxy is categorized in the ledger below. No delta is unexplained.\n")
L.append("### 1. Offset model (one line)\n")
L.append("> **The lock SRT is on the ETC timebase exactly: offset = 0.000 s, drift = 0 s/s, "
         "single-valued across the whole runtime.** The historical +/-6 s was never a shift in the lock "
         "SRT - it was the *pre-lock* SRT's shorter runtime being compared against the lock.\n")
L.append("### 2. Inputs of record\n")
L.append("| input | SHA-256 | measure |")
L.append("|---|---|---|")
L.append(f"| Filmage_Editor.mp4 | `{SHA['mp4']}` | 4846.633 s video stream, 320x180, 30 fps proxy |")
L.append(f"| Info.fcpxml | `{SHA['fcpxml']}` | sequence 4846.625 s, 3840x2160p24, tcStart 0 s, NDF |")
L.append(f"| lock SRT (\"SRT 2\") | `{SHA['srt']}` | 2,291 cues, 0.333 s -> 4841.208 s |")
L.append(f"| P2_LOCK_timing.json | `{SHA['etc']}` | 191 spine + 404 connected; declares source sha {SHA['fcpxml'][:16]}... |")
L.append("\nThe ETC's own `source_sha256` field equals the SHA-256 this run computed for Info.fcpxml. "
         "The four-source chain is therefore closed at the hash level, not merely asserted.\n")
L.append("### 3. Method\n")
L.append("Two independent methods were run, plus a resolver validation:\n")
L.append("**A - envelope correlation.** The master proxy's audio was decoded to a 0.25 s RMS envelope "
         "(19,386 samples). The lock SRT was rendered onto the same grid as a speech mask. The two were "
         "cross-correlated over +/-40 s. Significance was tested against a null built from 300 "
         "circular rotations of the mask; peaks at a search-window edge, non-positive peaks, and peaks "
         "failing p<0.05 are reported INDETERMINATE rather than converted into an offset.\n")
L.append(f"Global result: **best lag 0.000 s**, peak r = {off['global_A']['peak']}, "
         f"null p = {off['global_A']['null_p']}, null 95th percentile = {off['global_A']['null_p95']}. "
         f"Status **{off['global_A']['status']}**.\n")
L.append("**B - semantic anchors (SRT text vs ETC title text).** Title elements whose text matches a "
         "nearby SRT cue give a direct, audio-independent measurement of the relation between the two "
         "timebases. 11 high-quality anchors were found spanning 119.3 s to 4840.7 s (97.4% of runtime).\n")
L.append("| title in (s) | delta (s) | title text |")
L.append("|---|---|---|")
for r in anch:
    if abs(r['delta_title_minus_cue'])<=2.5:
        L.append(f"| {r['title_in']:.3f} | {r['delta_title_minus_cue']:+.3f} | {r['title']} |")
L.append("")
L.append("Median delta **+0.708 s**, sd 0.784 s. Regression of delta on time gives a total drift of "
         "**+0.684 s over the full runtime, 95% CI [-0.541, +1.909] s** - the interval contains zero, "
         "which rules out any rate mismatch (a 23.976/24 pulldown error would have shown -4.85 s). "
         "The residual +0.708 s is a constant editorial design lag: cards land just after the words.\n")
L.append("**C - picture verification.** Probe 3 sampled 01:19:44-01:20:46 at 1.000 s. Every closing "
         "title's ETC in/out is reproduced in the rendered picture to within one sample:\n")
L.append("| ETC title | ETC in/out | first sampled frame showing it | last |")
L.append("|---|---|---|---|")
L.append("| Why Do You Ride? | 01:20:27.750 - 01:20:31.333 | 01:20:28 | 01:20:30 |")
L.append("| What RU Rid'n? | 01:20:31.458 - 01:20:33.833 | 01:20:32 | 01:20:32 |")
L.append("| Who You Rid'n Wit? | 01:20:33.958 - 01:20:35.458 | 01:20:34 | 01:20:34 |")
L.append("| How Long You Been Rid'n | 01:20:35.500 - 01:20:39.208 | 01:20:36 | 01:20:38 |")
L.append("| ..and that's what's good! (nested) | 01:20:40.708 - 01:20:46.042 | 01:20:41 | 01:20:45 |")
L.append("\nThe nested card is the important one: it validates the compound-clip recursion in the "
         "resolver against the rendered picture, not just against the ETC.\n")
L.append("### 4. Resolver validation (the enabling result)\n")
L.append("`P2_LOCK_timing.json` carries `timeline_offset_s: null` for **all 404 connected elements**, "
         "and its `parent` references are clip *names*, which repeat. Absolute in/outs for the 16 "
         "audio-lane elements and the 40 titles therefore could not be read from the ETC. They were "
         "resolved from the FCPXML nesting instead:\n")
L.append("```\nabs(child) = abs(container) + (child.offset - container.start)\n"
         "anchored <spine lane=N>: children are expressed in the storyline's own base (0)\n```\n")
L.append("The resolver reproduces **191 of 191** ETC spine offsets and durations to within 0.0006 s, "
         "and its last spine element ends at exactly 4846.625 s. That is the licence to trust its "
         "connected-element output.\n")
L.append("### 5. Per-segment mapping\n")
L.append("| seg | span | dur | SRT cues | speech cov | status | lag | note |")
L.append("|---|---|---|---|---|---|---|---|")
for r in per:
    lag = f"{r['best_lag_s']:+.2f}" if 'best_lag_s' in r and r['status']!='INDETERMINATE' else "-"
    note = r.get('reason','')
    if r['seg'] in ('S08','S10') and r['status']!='INDETERMINATE':
        note="see D-11"
    L.append(f"| {r['seg']} | {r['span']} | {r['dur_s']} s | {r['n_cues_in_span']} | "
             f"{r['srt_speech_coverage']:.2f} | {r['status']} | {lag} | {note} |")
L.append("")
L.append("Read this table correctly: the per-segment column is a **diagnostic on the measurement**, not "
         "19 independent offset estimates. A locked cut cannot carry a different timebase in one "
         "two-minute stretch than in the stretches on either side of it. Where a segment disagrees with "
         "zero, the disagreement is a property of the probe (see D-11), and it is written down as such "
         "rather than averaged away.\n")
L.append("### 6. The 16 audio-lane elements - exact in/outs (resolved)\n")
L.append("| # | in | out | dur (s) | lane | classification | source |")
L.append("|---|---|---|---|---|---|---|")
for i,x in enumerate(audio16,1):
    L.append(f"| {i} | {tc(x['abs_in_s'])} | {tc(x['abs_out_s'])} | {x['duration_s']:.3f} | "
             f"{x['lane']} | {aud_class(x['name'])} | `{x['name']}` |")
L.append("")
L.append("Provenance is decisive here and it is read from the FCPXML asset paths, not guessed: "
         "**exactly one** of the sixteen is a score asset (`/AlphaRoundUp_2026/Soundtrack/KICKSTANDS UP "
         "v1.wav`). Fourteen are detached production audio from `P2_CHRONO_SETS/Original Media` - the "
         "route-map animation audio, whose picture this run observed directly at 00:27:12-00:27:21. "
         "One is the audio of a contributed video (`NOTOR1OUS_CARAVAN_2_`), and it sits inside SIL-01. "
         "That last one is escalated, not resolved: see D-18.\n")
L.append("### 7. Delta ledger - every delta categorized\n")
L.append("| id | category | magnitude | disposition |")
L.append("|---|---|---|---|")
for d in LEDGER:
    L.append(f"| {d['id']} | {d['category']} | {d['magnitude']} | {d['disposition']} |")
L.append("")
L.append("Full descriptions are carried in ESS_VALIDATION_REPORT.md section 6.\n")
L.append("### 8. Closure statement\n")
L.append(f"With offset = 0.000 s and drift within [-0.541, +1.909] s of zero over 4846.625 s, and with "
         f"{len(LEDGER)} deltas each carrying a category and a disposition, the +/-6 s tolerance is "
         f"**CLOSED**. Frame-accurate claims downstream of this report are licensed against the ETC "
         f"and the 24 fps sequence timebase - not against the 320x180 proxy and not against the "
         f"3.000 s DIE-V survey grid.\n")
open(OUT+"/STEP0_TIMING_CLOSURE.md","w").write("\n".join(L))
print("wrote STEP0_TIMING_CLOSURE.md")

# ------------------------------------------------- CAPTION_REGISTRY (enriched)
C=[]
C.append("registry_id: CAPTION_REGISTRY")
C.append("class: EXTENSION")
C.append("registry_version: 0.2.1   # 0.1.0 -> 0.2.0: position enrichment completed | 0.2.0 -> 0.2.1: D-26 serialization fix only (timecodes quoted); ZERO content change - byte diff is the quoting and this header")
C.append("registry_schema_version: 1.0")
C.append(f"enriched_by_run: {RUN_ID}")
C.append("enrichment_note: >-")
C.append(blk("Sprint 3A Step 0 completed the deferred local ETC pass. The 40 connected-lane title "
            "elements now carry resolved absolute in/out points on the 4846.625 s locked timebase, and "
            "17 further title elements nested inside compound clips - absent from the Sprint 2 "
            "statistics-level census - are enrolled here for the first time. Positions were resolved "
            "from FCPXML nesting because P2_LOCK_timing.json carries timeline_offset_s: null for every "
            "connected element; the resolver was validated by reproducing all 191 ETC spine offsets "
            "exactly. Five title in/out points were additionally verified against the rendered picture "
            "at a 1.000 s grid. No caption text was corrected, normalised or re-spaced: verbatim "
            "extraction per WET-SPEC-DIE-001 rule X-2.", 2))
C.append("sources:")
C.append(f"  fcpxml: {{sha256: {SHA['fcpxml']}, role: title positions and text}}")
C.append(f"  etc: {{sha256: {SHA['etc']}, role: census reconciliation}}")
C.append(f"  master_proxy: {{sha256: {SHA['mp4']}, role: picture verification of 5 title in/outs}}")
C.append("observed:")
C.append(f"  title_elements_connected_lane_depth1: {len(titles_d1)}   # matches the Sprint 2 ETC count of 40")
C.append(f"  title_elements_nested_in_compound_clips: {len(titles_d2)}  # NEW - not counted in Sprint 2")
C.append(f"  title_elements_total_in_fcpxml: {len(titles_d1)+len(titles_d2)}")
C.append("caption_classes:")
C.append("  QUESTION_CARD: recurring interview prompt cards - the Q-cadence rendered on screen")
C.append("  CIVIC_LOWER_THIRD: name/role identification of civic speakers")
C.append("  VENUE_CARD: venue name and street address")
C.append("  MAIN_TITLE: film title card")
C.append("  KINETIC_TEXT_CARD: designed answer-phrase cards nested inside compound clips")
C.append("  SIGN_OFF_CARD: closing phrase card")
def cclass(t):
    tx=t['text']
    if tx.strip().rstrip('?').strip() in ("ALPHA ROUNDUP II",): return "MAIN_TITLE"
    if 'Smyrna Event Center' in tx: return "VENUE_CARD"
    if re.search(r'(Council Member|Mayor|Town Manager)', tx): return "CIVIC_LOWER_THIRD"
    if tx.strip().endswith('?') or "One Question" in tx: return "QUESTION_CARD"
    if "what's good" in tx.lower(): return "SIGN_OFF_CARD"
    return "KINETIC_TEXT_CARD"
C.append("captions:")
for i,t in enumerate(sorted(titles_d1+titles_d2,key=lambda x:x['abs_in_s']),1):
    nested = t['depth']>=2
    C.append(f"  - id: CAP-{i:03d}")
    C.append(f"    text: {y(t['text'])}")
    C.append(f"    caption_class: {cclass(t)}")
    C.append(f"    span: {{start_s: {t['abs_in_s']}, end_s: {t['abs_out_s']}, "
             f"start_tc: {tc(t['abs_in_s'])}, end_tc: {tc(t['abs_out_s'])}}}")
    C.append(f"    duration_s: {t['duration_s']}")
    C.append(f"    lane: {y(t['lane'] if t['lane'] else 'nested-storyline')}")
    C.append(f"    census: {'NESTED_NOT_IN_ETC_40' if nested else 'ETC_CONNECTED_40'}")
    C.append(f"    element_name: {y(t['name'])}")
    C.append(f"    evidence_class: OBSERVED")
    C.append(f"    source: {{artifact: Info.fcpxml, sha256: {SHA['fcpxml']}}}")
C.append("caption_boundaries_policy: >-")
C.append(blk("SUPERSEDED-BY-EVIDENCE. The Sprint 2 policy line anticipated lower-third naming at each "
             "rider first-cue, giving 75 candidates from RIDER_REGISTRY. The locked cut contains no "
             "rider lower-thirds at all: of the 40 connected-lane titles, 22 are question cards in the "
             "first gauntlet, 5 are question cards in the second, 4 plus a sign-off close the film, "
             "8 are civic lower-thirds, and 1 is the venue card. Naming on screen is reserved for civic "
             "speakers. The proclamation-dignity rule holds: no caption is placed over the proclamation "
             "readings themselves. Recorded as an observation of the lock, not as a change of policy - "
             "any decision to add rider lower-thirds is a human editorial decision.", 2))
C.append("status: COMPLETE - position enrichment closed by Sprint 3A Step 0")
open(OUT+"/CAPTION_REGISTRY.yaml","w").write(yamlsafe(HDR+"\n".join(C)+"\n"))
print("wrote CAPTION_REGISTRY.yaml", len(titles_d1)+len(titles_d2), "captions")

# ---------------------------------------------------- VISUAL_EVENT_REGISTRY --
V=[]
V.append("registry_id: VISUAL_EVENT_REGISTRY")
V.append("module: DIE-V   # module of DIE per ADR-009; NOT an engine")
V.append("registry_version: 1.0.1   # 1.0.0 -> 1.0.1: D-26 serialization fix only (timecodes quoted); ZERO event-content change")
V.append("registry_schema_version: 1.0   # canonical sync_event schema")
V.append(f"run_id: {RUN_ID}")
V.append("evidence_class: OBSERVED")
V.append("governance:")
V.append("  authority: advisory under the Principle of Human Editorial Authority")
V.append("  precedence: >-")
V.append(blk("Visual observation REINFORCES governed registries and never supersedes them. Where an "
             "observation disagrees with a registry value, the registry value stands and the "
             "disagreement is recorded as CONFLICTED.", 4))
V.append("  prohibitions_observed:")
V.append("    - no_face_recognition_or_biometric_identification")
V.append("    - no_sentiment_or_emotion_inference")
V.append("    - no_person_identification (person linkage is human-confirmable registry reference only)")
V.append("    - enrichment namespaces nie/mie/pie left empty - DIE never writes them")
V.append("method:")
V.append("  source: {artifact: Filmage_Editor.mp4, sha256: %s}"%SHA['mp4'])
V.append("  proxy_declaration: >-")
V.append(blk("The supplied visual ground truth is a 320x180 30 fps proxy carrying a 'Filmage Editor' "
             "trial watermark, not the 3840x2160p24 master the FCPXML describes. Every observation "
             "below is capped by what that proxy can carry. Nothing in this registry claims detail the "
             "proxy cannot resolve.", 4))
V.append("  instrument_pass:")
V.append("    grid: 2 fps, 64x36 RGB downsample, 9693 samples covering 4846.5 s")
V.append("    measures: [mean_R, mean_G, mean_B, mean_luma, luma_sd, inter_frame_abs_luma_diff,")
V.append("               left_right_luma_split, top_band_luma, bottom_band_luma]")
V.append("    illumination_thresholds: {night_in_luma: 70.0, night_out_luma: 85.0, hysteresis: true}")
V.append("    motion_terciles: [13.04, 23.55]")
V.append("    cut_threshold_abs_luma_diff: %.2f"%obs['thresholds']['cut_threshold_absdiff'])
V.append("  observation_pass:")
V.append("    survey_grid: 1 frame / 3.000 s (1616 frames, 100% of runtime), tiled into 54 contact sheets")
V.append("    sheets_read_in_full: 20")
V.append("    sampling_declaration: >-")
V.append(blk("Every non-gauntlet span is covered by sheets read in full. The two interview gauntlets "
             "(00:01:51-00:27:02 and 00:38:55-00:52:00) are visually homogeneous and were covered by "
             "systematic sample; they therefore carry span-level classifications only. No per-event "
             "claim is made about a sheet that was not read.", 6))
V.append("    probe_grid: 1 frame / 1.000 s inside the three fixture windows")
V.append("  fixture_validation:")
V.append("    - {probe: P1, window: \"00:27:40-00:29:10\", expected: mass-ride/escort motion, "
         "result: PASS, observed: \"staging-lot mount-up, column departure, two-abreast public-road "
         "formation, marked police vehicle and officer at an intersection at 00:29:06\"}")
V.append("    - {probe: P2, window: \"00:52:04-00:53:49\", expected: static crowd/ceremony, "
         "result: PASS, observed: \"interior hall, podium with venue plate, US flag and standards, "
         "framed plaques presented and raised, line of recipients, wide seated banquet room\"}")
V.append("    - {probe: P3, window: \"01:19:44-end\", expected: riding + night, "
         "result: PASS, observed: \"night formation riding, helmet POV, lit portico arrival, closing "
         "card run; all five closing title in/outs reproduced in picture within one 1.000 s sample\"}")
V.append("  fixture_disposition: all three probes passed before the full run; no diagnose-and-stop was triggered")
V.append("")
V.append("camera_device_families_from_etc:")
V.append("  note: >-")
V.append(blk("Read from FCPXML clip names, an editorial fact, not a visual observation. Device family "
             "does NOT establish capture mode: the DJI-named material includes long handheld "
             "interview takes, so 'DJI' must not be read as 'aerial'. Recorded to prevent exactly that "
             "inference downstream.", 4))
import collections as _c
_tot=_c.defaultdict(float)
for r in cams: _tot[r['camera']]+=r['end_s']-r['start_s']
for k,v_ in sorted(_tot.items(), key=lambda kv:-kv[1]):
    V.append(f"  {k}: {{spine_seconds: {v_:.1f}, share_of_runtime: {v_/LOCK:.3f}}}")
V.append("")
V.append("events:")
for e in E:
    V.append(f"  - id: {e['id']}")
    V.append(f"    span: {{start_s: {e['span']['start_s']}, end_s: {e['span']['end_s']}, "
             f"start_tc: {e['span']['start_tc']}, end_tc: {e['span']['end_tc']}}}")
    V.append(f"    event_class: {e['event_class']}")
    V.append(f"    confidence: {e['confidence']}")
    V.append(f"    derivation: {e['derivation']}")
    V.append(f"    source: {{artifact: {e['source']['artifact']}, sha256: {e['source']['sha256']}}}")
    V.append(f"    evidence_ref: {y(e['evidence_ref'])}")
    V.append(f"    observation: >-")
    V.append(blk(e['observation'],6))
    V.append(f"    enrichment: {{nie: {{}}, mie: {{}}, pie: {{}}}}")
V.append("")
V.append("not_observed_declarations:")
for nb in NOT_OBSERVED:
    V.append(f"  - event_class: {nb['event_class']}")
    V.append(f"    status: {nb['status']}")
    V.append(f"    basis: >-")
    V.append(blk(nb['basis'],6))
V.append("")
V.append("conflicts_with_registries:")
V.append("  - id: VCONF-01")
V.append("    registry: TIMELINE_REGISTRY")
V.append("    registry_value: \"S16 00:58:43-01:06:25 activity: bike_night_arrivals\"")
V.append("    observation: \"span is bright daylight throughout; mean luma 130.7; sustained night onset "
         "measured at 3984.5 s (01:06:24.5)\"")
V.append("    state: CONFLICTED")
V.append("    resolution: registry value retained as authoritative; raised as PDR candidate")
V.append("  - id: VCONF-02")
V.append("    registry: TIMELINE_REGISTRY / CUE_SHEET_v1.1")
V.append("    registry_value: \"S05 escort_ride 00:27:40-00:29:10; CUE-03 ESCORT_ANTHEM same span\"")
V.append("    observation: \"mass ride observed continuously in picture from 00:28:15 to approximately "
         "00:33:00, with law-enforcement escort presence recurring to 00:31:48\"")
V.append("    state: CONFLICTED")
V.append("    resolution: registry and cue sheet retained as authoritative; raised as PDR candidate")
V.append("  - id: VCONF-03")
V.append("    registry: CAPTION_REGISTRY (Sprint 2 policy line)")
V.append("    registry_value: \"lower-third naming at each rider first-cue, 75 candidates\"")
V.append("    observation: \"the locked cut contains zero rider lower-thirds; on-screen naming is "
         "reserved for civic speakers\"")
V.append("    state: CONFLICTED")
V.append("    resolution: policy line marked SUPERSEDED-BY-EVIDENCE in the enriched registry; the "
         "decision whether to add rider lower-thirds remains human")
V.append(f"\nevent_count: {len(E)}")
V.append(f"runtime_covered_s: {LOCK}")
V.append("status: COMPLETE")
open(OUT+"/VISUAL_EVENT_REGISTRY.yaml","w").write(yamlsafe(HDR+"\n".join(V)+"\n"))
print("wrote VISUAL_EVENT_REGISTRY.yaml", len(E), "events")

# --------------------------------------------- EDITORIAL_SYNCHRONIZATION -----
PROG=[("P1","ARRIVAL",0,111),("P2","GAUNTLET_ONE",111,1622),("P3","RIDE_AND_TOWN",1622,2332),
      ("P4","GAUNTLET_TWO_HONORS",2335,3324),("P5","BIKE_NIGHT_WRAP",3324,4846.625)]
ENERGY={"S01":2,"S02":2,"S03":3,"S04":None,"S05":5,"S06":2,"S07":2,"S08":2,"S09":2,"S10":2,
        "S11":3,"S12":1,"S13":3,"S14":3,"S15":4,"S16":4,"S17":None,"S18":5,"S19":4}
VO=[("VO01",73,111,"day_brief"),("VO02",1622,1750,"ride_narration"),
    ("VO03",3276,3324,"service_wrap"),("VO04",4784,4846,"wrap_tease")]
def overlaps(a0,a1,b0,b1): return max(a0,b0) < min(a1,b1)-1e-9
def prog_of(s,e):
    for pid,nm,p0,p1 in PROG:
        if overlaps(s,e,p0,p1): return f"{pid} {nm}"
    return "UNASSIGNED"
def cue_of(s,e):
    hits=[c for c,c0,c1 in CUES if overlaps(s,e,c0,c1)]
    return hits or ["NONE"]

S=[]
S.append("artifact_id: EDITORIAL_SYNCHRONIZATION")
S.append("artifact_class: FIFTH_AUTHORITATIVE_PRODUCTION_ARTIFACT   # per ADR-009 section 2")
S.append("version: 1.1.0   # regenerated under Executive Ruling ESS-004")
S.append(f"run_id: {RUN_ID}")
S.append(f"regeneration_run_id: {REGEN_RUN_ID}")
S.append(f"regenerated_under_ruling: {RULING['id']} ({RULING['date']}, session {RULING['session']})")
S.append("regeneration_policy: >-")
S.append(blk("Never hand-edited. Regenerate on any source-hash mismatch. This artifact is a fusion of "
             "things that already exist under governance; it creates no new authority.", 2))
S.append("timebase:")
S.append(f"  lock_duration_s: {LOCK}")
S.append("  declared_lock_tc: \"01:20:46:14\"")
S.append("  fps: 24")
S.append("  offset_model: {value_s: 0.000, drift_s_per_s: 0.000, status: CLOSED, evidence: STEP0_TIMING_CLOSURE.md}")
S.append("sources:")
for k,role in (("fcpxml","locked FCPXML - editorial ground truth"),("etc","Editorial Timing Contract"),
               ("srt","canonical lock SRT (GT-2) - evidence of speech"),
               ("mp4","master proxy - visual ground truth (320x180)")):
    S.append(f"  - {{id: {k}, sha256: {SHA[k]}, role: {y(role)}}}")
S.append("  - {id: TIMELINE_REGISTRY, version: 1.0.0, role: segment authority}")
S.append("  - {id: DOCUMENTARY_PROGRESSION, version: 1.0.0, role: progression authority}")
S.append("  - {id: ENERGY_CURVE, version: 1.0.0, role: energy authority (observables-derived)}")
S.append("  - {id: VOICE_OVER_REGISTRY, version: 0.1.0, role: host-speech boundaries}")
S.append("  - {id: CAPTION_REGISTRY, version: 0.2.0, role: caption authority (enriched this run)}")
S.append("  - {id: LOCATION_REGISTRY, version: 1.0.0, role: location authority}")
S.append("  - {id: RIDER_REGISTRY, version: 1.0.0, role: person authority (reference only)}")
S.append("  - {id: VISUAL_EVENT_REGISTRY, version: 1.0.0, role: DIE-V observation (reinforcing, never superseding)}")
S.append("conflict_policy: >-")
S.append(blk("On any disagreement between a governed registry and a visual observation, the row records "
             "CONFLICTED and the registry value remains authoritative. Nothing is silently reconciled.", 2))
S.append("")
S.append("rows:")
rown=0
allspans=[(sid,s,e,act,loc,who) for sid,s,e,act,loc,who in SEG]
for a,b in seg_gaps:
    allspans.append((f"GAP-{mmss(a)}",a,b,"unsegmented_in_TIMELINE_REGISTRY",None,[]))
allspans.sort(key=lambda x:x[1])
for sid,s,e,act,loc,who in allspans:
    rown+=1
    ve=[x for x in E if overlaps(s,e,x['span']['start_s'],x['span']['end_s'])]
    caps=[t for t in titles_d1+titles_d2 if overlaps(s,e,t['abs_in_s'],t['abs_out_s'])]
    aud=[x for x in audio16 if overlaps(s,e,x['abs_in_s'],x['abs_out_s'])]
    vos=[v for v in VO if overlaps(s,e,v[1],v[2])]
    ncue=sum(1 for c in [1] for cc in [None])
    srtn=0
    S.append(f"  - row_id: ESS-{rown:03d}")
    S.append(f"    segment_ref: {sid}")
    S.append(f"    WHEN: {{start_s: {round(s,3)}, end_s: {round(e,3)}, start_tc: {tc(s)}, end_tc: {tc(e)}, "
             f"duration_s: {round(e-s,3)}, timebase: CLOSED}}")
    S.append(f"    WHERE: {{location_ref: {y(loc or 'UNSPECIFIED_IN_REGISTRY')}, "
             f"authority: LOCATION_REGISTRY}}")
    S.append(f"    WHO: {{registry_ids: {y(', '.join(who) if who else 'NONE_ASSERTED')}, "
             f"authority: RIDER_REGISTRY/ORGANIZATION_REGISTRY, "
             f"identification_method: registry_reference_only_no_biometrics}}")
    S.append(f"    WHAT: {{activity: {act}, authority: TIMELINE_REGISTRY, "
             f"progression: {y(prog_of(s,e))}, energy: {ENERGY.get(sid,'NULL')}, "
             f"energy_authority: ENERGY_CURVE}}")
    S.append(f"    WHAT_THE_AUDIENCE_SEES:")
    if ve:
        for x in ve:
            S.append(f"      - {{visual_event: {x['id']}, class: {x['event_class']}, "
                     f"confidence: {x['confidence']}, span_s: [{x['span']['start_s']}, {x['span']['end_s']}]}}")
    else:
        S.append("      - {visual_event: NONE, class: NO_DIE_V_EVENT_INTERSECTS_THIS_SPAN, "
                 "confidence: NOT_APPLICABLE}")
    S.append(f"    captions_on_screen: {len(caps)}")
    if caps:
        S.append("    caption_refs:")
        for t in caps[:12]:
            S.append(f"      - {{text: {y(t['text'][:60])}, in_s: {t['abs_in_s']}, out_s: {t['abs_out_s']}}}")
        if len(caps)>12: S.append(f"      - {{note: {len(caps)-12} further captions in span, see CAPTION_REGISTRY}}")
    S.append(f"    existing_audio_elements_in_span: {len(aud)}")
    if aud:
        S.append("    audio_element_refs:")
        for x in aud:
            S.append(f"      - {{name: {y(x['name'])}, in_s: {x['abs_in_s']}, out_s: {x['abs_out_s']}, "
                     f"classification: {aud_class(x['name'])}}}")
    S.append(f"    voice_over_windows: {y(', '.join(v[0]+' '+v[3] for v in vos) if vos else 'NONE')}")
    S.append(f"    cue_coverage: {y(', '.join(cue_of(s,e)))}")
    S.append(f"    source_refs: {{fcpxml: {SHA['fcpxml'][:16]}, etc: {SHA['etc'][:16]}, "
             f"srt: {SHA['srt'][:16]}, proxy: {SHA['mp4'][:16]}}}")
    st="CONFIRMED"
    if sid=="S16": st="CONFLICTED"
    if sid=="S05": st="CONFLICTED"
    if sid.startswith("GAP-"): st="UNSEGMENTED"
    S.append(f"    state: {st}")
    if st=="CONFLICTED":
        S.append(f"    conflict_ref: {'VCONF-01' if sid=='S16' else 'VCONF-02'}")
        S.append("    authoritative_value: registry")
S.append("")
S.append("unsegmented_spans:")
for a,b in seg_gaps:
    S.append(f"  - {{start_s: {round(a,3)}, end_s: {round(b,3)}, duration_s: {round(b-a,3)}, "
             f"start_tc: {tc(a)}, end_tc: {tc(b)}, state: UNSEGMENTED_IN_TIMELINE_REGISTRY}}")
S.append(f"coverage:")
S.append(f"  rows: {rown}")
S.append(f"  segment_covered_s: {round(seg_cov,3)}")
S.append(f"  unsegmented_s: {round(gap_total,3)}")
S.append(f"  total_s: {LOCK}")
S.append(f"  coverage_fraction: {round(seg_cov/LOCK,4)}")
S.append("status: COMPLETE")
open(OUT+"/EDITORIAL_SYNCHRONIZATION.yaml","w").write(yamlsafe(HDR+"\n".join(S)+"\n"))
print("wrote EDITORIAL_SYNCHRONIZATION.yaml", rown, "rows;", round(gap_total,1),"s unsegmented")

# ------------------------------------------------------- CONDUCTOR_SCORE -----
def parse_srt(p):
    out=[]
    for b in re.split(r'\n\s*\n', open(p,encoding='utf-8-sig').read().strip()):
        Ls=[x for x in b.strip().split('\n') if x.strip()]
        if len(Ls)<2: continue
        m=re.match(r'(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)',Ls[1])
        if not m: continue
        g=[int(x) for x in m.groups()]
        out.append(dict(i=int(Ls[0]),s=g[0]*3600+g[1]*60+g[2]+g[3]/1000,
                        e=g[4]*3600+g[5]*60+g[6]+g[7]/1000,t=' '.join(Ls[2:])))
    return out
CU=parse_srt(U+"inputs/lock_srt2.srt")
def speech_stats(a,b):
    ins=[c for c in CU if c['s']<b and c['e']>a]
    if len(ins)<2: return dict(n=len(ins),cov=0.0,gaps=[])
    gaps=[]
    prev=max(a,ins[0]['e'])
    for c in ins[1:]:
        g=c['s']-prev
        if g>0: gaps.append((prev,c['s'],g))
        prev=max(prev,c['e'])
    if b-prev>0: gaps.append((prev,b,b-prev))
    cov=sum(min(b,c['e'])-max(a,c['s']) for c in ins)/(b-a)
    return dict(n=len(ins),cov=cov,gaps=gaps)
def lyric_windows(a,b,minlen=8.0):
    st=speech_stats(a,b)
    return [(round(g0,3),round(g1,3),round(g,3)) for g0,g1,g in st['gaps'] if g>=minlen]
def rebuild_budget(a,b):
    st=speech_stats(a,b)
    gs=sorted(g for _,_,g in st['gaps'])
    if not gs: return None,None,None
    import statistics
    p10=gs[max(0,int(0.10*len(gs))-0)] if gs else None
    return round(float(np.median(gs)),3), round(float(p10),3), len(gs)

FAM={
 "CONVERSATION": dict(colour="Soul/Americana", instr="muted electric guitar comping (no lead) - "
   "rimshot-centred groove - upright-feel bass - subtle organ swell", tempo="98 BPM",
   tonality="warm major / Mixolydian; no minor-key tension", forbid="no horns, no vocals of any kind, "
   "no builds, no drops, no risers"),
 "MOTION": dict(colour="Road/Drive", instr="driving kit with a steady eighth-note floor - electric "
   "bass locked to kick - rhythm guitar figure - restrained brass or organ stabs at phrase heads",
   tempo="derive from the cut's own rhythm; do not fight the engine bed", tonality="major with modal "
   "brightness", forbid="no lyric content over law-enforcement escort imagery; no stingers on cuts"),
 "CELEBRATION": dict(colour="Groove/Party", instr="full kit, syncopated bass, clav or rhodes comping, "
   "horn section permitted", tempo="mid-up, danceable", tonality="major, bright",
   forbid="no ballad turns; must not swamp ambient engine and crowd sound"),
 "REFLECTION": dict(colour="Warm/Intimate", instr="fingerpicked or clean electric guitar, pad, brushed "
   "kit or no kit, low strings", tempo="slow to mid", tonality="warm major or dorian",
   forbid="no percussion transients that read as an event; no builds"),
 "LEGACY": dict(colour="Anthem/Resolve", instr="anthem kit, sustained low strings or organ, single "
   "melodic voice, optional lead vocal", tempo="mid, unhurried", tonality="major, resolving",
   forbid="no fade-out on the final cue - it resolves"),
}
CUEMETA={
 "CUE-01": ("ARRIVAL_AMBIENT","REFLECTION",2,"Exists to invite"),
 "CUE-02a":("GAUNTLET_BED_I","CONVERSATION",3,"Exists to yield"),
 "CUE-02b":("GAUNTLET_BED_II","CONVERSATION",3,"Exists to renew attention"),
 "CUE-02c":("GAUNTLET_BED_III","CONVERSATION",3,"Exists to lean forward"),
 "CUE-03": ("ESCORT_ANTHEM","MOTION",5,"Exists to transition arrival into shared momentum"),
 "SIL-01": ("CIVIC_SILENCE",None,0,"Exists as absence"),
 "CUE-04": ("GAUNTLET_TWO_BED","CONVERSATION",3,"Exists to warm the return"),
 "SIL-02": ("HONORS_SILENCE",None,0,"Exists as reverence"),
 "CUE-05": ("PHOTO_LIFT","REFLECTION",3,"Exists to exhale"),
 "CUE-06": ("DAY_WRAP_BRIDGE","REFLECTION",3,"Exists to close the day and promise the night"),
 "CUE-07": ("RIDE_PASSAGE","MOTION",4,"Exists to breathe"),
 "CUE-08": ("NIGHT_ARRIVALS","CELEBRATION",4,"Exists to gather"),
 "CUE-09a":("BIKE_NIGHT_PEAK_I","CELEBRATION",5,"Exists to celebrate"),
 "CUE-09b":("BIKE_NIGHT_PEAK_II","CELEBRATION",5,"Exists to sustain"),
 "CUE-10": ("VICTORY_CLOSE","LEGACY",4,"Exists to resolve"),
}
K=[]
K.append("artifact_id: CONDUCTOR_SCORE")
K.append("engine: MIE   # remains under MIE per ADR-009 section 3 - musical intent made executable")
K.append("version: 1.1.0   # regenerated under Executive Ruling ESS-004")
K.append(f"run_id: {RUN_ID}")
K.append(f"regeneration_run_id: {REGEN_RUN_ID}")
K.append(f"regenerated_under_ruling: {RULING['id']} ({RULING['date']}, session {RULING['session']})")
K.append("status: ADVISORY_UNTIL_CUE_PDRS   # Human Editorial Authority; nothing here is a verdict")
K.append("scope_declaration: >-")
K.append(blk("This artifact defines musical BEHAVIOUR, not musical CONTENT. No music was generated, "
             "no audio was synthesised, and no candidate was selected. Every reconciliation verdict "
             "below is a CANDIDATE for a human PDR.", 2))
K.append("pinned_to:")
K.append(f"  etc_sha256: {SHA['etc']}")
K.append(f"  fcpxml_sha256: {SHA['fcpxml']}")
K.append(f"  srt_sha256: {SHA['srt']}")
K.append(f"  proxy_sha256: {SHA['mp4']}")
K.append(f"  lock_duration_s: {LOCK}")
K.append("  offset_model: {value_s: 0.000, status: CLOSED, evidence: STEP0_TIMING_CLOSURE.md}")
K.append("  regenerate_on_mismatch: true")
K.append("consumes:")
K.append("  - EDITORIAL_SYNCHRONIZATION v1.0.0")
K.append("  - CUE_SHEET_v1.1 (MIE_CUE_SHEET 1.1.0)")
K.append("  - CUE-02A_SPEC (the only cue whose behaviour figures are already specified)")
K.append("")
K.append("global_behaviour_law:")
K.append("  yield_law: >-")
K.append(blk("Any cue whose family is CONVERSATION is a bed under speech and must yield. Ducking target "
             "-18 dB under dialogue, carried forward from CUE-02A_SPEC, which is the only PDR-adjacent "
             "figure in evidence. Between answers a bed may breathe upward no more than +3 dB and must "
             "return before the next question lands. Fail condition: at -18 dB under two minutes of "
             "gauntlet audio, any word requiring effort fails the candidate regardless of musical merit.", 4))
K.append("  speech_band_rule: keep approximately 1-4 kHz uncluttered in every cue that runs under speech")
K.append("  silence_law: >-")
K.append(blk("SIL-01, SIL-02 and the R46 carve-out are CONDUCTED SILENCES, not gaps in the score. They "
             "carry behaviour states of their own - an approach, a floor, and a return - and the "
             "conductor is responsible for the shape of the exit and the re-entry either side of them. "
             "DEFINITION (Executive Ruling ESS-004, 2026-08-22): " + RULING['definition'] + " "
             "The compliance test is PROVENANCE, not acoustics - " + RULING['test'], 4))
K.append("  vo_rule: >-")
K.append(blk("Voice-over windows (VOICE_OVER_REGISTRY VO01-VO04) duck like dialogue. VO is excluded by "
             "the Director's Notes from every silence zone, so no cue needs to plan for VO inside "
             "SIL-01, SIL-02 or the R46 carve-out.", 4))
K.append("")
K.append("cues:")
for cid,c0,c1 in CUES:
    nm,fam,en,reason = CUEMETA[cid]
    st=speech_stats(c0,c1)
    med,p10,ngaps = rebuild_budget(c0,c1)
    lw=lyric_windows(c0,c1)
    aud=[x for x in audio16 if overlaps(c0,c1,x['abs_in_s'],x['abs_out_s'])]
    ve=[x for x in E if overlaps(c0,c1,x['span']['start_s'],x['span']['end_s'])
        and x['derivation']=="MODEL_MEDIATED_FRAME_OBSERVATION"]
    K.append(f"  - id: {cid}")
    K.append(f"    name: {nm}")
    K.append(f"    reason_for_existing: {y(reason)}")
    if fam:
        K.append(f"    road_soul_family: {fam}")
        K.append(f"    energy_target: {en}")
    else:
        K.append("    road_soul_family: NONE   # conducted silence")
        K.append("    energy_target: 0")
    K.append(f"    boundaries: {{start_s: {float(c0):.3f}, end_s: {float(c1):.3f}, "
             f"start_tc: {tc(c0)}, end_tc: {tc(c1)}, duration_s: {float(c1-c0):.3f}, timebase: CLOSED}}")
    K.append(f"    speech_context: {{srt_cues_in_span: {st['n']}, speech_coverage: {st['cov']:.3f}, "
             f"inter_cue_gaps: {ngaps or 0}, median_gap_s: {med if med is not None else 'NULL'}, "
             f"tight_gap_s_p10: {p10 if p10 is not None else 'NULL'}}}")
    K.append("    behaviour_states:")
    if cid.startswith("SIL"):
        K.append("      - {state: APPROACH, window_s: 6.0, action: \"reduce to floor before the boundary; "
                 "the last musical event must land clear of the first word inside the zone\"}")
        K.append("      - {state: FLOOR, action: \"absolute silence - no bed, no pad, no tail, no reverb "
                 "return bleeding across the boundary\"}")
        K.append("      - {state: RETURN, window_s: 4.0, action: \"re-entry begins only after the last "
                 "word of the zone; enter under picture, never on a cut\"}")
    elif fam=="CONVERSATION":
        K.append("      - {state: ENTER, action: \"fade-in <=2s under the preceding handoff; never a "
                 "downbeat announcement\"}")
        K.append("      - {state: SUSTAIN, action: \"loop-stable; zero builds, zero drops, zero risers - "
                 "the bed does not editorialize; the Q-cadence IS the percussion\"}")
        K.append(f"      - {{state: DUCK, target_db: -18, sidechain: dialogue, action: \"duck on every "
                 f"answer onset\"}}")
        K.append(f"      - {{state: BREATHE, max_gain_db: +3, permitted_between_answers: true}}")
        K.append(f"      - {{state: REBUILD, budget_s: {p10 if p10 is not None else 'NULL'}, "
                 f"action: \"return to bed level within the tight-gap budget measured for this span; "
                 f"the median gap is {med if med is not None else 'NULL'} s, so the budget is set by the "
                 f"10th-percentile gap, not the median\"}}")
        K.append("      - {state: HANDOFF, action: \"crossfade <=4s at a phrase boundary; inaudible as "
                 "an event\"}")
    elif fam in ("MOTION","CELEBRATION"):
        K.append("      - {state: ENTER, action: \"enter under picture on a movement, not on a cut; "
                 "<=2s\"}")
        K.append("      - {state: LEAD, action: \"music carries the span; ambient engine and crowd sound "
                 "sit under it but must remain audible\"}")
        K.append("      - {state: DUCK, target_db: -12, sidechain: \"voice-over and any diegetic "
                 "announcement only\"}")
        K.append(f"      - {{state: REBUILD, budget_s: {p10 if p10 is not None else 'NULL'}}}")
        K.append("      - {state: HANDOFF, action: \"resolve on the last phrase before the boundary; do "
                 "not fade under the following cue's entry\"}")
    else:
        K.append("      - {state: ENTER, action: \"fade-in <=3s; the audience is being taught how to come "
                 "back\"}")
        K.append("      - {state: SUSTAIN, action: \"steady, unhurried; no event-shaped gestures\"}")
        K.append("      - {state: DUCK, target_db: -15, sidechain: dialogue_and_vo}")
        K.append(f"      - {{state: REBUILD, budget_s: {p10 if p10 is not None else 'NULL'}}}")
        K.append("      - {state: HANDOFF, action: \"crossfade <=4s\"}")
    if fam:
        f=FAM[fam]
        K.append("    instrumentation_guidance:")
        K.append(f"      colour: {y(f['colour'])}")
        K.append(f"      instruments: {y(f['instr'])}")
        K.append(f"      tempo: {y(f['tempo'])}")
        K.append(f"      tonality: {y(f['tonality'])}")
        K.append(f"      prohibited: {y(f['forbid'])}")
    K.append(f"    lyric_opportunity_windows:   # measured: no SRT cue present for >=8.0 s")
    if lw:
        for a,b,g in lw[:8]:
            K.append(f"      - {{start_s: {a}, end_s: {b}, duration_s: {g}, start_tc: {tc(a)}}}")
        if len(lw)>8: K.append(f"      - {{note: {len(lw)-8} further windows in span}}")
    else:
        K.append("      - NONE   # span carries continuous speech; no lyric content may be placed here")
    K.append(f"    visual_events_in_span: {y(', '.join(x['id'] for x in ve) or 'NONE')}")
    K.append(f"    existing_audio_elements_in_span: {len(aud)}")
    if aud:
        K.append("    reconciliation_candidates:")
        for x in aud:
            cl=aud_class(x['name'])
            if cl=="SCORE_ASSET":
                verdict="ADJUST_CANDIDATE"
                why=("existing score asset; its out-point at 00:01:16.417 runs 3.417 s past the CUE-01 "
                     "boundary of 01:13 - the cue in/out binds to the closed ETC, so either the cue "
                     "boundary or the element out-point must move")
            elif cl=="CONTRIBUTED_VIDEO_AUDIO":
                verdict="KEEP_PERMITTED"
                why=("audio of a contributed video - part of the documentary record, NOT a WE CAPE-added "
                     "score asset. Under Executive Ruling ESS-004 (2026-08-22) it is PERMITTED inside a "
                     "mandatory-silence window: the test is provenance, not acoustics. ELS-001 confirmed "
                     "the span is a composite production soundscape; that finding does not change the "
                     "verdict because diegesis is not the test. Previously ESCALATE_UNCERTAIN (D-18) - "
                     "now resolved")
            else:
                verdict="KEEP_CANDIDATE"
                why=("detached production audio from P2_CHRONO_SETS Original Media, not score; the "
                     "route-map animation audio whose picture is observed at 00:27:12-00:27:21; a music "
                     "cue must sit under it, not replace it")
            K.append(f"      - {{element: {y(x['name'])}, in_s: {x['abs_in_s']}, out_s: {x['abs_out_s']}, "
                     f"classification: {cl}, verdict: {verdict}, basis: {y(why)}, "
                     f"authority: HUMAN_PDR_REQUIRED}}")
    K.append("    transition_out: >-")
    K.append(blk("Crossfade at a phrase boundary unless the next entry is a conducted silence, in which "
                 "case the APPROACH state governs and nothing may tail across the boundary.", 6))
K.append("")
_incue=set()
for cid,c0,c1 in CUES:
    for x in audio16:
        if overlaps(c0,c1,x['abs_in_s'],x['abs_out_s']): _incue.add(x['abs_in_s'])
_out=[x for x in audio16 if x['abs_in_s'] not in _incue]
K.append("audio_elements_outside_any_cue_or_silence_note: >-")
K.append(blk("These existing audio-lane elements fall in spans the cue sheet does not cover. They are "
             "reconciled here so that the count of elements addressed equals the count of elements "
             "present - an element silently absent from the score would be exactly the kind of gap this "
             "sprint exists to prevent.", 2))
K.append("audio_elements_outside_any_cue_or_silence:")
for x in _out:
    K.append(f"  - {{element: {y(x['name'])}, in_s: {x['abs_in_s']}, out_s: {x['abs_out_s']}, "
             f"classification: {aud_class(x['name'])}, verdict: KEEP_CANDIDATE, "
             f"basis: {y('detached production audio in a span carrying no cue and no conducted silence; nothing to reconcile against until a cue is written there')}, "
             f"authority: HUMAN_PDR_REQUIRED}}")
K.append(f"audio_elements_addressed: {len(audio16)}")
K.append("silence_law_definition:")
K.append("  ruling: " + RULING['id'])
K.append("  date: " + RULING['date'])
K.append("  authority: " + RULING['authority'])
K.append("  session: " + RULING['session'])
K.append("  prohibits: WE_CAPE_ADDED_NON_DIEGETIC_SCORE")
K.append("  permits: [speech, ambience, engine_noise, wind, source_audio_of_the_documentary_record]")
K.append("  statement: >-")
K.append(blk(RULING['definition'], 4))
K.append("  compliance_test: >-")
K.append(blk(RULING['test'], 4))
K.append("  override: an Executive PDR may direct otherwise for a specific element")
K.append("")
K.append("silence_law_encoding:")
K.append("  - {id: SIL-01, name: CIVIC_SILENCE, start_s: 1903.000, end_s: 2332.000, "
         "start_tc: 00:31:43.000, end_tc: 00:38:52.000, mode: MANDATORY_SILENCE, "
         "states: [APPROACH, FLOOR, RETURN], conducted: true}")
K.append("  - {id: SIL-02, name: HONORS_SILENCE, start_s: 3124.000, end_s: 3229.000, "
         "start_tc: 00:52:04.000, end_tc: 00:53:49.000, mode: MANDATORY_SILENCE, "
         "states: [APPROACH, FLOOR, RETURN], conducted: true}")
K.append("  - id: R46-CARVE-OUT")
K.append("    name: R46_FULL_OUT")
K.append("    start_s: 2347.000")
K.append("    end_s: 2399.000")
K.append("    start_tc: 00:39:07.000")
K.append("    end_tc: 00:39:59.000")
K.append("    mode: FULL_OUT_WITHIN_CUE")
K.append("    parent_cue: CUE-04")
K.append("    states: [APPROACH, FLOOR, RETURN]")
K.append("    conducted: true")
K.append("    note: >-")
K.append(blk("The carve-out sits inside CUE-04, so the bed must step out and return within a live cue "
             "rather than between cues. Observed in picture: the second gauntlet's question cards run "
             "at 00:39:06, 00:39:18, 00:39:33 and 00:39:39 - inside the carve-out. The bed's APPROACH "
             "must therefore clear the 00:39:06 card, and the RETURN must not land on the 00:39:39 "
             "card's answer.", 6))
K.append("")
K.append("silence_law_integrity_findings:")
K.append("  - id: SLF-01")
K.append("    finding: >-")
K.append(blk("One existing audio-lane element, NOTOR1OUS_CARAVAN_2_, occupies 00:33:37.708-00:34:39.667 "
             "- 61.958 s lying entirely inside SIL-01. RE-001 classified it UNCERTAIN and escalated it "
             "rather than judging it. ELS-001 (2026-08-22) determined by listening that the span is a "
             "composite production soundscape including music/vocals, engine rumble, wind and speech, "
             "and expressly declined to conclude that the musical content is exclusively editorial.", 6))
K.append("    resolution: >-")
K.append(blk("RESOLVED by Executive Ruling ESS-004, 2026-08-22. The element's provenance is a contributed "
             "video - part of the documentary record, not a WE CAPE-added score asset - and the ruling "
             "makes provenance the test. The element is PERMITTED and SIL-01 is INTACT. The diegesis "
             "question that blocked RE-001 is not merely answered, it is retired: it was never the "
             "right question.", 6))
K.append("    state: RESOLVED")
K.append("  - id: SLF-02")
K.append("    finding: >-")
K.append(blk("SIL-01 opens at 00:31:43 while the mass ride is still on screen. Picture observation "
             "places continuous public-road riding from 00:28:15 to approximately 00:33:00 and "
             "law-enforcement escort presence recurring to 00:31:48. The conducted silence therefore "
             "begins over motion, not over civic speech, and its APPROACH state has to bring the escort "
             "energy down while the ride is still visibly running. That is a conducting problem worth "
             "naming before a cue is written against it.", 6))
K.append("    state: OPEN_TO_PDR")
K.append("")
SILENCE_ZONES=[("SIL-01",1903.0,2332.0),("SIL-02",3124.0,3229.0),("R46-CARVE-OUT",2347.0,2399.0)]
K.append("silence_law_compliance:   # machine-checked under ESS-004; no acoustic judgement involved")
K.append("  method: >-")
K.append(blk("For each silence zone, every audio-lane element intersecting it is classified by the "
             "FCPXML asset media-rep path. A breach requires classification SCORE_ASSET. This check is "
             "reproducible from the locked FCPXML alone and needs neither the master audio nor a "
             "listener.", 4))
_tot_b=0
K.append("  zones:")
for zid,z0,z1 in SILENCE_ZONES:
    inside=[x for x in audio16 if overlaps(z0,z1,x['abs_in_s'],x['abs_out_s'])]
    breach=[x for x in inside if aud_class(x['name'])=="SCORE_ASSET"]
    _tot_b+=len(breach)
    K.append(f"    - id: {zid}")
    K.append(f"      span: {{start_s: {z0}, end_s: {z1}, start_tc: {tc(z0)}, end_tc: {tc(z1)}}}")
    K.append(f"      audio_elements_intersecting: {len(inside)}")
    K.append("      elements:" + ("" if inside else " []"))
    for x in inside:
        K.append(f"        - {{element: {y(x['name'])}, in_s: {x['abs_in_s']}, out_s: {x['abs_out_s']}, "
                 f"classification: {aud_class(x['name'])}, "
                 f"verdict: {'BREACH' if aud_class(x['name'])=='SCORE_ASSET' else 'PERMITTED'}}}")
    K.append(f"      breaches: {len(breach)}")
    K.append(f"      state: {'BREACHED' if breach else 'INTACT'}")
K.append(f"  total_breaches: {_tot_b}")
K.append(f"  covenant_state: {'BREACHED' if _tot_b else 'INTACT'}")
K.append("  note: >-")
K.append(blk("Every audio-lane element sitting inside a mandatory-silence zone in this lock is "
             "documentary-record audio. The lock's only WE CAPE-added score asset, KICKSTANDS UP v1 "
             "(00:00:00.000-00:01:16.417), lies outside every silence zone. The silence law is intact "
             "as cut.", 4))
K.append("")
K.append("uncovered_spans:   # carrying neither a cue nor a mandatory silence")
for a,b in cue_gaps:
    ve=[x for x in E if overlaps(a,b,x['span']['start_s'],x['span']['end_s'])
        and x['derivation']=="MODEL_MEDIATED_FRAME_OBSERVATION"]
    K.append(f"  - {{start_s: {round(a,3)}, end_s: {round(b,3)}, duration_s: {round(b-a,3)}, "
             f"start_tc: {tc(a)}, end_tc: {tc(b)}, "
             f"visual_events: {y(', '.join(x['event_class'] for x in ve[:3]) or 'NONE')}}}")
K.append(f"uncovered_total_s: {round(cue_gap_total,3)}")
K.append("uncovered_note: >-")
K.append(blk("The two largest uncovered spans are 00:29:10-00:31:43 (153 s) and 01:06:48-01:09:25 "
             "(157 s). Both carry continuous riding in picture. Enumerated, not filled: writing cues "
             "into them is a human editorial decision, not an automation output.", 2))
K.append("")
K.append(f"cue_count: {len(CUES)}")
K.append(f"cue_covered_s: {round(cue_cov,3)}")
K.append(f"coverage_fraction: {round(cue_cov/LOCK,4)}")
K.append("music_generated: false")
K.append("candidates_selected: false")
K.append("status: COMPLETE_AS_ADVISORY")
open(OUT+"/CONDUCTOR_SCORE.yaml","w").write(yamlsafe(HDR+"\n".join(K)+"\n"))
print("wrote CONDUCTOR_SCORE.yaml", len(CUES), "cues; uncovered", round(cue_gap_total,1),"s")

# ------------------------------------------------- ESS_VALIDATION_REPORT -----
R=[]
R.append("# ESS_VALIDATION_REPORT.md")
R.append(f"## Sprint 3A Validation - {RUN_ID}\n")
R.append("**Verdict: PASS with three CONFLICTED observations and two items escalated for human "
         "adjudication.** No delta is uncategorized. No music was generated. No biometric identification "
         "was performed. No inferred value was silently substituted for a missing one.\n")
R.append("### 1. Four-source chain\n")
R.append("| link | test | result |")
R.append("|---|---|---|")
R.append(f"| FCPXML -> ETC | ETC `source_sha256` vs computed SHA-256 of Info.fcpxml | **MATCH** "
         f"`{SHA['fcpxml'][:24]}...` |")
R.append("| FCPXML -> ETC | resolver reproduces ETC spine offsets and durations | **191 / 191** within 0.0006 s |")
R.append(f"| FCPXML -> lock | last spine element out-point vs sequence duration | **4846.625 s = 4846.625 s** |")
R.append("| SRT -> ETC | envelope correlation, null-tested | **offset 0.000 s**, p = 0.0 vs null |")
R.append("| SRT -> FCPXML | 11 semantic title/cue anchors over 97.4% of runtime | median **+0.708 s** constant, drift CI contains 0 |")
R.append("| ETC -> picture | 5 title in/outs vs rendered frames at 1.000 s | **5 / 5** within one sample |")
R.append(f"| proxy -> lock | container duration vs sequence | 4846.633 s vs 4846.625 s (**D-05**) |")
R.append("\nThe chain is closed at the hash level in both directions: the ETC names the FCPXML hash this "
         "run computed, and the resolver built from that FCPXML reproduces the ETC's own numbers exactly. "
         "Neither artifact is being taken on trust.\n")
R.append("### 2. Step 0 closure evidence\n")
R.append("- Offset model: **0.000 s, single-valued, no drift.** Two independent methods agree; a third "
         "(picture verification) confirms at frame level.\n")
R.append("- Drift bound: **+0.684 s over 4846.625 s, 95% CI [-0.541, +1.909] s.** Zero is inside the "
         "interval; a 23.976/24 rate error (-4.85 s) is far outside it.\n")
R.append("- The +/-6 s tolerance is discharged. Its origin is identified: the *pre-lock* SRT ran to "
         "01:20:40 against a 01:20:46.625 lock. The lock SRT itself was never shifted.\n")
R.append("- Enabling result: the ETC publishes `timeline_offset_s: null` for all 404 connected elements, "
         "so the 16 audio elements and 40 titles had to be resolved from FCPXML nesting. The resolver "
         "earned the right to be believed by reproducing all 191 spine offsets first.\n")
R.append("### 3. Probe results (fixture validation before registry custody)\n")
R.append("| probe | window | expectation | result | what was actually observed |")
R.append("|---|---|---|---|---|")
R.append("| P1 | 00:27:40-00:29:10 | mass-ride / escort motion | **PASS** | staging-lot mount-up, column "
         "departure, two-abreast public-road formation, marked police vehicle and officer at an "
         "intersection at 00:29:06 |")
R.append("| P2 | 00:52:04-00:53:49 | static crowd / ceremony | **PASS** | interior hall, podium with "
         "venue plate, US flag and standards, framed plaques presented and raised, line of recipients, "
         "wide seated banquet room |")
R.append("| P3 | 01:19:44-end | riding + night | **PASS** | night formation riding, helmet POV, lit "
         "portico arrival, closing card run; five closing title in/outs reproduced in picture |")
R.append("\nP3 did double duty. Because the closing cards are legible in the rendered frames, it is "
         "simultaneously the night/riding fixture and the frame-accuracy evidence for Step 0 - including "
         "for a title nested inside a compound clip, which is the case the resolver was most likely to "
         "get wrong.\n")
R.append("### 4. Coverage reconciliation\n")
R.append("**Events vs runtime**\n")
R.append("| measure | value |")
R.append("|---|---|")
R.append(f"| runtime | {LOCK} s |")
R.append(f"| DIE-V events emitted | {len(E)} |")
R.append("| instrument-derived events | 4 (illumination runs, 100% of runtime) |")
R.append(f"| observation-derived events | {len(E)-4} |")
R.append("| survey frames extracted | 1616 at 3.000 s (100% of runtime) |")
R.append("| contact sheets built / read in full | 54 / 20 |")
R.append("| probe frames extracted | 258 at 1.000 s |")
R.append("| explicit NOT_OBSERVED declarations | %d |"%len(NOT_OBSERVED))
R.append("\n**Sync rows vs spine**\n")
R.append("| measure | value |")
R.append("|---|---|")
R.append(f"| ESS rows | 32 |")
R.append(f"| registry segments covered | 19 of 19 |")
R.append(f"| runtime inside a registry segment | {seg_cov:.3f} s ({seg_cov/LOCK:.1%}) |")
R.append(f"| runtime unsegmented | {gap_total:.3f} s ({gap_total/LOCK:.1%}) across {len(seg_gaps)} spans (D-20) |")
R.append(f"| spine story elements | 191 (ETC) / 214 incl. transitions (FCPXML) (D-06) |")
R.append("\n**Cues vs spine**\n")
R.append("| measure | value |")
R.append("|---|---|")
R.append(f"| cues + silences scored | {len(CUES)} |")
R.append(f"| runtime under a cue or conducted silence | {cue_cov:.3f} s ({cue_cov/LOCK:.1%}) |")
R.append(f"| runtime uncovered | {cue_gap_total:.3f} s ({cue_gap_total/LOCK:.1%}) across {len(cue_gaps)} spans (D-19) |")
R.append(f"| existing audio-lane elements reconciled | {len(audio16)} of {len(audio16)} |")
R.append("| of which score assets | 1 |")
R.append("| of which detached production audio | 14 |")
R.append("| of which contributed-video audio | 1 (escalated) |")
R.append(f"| caption elements enrolled | {len(titles_d1)+len(titles_d2)} (40 ETC-census + 17 newly enrolled) |")
R.append("\n### 5. Conflict ledger\n")
R.append("| id | registry value | observation | state | resolution |")
R.append("|---|---|---|---|---|")
R.append("| VCONF-01 | TIMELINE_REGISTRY S16 labelled `bike_night_arrivals` (00:58:43-01:06:25) | span is "
         "bright daylight; mean luma 130.7; sustained night onset measured at 01:06:24.5 | **CONFLICTED** | "
         "registry authoritative; PDR candidate |")
R.append("| VCONF-02 | S05 / CUE-03 escort ride 00:27:40-00:29:10 (90 s) | mass ride observed "
         "continuously 00:28:15 to approx 00:33:00; escort presence to 00:31:48 | **CONFLICTED** | "
         "registry authoritative; PDR candidate |")
R.append("| VCONF-03 | CAPTION_REGISTRY policy: rider lower-thirds at 75 first-cues | the lock contains "
         "zero rider lower-thirds; on-screen naming is reserved for civic speakers | **CONFLICTED** | "
         "policy line marked SUPERSEDED-BY-EVIDENCE; adding them stays a human decision |")
R.append("| SLF-01 | SIL-01 is mandatory silence 00:31:43-00:38:52 | audio-lane element "
         "NOTOR1OUS_CARAVAN_2_ occupies 00:33:37.708-00:34:39.667 inside it | **UNCERTAIN** | escalated, "
         "not resolved - contributed-video audio, content undetermined, source media offline (D-18, D-22) |")
R.append("| SLF-02 | SIL-01 framed as civic silence | the zone opens over continuous ride footage, not "
         "over speech | **OBSERVATION** | named for the conductor; no registry change |")
R.append("\nThree conflicts, one escalation, one framing note. In every case the registry value stands "
         "and the observation is recorded beside it. That is the whole point of DIE-V being a module "
         "rather than an authority.\n")
R.append("### 6. Delta ledger - full descriptions\n")
R.append("Every measurable difference found anywhere in this run, with a category and a disposition. "
         "An uncategorized delta would be a failure of this sprint; there are none.\n")
for d in LEDGER:
    R.append(f"**{d['id']} - {d['category']}** *(magnitude: {d['magnitude']})*  ")
    R.append(f"{d['description']}  ")
    R.append(f"*Disposition:* {d['disposition']}\n")
R.append("### 7. Constitutional compliance\n")
R.append("| constraint | evidence |")
R.append("|---|---|")
R.append("| No music generated | CONDUCTOR_SCORE declares `music_generated: false`; no audio was "
         "synthesised at any point in the run |")
R.append("| No biometric identification | no face detection or recognition was run. The only person "
         "names in any artifact are text read from FCPXML title elements, carried as caption text |")
R.append("| No sentiment inference | event classes are physical observables only. No emotional, "
         "atmospheric or affective term appears as an event class |")
R.append("| Energy from observables only | ENERGY_CURVE values are carried through from the governed "
         "registry; DIE-V contributes luma, colour ratio, frame-difference energy and shot-change "
         "density, never an energy judgement |")
R.append("| Enrichment namespaces untouched | every DIE-V event carries `enrichment: {nie: {}, mie: {}, "
         "pie: {}}` empty |")
R.append("| Registries outrank visual observation | three conflicts recorded; registry value retained in "
         "all three |")
R.append("| No silent recovery | 12 correlation spans reported INDETERMINATE with reasons rather than "
         "given inferred offsets; one silence-law item escalated as UNCERTAIN rather than judged; "
         "aerial-vs-elevated classified MEDIUM rather than asserted; five explicit NOT_OBSERVED "
         "declarations |")
R.append("| No undocumented assumptions | the proxy-resolution ceiling (D-24) and the sheet-sampling "
         "plan (D-25) are declared in the registry itself, not left implicit |")
R.append("| Frozen documents untouched | only CAPTION_REGISTRY was modified, with the enrichment noted "
         "in its header as the work order permits |")
R.append("\n### 8. Reproducibility envelope (WET-SPEC-DIE-001 section 3)\n")
R.append("| field | value |")
R.append("|---|---|")
R.append(f"| run_id | {RUN_ID} |")
R.append("| specification version | WET-SPEC-DIE-001 v0.2 (frozen tag wet-spec-die-001-v0.2-frozen) |")
R.append("| architecture | ADR-009 (ACCEPTED) |")
R.append(f"| repository commit at launch | {GIT} |")
R.append("| source grades | FCPXML/ETC: editorial ground truth; SRT: GT-2; proxy: derived visual reference |")
R.append("| source hashes | all four recorded in every artifact header |")
R.append("| deterministic | frame extraction, envelope, correlation and null test are seeded "
         "(`numpy.random.default_rng(20260822)`); rerunning the scripts on the same hashes reproduces "
         "the numbers |")
R.append("| model-mediated component | contact-sheet observation; fixture-validated on three probes "
         "before registry custody per DIE-X rule X-5 |")
R.append("\n### 9. What a reviewer should push on\n")
R.append("Three things in this report are weaker than they look, and it is better that the Executive "
         "Team hears it here than discovers it later:\n")
R.append("1. **The envelope correlation is a weak instrument.** Its peak r is 0.278. It is convincing "
         "because the peak is at exactly zero and beats a proper null, and because two independent "
         "methods agree - not because the correlation itself is strong. On its own it would not close "
         "the tolerance.\n")
R.append("2. **The visual ground truth is a 320x180 watermarked proxy.** It is sufficient for "
         "day/night, riding/static, crowd bands, ceremony/formation and reading burned-in titles. It is "
         "not sufficient for formation geometry, flag identification, or separating camera motion from "
         "subject motion. If Sprint 4 wants richer visual events, it needs a better proxy, not a better "
         "prompt.\n")
R.append("3. **Twenty of 54 contact sheets were read in full.** Coverage of the non-gauntlet material is "
         "complete; the two interview gauntlets - 38% of runtime - are covered at span level by "
         "systematic sample. No per-event claim is made inside an unread sheet, but a reviewer should "
         "know the difference.\n")
R.append("### 10. Verdict\n")
R.append("**PASS.** Step 0 closed. Three artifacts produced under the canonical sync_event schema, each "
         "hash-pinned to all four sources. Fifteen cues and three conducted silences encoded as "
         "behaviour. Sixteen of sixteen existing audio elements reconciled as candidates. Twenty-five "
         "deltas, all categorized. Two items escalated to human adjudication rather than resolved by "
         "the implementation.\n")
open(OUT+"/ESS_VALIDATION_REPORT.md","w").write("\n".join(R))
print("wrote ESS_VALIDATION_REPORT.md")

# ------------------------------------------- PRODUCTION_INTELLIGENCE_SEED ----
P=[]
P.append("seed_id: PRODUCTION_INTELLIGENCE_SEED")
P.append("version: 1.0.0")
P.append(f"run_id: {RUN_ID}")
P.append("purpose: >-")
P.append(blk("Factual execution metrics only. This artifact SEEDS the future Production Intelligence "
             "Review and Executive Dashboard; it does not create them, and it contains no analysis, "
             "no judgement and no recommendation.", 2))
P.append("assets_processed:")
P.append(f"  - {{name: Filmage_Editor.mp4, sha256: {SHA['mp4']}, bytes: 399320021, "
         f"duration_s: 4846.633, resolution: 320x180, fps: 30}}")
P.append(f"  - {{name: Info.fcpxml, sha256: {SHA['fcpxml']}, bytes: 4479627, "
         f"sequence_duration_s: {LOCK}, format: 3840x2160p24}}")
P.append(f"  - {{name: \"Alpha RoudUp Part 2_SRT__SRT 2_English (United States).srt\", "
         f"sha256: {SHA['srt']}, bytes: 140526, cues: 2291}}")
P.append(f"  - {{name: P2_LOCK_timing.json, sha256: {SHA['etc']}, bytes: 183116, "
         f"spine_elements: 191, connected_elements: 404}}")
P.append("registries_consumed:")
for r in ["TIMELINE_REGISTRY","DOCUMENTARY_PROGRESSION","ENERGY_CURVE","VOICE_OVER_REGISTRY",
          "CAPTION_REGISTRY","RIDER_REGISTRY","LOCATION_REGISTRY","ORGANIZATION_REGISTRY",
          "MOTORCYCLE_REGISTRY","WHY_I_RIDE_REGISTRY","QUOTE_LIBRARY","PROMPT_REGISTRY",
          "MIE_INPUT_PACKAGE","CUE_SHEET_v1.1","CUE-02A_SPEC"]:
    P.append(f"  - {r}")
P.append("registries_updated:")
P.append("  - {registry: CAPTION_REGISTRY, from_version: 0.1.0, to_version: 0.2.0, "
         "change: position enrichment completed, header_note: present}")
P.append("artifacts_created:")
for f in ["STEP0_TIMING_CLOSURE.md","VISUAL_EVENT_REGISTRY.yaml","EDITORIAL_SYNCHRONIZATION.yaml",
          "CONDUCTOR_SCORE.yaml","ESS_VALIDATION_REPORT.md","PRODUCTION_INTELLIGENCE_SEED.yaml",
          "EXECUTION_LOG.md"]:
    P.append(f"  - {f}")
P.append("metrics:")
P.append(f"  runtime_processed_s: {LOCK}")
P.append("  runtime_processed_tc: \"01:20:46.625\"")
P.append(f"  visual_events_extracted: {len(E)}")
P.append("  visual_events_instrument_derived: 4")
P.append(f"  visual_events_observation_derived: {len(E)-4}")
P.append(f"  not_observed_declarations: {len(NOT_OBSERVED)}")
P.append(f"  synchronization_rows: 32")
P.append(f"  synchronization_coverage_fraction: {round(seg_cov/LOCK,4)}")
P.append(f"  cue_count: {len(CUES)}")
P.append("  conducted_silences: 3")
P.append(f"  cue_coverage_fraction: {round(cue_cov/LOCK,4)}")
P.append(f"  audio_elements_reconciled: {len(audio16)}")
P.append("  audio_elements_score_assets: 1")
P.append("  audio_elements_production_audio: 14")
P.append("  audio_elements_contributed_video_audio: 1")
P.append(f"  caption_elements_enrolled: {len(titles_d1)+len(titles_d2)}")
P.append(f"  caption_elements_newly_enrolled: {len(titles_d2)}")
P.append("  srt_cues_parsed: 2291")
P.append("  etc_elements_resolved: 1025")
P.append("  etc_spine_offsets_validated: \"191/191\"")
P.append(f"  deltas_logged: {len(LEDGER)}")
P.append("  deltas_uncategorized: 0")
P.append("  conflicts_recorded: 3")
P.append("  items_escalated_to_human: 2")
P.append("  probes_run: 3")
P.append("  probes_passed: 3")
P.append("timing_closure_status: CLOSED")
P.append("offset_model: {value_s: 0.000, drift_s_per_s: 0.000, method_count: 3}")
P.append("validation_status: PASS")
P.append("automation_summary:")
P.append("  frames_extracted: 1874   # 1616 survey at 3.000 s + 258 probe at 1.000 s")
P.append("  contact_sheets_built: 57   # 54 survey + 3 probe")
P.append("  contact_sheets_read_in_full: 23")
P.append("  audio_envelope_samples: 19386   # 0.25 s grid")
P.append("  video_observable_samples: 9693  # 0.5 s grid, 9 measures each")
P.append("  correlation_null_trials: 300")
P.append("  semantic_anchors_used: 11")
P.append("  scripts_executed: 6")
P.append("  music_generated: 0")
P.append("  biometric_operations: 0")
P.append("  sentiment_inferences: 0")
P.append("consumes_forward_into: [PRODUCTION_INTELLIGENCE_REVIEW, EXECUTIVE_DASHBOARD]")
P.append("creates_forward_artifacts: false")
open(OUT+"/PRODUCTION_INTELLIGENCE_SEED.yaml","w").write(HDR+"\n".join(P)+"\n")
print("wrote PRODUCTION_INTELLIGENCE_SEED.yaml")
