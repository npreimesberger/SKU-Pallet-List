import streamlit as st

# Keep SKU data across interactions
if "sku_dict" not in st.session_state:
    st.session_state.sku_dict = {}

st.title("SKU Pallet Optimizer")

# --- Input section ---
sku = st.text_input("Enter a SKU:")
pallet_locations = st.text_input(
    "Enter pallet locations for this SKU (comma-separated):"
)

if st.button("Add SKU"):
    if sku and pallet_locations:
        locations = {loc.strip() for loc in pallet_locations.split(",")}
        if sku in st.session_state.sku_dict:
            st.session_state.sku_dict[sku].update(locations)
        else:
            st.session_state.sku_dict[sku] = locations
        st.success(f"Added SKU {sku} with locations: {', '.join(locations)}")
    else:
        st.warning("Please enter both a SKU and at least one pallet location.")

# --- Show current entries ---
if st.session_state.sku_dict:
    st.subheader("Current SKUs and Pallet Locations")
    for s, locs in st.session_state.sku_dict.items():
        st.write(f"- {s}: {', '.join(sorted(locs))}")

# --- Function for greedy set cover ---
def find_min_pallet_locations(sku_dict):
    pallet_dict = {}
    for sku, pallets in sku_dict.items():
        for pallet in pallets:
            pallet_dict.setdefault(pallet, set()).add(sku)

    selected_pallets = set()
    covered_skus = set()
    all_skus = set(sku_dict.keys())

    while covered_skus != all_skus:
        best_pallet = max(
            pallet_dict.items(), key=lambda x: len(x[1] - covered_skus)
        )[0]
        selected_pallets.add(best_pallet)
        covered_skus.update(pallet_dict[best_pallet])

    return selected_pallets

# --- Always show this button ---
if st.button("Generate Minimum Pallet List"):
    if st.session_state.sku_dict:
        result = find_min_pallet_locations(st.session_state.sku_dict)
        st.subheader("Minimum Pallet Locations Required")
        for pallet in sorted(result):
            st.write(f"- {pallet}")
    else:
        st.warning("No SKUs entered yet.")
