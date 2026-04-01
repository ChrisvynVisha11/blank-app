import streamlit as st

st.title("🎈 Household Renovation Recommendation")

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
.rec-detail  { font-size: 0.8rem; color: var(--muted); }

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
    ("Heating Source", "Mechanical Ventilation with Heat Recovery (high efficiency)",    2,0,2,2,2,2,1,1),
    ("Heating Source", "Mechanical Ventilation with Heat Recovery (low efficiency)",     2,0,2,2,2,2,1,1),
    ("Heating Source", "ASHP (small-scale/low-efficiency)",                              1,0,2,2,0,1,0,1),
    ("Heating Source", "ASHP (medium-scale/medium efficiency)",                          1,0,2,2,0,1,0,1),
    ("Heating Source", "ASHP (large-scale/high efficiency)",                             1,0,2,2,0,1,0,1),
    ("Heating Source", "GSHP (small-scale/low efficiency)",                              1,0,2,2,0,1,0,1),
    ("Heating Source", "GSHP (medium-scale/medium efficiency)",                          1,0,2,2,0,1,0,1),
    ("Heating Source", "GSHP (large-scale/high efficiency)",                             1,0,2,2,0,1,0,1),
    ("Heating Source", "WSHP (small-scale/low efficiency)",                              1,0,2,2,0,1,0,1),
    ("Heating Source", "WSHP (medium-scale/medium efficiency)",                          1,0,2,2,0,1,0,1),
    ("Heating Source", "WSHP (large-scale/high efficiency)",                             1,0,2,2,0,1,0,1),
    ("Heating Source", "District Energy Network Heat Exchanger",                         2,1,1,2,1,2,2,1),
    ("Smart Heating Controls", "Small-scale",                                            2,1,2,2,0,2,1,2),
    ("Smart Heating Controls", "Medium-scale",                                           2,1,2,2,0,2,1,2),
    ("Smart Heating Controls", "Large-scale",                                            2,1,2,2,0,2,1,2),
    ("LED Lighting", "Small-scale",                                                      1,1,2,1,1,2,1,1),
    ("LED Lighting", "Medium-scale",                                                     1,1,2,1,1,2,1,1),
    ("LED Lighting", "Large-scale",                                                      1,1,2,1,1,2,1,1),
    ("Solar PV", "Solar Photovoltaics",                                                  1,0,1,2,2,2,1,2),
    ("Wall Insulation", "External Solid Wall Insulation",                                1,0,1,2,0,0,1,2),
    ("Wall Insulation", "Internal Solid Wall Insulation",                                1,0,1,2,0,0,1,2),
    ("Wall Insulation", "Cavity Wall Insulation (small-scale)",                          1,0,1,2,0,0,1,2),
    ("Wall Insulation", "Cavity Wall Insulation (medium-scale)",                         1,0,1,2,0,0,1,2),
    ("Wall Insulation", "Cavity Wall Insulation (large-scale)",                          1,0,1,2,0,0,1,2),
    ("Glazing", "Triple Glazing – Hardwood frames",                                      2,2,1,2,2,2,2,2),
    ("Glazing", "Triple Glazing – uPVC frames",                                          2,2,1,2,2,2,2,2),
    ("Glazing", "Triple Glazing – Aluminium frames",                                     2,2,1,2,2,2,2,2),
    ("Glazing", "Secondary Glazing – Hardwood frames",                                   0,0,2,0,2,1,0,0),
    ("Glazing", "Secondary Glazing – uPVC frames",                                       0,0,2,0,2,1,0,0),
    ("Glazing", "Secondary Glazing – Aluminium frames",                                  0,0,2,0,2,1,0,0),
    ("Glazing", "Water-filled Glass",                                                    1,2,0,2,0,0,0,1),
    ("Floor Insulation", "Floor Insulation (small-scale)",                               0,0,1,2,0,0,1,2),
    ("Floor Insulation", "Floor Insulation (medium-scale)",                              0,0,1,2,0,0,1,2),
    ("Floor Insulation", "Floor Insulation (large-scale)",                               0,0,1,2,0,0,1,2),
    ("Roof/Loft", "Loft Insulation (small-scale)",                                       0,0,1,2,0,0,1,2),
    ("Roof/Loft", "Loft Insulation (medium-scale)",                                      0,0,1,2,0,0,1,2),
    ("Roof/Loft", "Loft Insulation (large-scale)",                                       0,0,1,2,0,0,1,2),
    ("Roof/Loft", "Draught-proofing (small-scale)",                                      1,0,2,2,0,0,2,2),
    ("Roof/Loft", "Draught-proofing (medium-scale)",                                     1,0,2,2,0,0,2,2),
    ("Roof/Loft", "Draught-proofing (large-scale)",                                      1,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Mineral Wool (Blown-in) – small",                      1,0,1,2,0,0,1,2),
    ("Wall Insulation Material", "Mineral Wool (Blown-in) – medium",                     1,0,1,2,0,0,1,2),
    ("Wall Insulation Material", "Mineral Wool (Blown-in) – large",                      1,0,1,2,0,0,1,2),
    ("Wall Insulation Material", "Spray Foam (closed-cell) – small",                     0,0,2,2,0,0,0,1),
    ("Wall Insulation Material", "Spray Foam (closed-cell) – medium",                    0,0,2,2,0,0,0,1),
    ("Wall Insulation Material", "Spray Foam (closed-cell) – large",                     0,0,2,2,0,0,0,1),
    ("Wall Insulation Material", "EPS Beads – small",                                    0,0,1,2,0,0,0,1),
    ("Wall Insulation Material", "EPS Beads – medium",                                   0,0,1,2,0,0,0,1),
    ("Wall Insulation Material", "EPS Beads – large",                                    0,0,1,2,0,0,0,1),
    ("Wall Insulation Material", "EPS Boards – small",                                   1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "EPS Boards – medium",                                  1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "EPS Boards – large",                                   1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "Phenolic Foam – small",                                1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "Phenolic Foam – medium",                               1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "Phenolic Foam – large",                                1,0,1,1,0,0,1,2),
    ("Wall Insulation Material", "Cork – small",                                         0,0,0,1,0,0,2,2),
    ("Wall Insulation Material", "Cork – medium",                                        0,0,0,1,0,0,2,2),
    ("Wall Insulation Material", "Cork – large",                                         0,0,0,1,0,0,2,2),
    ("Wall Insulation Material", "Mineral Wool Boards – small",                          1,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Mineral Wool Boards – medium",                         1,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Mineral Wool Boards – large",                          1,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "PIR/Phenolic/EPS Board – small",                       0,0,1,0,0,0,1,1),
    ("Wall Insulation Material", "PIR/Phenolic/EPS Board – medium",                      0,0,1,0,0,0,1,1),
    ("Wall Insulation Material", "PIR/Phenolic/EPS Board – large",                       0,0,1,0,0,0,1,1),
    ("Wall Insulation Material", "Wood Fibre – small",                                   2,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Wood Fibre – medium",                                  2,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Wood Fibre – large",                                   2,0,2,2,0,0,2,2),
    ("Wall Insulation Material", "Aerogel Insulation – small",                           1,0,1,2,0,0,1,1),
    ("Wall Insulation Material", "Aerogel Insulation – medium",                          1,0,1,2,0,0,1,1),
    ("Wall Insulation Material", "Aerogel Insulation – large",                           1,0,1,2,0,0,1,1),
    ("Floor Insulation Material", "Mineral Wool Batts",                                  1,0,0,2,0,0,1,2),
    ("Floor Insulation Material", "Rigid Foam Boards (PIR)",                             1,0,0,1,0,0,0,1),
    ("Roof/Loft Material", "Mineral Wool/Fibreglass Rolls",                              1,0,2,2,0,0,1,2),
    ("Roof/Loft Material", "Cellulose (Blown-in)",                                       1,0,1,2,0,0,1,2),
    ("Roof/Loft Material", "Rigid Boards (PIR/Phenolic)",                                0,0,1,1,0,0,0,1),
]

SOLUTIONS_DF = pd.DataFrame(SOLUTIONS_RAW, columns=[
    "Category", "Solution", "C1","C2","C3","C4","C5","C6","C7","C8"
])

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def score_label(s):
    if s == 2: return ("Best Solution", "badge-green")
    if s == 1: return ("2nd Best Solution", "badge-amber")
    return ("Not Applicable", "badge-red")

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
        score = sum(1 for f in fields if cdata.get(f, "").lower() == user_props.get(f, "").lower())
        fa_diff = abs(cdata["floor_area"] - user_props.get("floor_area", 80)) / 200
        score -= fa_diff * 0.5
        if score > best_score:
            best_score = score
            best_archetype = cid
    return best_archetype, best_score

def render_solution_card(row, score):
    label, badge_cls = score_label(score)
    priority_cls = "priority-high" if score == 2 else "priority-medium"
    st.markdown(f"""
    <div class="rec-card {priority_cls}">
        <div class="rec-title">{row['Solution']}</div>
        <div class="rec-badges">
            <span class="badge {badge_cls}">{label}</span>
            <span class="badge badge-blue">{row['Category']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏠 RetroFit")
    st.markdown("---")
    mode = st.radio("How would you like to proceed?", ["Use an Archetype", "Enter my own property details"], index=0)
    st.markdown("---")

    if mode == "Use an Archetype":
        st.markdown("**Select an archetype that best matches your property:**")
        archetype_options = {f"Archetype {cid}: {cdata['label'].split('–')[1].strip()}": cid for cid, cdata in CLUSTERS.items()}
        chosen_label = st.selectbox("Archetype", list(archetype_options.keys()))
        chosen_archetype = archetype_options[chosen_label]
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
        prop_type   = st.selectbox("Property Type", ["House", "Flat", "Bungalow"])
        wall_ins    = st.selectbox("Wall Insulation Status", ["None", "Partial", "Full"])
        wall_type   = st.selectbox("Wall Type", ["Cavity", "System", "Solid"])
        built_form  = st.selectbox("Built Form", ["Detached", "Semi-Detached", "Mid-Terrace", "End Terrace"])
        tenure      = st.selectbox("Tenure", ["Owner Occupied", "Rental (Private)", "Rented (Private)", "Rental (Social)"])
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
    <p>Tailored retrofit solutions for UK residential properties — matched to your archetype or property characteristics.</p>
</div>
""", unsafe_allow_html=True)

if not run:
    st.markdown('<div class="section-header">About the Archetypes</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#3d3d3d;font-size:1rem;margin-bottom:1.2rem;">Each archetype represents a common UK residential property type. Select one in the sidebar, or enter your own details to get matched.</p>', unsafe_allow_html=True)

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
            "property_type":     prop_type,
            "wall_insulation":   wall_ins,
            "wall_type":         wall_type,
            "built_form":        built_form,
            "tenure":            tenure,
            "construction_age":  const_age,
            "floor_area":        float(floor_area),
        }
        resolved, _ = match_archetype(user_props)
        match_method = "matched"

    cdata  = CLUSTERS[resolved]
    col_id = f"C{resolved}"

    st.markdown(f'<div class="section-header">{"📌 Selected" if match_method=="archetype" else "🎯 Best Matched"} Archetype: {cdata["label"]}</div>', unsafe_allow_html=True)

    if match_method == "matched":
        st.markdown(f"""
        <div class="info-box">
            Your property characteristics have been matched to <strong>Archetype {resolved}</strong>.
            Review the archetype profile below and refine your selections in the sidebar if needed.
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:0.5rem;margin-bottom:1rem;">
        <span class="stat-pill">Floor Area: ~{cdata['floor_area']} m²</span>
        <span class="stat-pill">IMD Decile: {cdata['imd_decile']}</span>
        <span class="stat-pill">Avg Income: £{cdata['income']:,}/yr</span>
    </div>
    """, unsafe_allow_html=True)

    rec_df = get_recommendations_for_archetype(resolved, min_score_val)
    rec_df = rec_df[rec_df["Category"].isin(category_filter)]

    st.markdown(f'<div class="section-header">✅ Recommendations for Archetype {resolved}</div>', unsafe_allow_html=True)

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
                rec_df[["Category", "Solution", col_id]].rename(columns={col_id: "Score"}).reset_index(drop=True),
                use_container_width=True,
                hide_index=True
            )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem;color:#6b7280;">
        <strong>Score guide:</strong>
        <span style="color:#2d6a4f;font-weight:600;">2 = Best Solution for this archetype</span> ·
        <span style="color:#b45309;font-weight:600;">1 = 2nd Best Solution</span> ·
        0 = Not applicable (hidden)
    </div>
    """, unsafe_allow_html=True)