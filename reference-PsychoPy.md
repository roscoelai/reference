## 'Invisible Boxes' Strategy

Todo:
- For tasks that depend on slides with clickable regions
- Positions and sizes of invisible boxes are currently hardcoded manually
- Figure out the relationship between box positions/sizes to slide positions/sizes
- Will still require hardcoding for relative positions/sizes, but slides may then be freely resized without breaking the correct positioning of the boxes

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

## Snap/Repel

```python
def within_radius(obj1_pos, obj2_pos, thresh):
    x1, y1 = obj1_pos
    x2, y2 = obj2_pos
    dx, dy = x1 - x2, y1 - y2
    return (dx * dx) + (dy * dy) <= (thresh * thresh)

def within_box(obj_pos, box_pos, box_size):
    """
    Determine if object is within box
    - Squared difference in x (and y) coordinates 
    should be less than the square of half the 
    box width (and height)
    - That would mean the center of the object is
    within the box boundaries
    """
    obj_x, obj_y = obj_pos
    box_x, box_y = box_pos
    box_w, box_h = box_size
    dx, dy = obj_x - box_x, obj_y - box_y
    hw, hh = box_w / 2, box_h / 2
    return dx * dx < hw * hw and dy * dy < hh * hh

def snapped(obj1, obj2, func, **kwargs):
    """
    Determine if obj1 snapped to center of obj2
    - Check if obj1 is 'near' obj2, based on func
    - If yes, set the obj1's position to be 
    equal to obj2's position and return True
    - Otherwise, do nothing and return False
    """
    if func(obj1.pos, obj2.pos, **kwargs):
        obj1.pos = obj2.pos
        return True
    return False
```

## Detecting Clicks

```python
# Coming soon!
```

## Slide Reel in a Single Routine

```python
# Coming soon!
```

## Animation

```python
def anim_linear_xy(start_xy, end_xy, n_frames):
    """
    Calculate the coordinates at each frame for a 
    linear translation from `start_xy` to `end_xy`.
    """
    x0, y0 = start_xy
    x1, y1 = end_xy
    steps, = (n_frames - 1),
    dx, dy = (x1 - x0) / steps, (y1 - y0) / steps
    xys, = [],
    for i in range(n_frames):
        xys.append((x0 + dx * i, y0 + dy * i))
    return xys
```

## 'Utils' (?)

```python
def hide(obj):
    obj.size = (0, 0)
    obj.autoDraw = False

def unhide(obj, size):
    obj.size = size
    obj.autoDraw = True
```
