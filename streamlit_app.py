import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Retrofit Recommender",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #f5f2eb;
    --card: #ffffff;
    --accent: #2d6a4f;
    --accent2: #52b788;
    --accent3: #e9c46a;
    --text: #1a1a2e;
    --muted: #6b7280;
    --border: #e5e0d5;
    --red: #e63946;
    --amber: #e9c46a;
    --green: #2d6a4f;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text) !important;
}

[data-testid="stSidebar"] {
    background-color: #1a1a2e !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #e8e4dc !important;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stRadio > label > div,
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stMultiSelect > label {
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span p {
    color: #e8e4dc !important;
    text-transform: none !important;
    font-size: 0.9rem !important;
    letter-spacing: 0 !important;
}

.stButton > button {
    background-color: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease;
    width: 100%;
}
.stButton > button:hover {
    background-color: #1b4332 !important;
    transform: translateY(-1px);
}

.hero-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d6a4f 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    color: white;
}
.hero-banner h1 {
    color: white !important;
    margin: 0;
    font-size: 2.4rem;
}
.hero-banner p {
    color: #c8f4de;
    margin: 0.5rem 0 0;
    font-size: 1.05rem;
}

.archetype-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    border: 2px solid var(--border);
    cursor: default;
}
.archetype-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
    color: var(--text);
    margin-bottom: 0.3rem;
}
.archetype-meta {
    font-size: 0.78rem;
    color: var(--muted);
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.tag {
    background: #f0faf4;
    border: 1px solid #b7e4c7;
    border-radius: 100px;
    padding: 0.1rem 0.55rem;
    font-size: 0.73rem;
    color: var(--accent);
    font-weight: 500;
}

.rec-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.9rem;
    border-left: 5px solid var(--accent2);
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.rec-card.priority-high  { border-left-color: var(--accent); }
.rec-card.priority-medium { border-left-color: var(--accent3); }
.rec-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text);
    margin-bottom: 0.5rem;
}
.rec-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.5rem;
}
.badge {
    border-radius: 6px;
    padding: 0.15rem 0.55rem;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-green { background: #d8f3dc; color: #1b4332; }
.badge-amber { background: #fef3cd; color: #7d5a00; }
.badge-blue  { background: #dbeafe; color: #1e3a5f; }
.badge-red   { background: #fee2e2; color: #7f1d1d; }
.badge-gray  { background: #f3f4f6; color: #374151; }
.rec-detail  { font-size: 0.8rem; color: var(--muted); }
.rating-pill {
    border-radius: 6px;
    padding: 0.15rem 0.6rem;
    font-size: 0.72rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}
.rating-A  { background: #d8f3dc; color: #1b4332; }  /* green */
.rating-B  { background: #dbeafe; color: #1e3a5f; }  /* blue */
.rating-BC { background: #e0e7ff; color: #3730a3; }  /* indigo */
.rating-C  { background: #fef9c3; color: #713f12; }  /* yellow */
.rating-D  { background: #fed7aa; color: #7c2d12; }  /* orange */
.rating-DE { background: #fecaca; color: #7f1d1d; }  /* light red */
.rating-E  { background: #f3e8ff; color: #581c87; }  /* purple */

.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--text);
    margin: 1.5rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
}

.stat-pill {
    background: #f0faf4;
    border: 1px solid #b7e4c7;
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    display: inline-block;
    font-size: 0.8rem;
    color: var(--accent);
    font-weight: 500;
    margin: 0.2rem;
}

.info-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: #78350f;
    margin-bottom: 1rem;
}

[data-testid="stTabs"] button[role="tab"] {
    color: #3d3d3d !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #2d6a4f !important;
    font-weight: 700 !important;
    border-bottom-color: #2d6a4f !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: #2d6a4f !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────

CLUSTERS = {
    1: {"label": "Archetype 1", "property_type": "House", "wall_insulation": "Partial", "wall_type": "System",  "built_form": "Detached",      "tenure": "Rental (Private)",  "construction_age": "1900-1949", "floor_area": 77.7,  "imd_decile": 2, "income": 34951},
    2: {"label": "Archetype 2", "property_type": "House", "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "Semi-Detached", "tenure": "Owner Occupied",    "construction_age": "1900-1949", "floor_area": 134.6, "imd_decile": 0, "income": 47848},
    3: {"label": "Archetype 3", "property_type": "House", "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "Detached",      "tenure": "Rented (Private)",  "construction_age": "1900-1949", "floor_area": 46.7,  "imd_decile": 2, "income": 30876},
    4: {"label": "Archetype 4", "property_type": "House", "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "Mid-Terrace",   "tenure": "Owner Occupied",    "construction_age": "1900-1949", "floor_area": 47.6,  "imd_decile": 3, "income": 38518},
    5: {"label": "Archetype 5", "property_type": "Flat",  "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "End Terrace",   "tenure": "Rental (Social)",   "construction_age": "1950-2002", "floor_area": 46.9,  "imd_decile": 0, "income": 32923},
    6: {"label": "Archetype 6", "property_type": "House", "wall_insulation": "None",    "wall_type": "Cavity",  "built_form": "Detached",      "tenure": "Owner Occupied",    "construction_age": "1900-1949", "floor_area": 23.3,  "imd_decile": 1, "income": 33125},
    7: {"label": "Archetype 7", "property_type": "House", "wall_insulation": "Full",    "wall_type": "Cavity",  "built_form": "Semi-Detached", "tenure": "Owner Occupied",    "construction_age": "1950-2002", "floor_area": 44.8,  "imd_decile": 1, "income": 33804},
    8: {"label": "Archetype 8", "property_type": "House", "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "Detached",      "tenure": "Owner Occupied",    "construction_age": "1900-1949", "floor_area": 267.8, "imd_decile": 6, "income": 36368},
}

SOLUTIONS_RAW = [
    # Category, Solution, Carbon, Energy, Afford, C1..C8
    ("Heating Source", "Mechanical Ventilation with Heat Recovery (high efficiency)",   "A","D","A",  2,0,2,2,2,2,1,1),
    ("Heating Source", "Mechanical Ventilation with Heat Recovery (low efficiency)",    "A","D","B/C",2,0,2,2,2,2,1,1),
    ("Heating Source", "ASHP (small-scale/low-efficiency)",                             "B","A","B",  1,0,2,2,0,1,0,1),
    ("Heating Source", "ASHP (medium-scale/medium efficiency)",                         "C","A","B",  1,0,2,2,0,1,0,1),
    ("Heating Source", "ASHP (large-scale/high efficiency)",                            "C","A","A",  1,0,2,2,0,1,0,1),
    ("Heating Source", "GSHP (small-scale/low efficiency)",                             "B","A","D",  1,0,2,2,0,1,0,1),
    ("Heating Source", "GSHP (medium-scale/medium efficiency)",                         "B","A","C",  1,0,2,2,0,1,0,1),
    ("Heating Source", "GSHP (large-scale/high efficiency)",                            "C","A","B",  1,0,2,2,0,1,0,1),
    ("Heating Source", "WSHP (small-scale/low efficiency)",                             "B","B","B",  1,0,2,2,0,1,0,1),
    ("Heating Source", "WSHP (medium-scale/medium efficiency)",                         "C","B","B",  1,0,2,2,0,1,0,1),
    ("Heating Source", "WSHP (large-scale/high efficiency)",                            "C","B","A",  1,0,2,2,0,1,0,1),
    ("Heating Source", "District Energy Network Heat Exchanger",                        "E","D","B",  2,1,1,2,1,2,2,1),
    ("Smart Heating Controls", "Small-scale",                                           "B","E","A",  2,1,2,2,0,2,1,2),
    ("Smart Heating Controls", "Medium-scale",                                          "B","E","A",  2,1,2,2,0,2,1,2),
    ("Smart Heating Controls", "Large-scale",                                           "B","E","A",  2,1,2,2,0,2,1,2),
    ("LED Lighting", "Small-scale",                                                     "C","D","A",  1,1,2,1,1,2,1,1),
    ("LED Lighting", "Medium-scale",                                                    "C","D","A",  1,1,2,1,1,2,1,1),
    ("LED Lighting", "Large-scale",                                                     "C","D","A",  1,1,2,1,1,2,1,1),
    ("Solar PV", "Solar Photovoltaics",                                                 "C","C","A",  1,0,1,2,2,2,1,2),
    ("Wall Insulation", "External Solid Wall Insulation",                               "","E","",    1,0,1,2,0,0,1,2),
    ("Wall Insulation", "Internal Solid Wall Insulation",                               "","E","",    1,0,1,2,0,0,1,2),
    ("Wall Insulation", "Cavity Wall Insulation (small-scale)",                         "","E","",    1,0,1,2,0,0,1,2),
    ("Wall Insulation", "Cavity Wall Insulation (medium-scale)",                        "","E","",    1,0,1,2,0,0,1,2),
    ("Wall Insulation", "Cavity Wall Insulation (large-scale)",                         "","E","",    1,0,1,2,0,0,1,2),
    ("Glazing", "Triple Glazing – Hardwood frames",                                     "E","D","C",  2,2,1,2,2,2,2,2),
    ("Glazing", "Triple Glazing – uPVC frames",                                         "E","D","C",  2,2,1,2,2,2,2,2),
    ("Glazing", "Triple Glazing – Aluminium frames",                                    "E","D","C",  2,2,1,2,2,2,2,2),
    ("Glazing", "Secondary Glazing – Hardwood frames",                                  "E","D","A",  0,0,2,0,2,1,0,0),
    ("Glazing", "Secondary Glazing – uPVC frames",                                      "E","D","A",  0,0,2,0,2,1,0,0),
    ("Glazing", "Secondary Glazing – Aluminium frames",                                 "E","D","A",  0,0,2,0,2,1,0,0),
    ("Glazing", "Water-filled Glass",                                                   "B/C","B","B",1,2,0,2,0,0,0,1),
    ("Floor Insulation", "Floor Insulation (small-scale)",                              "","E","",    0,0,1,2,0,0,1,2),
    ("Floor Insulation", "Floor Insulation (medium-scale)",                             "","E","",    0,0,1,2,0,0,1,2),
    ("Floor Insulation", "Floor Insulation (large-scale)",                              "","E","",    0,0,1,2,0,0,1,2),
    ("Roof/Loft", "Loft Insulation (small-scale)",                                      "","E","",    0,0,1,2,0,0,1,2),
    ("Roof/Loft", "Loft Insulation (medium-scale)",                                     "","E","",    0,0,1,2,0,0,1,2),
    ("Roof/Loft", "Loft Insulation (large-scale)",                                      "","E","",    0,0,1,2,0,0,1,2),
    ("Roof/Loft", "Draught-proofing (small-scale)",                                     "","E","",    1,0,2,2,0,0,2,2),
    ("Roof/Loft", "Draught-proofing (medium-scale)",                                    "","E","",    1,0,2,2,0,0,2,2),
    ("Roof/Loft", "Draught-proofing (large-scale)",                                     "","E","",    1,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Mineral Wool (Blown-in) – small",                     "B","","A",   1,0,1,2,0,0,1,2),
    ("Wall Insulation Material", "Mineral Wool (Blown-in) – medium",                    "B","","A",   1,0,1,2,0,0,1,2),
    ("Wall Insulation Material", "Mineral Wool (Blown-in) – large",                     "B","","A",   1,0,1,2,0,0,1,2),
    ("Wall Insulation Material", "Spray Foam (closed-cell) – small",                    "D","","B",   0,0,2,2,0,0,0,1),
    ("Wall Insulation Material", "Spray Foam (closed-cell) – medium",                   "C","","A",   0,0,2,2,0,0,0,1),
    ("Wall Insulation Material", "Spray Foam (closed-cell) – large",                    "C","","A",   0,0,2,2,0,0,0,1),
    ("Wall Insulation Material", "EPS Beads – small",                                   "C","","A",   0,0,1,2,0,0,0,1),
    ("Wall Insulation Material", "EPS Beads – medium",                                  "C","","A",   0,0,1,2,0,0,0,1),
    ("Wall Insulation Material", "EPS Beads – large",                                   "B/C","","A", 0,0,1,2,0,0,0,1),
    ("Wall Insulation Material", "EPS Boards – small",                                  "D","","C",   1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "EPS Boards – medium",                                 "C","","B/C", 1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "EPS Boards – large",                                  "C","","B",   1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "Phenolic Foam – small",                               "E","","D",   1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "Phenolic Foam – medium",                              "E","","B/C", 1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "Phenolic Foam – large",                               "D","","B",   1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "Cork – small",                                        "A","","E",   0,0,0,1,0,0,2,2),
    ("Wall Insulation Material", "Cork – medium",                                       "A","","D",   0,0,0,1,0,0,2,2),
    ("Wall Insulation Material", "Cork – large",                                        "A","","C",   0,0,0,1,0,0,2,2),
    ("Wall Insulation Material", "Mineral Wool Boards – small",                         "D","","E",   1,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Mineral Wool Boards – medium",                        "D","","D",   1,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Mineral Wool Boards – large",                         "C","","C",   1,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "PIR/Phenolic/EPS Board – small",                      "D","","E",   0,0,1,0,0,0,1,1),
    ("Wall Insulation Material", "PIR/Phenolic/EPS Board – medium",                     "D","","D",   0,0,1,0,0,0,1,1),
    ("Wall Insulation Material", "PIR/Phenolic/EPS Board – large",                      "C","","C",   0,0,1,0,0,0,1,1),
    ("Wall Insulation Material", "Wood Fibre – small",                                  "A","","E",   2,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Wood Fibre – medium",                                 "A","","D",   2,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Wood Fibre – large",                                  "A","","B/C", 2,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Aerogel Insulation – small",                          "E","","E",   1,0,1,2,0,0,1,1),
    ("Wall Insulation Material", "Aerogel Insulation – medium",                         "E","","D",   1,0,1,2,0,0,1,1),
    ("Wall Insulation Material", "Aerogel Insulation – large",                          "D","","C",   1,0,1,2,0,0,1,1),
    ("Floor Insulation Material", "Mineral Wool Batts (Concrete floor)",                "C","","C",   1,0,0,2,0,0,1,2),
    ("Floor Insulation Material", "Mineral Wool Batts (Suspended timber floor)",        "C","","B",   1,0,0,2,0,0,1,2),
    ("Floor Insulation Material", "Rigid Foam Boards (PIR)",                            "D","","B",   1,0,0,1,0,0,0,1),
    ("Roof/Loft Material", "Mineral Wool/Fibreglass Rolls",                             "C","","A",   1,0,2,2,0,0,1,2),
    ("Roof/Loft Material", "Cellulose (Blown-in)",                                      "B","","A",   1,0,1,2,0,0,1,2),
    ("Roof/Loft Material", "Rigid Boards (PIR/Phenolic)",                               "D/E","","A", 0,0,1,1,0,0,0,1),
]

SOLUTIONS_DF = pd.DataFrame(SOLUTIONS_RAW, columns=[
    "Category", "Solution", "CarbonRating", "EnergyRating", "AffordRating",
    "C1","C2","C3","C4","C5","C6","C7","C8"
])

ARCHETYPE_METRICS = {
    1: {"co2": 3.95, "gap": 14.49, "cost": 12.29},
    2: {"co2": 2.43, "gap": 15.06, "cost": 10.96},
    3: {"co2": 3.48, "gap": 14.52, "cost": 12.07},
    4: {"co2": 4.54, "gap": 19.77, "cost": 13.90},
    5: {"co2": 4.59, "gap": 3.99,  "cost": 10.62},
    6: {"co2": 3.67, "gap": 16.56, "cost": 11.39},
    7: {"co2": 3.43, "gap": 16.28, "cost": 11.45},
    8: {"co2": 9.04, "gap": 39.82, "cost": 26.08},
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def score_label(s):
    if s == 2: return ("Best Solution", "badge-green")
    if s == 1: return ("2nd Best Solution", "badge-amber")
    return ("Not Applicable", "badge-red")

def get_scale_for_built_form(built_form):
    bf = built_form.lower()
    if bf == "detached":
        return "small"
    elif bf in ["semi-detached", "mid-terrace", "enclosed mid-terrace"]:
        return "medium"
    elif bf in ["end terrace", "enclosed end terrace"]:
        return "large"
    return None

def filter_by_scale(df, scale):
    if scale is None or df.empty or "Solution" not in df.columns:
        return df
    scale_keywords = ["small", "medium", "large"]
    def row_matches(solution_name):
        name_lower = solution_name.lower()
        has_any_scale = any(kw in name_lower for kw in scale_keywords)
        if not has_any_scale:
            return True
        return scale in name_lower
    return df[df["Solution"].apply(row_matches)]

def filter_by_wall_type(df, wall_type, wall_insulation=""):
    if df.empty or "Solution" not in df.columns:
        return df
    wt = wall_type.lower() if wall_type else ""

    if wt in ("", "other", "timber", "system"):
        return df  # no wall filtering

    # If wall insulation is none, show all wall solutions regardless of wall type
    wall_ins = wall_insulation.lower() if wall_insulation else ""
    if wall_ins == "none":
        return df
    SOLID_ONLY = [
        "external solid wall insulation",
        "internal solid wall insulation",
        "eps boards",
        "phenolic foam",
        "cork",
        "mineral wool boards",
        "pir/phenolic/eps board",
        "wood fibre",
        "aerogel insulation",
        "mineral wool (small", "mineral wool (medium", "mineral wool (large",
    ]
    CAVITY_ONLY = [
        "cavity wall insulation",
        "mineral wool (blown-in)",
        "spray foam",
        "eps beads",
    ]
    def is_solid_only(sol):
        s = sol.lower()
        return any(k in s for k in SOLID_ONLY)
    def is_cavity_only(sol):
        s = sol.lower()
        return any(k in s for k in CAVITY_ONLY)

    if "solid" in wt:
        return df[~df["Solution"].apply(is_cavity_only)]
    elif "cavity" in wt:
        return df[~df["Solution"].apply(is_solid_only)]
    else:
        return df

def filter_by_floor_type(df, floor_type):
    if df.empty or "Solution" not in df.columns:
        return df
    ft = floor_type.lower() if floor_type else ""
    def row_matches(solution_name):
        s = solution_name.lower()
        if "mineral wool batts" not in s:
            return True
        if "concrete" in ft:
            return "concrete" in s
        elif "timber" in ft or "suspended" in ft:
            return "suspended" in s or "timber" in s
        return True
    return df[df["Solution"].apply(row_matches)]

def get_recommendations_for_archetype(archetype_id, min_score=1):
    col = f"C{archetype_id}"
    df = SOLUTIONS_DF[(SOLUTIONS_DF[col] >= 1) & (SOLUTIONS_DF[col] >= min_score)].copy()
    df = df.sort_values(col, ascending=False)
    return df

def match_archetype(user_props):
    fields = ["property_type", "wall_insulation", "wall_type", "built_form", "tenure", "construction_age"]
    best_archetype = None
    best_score = -1
    for cid, cdata in CLUSTERS.items():
        score = 0
        for f in fields:
            user_val = user_props.get(f, "").lower()
            if user_val in ("", ):
                continue  # skip — don't penalise or reward
            if cdata.get(f, "").lower() == user_val:
                score += 1
        fa_diff = abs(cdata["floor_area"] - user_props.get("floor_area", 80)) / 200
        score -= fa_diff * 0.5
        if score > best_score:
            best_score = score
            best_archetype = cid
    return best_archetype, best_score

def rating_css(r):
    mapping = {"A": "rating-A", "B": "rating-B", "B/C": "rating-BC",
               "C": "rating-C", "D": "rating-D", "D/E": "rating-DE", "E": "rating-E"}
    return mapping.get(r.strip(), "badge-gray")

# Material sub-options for wall insulation types
EXTERNAL_SOLID_MATERIALS = ["eps boards", "phenolic foam", "cork", "mineral wool boards", "mineral wool (small", "mineral wool (medium", "mineral wool (large"]
INTERNAL_SOLID_MATERIALS = ["pir/phenolic/eps board", "wood fibre", "aerogel insulation"]
CAVITY_MATERIALS         = ["mineral wool (blown-in)", "spray foam", "eps beads"]
ALL_WALL_MATERIAL_KEYS   = EXTERNAL_SOLID_MATERIALS + INTERNAL_SOLID_MATERIALS + CAVITY_MATERIALS

def is_wall_material(solution_name):
    s = solution_name.lower()
    return any(k in s for k in ALL_WALL_MATERIAL_KEYS)

def get_sub_materials(solution_name, scale, full_df):
    """Return nested HTML of materials for a wall insulation parent card."""
    sol_lower = solution_name.lower()
    if "external solid" in sol_lower:
        keywords = EXTERNAL_SOLID_MATERIALS
    elif "internal solid" in sol_lower:
        keywords = INTERNAL_SOLID_MATERIALS
    elif "cavity wall insulation" in sol_lower:
        keywords = CAVITY_MATERIALS
    else:
        return ""

    mat_df = full_df[full_df["Category"] == "Wall Insulation"].copy()
    matched = mat_df[mat_df["Solution"].str.lower().apply(
        lambda s: any(k in s for k in keywords)
    )]
    if scale:
        matched = filter_by_scale(matched, scale)

    if matched.empty:
        return ""

    items_html = ""
    for _, mrow in matched.iterrows():
        mc = mrow["CarbonRating"] if mrow["CarbonRating"] else ""
        ma = mrow["AffordRating"] if mrow["AffordRating"] else ""
        mc_html = f'<span class="rating-pill {rating_css(mc)}" style="font-size:0.65rem;">🌿 {mc}</span>' if mc else ""
        ma_html = f'<span class="rating-pill {rating_css(ma)}" style="font-size:0.65rem;">💷 {ma}</span>' if ma else ""
        sol_name = str(mrow["Solution"]).replace("'", "&#39;").replace('"', "&quot;")
        items_html += (
            '<div style="display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:0.5px solid #f0ede6;">'
            f'<span style="font-size:0.8rem; color:#1a1a2e; flex:1;">{sol_name}</span>'
            f'{mc_html}{ma_html}'
            '</div>'
        )

    return (
        '<div style="margin-top:10px; background:#f9f7f4; border-radius:8px; padding:10px 12px;">'
        '<div style="font-size:0.72rem; color:#6b7280; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">Recommended Materials</div>'
        + items_html + '</div>'
    )

def render_solution_card(row, score, scale=None, rec_df=None, col_id=None):
    label, badge_cls = score_label(score)
    priority_cls = "priority-high" if score == 2 else "priority-medium"

    carbon = row["CarbonRating"] if row["CarbonRating"] else ""
    energy = row["EnergyRating"] if row["EnergyRating"] else ""
    afford = row["AffordRating"] if row["AffordRating"] else ""

    carbon_html = f'<span class="rating-pill {rating_css(carbon)}">🌿 Carbon: {carbon}</span>' if carbon else ""
    energy_html = f'<span class="rating-pill {rating_css(energy)}">⚡ Energy: {energy}</span>'   if energy else ""
    afford_html = f'<span class="rating-pill {rating_css(afford)}">💷 Afford: {afford}</span>'   if afford else ""

    sub_html = ""
    if rec_df is not None:
        sub_html = get_sub_materials(row["Solution"], scale, rec_df)

    sol_title = str(row['Solution']).replace("'", "&#39;").replace('"', "&quot;")
    cat_title  = str(row['Category']).replace("'", "&#39;").replace('"', "&quot;")

    st.markdown(f"""
    <div class="rec-card {priority_cls}">
        <div class="rec-title">{sol_title}</div>
        <div class="rec-badges">
            <span class="badge {badge_cls}">{label}</span>
            <span class="badge badge-blue">{cat_title}</span>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
            {carbon_html}{energy_html}{afford_html}
        </div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## How would you like to proceed?")
    st.markdown("---")
    mode = st.radio("Here are your options:", ["Use an Archetype", "Enter my own property details"], index=0)
    st.markdown("---")

    if mode == "Use an Archetype":
        st.markdown("**Select an archetype that best matches your property:**")
        # Use label directly — no '–' split needed
        archetype_options = {cdata["label"]: cid for cid, cdata in CLUSTERS.items()}
        chosen_label = st.selectbox("Archetype", list(archetype_options.keys()))
        chosen_archetype = archetype_options[chosen_label]
        min_score = st.radio("Show recommendations:", ["Best solutions only (score 2)", "All applicable solutions (score 1 & 2)"], index=1)
        min_score_val = 2 if "Best" in min_score else 1
        ask_floor  = st.radio("Would you like floor insulation recommendations?", ["Yes", "No"], index=1, key="ask_floor_arch")
        floor_type = st.selectbox("Floor Type", ["Concrete", "Suspended Timber"], key="ft_arch") if ask_floor == "Yes" else None
        _cats = [c if c != "Wall Insulation Material" else "Wall Insulation"
                 for c in SOLUTIONS_DF["Category"].unique().tolist()
                 if c not in ("Floor Insulation", "Floor Insulation Material")]
        _cats = list(dict.fromkeys(_cats))
        category_filter = st.multiselect("Filter by category", options=_cats, default=_cats, key="cf_arch")
        expanded_filter = []
        for c in category_filter:
            expanded_filter.append(c)
            if c == "Wall Insulation":
                expanded_filter.append("Wall Insulation Material")
        category_filter = expanded_filter
        run = st.button("Get Recommendations →")

    else:
        st.markdown("**Your property details:**")
        prop_type   = st.selectbox("Property Type", ["House", "Flat", "Bungalow", "Maisonette"])
        wall_ins    = st.selectbox("Wall Insulation Status", ["None", "Partial", "Full"])
        wall_type   = st.selectbox("Wall Type", ["Cavity", "Solid", "Timber", "System", "Other"])
        built_form  = st.selectbox("Built Form", ["Detached", "Semi-Detached", "End Terrace", "Mid-Terrace", "Enclosed Mid-Terrace", "Enclosed End Terrace"])
        tenure      = st.selectbox("Tenure", ["Owner Occupied", "Rental (Private)", "Rental (Social)", "Rented (Private)", "Rented (Social)"])
        const_age   = st.selectbox("Construction Age", ["Pre-1900", "1900-1949", "1950-2002", "Post-2002"])
        floor_area  = st.slider("Total Floor Area (m²)", 20, 400, 80)
        ask_floor   = st.radio("Would you like floor insulation recommendations?", ["Yes", "No"], index=1, key="ask_floor_custom")
        floor_type  = st.selectbox("Floor Type", ["Concrete", "Suspended Timber"], key="ft_custom") if ask_floor == "Yes" else None
        min_score   = st.radio("Show recommendations:", ["Best solutions only (score 2)", "All applicable solutions (score 1 & 2)"], index=1)
        min_score_val = 2 if "Best" in min_score else 1
        _cats = [c if c != "Wall Insulation Material" else "Wall Insulation"
                 for c in SOLUTIONS_DF["Category"].unique().tolist()
                 if c not in ("Floor Insulation", "Floor Insulation Material")]
        _cats = list(dict.fromkeys(_cats))
        category_filter = st.multiselect("Filter by category", options=_cats, default=_cats, key="cf_custom")
        expanded_filter = []
        for c in category_filter:
            expanded_filter.append(c)
            if c == "Wall Insulation":
                expanded_filter.append("Wall Insulation Material")
        category_filter = expanded_filter
        run = st.button("Find Matching Archetype & Recommendations →")

# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero-banner">
    <h1>🏠 Retrofit Recommender</h1>
    <p>Provides retrofit solutions for UK residential properties matched to your archetype or property characteristics.</p>
    <p style="margin-top:0.6rem;font-size:0.8rem;color:#a8d5be;letter-spacing:0.04em;">by Sheffield WattWatchers</p>
</div>
""", unsafe_allow_html=True)

if not run:
    st.markdown('<div class="section-header">About the Archetypes</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#3d3d3d;font-size:1rem;margin-bottom:1.2rem;">Each archetype represents a common UK residential property type. Select one in the sidebar or enter your own details to get matched.</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (cid, cdata) in enumerate(CLUSTERS.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="archetype-card">
                <div class="archetype-title">Archetype {cid}</div>
                <div class="archetype-meta">
                    <span class="tag">{cdata['property_type']}</span>
                    <span class="tag">{cdata['built_form']}</span>
                    <span class="tag">{cdata['construction_age']}</span>
                    <span class="tag">{cdata['tenure']}</span>
                </div>
                <div style="margin-top:0.5rem;font-size:0.75rem;color:#6b7280;">
                    ~{cdata['floor_area']} m² · IMD {cdata['imd_decile']} · £{cdata['income']:,}/yr
                </div>
            </div>
            """, unsafe_allow_html=True)

else:
    if mode == "Use an Archetype":
        resolved = chosen_archetype
        match_method = "archetype"
    else:
        user_props = {
            "property_type":    prop_type,
            "wall_insulation":  wall_ins,
            "wall_type":        wall_type,
            "built_form":       built_form,
            "tenure":           tenure,
            "construction_age": const_age,
            "floor_area":       float(floor_area),
        }
        resolved, _ = match_archetype(user_props)
        match_method = "matched"

    cdata  = CLUSTERS[resolved]
    col_id = f"C{resolved}"

    st.markdown(f'<div class="section-header">{"📌 Selected" if match_method=="archetype" else "🎯 Best Matched"} Archetype {resolved}</div>', unsafe_allow_html=True)

    if match_method == "matched":
        st.markdown(f"""
        <div class="info-box">
            Your property characteristics have been matched to <strong>Archetype {resolved}</strong>. You can refine your selections in the sidebar if needed.
        </div>
        """, unsafe_allow_html=True)

    rec_df = get_recommendations_for_archetype(resolved, min_score_val)

    # If wall insulation is None, force-include all wall insulation solutions
    # regardless of cluster score (they may have score 0 for this cluster)
    if match_method == "matched":
        wall_ins_resolved = wall_ins
    else:
        wall_ins_resolved = cdata["wall_insulation"]

    if wall_ins_resolved.lower() == "none":
        wall_cats = ["Wall Insulation", "Wall Insulation Material"]
        extra = SOLUTIONS_DF[SOLUTIONS_DF["Category"].isin(wall_cats)].copy()
        extra[col_id] = extra[col_id].clip(lower=1)  # treat as at least score 1
        rec_df = pd.concat([rec_df, extra]).drop_duplicates(subset=["Solution"]).reset_index(drop=True)

    # Always force-include floor insulation — score is 0 for many clusters but still applicable
    floor_cats = ["Floor Insulation", "Floor Insulation Material"]
    floor_extra = SOLUTIONS_DF[SOLUTIONS_DF["Category"].isin(floor_cats)].copy()
    floor_extra[col_id] = floor_extra[col_id].clip(lower=1)
    rec_df = pd.concat([rec_df, floor_extra]).drop_duplicates(subset=["Solution"]).reset_index(drop=True)

    built_form_resolved = cdata["built_form"]
    scale = get_scale_for_built_form(built_form_resolved)
    rec_df = filter_by_scale(rec_df, scale)

    # Wall type filter
    if match_method == "matched":
        wall_type_resolved = wall_type
    else:
        wall_type_resolved = cdata["wall_type"]
    rec_df = filter_by_wall_type(rec_df, wall_type_resolved, wall_ins_resolved)
    # Remove floor insulation from cluster recommendations — handled separately below
    rec_df = rec_df[~rec_df["Category"].isin(["Floor Insulation", "Floor Insulation Material"])]

    scale_label_map = {"small": "Small-scale", "medium": "Medium-scale", "large": "Large-scale"}
    scale_display = scale_label_map.get(scale, "All scales")

    st.markdown(f'<div class="section-header">✅ Recommendations for Archetype {resolved}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#3d3d3d;font-size:0.85rem;margin-bottom:0.8rem;">Showing <strong>{scale_display}</strong> solutions · Wall type: <strong>{wall_type_resolved}</strong> · Built form: <strong>{built_form_resolved}</strong></p>', unsafe_allow_html=True)

    if rec_df.empty:
        st.info("No recommendations found for the selected filters. Try lowering the minimum score threshold.")
    else:
        strong   = rec_df[rec_df[col_id] == 2]
        consider = rec_df[rec_df[col_id] == 1]
        total    = len(rec_df)

        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <span class="stat-pill">🟢 {len(strong)} Best Solutions</span>
            <span class="stat-pill">🟡 {len(consider)} 2nd Best Solutions</span>
            <span class="stat-pill">📋 {total} Total Applicable</span>
        </div>
        """, unsafe_allow_html=True)

        # Merge "Wall Insulation" and "Wall Insulation Material" into one category
        rec_df["Category"] = rec_df["Category"].replace("Wall Insulation Material", "Wall Insulation")

        categories = list(dict.fromkeys(rec_df["Category"].tolist()))  # preserve order, deduplicate
        tabs = st.tabs(categories + ["All Solutions"])

        for i, cat in enumerate(categories):
            with tabs[i]:
                cat_df       = rec_df[rec_df["Category"] == cat]
                # For Wall Insulation tab: hide individual material rows (they appear nested inside parent cards)
                if cat == "Wall Insulation":
                    cat_df = cat_df[~cat_df["Solution"].apply(is_wall_material)]
                cat_strong   = cat_df[cat_df[col_id] == 2]
                cat_consider = cat_df[cat_df[col_id] == 1]
                if not cat_strong.empty:
                    st.markdown('<p style="color:#2d6a4f;font-weight:700;font-size:1rem;margin-bottom:0.5rem;">🟢 Best Solutions</p>', unsafe_allow_html=True)
                    for _, row in cat_strong.iterrows():
                        render_solution_card(row, 2, scale=scale, rec_df=rec_df, col_id=col_id)
                if not cat_consider.empty:
                    st.markdown('<p style="color:#b45309;font-weight:700;font-size:1rem;margin-bottom:0.5rem;">🟡 2nd Best Solutions</p>', unsafe_allow_html=True)
                    for _, row in cat_consider.iterrows():
                        render_solution_card(row, 1, scale=scale, rec_df=rec_df, col_id=col_id)

        with tabs[-1]:
            st.dataframe(
                rec_df[["Category", "Solution", "CarbonRating", "EnergyRating", "AffordRating", col_id]]
                    .rename(columns={col_id: "Score", "CarbonRating": "Carbon", "EnergyRating": "Energy", "AffordRating": "Affordability"})
                    .reset_index(drop=True),
                use_container_width=True,
                hide_index=True
            )

    st.markdown("---")

    # ── Standalone Floor Insulation Section ──
    if floor_type is not None:
        st.markdown('<div class="section-header">🏗️ Floor Insulation Recommendations</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:#3d3d3d;font-size:0.85rem;margin-bottom:0.8rem;">Based on your floor type: <strong>{floor_type}</strong></p>', unsafe_allow_html=True)

        floor_df = SOLUTIONS_DF[SOLUTIONS_DF["Category"].isin(["Floor Insulation", "Floor Insulation Material"])].copy()
        floor_df = filter_by_floor_type(floor_df, floor_type)
        floor_df = filter_by_scale(floor_df, scale)

        for _, row in floor_df.iterrows():
            carbon = row["CarbonRating"] if row["CarbonRating"] else ""
            energy = row["EnergyRating"] if row["EnergyRating"] else ""
            afford = row["AffordRating"] if row["AffordRating"] else ""
            carbon_html = f'<span class="rating-pill {rating_css(carbon)}">🌿 Carbon: {carbon}</span>' if carbon else ""
            energy_html = f'<span class="rating-pill {rating_css(energy)}">⚡ Energy: {energy}</span>' if energy else ""
            afford_html = f'<span class="rating-pill {rating_css(afford)}">💷 Afford: {afford}</span>' if afford else ""
            st.markdown(f"""
            <div class="rec-card priority-medium">
                <div class="rec-title">{row['Solution']}</div>
                <div class="rec-badges">
                    <span class="badge badge-blue">{row['Category']}</span>
                </div>
                <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
                    {carbon_html}{energy_html}{afford_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

    st.markdown('<div class="section-header">📊 How You Compare to Other Archetypes</div>', unsafe_allow_html=True)

    my       = ARCHETYPE_METRICS[resolved]
    all_co2  = [v["co2"]  for v in ARCHETYPE_METRICS.values()]
    all_gap  = [v["gap"]  for v in ARCHETYPE_METRICS.values()]
    all_cost = [v["cost"] for v in ARCHETYPE_METRICS.values()]
    avg_co2  = round(sum(all_co2)  / len(all_co2),  2)
    avg_gap  = round(sum(all_gap)  / len(all_gap),  2)
    avg_cost = round(sum(all_cost) / len(all_cost), 2)

    def compare_text(val, avg, unit, label, higher_is_worse=True):
        if abs(val - avg) < avg * 0.05:
            return f"Your {label} ({val} {unit}) is <strong>close to the average</strong> ({avg} {unit}) across all archetypes."
        elif (val > avg) == higher_is_worse:
            return f"Your {label} ({val} {unit}) is <strong style='color:#b45309;'>above average</strong> — the average is {avg} {unit}. There is meaningful room for improvement here."
        else:
            return f"Your {label} ({val} {unit}) is <strong style='color:#2d6a4f;'>below average</strong> — the average is {avg} {unit}. You are performing well on this metric."

    co2_text  = compare_text(my["co2"],  avg_co2,  "kgCO₂e/m²", "CO₂ emissions")
    gap_text  = compare_text(my["gap"],  avg_gap,  "",           "efficiency gap")
    cost_text = compare_text(my["cost"], avg_cost, "£/m²",       "energy cost/area")

    metrics_html = f"""
    <div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:1.2rem;">
        <div style="flex:1; min-width:160px; background:#f0faf4; border:1px solid #b7e4c7; border-radius:10px; padding:14px 16px;">
            <div style="font-size:0.75rem; color:#2d6a4f; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">CO₂ Emissions</div>
            <div style="font-size:1.6rem; font-weight:600; color:#1a1a2e;">{my['co2']}</div>
            <div style="font-size:0.78rem; color:#6b7280;">kgCO₂e/m² · avg {avg_co2}</div>
            <div style="margin-top:8px; background:#e5e0d5; border-radius:100px; height:6px;">
                <div style="width:{min(100, round(my['co2'] / max(all_co2) * 100))}%; background:#2d6a4f; height:6px; border-radius:100px;"></div>
            </div>
        </div>
        <div style="flex:1; min-width:160px; background:#fffbeb; border:1px solid #fde68a; border-radius:10px; padding:14px 16px;">
            <div style="font-size:0.75rem; color:#b45309; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">Efficiency Gap</div>
            <div style="font-size:1.6rem; font-weight:600; color:#1a1a2e;">{my['gap']}</div>
            <div style="font-size:0.78rem; color:#6b7280;">score · avg {avg_gap}</div>
            <div style="margin-top:8px; background:#e5e0d5; border-radius:100px; height:6px;">
                <div style="width:{min(100, round(my['gap'] / max(all_gap) * 100))}%; background:#e9c46a; height:6px; border-radius:100px;"></div>
            </div>
        </div>
        <div style="flex:1; min-width:160px; background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; padding:14px 16px;">
            <div style="font-size:0.75rem; color:#1e3a5f; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">Energy Cost / Area</div>
            <div style="font-size:1.6rem; font-weight:600; color:#1a1a2e;">£{my['cost']}</div>
            <div style="font-size:0.78rem; color:#6b7280;">/m² · avg £{avg_cost}</div>
            <div style="margin-top:8px; background:#e5e0d5; border-radius:100px; height:6px;">
                <div style="width:{min(100, round(my['cost'] / max(all_cost) * 100))}%; background:#378add; height:6px; border-radius:100px;"></div>
            </div>
        </div>
    </div>
    <div style="background:#f9f7f4; border:1px solid #e5e0d5; border-radius:10px; padding:1rem 1.2rem; font-size:0.85rem; color:#3d3d3d; line-height:1.8;">
        <div style="margin-bottom:0.4rem;">🌿 {co2_text}</div>
        <div style="margin-bottom:0.4rem;">⚡ {gap_text}</div>
        <div>💷 {cost_text}</div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem;color:#6b7280;margin-bottom:0.8rem;">
        <strong style="color:#3d3d3d;">Score guide:</strong>
        <span style="color:#2d6a4f;font-weight:600;"> 2 = Best Solution</span> ·
        <span style="color:#b45309;font-weight:600;"> 1 = 2nd Best Solution</span> ·
        0 = Not applicable (hidden)
    </div>
    <div style="font-size:0.78rem;color:#3d3d3d;font-weight:600;margin-bottom:0.5rem;">Rating Icons</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:1rem;">
        <span class="rating-pill rating-A">🌿 Carbon Rating</span>
        <span class="rating-pill rating-B">⚡ Energy Rating</span>
        <span class="rating-pill rating-C">💷 Affordability Rating</span>
    </div>
    <div style="font-size:0.78rem;color:#3d3d3d;font-weight:600;margin-bottom:0.6rem;">Rating Scale</div>
    <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:0.4rem;">
        <span class="rating-pill rating-A">A — Best</span>
        <span class="rating-pill rating-B">B — Good</span>
        <span class="rating-pill rating-BC">B/C — Above average</span>
        <span class="rating-pill rating-C">C — Average</span>
        <span class="rating-pill rating-D">D — Below average</span>
        <span class="rating-pill rating-DE">D/E — Poor</span>
        <span class="rating-pill rating-E">E — Worst</span>
    </div>
    """, unsafe_allow_html=True)