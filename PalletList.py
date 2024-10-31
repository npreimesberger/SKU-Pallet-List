def get_unique_pallets():
    sku_dict = {}
    
    while True:
        sku = input("Enter SKU (or type 'done' to finish): ").strip()
        if sku.lower() == 'done':
            break
        
        pallet_locations = input(
            f"Enter pallet locations for SKU {sku} (comma-separated): "
        ).strip().split(',')
        
        # Clean and store pallet locations in a set
        pallet_locations = {loc.strip() for loc in pallet_locations}
        
        # Store the pallet locations for the SKU
        if sku in sku_dict:
            sku_dict[sku].update(pallet_locations)
        else:
            sku_dict[sku] = pallet_locations

    return sku_dict

def find_min_pallet_locations(sku_dict):
    # Invert the dictionary to have pallets as keys and SKUs as values
    pallet_dict = {}
    for sku, pallets in sku_dict.items():
        for pallet in pallets:
            if pallet not in pallet_dict:
                pallet_dict[pallet] = set()
            pallet_dict[pallet].add(sku)
    
    # Use a greedy approach to find the minimum pallet locations
    selected_pallets = set()
    covered_skus = set()
    all_skus = set(sku_dict.keys())

    while covered_skus != all_skus:
        # Find the pallet that covers the most uncovered SKUs
        best_pallet = max(
            pallet_dict.items(),
            key=lambda x: len(x[1] - covered_skus)
        )[0]
        
        # Add the selected pallet and update covered SKUs
        selected_pallets.add(best_pallet)
        covered_skus.update(pallet_dict[best_pallet])
    
    return selected_pallets

def display_results(sku_dict, selected_pallets):
    print("\nMinimum Pallet Locations Required:")
    for pallet in selected_pallets:
        print(pallet)

    print("\nAll SKUs and their Pallet Locations:")
    for sku, locations in sku_dict.items():
        print(f"{sku}: {', '.join(locations)}")

if __name__ == "__main__":
    sku_dict = get_unique_pallets()
    selected_pallets = find_min_pallet_locations(sku_dict)
    display_results(sku_dict, selected_pallets)
