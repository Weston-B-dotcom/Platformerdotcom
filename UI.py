from typing import Optional, Dict, Union

from pygame import Rect, Color
from pygame.typing import RectLike
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface, UIElement, ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface, IUIElementInterface
from pygame_gui.elements import UIPanel, UIHorizontalSlider, UITextEntryLine
import pygame, pygame_gui


class UIColorEntry(UIPanel):
    """
    454x52
    """
    def __init__(
        self,
        relative_rect: RectLike,
        starting_height: int = 1,
        manager: Optional[IUIManagerInterface] = None,
        *,
        element_id: str = "panel",
        margins: Optional[Dict[str, int]] = None,
        container: Optional[IContainerLikeInterface] = None,
        parent_element: Optional[UIElement] = None,
        object_id: Optional[Union[ObjectID, str]] = None,
        anchors: Optional[Dict[str, Union[str, IUIElementInterface]]] = None,
        visible: int = 1,
    ):
        super().__init__(relative_rect, starting_height, manager, element_id=element_id, margins=margins, container=container, parent_element=parent_element, object_id=object_id, anchors=anchors, visible=visible)
        self.r_text = UITextEntryLine(Rect(0, 0, 150, 24), manager, container=self, object_id=object_id, initial_text="0")
        self.r_slider = UIHorizontalSlider(Rect(0, 24, 150, 24), 0, (0, 255), manager, self, object_id=object_id)
        self.red = 0
        self.g_text = UITextEntryLine(Rect(150, 0, 150, 24), manager, container=self, object_id=object_id, initial_text="0")
        self.g_slider = UIHorizontalSlider(Rect(150, 24, 150, 24), 0, (0, 255), manager, self, object_id=object_id)
        self.green = 0
        self.b_text = UITextEntryLine(Rect(300, 0, 150, 24), manager, container=self, object_id=object_id, initial_text="0")
        self.b_slider = UIHorizontalSlider(Rect(300, 24, 150, 24), 0, (0, 255), manager, self, object_id=object_id)
        self.blue = 0

    def ValidateRed(self, text: bool = True):
        value = self.red
        if text:
            try:
                value = int(self.r_text.get_text().strip())
            except Exception as _:
                value = self.red
        else:
            value = self.r_slider.get_current_value()

        self.red = min(max(0, value), 255)
        self.r_text.set_text(f"{self.red}")
        self.r_slider.set_current_value(self.red)

    def ValidateGreen(self, text: bool = True):
        value = self.green
        if text:
            try:
                value = int(self.g_text.get_text().strip())
            except Exception as _:
                value = self.green
        else:
            value = self.g_slider.get_current_value()

        self.green = min(max(0, value), 255)
        self.g_text.set_text(f"{self.green}")
        self.g_slider.set_current_value(self.green)

    def ValidateBlue(self, text: bool = True):
        value = self.blue
        if text:
            try:
                value = int(self.b_text.get_text().strip())
            except Exception as _:
                value = self.blue
        else:
            value = self.b_slider.get_current_value()

        self.blue = min(max(0, value), 255)
        self.b_text.set_text(f"{self.blue}")
        self.b_slider.set_current_value(self.blue)

    def process_event(self, event: pygame.event.Event):
        super().process_event(event)
        if self is not None:
            match event.type:
                case pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    #print("Change")
                    ...
                case pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    #print("Finished")
                    match event.ui_element:
                        case self.r_text:
                            self.ValidateRed(True)
                        case self.g_text:
                            self.ValidateGreen(True)
                        case self.b_text:
                            self.ValidateBlue(True)
                case pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    #print("Slider")
                    match event.ui_element:
                        case self.r_slider:
                            self.ValidateRed(False)
                        case self.g_slider:
                            self.ValidateGreen(False)
                        case self.b_slider:
                            self.ValidateBlue(False)