from typing import List, Dict, Any, Tuple
from app.schemas import SOVDiffItem

class SOVDiffEngine:
    """
    Solves the rework caused when:
    'Brokers often send updated schedules mid-way, restarting extraction and pricing' (PDF p. 19).
    Compares original Schedule of Values (SOV v1) vs revised Schedule (SOV v2).
    """
    
    @classmethod
    def compare_schedules(
        cls,
        old_schedule: List[Dict[str, Any]],
        new_schedule: List[Dict[str, Any]],
        key_field: str = "asset_id"
    ) -> Tuple[List[SOVDiffItem], float]:
        """
        Compares two list-of-dicts schedules and returns:
        (diff_items, net_sum_insured_delta)
        """
        old_map = {str(item.get(key_field, idx)): item for idx, item in enumerate(old_schedule)}
        new_map = {str(item.get(key_field, idx)): item for idx, item in enumerate(new_schedule)}
        
        diffs: List[SOVDiffItem] = []
        old_total = sum(float(item.get("sum_insured", 0.0)) for item in old_schedule)
        new_total = sum(float(item.get("sum_insured", 0.0)) for item in new_schedule)
        net_delta = new_total - old_total
        
        # 1. Check for Modified & Deleted items
        for k, old_item in old_map.items():
            if k not in new_map:
                diffs.append(SOVDiffItem(
                    asset_id=k,
                    field_name="row",
                    old_value=old_item.get("description", "Asset"),
                    new_value=None,
                    change_type="DELETED"
                ))
            else:
                new_item = new_map[k]
                for field in ["sum_insured", "occupancy", "category", "location"]:
                    old_val = old_item.get(field)
                    new_val = new_item.get(field)
                    if old_val != new_val and (old_val is not None or new_val is not None):
                        diffs.append(SOVDiffItem(
                            asset_id=k,
                            field_name=field,
                            old_value=old_val,
                            new_value=new_val,
                            change_type="MODIFIED"
                        ))
                        
        # 2. Check for Added items
        for k, new_item in new_map.items():
            if k not in old_map:
                diffs.append(SOVDiffItem(
                    asset_id=k,
                    field_name="row",
                    old_value=None,
                    new_value=f"{new_item.get('description', 'New Asset')} (₹{float(new_item.get('sum_insured', 0)):,.0f})",
                    change_type="ADDED"
                ))
                
        return diffs, net_delta
