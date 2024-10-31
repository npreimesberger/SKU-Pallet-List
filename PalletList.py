import streamlit as st

def get_unique_pallets():
    sku_dict = {}
    num_entries = st.number_input("How many SKUs do you want to enter?", min_value=1, step=1)

    for _ in range(num_entries):
        sku = st.text_input("Enter SKU", key=f'sku_{_}')
        pallet_locations = st.text_input(
            f"Enter pallet locations for SKU {sku} (comma-separated):", key=f'locations_{_}'
        ).split(',')

        pallet_locations = {loc.strip() for loc in pallet_locations}
        if sku in sku_dict:
            sku_dict[sku].update(pallet_locations)
        else:
            sku_dict[sku] = pallet_locations

    return sku_dict

def find_min_pallet_locations(sku_dict):
    pallet_dict = {}
    for sku, pallets in sku_dict.items():
        for pallet in pallets:
            if pallet not in pallet_dict:
                pallet_dict[pallet] = set()
            pallet_dict[pallet].add(sku)

    selected_pallets = set()
    covered_skus = set()
    all_skus = set(sku_dict.keys())

    while covered_skus != all_skus:
        best_pallet = max(
            pallet_dict.items(),
            key=lambda x: len(x[1] - covered_skus)
        )[0]
        selected_pallets.add(best_pallet)
        covered_skus.update(pallet_dict[best_pallet])

    return selected_pallets

def display_results(sku_dict, selected_pallets):
    st.write("\nMinimum Pallet Locations Required:")
    for pallet in selected_pallets:
        st.write(pallet)

    st.write("\nAll SKUs and their Pallet Locations:")
    for sku, locations in sku_dict.items():
        st.write(f"{sku}: {', '.join(locations)}")

sku_dict = get_unique_pallets()
if st.button("Calculate Minimum Pallet Locations"):
    selected_pallets = find_min_pallet_locations(sku_dict)
    display_results(sku_dict, selected_pallets)
