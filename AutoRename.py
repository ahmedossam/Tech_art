import maya.cmds as cmds

def auto_rename(prefix="object"):
    # Get selected objects
    selected_objects = cmds.ls(selection=True)
    
    if not selected_objects:
        cmds.warning("No objects selected!")
        return
    
    # Rename each object with the prefix and index
    for i, obj in enumerate(selected_objects):
        new_name = f"{prefix}_{i+1:03}"
        cmds.rename(obj, new_name)
    
    print(f"Renamed {len(selected_objects)} objects with prefix '{prefix}'.")

# Example Usage:
auto_rename("myObject")
