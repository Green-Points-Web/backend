def get_level_info(total_points: int) -> dict:
    levels = [
        {"name": "Seed", "min": 0, "max": 100},
        {"name": "Sprout", "min": 100, "max": 300},
        {"name": "Tree", "min": 300, "max": 700},
        {"name": "Forest", "min": 700, "max": 1500},
        {"name": "Planet Hero", "min": 1500, "max": float('inf')}
    ]
    
    current = levels[0]
    for level in levels:
        if total_points >= level["min"]:
            current = level
            
    current_index = levels.index(current)
    
    if current_index + 1 < len(levels):
        next_level = levels[current_index + 1]
        points_to_next = next_level["min"] - total_points
        progress = ((total_points - current["min"]) / (next_level["min"] - current["min"])) * 100
        
        return {
            "current_level": current["name"],
            "level_min": current["min"],
            "next_level": next_level["name"],
            "next_level_min": next_level["min"],
            "points_to_next": points_to_next,
            "progress_percent": min(100, max(0, progress))
        }
    else:
        return {
            "current_level": current["name"],
            "level_min": current["min"],
            "next_level": None,
            "next_level_min": None,
            "points_to_next": 0,
            "progress_percent": 100
        }