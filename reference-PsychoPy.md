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
