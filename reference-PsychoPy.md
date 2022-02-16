## Click and Drag

```python
# https://discourse.psychopy.org/t/click-and-drag-lag/10156/4
# Michael MacAskill, 2019

# Under Begin Routine

drag_in_process = False
clicked_object = None

# Under Each Frame

if not drag_in_process:
    for draggable_object in draggable_objects:
        if mouse.isPressedIn(draggable_object):
            clicked_object = draggable_object
            # Implement 'unset' logic, if necessary
            drag_in_process = True

if sum(mouse.getPressed()) > 0:
    if drag_in_process:
        # Implement 'snap' logic here if snap before mouse up
        clicked_object.pos = mouse.getPos()
else:
    drag_in_process = False
    # Implement 'snap' logic here if snap after mouse up
    # Other events, such as 'set' or 'repel' etc.
```

## 'Utils' (?)

```python
def within_box(obj, box):
    """
    Determine if object is within box
    - Squared difference in x (and y) coordinates 
    should be less than the square of half the 
    box width (and height)
    - That would mean the center of the object is
    within the box boundaries
    """
    obj_x, obj_y = obj.pos
    box_x, box_y = box.pos
    box_w, box_h = box.size
    dx, dy = obj_x - box_x, obj_y - box_y
    hw, hh = box_w / 2, box_h / 2
    return dx * dx < hw * hw and dy * dy < hh * hh

def snapped(obj1, obj2, func=within_box):
    """
    Determine if obj1 snapped to center of obj2
    - Check if obj1 is 'near' obj2, based on func
    - If yes, set the obj1's position to be 
    equal to obj2's position and return True
    - Otherwise, do nothing and return False
    """
    if func(obj1, obj2):
        obj1.pos = obj2.pos
        return True
    return False

def hide(obj):
    obj.size = (0, 0)
    obj.autoDraw = False

def unhide(obj, size):
    obj.size = size
    obj.autoDraw = True
```
