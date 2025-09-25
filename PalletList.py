import streamlit as st

# Store SKU data persistently across interactions
if "sku_dict" not in st.session_state:
    st.session_state.sku_dict = {}

st.title("SKU Pallet Optimizer")

# Input for SKU
sku = st.text_input("Enter a SKU (leave blank if you're done):")

# Input for pallet locations
pallet_locations = st.text_input(
    "Enter pallet locations for this SKU (comma-separated):"
)

# Button to add the SKU + pallets to the dictionary
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

# Show current entries
if st.session_state.sku_dict:
    st.write("### Current SKUs and Pallet Locations:")
    for s, locs in st.session_state.sku_dict.items():
        st.write(f"- {s}: {', '.join(locs)}")

# Greedy set cover to minimize pallets
def find_min_pallet_locations(sku_dict):
    pallet_dict = {}
    for sku, pallets in sku_dict.items():
        for pallet in pallets:
            pallet_dict.setdefault(pallet, set()).add(sku)

    selected_pallets = set()
    covered_skus = set()
    all_skus = set(sku_dict.keys())

    while covered_skus != all_skus:
        best
