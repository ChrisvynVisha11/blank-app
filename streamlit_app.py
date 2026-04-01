import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RetroFit Recommender",
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

/* Archetype card — no hover effect */
.Archetype-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
    border: 2px solid var(--border);
    cursor: default;
}
.Archetype-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
    color: var(--text);
    margin-bottom: 0.3rem;
}
.Archetype-meta {
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
.rating-A  { background: #d8f3dc; color: #1b4332; }
.rating-B  { background: #dcfce7; color: #166534; }
.rating-BC { background: #fef9c3; color: #713f12; }
.rating-C  { background: #fef3cd; color: #7d5a00; }
.rating-D  { background: #fee2e2; color: #7f1d1d; }
.rating-DE { background: #fce7f3; color: #831843; }
.rating-E  { background: #f3e8ff; color: #581c87; }

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
    1: {"label": "Archetype 1 – Older Private Rental Detached",   "property_type": "House", "wall_insulation": "Partial", "wall_type": "System",  "built_form": "Detached",      "tenure": "Rental (Private)",  "construction_age": "1900-1949", "floor_area": 77.7,  "imd_decile": 2, "income": 34951},
    2: {"label": "Archetype 2 – Owner-Occupied Pre-War Semi",      "property_type": "House", "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "Semi-Detached", "tenure": "Owner Occupied",    "construction_age": "1900-1949", "floor_area": 134.6, "imd_decile": 0, "income": 47848},
    3: {"label": "Archetype 3 – Private Rental Pre-War Detached",  "property_type": "House", "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "Detached",      "tenure": "Rented (Private)",  "construction_age": "1900-1949", "floor_area": 46.7,  "imd_decile": 2, "income": 30876},
    4: {"label": "Archetype 4 – Owner-Occupied Pre-War Terrace",   "property_type": "House", "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "Mid-Terrace",   "tenure": "Owner Occupied",    "construction_age": "1900-1949", "floor_area": 47.6,  "imd_decile": 3, "income": 38518},
    5: {"label": "Archetype 5 – Social Rental Post-War Flat",      "property_type": "Flat",  "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "End Terrace",   "tenure": "Rental (Social)",   "construction_age": "1950-2002", "floor_area": 46.9,  "imd_decile": 0, "income": 32923},
    6: {"label": "Archetype 6 – Uninsulated Owner Detached",       "property_type": "House", "wall_insulation": "None",    "wall_type": "Cavity",  "built_form": "Detached",      "tenure": "Owner Occupied",    "construction_age": "1900-1949", "floor_area": 23.3,  "imd_decile": 1, "income": 33125},
    7: {"label": "Archetype 7 – Well-Insulated Post-War Semi",     "property_type": "House", "wall_insulation": "Full",    "wall_type": "Cavity",  "built_form": "Semi-Detached", "tenure": "Owner Occupied",    "construction_age": "1950-2002", "floor_area": 44.8,  "imd_decile": 1, "income": 33804},
    8: {"label": "Archetype 8 – Large Wealthy Owner Detached",     "property_type": "House", "wall_insulation": "Partial", "wall_type": "Cavity",  "built_form": "Detached",      "tenure": "Owner Occupied",    "construction_age": "1900-1949", "floor_area": 267.8, "imd_decile": 6, "income": 36368},
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

# Archetype comparison metrics (from cluster data)
Archetype_METRICS = {
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
    """Return the scale keyword to filter solutions by, based on built form."""
    bf = built_form.lower()
    if bf == "detached":
        return "small"
    elif bf in ["semi-detached", "mid-terrace", "enclosed mid-terrace"]:
        return "medium"
    elif bf in ["end terrace", "enclosed end terrace"]:
        return "large"
    return None  # No scale filtering for flats / unknown

def filter_by_scale(df, scale):
    """
    Keep rows that either:
      - contain the matching scale keyword in the solution name, OR
      - have no scale keyword at all (e.g. single-option solutions like Solar PV, glazing types)
    """
    if scale is None:
        return df
    scale_keywords = ["small", "medium", "large"]
    def row_matches(solution_name):
        name_lower = solution_name.lower()
        has_any_scale = any(kw in name_lower for kw in scale_keywords)
        if not has_any_scale:
            return True   # no scale in name → always include
        return scale in name_lower
    return df[df["Solution"].apply(row_matches)]

def get_recommendations_for_Archetype(Archetype_id, min_score=1):
    col = f"C{Archetype_id}"
    df = SOLUTIONS_DF[(SOLUTIONS_DF[col] >= 1) & (SOLUTIONS_DF[col] >= min_score)].copy()
    df = df.sort_values(col, ascending=False)
    return df

def match_Archetype(user_props):
    fields = ["property_type", "wall_insulation", "wall_type", "built_form", "tenure", "construction_age"]
    best_Archetype = None
    best_score = -1
    for cid, cdata in CLUSTERS.items():
        score = sum(1 for f in fields if cdata.get(f, "").lower() == user_props.get(f, "").lower())
        fa_diff = abs(cdata["floor_area"] - user_props.get("floor_area", 80)) / 200
        score -= fa_diff * 0.5
        if score > best_score:
            best_score = score
            best_Archetype = cid
    return best_Archetype, best_score

def rating_css(r):
    """Map a rating string to a CSS class."""
    mapping = {"A": "rating-A", "B": "rating-B", "B/C": "rating-BC",
               "C": "rating-C", "D": "rating-D", "D/E": "rating-DE", "E": "rating-E"}
    return mapping.get(r.strip(), "badge-gray")

def render_solution_card(row, score):
    label, badge_cls = score_label(score)
    priority_cls = "priority-high" if score == 2 else "priority-medium"

    carbon  = row.get("CarbonRating", "")
    energy  = row.get("EnergyRating", "")
    afford  = row.get("AffordRating", "")

    carbon_html = f'<span class="rating-pill {rating_css(carbon)}">🌿 Carbon: {carbon}</span>' if carbon else ""
    energy_html = f'<span class="rating-pill {rating_css(energy)}">⚡ Energy: {energy}</span>'   if energy else ""
    afford_html = f'<span class="rating-pill {rating_css(afford)}">💷 Afford: {afford}</span>'   if afford else ""

    st.markdown(f"""
    <div class="rec-card {priority_cls}">
        <div class="rec-title">{row['Solution']}</div>
        <div class="rec-badges">
            <span class="badge {badge_cls}">{label}</span>
            <span class="badge badge-blue">{row['Category']}</span>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:6px;">
            {carbon_html}{energy_html}{afford_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏠 How would you like to proceed")
    st.markdown("---")
    mode = st.radio("Here are your options :", ["Use an Archetype", "Enter my own property details"], index=0)
    st.markdown("---")

    if mode == "Use an Archetype":
        st.markdown("**Select an Archetype that best matches your property:**")
        Archetype_options = {f"Archetype {cid}: {cdata['label'].split('–')[1].strip()}": cid for cid, cdata in CLUSTERS.items()}
        chosen_label = st.selectbox("Archetype", list(Archetype_options.keys()))
        chosen_Archetype = Archetype_options[chosen_label]
        min_score = st.radio("Show recommendations:", ["Best solutions only (score 2)", "All applicable solutions (score 1 & 2)"], index=1)
        min_score_val = 2 if "Best" in min_score else 1
        category_filter = st.multiselect(
            "Filter by category",
            options=SOLUTIONS_DF["Category"].unique().tolist(),
            default=SOLUTIONS_DF["Category"].unique().tolist()
        )
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
        min_score   = st.radio("Show recommendations:", ["Best solutions only (score 2)", "All applicable solutions (score 1 & 2)"], index=1)
        min_score_val = 2 if "Best" in min_score else 1
        category_filter = st.multiselect(
            "Filter by category",
            options=SOLUTIONS_DF["Category"].unique().tolist(),
            default=SOLUTIONS_DF["Category"].unique().tolist()
        )
        run = st.button("Find Matching Archetype & Recommendations →")

# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero-banner">
    <h1>🏠 RetroFit Recommender</h1>
    <p>Tailored retrofit solutions for UK residential properties — matched to your Archetype or property characteristics.</p>
</div>
""", unsafe_allow_html=True)

if not run:
    st.markdown('<div class="section-header">About the Archetypes</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#3d3d3d;font-size:1rem;margin-bottom:1.2rem;">Each Archetype represents a common UK residential property type. Select one in the sidebar, or enter your own details to get matched.</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (cid, cdata) in enumerate(CLUSTERS.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="Archetype-card">
                <div class="Archetype-title">Archetype {cid}</div>
                <div class="Archetype-meta">
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
        resolved = chosen_Archetype
        match_method = "Archetype"
    else:
        user_props = {
            "property_type":     prop_type,
            "wall_insulation":   wall_ins,
            "wall_type":         wall_type,
            "built_form":        built_form,
            "tenure":            tenure,
            "construction_age":  const_age,
            "floor_area":        float(floor_area),
        }
        resolved, _ = match_Archetype(user_props)
        match_method = "matched"

    cdata  = CLUSTERS[resolved]
    col_id = f"C{resolved}"

    st.markdown(f'<div class="section-header">{"📌 Selected" if match_method=="Archetype" else "🎯 Best Matched"} Archetype {resolved}</div>', unsafe_allow_html=True)

    if match_method == "matched":
        st.markdown(f"""
        <div class="info-box">
            Your property characteristics have been matched to <strong>Archetype {resolved}</strong>.
            Review the Archetype profile below and refine your selections in the sidebar if needed.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:0.5rem;margin-bottom:1rem;">
        <span class="stat-pill">Floor Area: ~{cdata['floor_area']} m²</span>
        <span class="stat-pill">IMD Decile: {cdata['imd_decile']}</span>
        <span class="stat-pill">Avg Income: £{cdata['income']:,}/yr</span>
    </div>
    """, unsafe_allow_html=True)

    rec_df = get_recommendations_for_Archetype(resolved, min_score_val)
    rec_df = rec_df[rec_df["Category"].isin(category_filter)]

    # Scale filtering based on built form
    built_form_resolved = cdata["built_form"]
    scale = get_scale_for_built_form(built_form_resolved)
    rec_df = filter_by_scale(rec_df, scale)

    scale_label_map = {"small": "Small-scale", "medium": "Medium-scale", "large": "Large-scale"}
    scale_display = scale_label_map.get(scale, "All scales")

    st.markdown(f'<div class="section-header">✅ Recommendations for Archetype {resolved}</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#3d3d3d;font-size:0.85rem;margin-bottom:0.8rem;">Showing <strong>{scale_display}</strong> solutions based on built form: <strong>{built_form_resolved}</strong></p>', unsafe_allow_html=True)

    if rec_df.empty:
        st.info("No recommendations found for the selected filters. Try lowering the minimum score threshold.")
    else:
        strong  = rec_df[rec_df[col_id] == 2]
        consider = rec_df[rec_df[col_id] == 1]
        total   = len(rec_df)

        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <span class="stat-pill">🟢 {len(strong)} Best Solutions</span>
            <span class="stat-pill">🟡 {len(consider)} 2nd Best Solutions</span>
            <span class="stat-pill">📋 {total} Total Applicable</span>
        </div>
        """, unsafe_allow_html=True)

        categories = rec_df["Category"].unique()
        tabs = st.tabs(list(categories) + ["All Solutions"])

        for i, cat in enumerate(categories):
            with tabs[i]:
                cat_df      = rec_df[rec_df["Category"] == cat]
                cat_strong  = cat_df[cat_df[col_id] == 2]
                cat_consider = cat_df[cat_df[col_id] == 1]
                if not cat_strong.empty:
                    st.markdown('<p style="color:#2d6a4f;font-weight:700;font-size:1rem;margin-bottom:0.5rem;">🟢 Best Solutions</p>', unsafe_allow_html=True)
                    for _, row in cat_strong.iterrows():
                        render_solution_card(row, 2)
                if not cat_consider.empty:
                    st.markdown('<p style="color:#b45309;font-weight:700;font-size:1rem;margin-bottom:0.5rem;">🟡 2nd Best Solutions</p>', unsafe_allow_html=True)
                    for _, row in cat_consider.iterrows():
                        render_solution_card(row, 1)

        with tabs[-1]:
            st.dataframe(
                rec_df[["Category", "Solution", "CarbonRating", "EnergyRating", "AffordRating", col_id]]
                    .rename(columns={col_id: "Score", "CarbonRating": "Carbon", "EnergyRating": "Energy", "AffordRating": "Affordability"})
                    .reset_index(drop=True),
                use_container_width=True,
                hide_index=True
            )

    st.markdown("---")
    st.markdown('<div class="section-header">📊 How You Compare to Other Archetypes</div>', unsafe_allow_html=True)

    my = Archetype_METRICS[resolved]
    all_co2  = [v["co2"]  for v in Archetype_METRICS.values()]
    all_gap  = [v["gap"]  for v in Archetype_METRICS.values()]
    all_cost = [v["cost"] for v in Archetype_METRICS.values()]
    avg_co2  = round(sum(all_co2)  / len(all_co2),  2)
    avg_gap  = round(sum(all_gap)  / len(all_gap),  2)
    avg_cost = round(sum(all_cost) / len(all_cost), 2)

    # Build summary text
    def compare_text(val, avg, unit, label, higher_is_worse=True):
        diff = round(abs(val - avg), 2)
        if abs(val - avg) < avg * 0.05:
            return f"Your {label} ({val} {unit}) is <strong>close to the average</strong> ({avg} {unit}) across all Archetypes."
        elif (val > avg) == higher_is_worse:
            return f"Your {label} ({val} {unit}) is <strong style='color:#b45309;'>above average</strong> — the average is {avg} {unit}. There is meaningful room for improvement here."
        else:
            return f"Your {label} ({val} {unit}) is <strong style='color:#2d6a4f;'>below average</strong> — the average is {avg} {unit}. You are performing well on this metric."

    co2_text  = compare_text(my["co2"],  avg_co2,  "kgCO₂e/m²", "CO₂ emissions")
    gap_text  = compare_text(my["gap"],  avg_gap,  "",           "efficiency gap")
    cost_text = compare_text(my["cost"], avg_cost, "£/m²",       "energy cost/area")

    # Metric cards + gauges as HTML
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
    <div style="font-size:0.78rem;color:#6b7280;">
        <strong>Score guide:</strong>
        <span style="color:#2d6a4f;font-weight:600;">2 = Best Solution for this Archetype</span> ·
        <span style="color:#b45309;font-weight:600;">1 = 2nd Best Solution</span> ·
        0 = Not applicable (hidden)
    </div>
    """, unsafe_allow_html=True)