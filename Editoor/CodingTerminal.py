from pygame import Rect, Color
from pygame.typing import RectLike
from pygame_gui import UIManager
from pygame_gui.core import IContainerLikeInterface, UIElement, ObjectID
from pygame_gui.core.interfaces import IUIManagerInterface, IUIElementInterface, IContainerAndContainerLike
from pygame_gui.elements import UIPanel, UIHorizontalSlider, UITextEntryLine, UITabContainer, UIScrollingContainer
from Interaction import Interaction, InteractionType, DataType, UnaryType, BinaryType, OperatorType
from DataValues.TypeAliases import Tcolor, Tvec2, Trect
from typing import Iterator
import pygame, pygame_gui

class IUIZeroBorderPanelDefault(UIPanel):
    def __init__(self):
        self.border_width = {
            "left": 0,
            "right": 0,
            "top": 0,
            "bottom": 0
        }
    
    def rebuild_from_changed_theme_data(self):
        """
        Checks if any theming parameters have changed, and if so triggers a full rebuild of the
        panel's drawable shape.
        """
        super().rebuild_from_changed_theme_data()
        has_any_changed = False

        background_colour = self.ui_theme.get_colour_or_gradient(
            "dark_bg", self.combined_element_ids
        )
        if background_colour != self.background_colour:
            self.background_colour = background_colour
            has_any_changed = True

        border_colour = self.ui_theme.get_colour_or_gradient(
            "normal_border", self.combined_element_ids
        )
        if border_colour != self.border_colour:
            self.border_colour = border_colour
            has_any_changed = True

        def parse_to_bool(str_data: str):
            return bool(int(str_data))

        # Load auto_scale_images parameter BEFORE loading images so scaling can be applied
        if self._check_misc_theme_data_changed(
            attribute_name="auto_scale_images",
            default_value=False,
            casting_func=parse_to_bool,
        ):
            has_any_changed = True

        # Use the enhanced image loading system
        if self._set_any_images_from_theme():
            has_any_changed = True

        # misc
        if self._check_misc_theme_data_changed(
            attribute_name="shape",
            default_value="rectangle",
            casting_func=str,
            allowed_values=["rectangle", "rounded_rectangle"],
        ):
            has_any_changed = True

        if self._check_misc_theme_data_changed(
            attribute_name="tool_tip_delay", default_value=1.0, casting_func=float
        ):
            has_any_changed = True

        if self._check_shape_theming_changed(
            defaults={
                "border_width": {"left": 0, "right": 0, "top": 0, "bottom": 0},
                "shadow_width": 2,
                "border_overlap": 1,
                "shape_corner_radius": [2, 2, 2, 2],
            }
        ):
            has_any_changed = True

        if has_any_changed:
            self.rebuild()

class IUIZeroBorderElementDefault(UIElement):
    def __init__(self):
        self.border_width = {
            "left": 0,
            "right": 0,
            "top": 0,
            "bottom": 0
        }
    
    def rebuild_from_changed_theme_data(self):
        """
        Checks if any theming parameters have changed, and if so triggers a full rebuild of the
        panel's drawable shape.
        """
        super().rebuild_from_changed_theme_data()
        has_any_changed = False

        background_colour = self.ui_theme.get_colour_or_gradient(
            "dark_bg", self.combined_element_ids
        )
        if background_colour != self.background_colour:
            self.background_colour = background_colour
            has_any_changed = True

        border_colour = self.ui_theme.get_colour_or_gradient(
            "normal_border", self.combined_element_ids
        )
        if border_colour != self.border_colour:
            self.border_colour = border_colour
            has_any_changed = True

        def parse_to_bool(str_data: str):
            return bool(int(str_data))

        # Load auto_scale_images parameter BEFORE loading images so scaling can be applied
        if self._check_misc_theme_data_changed(
            attribute_name="auto_scale_images",
            default_value=False,
            casting_func=parse_to_bool,
        ):
            has_any_changed = True

        # misc
        if self._check_misc_theme_data_changed(
            attribute_name="shape",
            default_value="rectangle",
            casting_func=str,
            allowed_values=["rectangle", "rounded_rectangle"],
        ):
            has_any_changed = True

        if self._check_misc_theme_data_changed(
            attribute_name="tool_tip_delay", default_value=1.0, casting_func=float
        ):
            has_any_changed = True

        if self._check_shape_theming_changed(
            defaults={
                "border_width": {"left": 0, "right": 0, "top": 0, "bottom": 0},
                "shadow_width": 2,
                "border_overlap": 1,
                "shape_corner_radius": [2, 2, 2, 2],
            }
        ):
            has_any_changed = True

        if has_any_changed:
            self.rebuild()

class UIInteractionEditor(IUIZeroBorderPanelDefault):
    def __init__(
        self,
        relative_rect: RectLike,
        starting_height: int = 1,
        manager: IUIManagerInterface|None = None,
        *,
        element_id: str = "panel",
        margins: dict[str, int]|None = None,
        container: IContainerLikeInterface|None = None,
        parent_element: UIElement|None = None,
        object_id: ObjectID|str|None = None,
        anchors: dict[str, str|IUIElementInterface]|None = None,
        visible: int = 1,
    ):
        super().__init__(relative_rect, starting_height, manager, element_id=element_id, margins=margins, container=container, parent_element=parent_element, object_id=ObjectID(class_id="@code_terminal_panel") if object_id is None else object_id, anchors=anchors, visible=visible)
        super(UIPanel, self).__init__()
        self.panel_container = None
        #self.panel_container = UIContainer()
        self.rebuild()
        self.type: InteractionType = InteractionType.none
        self.data: dict[str, str|int|float|bool|Tvec2|Tcolor|Trect] = {}
        self.args: list[UIInteractionEditor] = []
        self.dirty_size: bool = False
        self.elements: list[IUIElementInterface] = []
    
    def update(self, time_delta):
        super().update(time_delta)
        
        if self.dirty_size:
            self.set_dimensions()

    def on_contained_elements_changed(self, target: IUIElementInterface) -> None:
        """
        Update the positioning of the contained elements of this container. To be called when one of the contained
        elements may have moved, been resized or changed its anchors.

        :param target: the UI element that has been benn moved resized or changed its anchors.
        :return: None
        """
        for element in self.elements:
            if target in element.get_anchor_targets():
                element.update_containing_rect_position()
                self.on_contained_elements_changed(element)

        self.should_update_dimensions = True

    def rebuild(self):
        return super(UIPanel, self).rebuild()

    def add_element(self, element: IUIElementInterface):
        """
        Add a UIElement to the container. The element's relative_rect parameter will be relative to
        this container.

        :param element: A UIElement to add to this container.

        """
        element.change_layer(self._layer + element.get_starting_height())
        self.elements.append(element)
        self.calc_add_element_changes_thickness(element)
        if not self.is_enabled:
            element.disable()
        if not self.visible and hasattr(element, "hide"):
            element.hide()

    def remove_element(self, element: IUIElementInterface):
        """
        Remove a UIElement from this container.

        :param element: A UIElement to remove from this container.

        """
        if element in self.elements:
            self.elements.remove(element)
        if element.get_top_layer() == self.max_element_top_layer:
            self.recalculate_container_layer_thickness()

    def recalculate_container_layer_thickness(self):
        """
        This function will iterate through the elements in our container and determine the
        maximum 'height' that they reach in the 'layer stack'. We then use that to determine the
        overall 'thickness' of this container. The thickness value is used to determine where to
        place overlapping windows in the layers
        """
        max_element_top_layer = self._layer
        for element in self.elements:
            if (
                element.get_top_layer() > max_element_top_layer
                and element not in self.ui_manager.get_window_stack().get_full_stack()
                and (
                    not isinstance(element, UIInteractionEditor)
                    or not element.is_window_root_container
                )
            ):
                max_element_top_layer = element.get_top_layer()
        self.max_element_top_layer = max_element_top_layer
        new_thickness = self.max_element_top_layer - self._layer
        if new_thickness != self.layer_thickness:
            self.layer_thickness = new_thickness
            if self.ui_container is not None and self.ui_container != self:
                self.ui_container.get_container().recalculate_container_layer_thickness()

    def calc_add_element_changes_thickness(self, element: IUIElementInterface):
        """
        This function checks if a single added element will increase the containers thickness
        and if so updates containers recursively.

        :param element: the element to check.
        """
        if (
            element.get_top_layer() > self.max_element_top_layer
            and element not in self.ui_manager.get_window_stack().get_full_stack()
            and (
                not isinstance(element, UIInteractionEditor)
                or not element.is_window_root_container
            )
        ):
            self.max_element_top_layer = element.get_top_layer()
            self.layer_thickness = self.max_element_top_layer - self._layer
            if self.ui_container is not None and self.ui_container != self:
                self.ui_container.get_container().calc_add_element_changes_thickness(
                    self
                )

    def get_size(self) -> tuple[int, int] | tuple[float, float]:
        """
        Get the container's pixel size.

        :return: the pixel size as tuple [x, y]
        """
        return self.relative_rect.size
    
    
    def disable(self):
        """
        Disables all elements in the panel, so they are no longer interactive.
        """
        if self.is_enabled:
            self.is_enabled = False
            for element in self.elements:
                element.disable()

    def enable(self):
        """
        Enables all elements in the panel, so they are interactive again.
        """
        if not self.is_enabled:
            self.is_enabled = True
            for element in self.elements:
                element.enable()

    def show(self, show_contents: bool = True):
        """
        In addition to the base UIElement.show() - call show() of owned container - panel_container.

        :param show_contents: whether to also show the contents of the panel. Defaults to True.
        """
        super().show()
        if not self.visible:
            self.visible = True

            if show_contents:
                for element in self.elements:
                    if hasattr(element, "show"):
                        element.show()

    def hide(self, hide_contents: bool = True):
        """
        In addition to the base UIElement.hide() - call hide() of owned container - panel_container.

        :param hide_contents: whether to also hide the contents of the panel. Defaults to True.
        """
        if self.visible:
            if hide_contents:
                for element in self.elements:
                    if hasattr(element, "hide"):
                        element.hide()

            self.visible = False
        super().hide()

    def get_container(self) -> IContainerAndContainerLike:
        """
        Gets an actual container from this container-like UI element.
        """
        return self

    def __iter__(self) -> Iterator[IUIElementInterface]:
        """
        Iterates over the elements within the container.
        :return Iterator: An iterator over the elements within the container.
        """
        return iter(self.elements)

    def __contains__(self, item: IUIElementInterface) -> bool:
        """
        Checks if the given element is contained within the container.
        :param item: The element to check for containment.
        :return bool: Return True if the element is found, False otherwise.
        """
        return item in self.elements
    
class UICodingPanelContainer(UIScrollingContainer, IUIZeroBorderElementDefault):
    """
    A container like UI element that lets users scroll around a larger container of content with
    scroll bars.

    :param relative_rect: The size and relative position of the container. This will also be the
                          starting size of the scrolling area.
    :param manager: The UI manager for this element. If not provided or set to None,
                    it will try to use the first UIManager that was created by your application.
    :param starting_height: The starting layer height of this container above its container.
                            Defaults to 1.
    :param container: The container this container is within. Defaults to None (which is the root
                      container for the UI)
    :param parent_element: A parent element for this container. Defaults to None, or the
                           container if you've set that.
    :param object_id: An object ID for this element.
    :param anchors: Layout anchors in a dictionary.
    :param visible: Whether the element is visible by default. Warning - container visibility
                    may override this.
    :param allow_scroll_x: Whether a scrollbar should be added to scroll horizontally (when needed).
                           Defaults to True.
    :param allow_scroll_y: Whether a scrollbar should be added to scroll vertically (when needed).
                           Defaults to True.
    """
    def __init__(
        self,
        relative_rect: pygame.Rect,
        manager: IUIManagerInterface|None = None,
        *,
        starting_height: int = 1,
        container: IContainerLikeInterface|None = None,
        parent_element: UIElement|None = None,
        object_id: ObjectID|str|None = None,
        element_id: list[str]|None = None,
        anchors: dict[str, str|IUIElementInterface]|None = None,
        visible: int = 1,
        should_grow_automatically: bool = False,
        allow_scroll_x: bool = True,
        allow_scroll_y: bool = True,
    ):
        super().__init__(relative_rect, manager, starting_height=starting_height, container=container, parent_element=parent_element, object_id=object_id, element_id=element_id, anchors=anchors, visible=visible, should_grow_automatically=should_grow_automatically, allow_scroll_x=allow_scroll_x, allow_scroll_y=allow_scroll_y)
        super(UIScrollingContainer, self).__init__()
        self.rebuild()

        self.instance_tree: list[Interaction] = []
        self.instance_ui: list[UIInteractionEditor] = []
    
    def update(self, time_delta):
        super().update(time_delta)

    def rebuild(self):
        return super(UIScrollingContainer, self).rebuild()

class UICodingTerminal(IUIZeroBorderPanelDefault):
    def __init__(
        self,
        relative_rect: RectLike,
        starting_height: int = 1,
        manager: IUIManagerInterface|None = None,
        *,
        element_id: str = "panel",
        margins: dict[str, int]|None = None,
        container: IContainerLikeInterface|None = None,
        parent_element: UIElement|None = None,
        object_id: ObjectID|str|None = None,
        anchors: dict[str, str|IUIElementInterface]|None = None,
        visible: int = 1,
    ):
        super().__init__(relative_rect, starting_height, manager, element_id=element_id, margins=margins, container=container, parent_element=parent_element, object_id=ObjectID(class_id="@code_terminal_panel") if object_id is None else object_id, anchors=anchors, visible=visible)
        super(UIPanel, self).__init__()
        self.rebuild()

        self.tabs: UITabContainer = UITabContainer(Rect(0, 0, relative_rect.w, relative_rect.h), manager, self)
        self.top_collision_tab_index = self.tabs.add_tab("Top Collision", f"#tab_top_collision_title_button") # top_collision
        self.bottom_collision_tab_index = self.tabs.add_tab("Bottom Collision", f"#tab_bottom_collision_title_button") # bottom_collision
        self.side_collision_tab_index = self.tabs.add_tab("Side Collision", f"#tab_side_collision_title_button") # side_collision
        self.frame_tab_index = self.tabs.add_tab("Frame", f"#tab_frame_title_button") # frame
        self.top_collision_tab_scroll: UICodingPanelContainer = UICodingPanelContainer(Rect(0, 0, relative_rect.w - 2, relative_rect.h - 2), manager, container=self.tabs.get_tab_container(self.top_collision_tab_index), should_grow_automatically=True)
        self.tabs.switch_current_container(self.bottom_collision_tab_index)
        self.bottom_collision_tab_scroll: UICodingPanelContainer = UICodingPanelContainer(Rect(0, 0, relative_rect.w - 2, relative_rect.h - 2), manager, container=self.tabs.get_tab_container(self.bottom_collision_tab_index), should_grow_automatically=True)
        self.tabs.switch_current_container(self.side_collision_tab_index)
        self.side_collision_tab_scroll: UICodingPanelContainer = UICodingPanelContainer(Rect(0, 0, relative_rect.w - 2, relative_rect.h - 2), manager, container=self.tabs.get_tab_container(self.side_collision_tab_index), should_grow_automatically=True)
        self.tabs.switch_current_container(self.frame_tab_index)
        self.frame_tab_scroll: UICodingPanelContainer = UICodingPanelContainer(Rect(0, 0, relative_rect.w - 2, relative_rect.h - 2), manager, container=self.tabs.get_tab_container(self.frame_tab_index), should_grow_automatically=True)
        self.tabs.switch_current_container(self.top_collision_tab_index)

    def process_event(self, event: pygame.event.Event):
        super().process_event(event)
        if self is not None:
            match event.type:
                case pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    ...

    def rebuild(self):
        return super(UIPanel, self).rebuild()