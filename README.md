# 🎈 Blank app template

import streamlit as st
import numpy as np

# ─────────────────────────────────────────────
# ORDINAL ENCODING MAPPINGS
# ─────────────────────────────────────────────
PROPERTY_TYPE_MAP = {"house": 0, "flat": 1, "bungalow": 2}
WALL_INSULATION_MAP = {"none": 0, "partial": 1, "full": 2}
WALL_TYPE_MAP = {"cavity": 0, "solid": 1, "timber": 2}
BUILT_FORM_MAP = {"mid-terrace": 0, "end-terrace": 1, "semi-detached": 2, "detached": 3}
TENURE_MAP = {
    "owner-occupied": 0,
    "owner(occupied)/rental(private)": 1,
    "rented (private)": 2,
    "rental (private)": 2,
    "rental (social)": 3,
}
CONSTRUCTION_AGE_MAP = {"pre-1900": 0, "1900-1949": 1, "1950-2002": 2, "2003-2019": 3}

# ─────────────────────────────────────────────
# CLUSTER CENTROIDS  (12 clusters × 11 features)
# Feature order:
#   PROPERTY_TYPE, wall_insulation, wall_type, BUILT_FORM,
#   TENURE, CONSTRUCTION_AGE, efficiency_gap,
#   ecc/a, c02/a, TOTAL_FLOOR_AREA, energy_cost/area
# ─────────────────────────────────────────────
CLUSTER_CENTROIDS = np.array([
    [0, 2, 0, 0, 0, 1, 19.611597,  4.265977,   0.058906,  83.253749,  13.395242],  # 0
    [1, 2, 0, 1, 3, 2,  4.098593,  4.581339,   0.038870,  54.746362,  10.808684],  # 1
    [0, 0, 0, 2, 0, 2, 16.607173,  3.390204,   0.048211,  87.091145,  11.313478],  # 2
    [0, 0, 0, 0, 1, 1, 19.372151,  4.234911,   0.058505,  82.726392,  13.036426],  # 3
    [1, 1, 0, 0, 2, 3, 14.000000, 14360.484,   1.290323,   0.620000, 383.870968],  # 4
    [0, 1, 0, 3, 1, 1, 40.425081,  9.557650,   0.097491,  76.725506,  27.222988],  # 5
    [2, 1, 0, 3, 2, 2, 14.207960,  3.438594,   0.040755,  72.393372,  12.006892],  # 6
    [1, 0, 1, 2, 2, 0,  4.000000, 1133.000000,  9.500000,   1.000000, 1243.000000],# 7
    [0, 2, 0, 2, 0, 2, 16.157309,  3.284138,   0.046963,  87.442936,  11.459795],  # 8
    [0, 1, 2, 3, 2, 2, 14.513442,  3.878813,   0.048005,  78.426476,  12.266082],  # 9
    [0, 1, 0, 3, 0, 1, 16.264456,  1.330150,   0.047446, 214.753279,  10.642293],  # 10
    [1, 0, 0, 1, 3, 2,  4.771316,  4.633044,   0.040153,  56.533517,  10.361959],  # 11
])

# ─────────────────────────────────────────────
# CLUSTER RECOMMENDATIONS  (placeholders)
# Replace each string with your real recommendations!
# ─────────────────────────────────────────────
CLUSTER_RECOMMENDATIONS = {
    0:  ("Owner-occupied mid-terrace house, pre-1949, fully insulated cavity walls.",
         "📌 _Placeholder: Add your recommendations for Cluster 0 here._"),
    1:  ("Social rental flat, post-1950, fully insulated cavity walls.",
         "📌 _Placeholder: Add your recommendations for Cluster 1 here._"),
    2:  ("Owner-occupied semi-detached house, no insulation, post-1950.",
         "📌 _Placeholder: Add your recommendations for Cluster 2 here._"),
    3:  ("Mid-terrace house, no insulation, pre-1949, mixed tenure.",
         "📌 _Placeholder: Add your recommendations for Cluster 3 here._"),
    4:  ("Modern private rental flat, partial insulation, 2003–2019.",
         "📌 _Placeholder: Add your recommendations for Cluster 4 here._"),
    5:  ("Detached house, partial insulation, high efficiency gap.",
         "📌 _Placeholder: Add your recommendations for Cluster 5 here._"),
    6:  ("Detached bungalow, partial insulation, private rental.",
         "📌 _Placeholder: Add your recommendations for Cluster 6 here._"),
    7:  ("Pre-1900 solid wall flat, no insulation, private rental.",
         "📌 _Placeholder: Add your recommendations for Cluster 7 here._"),
    8:  ("Owner-occupied semi-detached house, fully insulated, post-1950.",
         "📌 _Placeholder: Add your recommendations for Cluster 8 here._"),
    9:  ("Detached timber-frame house, partial insulation, private rental.",
         "📌 _Placeholder: Add your recommendations for Cluster 9 here._"),
    10: ("Large detached owner-occupied house, partial insulation, pre-1949.",
         "📌 _Placeholder: Add your recommendations for Cluster 10 here._"),
    11: ("Social rental flat, no insulation, end-terrace, post-1950.",
         "📌 _Placeholder: Add your recommendations for Cluster 11 here._"),
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
CENTROID_MIN = CLUSTER_CENTROIDS.min(axis=0)
CENTROID_MAX = CLUSTER_CENTROIDS.max(axis=0)

def normalise(vec):
    rng = CENTROID_MAX - CENTROID_MIN
    rng[rng == 0] = 1
    return (np.array(vec, dtype=float) - CENTROID_MIN) / rng

def find_closest_cluster(user_vec):
    u = normalise(user_vec)
    c = np.array([normalise(row) for row in CLUSTER_CENTROIDS])
    distances = np.linalg.norm(c - u, axis=1)
    return int(np.argmin(distances)), distances

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
st.set_page_config(page_title="House Recommendation Tool", page_icon="🏠", layout="centered")

st.title("🏠 House Energy Recommendation Tool")
st.markdown(
    "Enter your property details below. We'll match you to the closest energy profile "
    "and provide tailored recommendations."
)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Property Details")
    property_type  = st.selectbox("Property Type",      list(PROPERTY_TYPE_MAP.keys()))
    built_form     = st.selectbox("Built Form",          list(BUILT_FORM_MAP.keys()))
    wall_type      = st.selectbox("Wall Type",           list(WALL_TYPE_MAP.keys()))
    wall_insulation= st.selectbox("Wall Insulation",     list(WALL_INSULATION_MAP.keys()))
    tenure         = st.selectbox("Tenure",              list(TENURE_MAP.keys()))
    construction_age = st.selectbox("Construction Age",  list(CONSTRUCTION_AGE_MAP.keys()))

with col2:
    st.subheader("Energy Metrics")
    efficiency_gap   = st.slider("Efficiency Gap",           0.0, 50.0, 15.0, 0.5,
                                  help="Gap between potential and current EPC rating")
    floor_area       = st.number_input("Total Floor Area (m²)", 1.0, 500.0, 80.0, 1.0)
    ecc_a            = st.number_input("Energy Cost Change / year (£)", 0.0, 500.0, 5.0, 0.5)
    energy_cost_area = st.number_input("Energy Cost per m² (£/m²)", 0.0, 50.0, 12.0, 0.5)
    co2_a            = st.number_input("CO₂ Emissions / year (tonnes)", 0.0, 10.0, 0.05, 0.005, format="%.3f")

st.divider()

if st.button("🔍 Get My Recommendation", use_container_width=True, type="primary"):

    user_vector = np.array([
        PROPERTY_TYPE_MAP[property_type],
        WALL_INSULATION_MAP[wall_insulation],
        WALL_TYPE_MAP[wall_type],
        BUILT_FORM_MAP[built_form],
        TENURE_MAP[tenure],
        CONSTRUCTION_AGE_MAP[construction_age],
        efficiency_gap,
        ecc_a,
        co2_a,
        floor_area,
        energy_cost_area,
    ])

    cluster_idx, distances = find_closest_cluster(user_vector)
    profile, rec = CLUSTER_RECOMMENDATIONS[cluster_idx]

    st.success(f"✅ You matched **Cluster {cluster_idx}**")

    st.markdown("#### 🏷️ Cluster Profile")
    st.info(profile)

    st.markdown("#### 💡 Recommendations")
    st.warning(rec)

    with st.expander("📊 Distance to all clusters (lower = closer)"):
        sorted_idx = np.argsort(distances)
        for i in sorted_idx:
            d = distances[i]
            bar_len = max(1, int((1 - d / (distances.max() + 1e-9)) * 30))
            bar = "█" * bar_len
            tag = "  ← **your match**" if i == cluster_idx else ""
            st.markdown(f"`Cluster {i:>2}`  {d:.4f}  `{bar}`{tag}")