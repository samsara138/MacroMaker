from . import globals


def center_to_global_translation(x, y):
    """
    From center screen relative position to global position
    """
    x -= globals.x_offset
    y -= globals.y_offset
    return x, y


def global_to_center_translation(x, y):
    """
    From global position to center screen relative position
    """
    x += globals.x_offset
    y += globals.y_offset
    return x, y
