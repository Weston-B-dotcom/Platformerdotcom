from pygame_gui.elements import UIPanel, UIButton, UITextBox, UIScrollingContainer, UIHorizontalSlider, UILabel
from pygame_gui.core import ObjectID
from pygame import Rect, Color, Vector2
from pygame.gfxdraw import rectangle, box
from Application import Application
from Levels import Level
from Platform import Platform
from DataValues import Constants, Assets
from DataValues.TypeAliases import dictStrAny, dictStrStr, Tcolor
from typing import Callable, Any
from Keybinds import Keybinds
from enum import Enum, auto
import pygame, pygame_gui, json, pygame

class DragType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return count

    NONE     = auto()
    PANNING  = auto()
    SELECT   = auto()
    CREATING = auto()
    DELETING = auto()
    MOVING   = auto()
    RESIZING = auto()

class MouseMode(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return count

    CURSOR = auto()
    DELETE = auto()
    INSERT = auto()

def SnapToGrid(vector: Vector2, scale: int):
    return ((vector + Vector2(scale * 0.5, scale * 0.5)) // scale) * scale

GRID_RESIZING_KEYBINDS = [Keybinds.GRID_DECREASE_ONE, Keybinds.GRID_INCREASE_ONE, Keybinds.GRID_DECREASE_TEN, Keybinds.GRID_INCREASE_TEN]

class Editor:
    def __init__(self, app: Application|None = None, key = None):
        self.running: bool|None = None
        self.app = app
        self.key: list[dictStrAny] = [] if key is None else key
        self.color: Color = Color(0, 0, 0)
        self.level: Level = Level.new_level("")
        self.level.background = Assets.GREEN
        self.grid_slider: UIHorizontalSlider = None
        self.grid_slider_label: UILabel = None
        self.cursor_mode: MouseMode = MouseMode.CURSOR

    def run(self):
        dragging: DragType = DragType.NONE
        drag_pos: Vector2 = Vector2(0, 0)
        platform_index: int = -1

        while self.running:
            self.app.StepDeltaTime()
            mouse_level_pos: Vector2 = Vector2(pygame.mouse.get_pos()) + self.app.camera.pos
            mouse_grid_pos: Vector2 = SnapToGrid(mouse_level_pos, self.grid_slider.get_current_value())
            mods: int = pygame.key.get_mods()

            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False
                    case pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pressed()
                        if mouse[0] and mods & pygame.KMOD_LALT:
                            pygame.mouse.get_rel()
                            dragging = DragType.PANNING
                        else:
                            match self.cursor_mode:
                                case MouseMode.CURSOR:
                                    if mouse[0]:
                                        drag_pos = mouse_grid_pos
                                        for i, platform in enumerate(self.level.platforms):
                                            if Rect(platform.rect.topleft - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE).collidepoint(drag_pos.x, drag_pos.y):
                                                platform_index = i
                                                dragging = DragType.MOVING
                                                break
                                            elif Rect(platform.rect.bottomright - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE).collidepoint(drag_pos.x, drag_pos.y):
                                                pygame.mouse.get_rel()
                                                platform_index = i
                                                dragging = DragType.RESIZING
                                                break
                                    elif mouse[2] and mods & pygame.KMOD_LALT:
                                        pygame.mouse.get_rel()
                                        dragging = DragType.SELECT
                                        drag_pos = mouse_grid_pos
                                case MouseMode.DELETE:
                                    if mouse[0]:
                                        drag_pos = mouse_grid_pos
                                        if mods & pygame.KMOD_LSHIFT:
                                            pygame.mouse.get_rel()
                                            dragging = DragType.DELETING
                                        else:
                                            index = -1
                                            for i, platform in enumerate(self.level.platforms):
                                                if platform.rect.collidepoint(drag_pos.x, drag_pos.y):
                                                    index = i
                                                    break
                                            if index != -1:
                                                self.level.platforms.pop(index)
                                case MouseMode.INSERT:
                                    if mouse[0]:
                                        pygame.mouse.get_rel()
                                        dragging = DragType.CREATING
                                        drag_pos = mouse_grid_pos
                    case pygame.MOUSEBUTTONUP:
                        match dragging:
                            case DragType.MOVING:
                                self.level.platforms[platform_index].rect.update(mouse_grid_pos.x, mouse_grid_pos.y, self.level.platforms[platform_index].rect.w, self.level.platforms[platform_index].rect.h)
                                platform_index = -1
                            case DragType.RESIZING:
                                diff = mouse_grid_pos - drag_pos
                                self.level.platforms[platform_index].Resize((self.level.platforms[platform_index].rect.w + diff.x, self.level.platforms[platform_index].rect.h + diff.y))
                                platform_index = -1
                            case DragType.SELECT:
                                ...
                            case DragType.CREATING:
                                x = int(min(drag_pos.x, mouse_grid_pos.x))
                                y = int(min(drag_pos.y, mouse_grid_pos.y))
                                w = int(abs(drag_pos.x - mouse_grid_pos.x))
                                h = int(abs(drag_pos.y - mouse_grid_pos.y))
                                if w != 0 and h != 0:
                                    self.level.platforms.append(Platform((x, y), (w, h), (self.color.r, self.color.g, self.color.b)))
                            case DragType.DELETING:
                                x = int(min(drag_pos.x, mouse_grid_pos.x))
                                y = int(min(drag_pos.y, mouse_grid_pos.y))
                                w = int(abs(drag_pos.x - mouse_grid_pos.x))
                                h = int(abs(drag_pos.y - mouse_grid_pos.y))
                                rect = Rect(x, y, w, h)
                                #print(rect)
                                to_del = []
                                for i, platform in enumerate(self.level.platforms):
                                    print(platform.rect)
                                    if platform.rect.colliderect(rect):
                                        to_del.append(i)
                                to_del.reverse()
                                #print(to_del)
                                for i in to_del:
                                    self.level.platforms.pop(i)
                        dragging = DragType.NONE
                    case pygame.KEYDOWN:
                        if dragging == DragType.NONE or dragging == DragType.PANNING:
                            thingy = sorted([(val, val.IsValid(mods, event.key)) for val in GRID_RESIZING_KEYBINDS if val.IsValid(mods, event.key) > -1], key=lambda x: x[1], reverse=True)
                            if len(thingy) > 0:
                                match thingy[0][0]:
                                    case Keybinds.GRID_DECREASE_ONE:
                                        self.grid_slider.set_current_value(self.grid_slider.get_current_value() - 1, False)
                                        self.grid_slider_label.set_text(f"Grid: {self.grid_slider.get_current_value()}")
                                    case Keybinds.GRID_INCREASE_ONE:
                                        self.grid_slider.set_current_value(self.grid_slider.get_current_value() + 1, False)
                                        self.grid_slider_label.set_text(f"Grid: {self.grid_slider.get_current_value()}")
                                    case Keybinds.GRID_DECREASE_TEN:
                                        self.grid_slider.set_current_value(self.grid_slider.get_current_value() - 10, False)
                                        self.grid_slider_label.set_text(f"Grid: {self.grid_slider.get_current_value()}")
                                    case Keybinds.GRID_INCREASE_TEN:
                                        self.grid_slider.set_current_value(self.grid_slider.get_current_value() + 10, False)
                                        self.grid_slider_label.set_text(f"Grid: {self.grid_slider.get_current_value()}")
                    case pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                        match event.ui_element:
                            case self.grid_slider:
                                self.grid_slider_label.set_text(f"Grid: {self.grid_slider.get_current_value()}")

                self.app.manager.process_events(event)

            #region Game Update Code
            match dragging:
                case DragType.PANNING:
                    self.app.camera.pos -= Vector2(pygame.mouse.get_rel())
                    mouse_level_pos = Vector2(pygame.mouse.get_pos()) + self.app.camera.pos
                    mouse_grid_pos = SnapToGrid(mouse_level_pos, self.grid_slider.get_current_value())
            #endregion
            self.app.manager.update(self.app.delta_time)

            self.app.screen.fill(Assets.BLACK)
            #region Render the game
            level_origin_screen_pos: Vector2 = -self.app.camera.pos
            box(self.app.screen, Rect(level_origin_screen_pos, self.level.size), self.level.background)

            if dragging == DragType.MOVING and platform_index != -1:
                for platform in self.level.platforms:
                    new_rect = Rect((mouse_grid_pos if platform == self.level.platforms[platform_index] else platform.rect.topleft) + level_origin_screen_pos, platform.rect.size)
                    if -new_rect.w < new_rect.x < Constants.SCREEN_WIDTH and -new_rect.h < new_rect.y < Constants.SCREEN_HEIGHT:
                        self.app.screen.blit(platform.image, new_rect)
                        match self.cursor_mode:
                            case MouseMode.CURSOR:
                                box(self.app.screen, Rect(new_rect.topleft - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
                                box(self.app.screen, Rect(new_rect.bottomright - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
            elif dragging == DragType.RESIZING and platform_index != -1:
                diff = mouse_grid_pos - drag_pos
                for platform in self.level.platforms:
                    new_rect = Rect(platform.rect.topleft + level_origin_screen_pos, platform.rect.size + diff if platform == self.level.platforms[platform_index] else platform.rect.size)
                    if -new_rect.w < new_rect.x < Constants.SCREEN_WIDTH and -new_rect.h < new_rect.y < Constants.SCREEN_HEIGHT:
                        surf = platform.image
                        if self.level.platforms[platform_index] == platform:
                            #print(f"Diff: {diff}\nSize: {platform.rect.size}\nNew Size: {platform.rect.size + diff}")
                            surf = pygame.Surface(platform.rect.size + diff)
                            surf.fill(platform.color)
                        self.app.screen.blit(surf, new_rect)
                        match self.cursor_mode:
                            case MouseMode.CURSOR:
                                box(self.app.screen, Rect(new_rect.topleft - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
                                box(self.app.screen, Rect(new_rect.bottomright - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
            else:
                for platform in self.level.platforms:
                    new_rect = Rect((platform.rect.topleft) + level_origin_screen_pos, platform.rect.size)
                    if -new_rect.w < new_rect.x < Constants.SCREEN_WIDTH and -new_rect.h < new_rect.y < Constants.SCREEN_HEIGHT:
                        self.app.screen.blit(platform.image, new_rect)
                        match self.cursor_mode:
                            case MouseMode.CURSOR:
                                box(self.app.screen, Rect(new_rect.topleft - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
                                box(self.app.screen, Rect(new_rect.bottomright - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)


            match dragging:
                case DragType.SELECT:
                    rectangle(self.app.screen, Rect(drag_pos + level_origin_screen_pos, mouse_grid_pos - (drag_pos + level_origin_screen_pos)), Assets.LIGHT_BLUE)
                case DragType.DELETING:
                    rectangle(self.app.screen, Rect(drag_pos + level_origin_screen_pos, mouse_grid_pos - (drag_pos + level_origin_screen_pos)), Assets.DARK_RED)
                case DragType.CREATING:
                    rectangle(self.app.screen, Rect(drag_pos + level_origin_screen_pos, mouse_grid_pos - (drag_pos + level_origin_screen_pos)), self.color)
            #endregion
            self.app.manager.draw_ui(self.app.screen)

            pygame.display.flip()

    def init(self):
        self.app.manager.clear_and_reset()
        self.running = True
        self.app.camera.pos = Vector2(0, 0)

        side_panel = UIPanel(Rect((0, 0), (200, Constants.SCREEN_HEIGHT)), manager=self.app.manager, object_id=ObjectID("#side_panel", "@editor"))
        self.grid_slider_label = UILabel(Rect(0, 0, 200 - 4, 24), "Grid: 1", self.app.manager, side_panel)
        self.grid_slider = UIHorizontalSlider(Rect(0, 24, 200 - 4, 24), 1, (1, 100), self.app.manager, container=side_panel, object_id=ObjectID("#grid_slider", "@editor"), click_increment=1)
        ui_panel = UIPanel(Rect((200, Constants.SCREEN_HEIGHT - 150, Constants.SCREEN_WIDTH - 200, 150)), manager=self.app.manager, object_id=ObjectID("#ui_panel", "@editor"))

        #UITextBox("Editor", Rect(12, 7, Constants.SCREEN_WIDTH - 124, 50), self.app.manager, object_id=ObjectID("#sub_title", "@editor"))

        UITextBox("Materials:", Rect(0, 0, Constants.SCREEN_WIDTH - 200, 50), self.app.manager, container=ui_panel, object_id=ObjectID("#ui_panel", "@editor"))
        scrolling_container = UIScrollingContainer(Rect(20, 60, Constants.SCREEN_WIDTH - 200, 150), self.app.manager, container=ui_panel, should_grow_automatically=True)

        def ButtonMaker(color: Tcolor) -> Callable[[], None]:
            def InnerFunction() -> None:
                self.color = Color(color)
            return InnerFunction

        with open("Game/Materials.json", "r") as file:
            for i, entry in enumerate(json.load(file).get("Materials", [])):
                UIButton(Rect(i * 100, 0, 75, 75), f"{entry['text']}", self.app.manager, scrolling_container, object_id=ObjectID(f"{entry['id']}", "@editor"), command=ButtonMaker(entry['color']))

        UIButton(Rect(50, 50, 100, 100), "", self.app.manager, side_panel, object_id=ObjectID("#cursor_icon", "@editor"), command=lambda: self.SetCursorMode(MouseMode.CURSOR))
        UIButton(Rect(50, 250, 100, 100), "DELETE", self.app.manager, side_panel, object_id=ObjectID("#icon", "@editor"), command=lambda: self.SetCursorMode(MouseMode.DELETE))
        UIButton(Rect(50, 450, 100, 100), "INSERT", self.app.manager, side_panel, object_id=ObjectID("#icon", "@editor"), command=lambda: self.SetCursorMode(MouseMode.INSERT))

        return not self.running, "Editor"

    def SetCursorMode(self, cursor_mode: MouseMode):
        self.cursor_mode = cursor_mode

    def to_dict(self) -> dictStrAny:
        return {
            "Materials": self.key
        }

    @classmethod
    def from_dict(cls, data: dictStrAny):
        return cls(key=data["Materials"])