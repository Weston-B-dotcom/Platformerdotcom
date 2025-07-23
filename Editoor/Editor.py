from pygame_gui.elements import UIPanel, UIButton, UITextBox, UIScrollingContainer, UIHorizontalSlider, UILabel, \
    UIWindow, UITextEntryLine, UIDropDownMenu
from pygame_gui.core import ObjectID
from pygame_gui.windows import UIFileDialog
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

from UI import UIColorEntry


class DragType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return count

    NONE              = auto()
    PANNING           = auto()
    SELECT            = auto()
    CREATING          = auto()
    DELETING          = auto()
    MOVING            = auto()
    RESIZING          = auto()
    CHECKPOINT_MOVING = auto()

class MouseMode(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return count

    CURSOR     = auto()
    DELETE     = auto()
    INSERT     = auto()
    CHECKPOINT = auto()

def SnapToGrid(vector: Vector2, scale: int):
    return ((vector + Vector2(scale * 0.5, scale * 0.5)) // scale) * scale

class ChangeType(Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> Any:
        return count

    PLATFORM_CREATE   = auto()
    PLATFORM_DELETE   = auto()
    PLATFORM_MOVE     = auto()
    PLATFORM_RESIZE   = auto()
    CHECKPOINT_CREATE = auto()
    CHECKPOINT_DELETE = auto()
    CHECKPOINT_MOVE   = auto()
    

class ChangeInfo: # <- This makes it easier if we have a class to hold change info.
    def __init__(self, change_type: ChangeType, data: dictStrAny):
        self.change_type = change_type
        self.data = data

    def __repr__(self):
        return f"{self.change_type.name}: {self.data}"

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
        self.save_window: UIWindow = None
        self.cursor_mode: MouseMode = MouseMode.CURSOR
        self.changes: list[ChangeInfo] = []
        self.change_index: int = -1

        self.level_name: UITextEntryLine = None
        self.tag_add_name: UITextEntryLine = None
        self.tags_scroll: UIScrollingContainer = None
        self.tags_list: list[UIButton] = []
        self.growth_button: UIButton = None
        self.growth_direction: UIDropDownMenu = None
        self.growth_amount: UITextEntryLine = None
        self.background: UIColorEntry = None

        # Hop on down to init, we're making a window.


        # In theory we could add branching in the future.
        # what that
        # Like how git does it.
        # Aka when you make a new change instead of nuking everything in front of where you are.
        # You add a horizontal 'branch', so if you go back to the other branch.
        # That undo tree is kept.
        #   2
        # 1 2 <-                                            this 1 here
        # 1 2 <- point where change is made, instead of deleting ^, you split to a new branch.
        # 1
        # 1
        # 1 = branch 1
        # 2 = branch 2
        # definetly
        # Not hard to do, but we should probably get save screen in. Simple enough.

        # a = UIWindow(Rect(0, 0, 1, 1), self.app.manager)
        # a.kill()

    def undo(self):
        if self.change_index < 0:
            return
        #print("Undoing: ")
        #print(self.change_index)
        #print(self.changes)
        change: ChangeInfo = self.changes[self.change_index]
        match change.change_type:
            case ChangeType.PLATFORM_CREATE:
                self.level.platforms.pop()
            case ChangeType.PLATFORM_DELETE:
                self.level.platforms.insert(change.data["platform"], Platform.from_dict(change.data["data"]))
            case ChangeType.PLATFORM_MOVE:
                self.level.platforms[change.data["platform"]].rect.update(change.data["old_pos"], self.level.platforms[change.data["platform"]].rect.size)
            case ChangeType.PLATFORM_RESIZE:
                self.level.platforms[change.data["platform"]].Resize(Vector2(change.data["old_pos"]))
        self.change_index -= 1

    def redo(self):
        #print("Redoing (Pre index): ")
        #print(self.change_index)
        #print(self.changes)
        if self.change_index >= len(self.changes) - 1:
            return
        self.change_index += 1
        #print("Redoing (Post index): ")
        #print(self.change_index)
        #print(self.changes)
        change: ChangeInfo = self.changes[self.change_index]
        match change.change_type:
            case ChangeType.PLATFORM_CREATE:
                self.level.platforms.append(Platform.from_dict(change.data["data"]))
            case ChangeType.PLATFORM_DELETE:
                self.level.platforms.pop(change.data["platform"])
            case ChangeType.PLATFORM_MOVE:
                self.level.platforms[change.data["platform"]].rect.update(change.data["new_pos"], self.level.platforms[change.data["platform"]].rect.size)
            case ChangeType.PLATFORM_RESIZE:
                self.level.platforms[change.data["platform"]].Resize(Vector2(change.data["new_pos"]))

    def AddToStack(self, change: ChangeInfo):
        #print("Pre stack: ")
        #print(self.changes)
        #print(self.change_index)

        self.changes = self.changes[:(self.change_index + 1)]
        self.changes.append(change)
        self.change_index += 1

        #print("Post stack: ")
        #print(self.changes)
        #print(self.change_index)

    def run(self):
        dragging: DragType = DragType.NONE
        drag_pos: Vector2 = Vector2(0, 0)
        platform_index: int = -1
        checkpoint_index: int = -1

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
                            break
                        else:
                            match self.cursor_mode:
                                case MouseMode.CHECKPOINT:
                                    if mouse[0]:
                                        if mods & pygame.KMOD_LSHIFT:
                                            drag_pos = mouse_grid_pos
                                            for i, checkpoint in enumerate(self.level.checkpoints):
                                                if Assets.Textures.CHECKPOINT_TEXTURE.texture.get_rect(center=(checkpoint)).collidepoint(mouse_grid_pos.x, mouse_grid_pos.y):
                                                    checkpoint_index = i
                                                    dragging = DragType.CHECKPOINT_MOVING
                                                    break
                                        else:
                                            ...
                                    elif mouse[2]:
                                        index = -1
                                        for i, checkpoint in enumerate(self.level.checkpoints):
                                            if Assets.Textures.CHECKPOINT_TEXTURE.texture.get_rect(center=(checkpoint)).collidepoint(mouse_grid_pos.x, mouse_grid_pos.y):
                                                index = i
                                                break
                                        if index != -1:
                                            self.AddToStack(ChangeInfo(ChangeType.CHECKPOINT_DELETE, {
                                                "checkpoint": index,
                                                "data": self.level.checkpoints.pop(index)
                                            }))
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
                                                self.AddToStack(ChangeInfo(ChangeType.PLATFORM_DELETE, {
                                                    "platform": index,
                                                    "data": self.level.platforms.pop(index).to_dict()
                                                }))
                                case MouseMode.INSERT:
                                    if mouse[0]:
                                        pygame.mouse.get_rel()
                                        dragging = DragType.CREATING
                                        drag_pos = mouse_grid_pos
                    case pygame.MOUSEBUTTONUP:
                        match dragging:
                            case DragType.MOVING:
                                self.AddToStack(ChangeInfo(ChangeType.PLATFORM_RESIZE, {
                                    "platform": platform_index,
                                    "old_pos": self.level.platforms[platform_index].rect.topleft,
                                    "new_pos": mouse_grid_pos
                                }))
                                self.level.platforms[platform_index].rect.update(mouse_grid_pos.x, mouse_grid_pos.y, self.level.platforms[platform_index].rect.w, self.level.platforms[platform_index].rect.h)
                                platform_index = -1
                            case DragType.RESIZING:
                                diff = mouse_grid_pos - drag_pos
                                self.AddToStack(ChangeInfo(ChangeType.PLATFORM_RESIZE, {
                                    "platform": platform_index,
                                    "old_size": self.level.platforms[platform_index].rect.size,
                                    "new_size": (self.level.platforms[platform_index].rect.w + diff.x, self.level.platforms[platform_index].rect.h + diff.y)
                                }))
                                self.level.platforms[platform_index].Resize(Vector2(self.level.platforms[platform_index].rect.w + diff.x, self.level.platforms[platform_index].rect.h + diff.y))
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
                                    self.AddToStack(ChangeInfo(ChangeType.PLATFORM_CREATE, {
                                        "data": self.level.platforms[-1].to_dict()
                                    }))
                            case DragType.DELETING:
                                x = int(min(drag_pos.x, mouse_grid_pos.x))
                                y = int(min(drag_pos.y, mouse_grid_pos.y))
                                w = int(abs(drag_pos.x - mouse_grid_pos.x))
                                h = int(abs(drag_pos.y - mouse_grid_pos.y))
                                rect = Rect(x, y, w, h)
                                to_del = []
                                for i, platform in enumerate(self.level.platforms):
                                    if platform.rect.colliderect(rect):
                                        to_del.append(i)
                                to_del.reverse()
                                for i in to_del:
                                    self.AddToStack(ChangeInfo(ChangeType.PLATFORM_DELETE, {
                                        "platform": i,
                                        "data": self.level.platforms.pop(i).to_dict()
                                    }))
                        dragging = DragType.NONE
                    case pygame.KEYDOWN: # Test it
                        if Keybinds.REDO.IsValid(mods, event.key):
                            self.redo()
                        elif Keybinds.UNDO.IsValid(mods, event.key):
                            self.undo()
                        elif dragging == DragType.NONE or dragging == DragType.PANNING:
                            thingy = sorted([(val, val.IsValid(mods, event.key)) for val in GRID_RESIZING_KEYBINDS if val.IsValid(mods, event.key) > -1], key=lambda z: z[1], reverse=True)
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
                    case pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                        with open(event.text, "w") as file:
                            json.dump(self.level.to_dict(), file)

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
                            surf = pygame.Surface(platform.rect.size + diff)
                            surf.fill(platform.color)
                        self.app.screen.blit(surf, new_rect)
                        match self.cursor_mode:
                            case MouseMode.CURSOR:
                                box(self.app.screen, Rect(new_rect.topleft - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
                                box(self.app.screen, Rect(new_rect.bottomright - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
            else:
                for platform in self.level.platforms:
                    new_rect = Rect(platform.rect.topleft + level_origin_screen_pos, platform.rect.size)
                    if -new_rect.w < new_rect.x < Constants.SCREEN_WIDTH and -new_rect.h < new_rect.y < Constants.SCREEN_HEIGHT:
                        self.app.screen.blit(platform.image, new_rect)
                        match self.cursor_mode:
                            case MouseMode.CURSOR:
                                box(self.app.screen, Rect(new_rect.topleft - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
                                box(self.app.screen, Rect(new_rect.bottomright - Constants.HANDLE_HALF_SIZE, Constants.HANDLE_SIZE), Assets.DARK_GRAY)
            
            match self.cursor_mode:
                case MouseMode.CHECKPOINT:
                    self.app.screen.fblits([Assets.Textures.CHECKPOINT_TEXTURE.texture, Assets.Textures.CHECKPOINT_TEXTURE.texture.get_rect(center=(pt.x + level_origin_screen_pos.x, pt.y + level_origin_screen_pos.y)) for pt in self.level.checkpoints])

            match dragging:
                case DragType.SELECT:
                    rectangle(self.app.screen, Rect(drag_pos + level_origin_screen_pos, (mouse_grid_pos + level_origin_screen_pos) - (drag_pos + level_origin_screen_pos)), Assets.LIGHT_BLUE)
                case DragType.DELETING:
                    rectangle(self.app.screen, Rect(drag_pos + level_origin_screen_pos, (mouse_grid_pos + level_origin_screen_pos) - (drag_pos + level_origin_screen_pos)), Assets.DARK_RED)
                case DragType.CREATING:
                    rectangle(self.app.screen, Rect(drag_pos + level_origin_screen_pos, (mouse_grid_pos + level_origin_screen_pos) - (drag_pos + level_origin_screen_pos)), self.color)
            #endregion
            self.app.manager.draw_ui(self.app.screen)

            pygame.display.flip()

        # Ok, let's add a way to open this menu, then test if stuff is doing stuff.

    def PopTag(self, index: int):
        self.tags_list.pop(index)

    def AddTag(self):
        def GenDelTag(name: str):
            def DelTag():
                index = -1
                for i, rag in enumerate(self.tags_list):
                    print(f"{i} - {rag.text}/{name}")
                    if rag.text == name:
                        print("match")
                        index = i
                        break
                if index != -1:
                    print("Pop")
                    self.PopTag(index)
                    print("Refresh")
                    self.RefreshTags()
            return DelTag

        tag = self.tag_add_name.get_text()
        if tag.strip() != "" and tag not in map(lambda x: x.text, self.tags_list):
            self.tags_list.append(UIButton(Rect(0, 0, 127, 24), tag, self.app.manager, self.tags_scroll, command=GenDelTag(tag)))
            self.RefreshTags()

    def RefreshTags(self):
        # This should just be list stuff.
        print("Refreshed")
        MAX_LIST_WIDTH = Constants.SCREEN_WIDTH - 518
        list_width = 127 # Width of individual tags, since then you can fit 7.
        for i in range(len(self.tags_list)):
            x = i % 7 * list_width
            y = i // 7 * 24
            self.tags_list[i].set_relative_position((x, y))

    def Grow(self):
        try:
            amount = int(self.growth_amount.get_text())
            abs_amount = abs(amount)
            if amount > 0:
                self.level.Grow(abs_amount, self.growth_direction.selected_option)
            elif amount < 0:
                self.level.Shrink(abs_amount, self.growth_direction.selected_option)
        except Exception as _:

            ...

    def SaveLevel(self):
        self.level.name = self.level_name.get_text()
        UIFileDialog(Rect((0, 0), Constants.SCREEN_SIZE), self.app.manager, "Save level as:", {".json"}, "./Mods/level.json")


    def ApplyBackground(self):
        self.level.background = (self.background.red, self.background.green, self.background.blue)

    def init(self):
        self.app.manager.clear_and_reset()
        self.running = True
        self.app.camera.pos = Vector2(0, 0)

        self.save_window = UIWindow(Rect(150, 150, Constants.SCREEN_WIDTH - 300, 600), self.app.manager, "Save", object_id=ObjectID("#normal", "@save"))
        self.save_window.on_close_window_button_pressed = self.save_window.hide
        #Ok, now what goes in this?
        # Elements: #Ill fill in the exact types since I know them.
        #  - name (UIEntryLine): What is the level going to be called?
        #  - tags (Auto generated, probably in a scrolling, will figure this out): What type of stuff is in the level? (difficulty, materials etc.)
        #  - size (UIEntryLine 2x + UIDropdown + UIButton): How big does the level have to be to fit all materials?
        #  - background (Something exists for this, will find soon): What background does the level have?
        #  - save (UIButton):

        self.level_name = UITextEntryLine(Rect(10, 10, 100, 50), self.app.manager, self.save_window, object_id=ObjectID("#normal", "@save"))

        a = UIPanel(Rect(10, 60, Constants.SCREEN_WIDTH - 514, 128), 1, self.app.manager, container=self.save_window, object_id=ObjectID("#normal", "@save"))

        self.tag_add_name = UITextEntryLine(Rect(10, 0, Constants.SCREEN_WIDTH - 528 - 130, 24), self.app.manager, container=a, object_id=ObjectID("#normal", "@save"))
        UIButton(Rect(Constants.SCREEN_WIDTH - 528 - 120, 0, 120, 24), "Add Tag", self.app.manager, container=a, object_id=ObjectID("#normal", "@save"), command=lambda: self.AddTag()) #Lack of thing. Also a was meant to be embeded in the window. It was just the panel to hold the tags.
        self.tags_scroll = UIScrollingContainer(Rect(0, 24, Constants.SCREEN_WIDTH - 514, 100), self.app.manager, container=a, object_id=ObjectID("#normal", "@save"))
        self.tags_list = []

        self.growth_button = UIButton(Rect(10, 198, 100, 24), "Grow", self.app.manager, self.save_window, object_id=ObjectID("#normal", "@save"), command=lambda: self.Grow())           # These should be in the same row
        self.growth_direction = UIDropDownMenu(["Up", "Down", "Left", "Right"], "Up", Rect(110, 198, 100, 24), self.app.manager, self.save_window, object_id=ObjectID("#normal", "@save"))  # These should be in the same row
        self.growth_amount = UITextEntryLine(Rect(220, 198, Constants.SCREEN_WIDTH - 220 - 14, 24), self.app.manager, self.save_window, object_id=ObjectID("#normal", "@save"), initial_text="0")    # These should be in the same row

        self.background = UIColorEntry(Rect(10, 232, 229, 52), 1, self.app.manager, object_id=ObjectID("#normal", "@save"), container=self.save_window) # 154x52 trust me on this one.
        UIButton(Rect(239, 232, 120, 52), "Apply", self.app.manager, self.save_window, object_id=ObjectID("#normal", "@save"), command=lambda: self.ApplyBackground())
        UIButton(Rect(10, 294, Constants.SCREEN_WIDTH - 514, 24), "Save", self.app.manager, self.save_window, object_id=ObjectID("#normal", "@save"), command=lambda: self.SaveLevel()) # save button
        self.save_window.hide()

        side_panel = UIPanel(Rect((0, 0), (204, Constants.SCREEN_HEIGHT)), manager=self.app.manager, object_id=ObjectID("#side_panel", "@editor"))
        self.grid_slider_label = UILabel(Rect(0, 0, 200, 24), "Grid: 1", self.app.manager, side_panel)
        self.grid_slider = UIHorizontalSlider(Rect(0, 24, 200, 24), 1, (1, 100), self.app.manager, container=side_panel, object_id=ObjectID("#grid_slider", "@editor"), click_increment=1)
        ui_panel = UIPanel(Rect((204, Constants.SCREEN_HEIGHT - 150, Constants.SCREEN_WIDTH - 204, 150)), manager=self.app.manager, object_id=ObjectID("#ui_panel", "@editor"))

        #UITextBox("Editor", Rect(12, 7, Constants.SCREEN_WIDTH - 124, 50), self.app.manager, object_id=ObjectID("#sub_title", "@editor"))

        UITextBox("Materials:", Rect(0, 0, Constants.SCREEN_WIDTH - 204, 50), self.app.manager, container=ui_panel, object_id=ObjectID("#ui_panel", "@editor"))
        scrolling_container = UIScrollingContainer(Rect(20, 60, Constants.SCREEN_WIDTH - 204, 150), self.app.manager, container=ui_panel, should_grow_automatically=True)

        def ButtonMaker(color: Tcolor) -> Callable[[], None]:
            def InnerFunction() -> None:
                self.color = Color(color)
            return InnerFunction

        with open("Game/Materials.json", "r") as file:
            for i, entry in enumerate(json.load(file).get("Materials", [])):
                UIButton(Rect(i * 100, 0, 75, 75), f"{entry['text']}", self.app.manager, scrolling_container, object_id=ObjectID(f"{entry['id']}", "@editor"), command=ButtonMaker(entry['color']))

        for i, (object_id, func) in enumerate([
            ("#undo_icon", lambda: self.undo()),
            ("#redo_icon", lambda: self.redo()),
            ("#cursor_icon", lambda: self.SetCursorMode(MouseMode.CURSOR)),
            ("#trash_icon", lambda: self.SetCursorMode(MouseMode.DELETE)),
            ("#insert_icon", lambda: self.SetCursorMode(MouseMode.INSERT)),
            ("#save_icon", lambda: self.save_window.show())]):
            UIButton(Rect((i % 4) * 50, ((i // 4) * 50) + 50, 50, 50), "", self.app.manager, side_panel, object_id=ObjectID(object_id, "@round_big_button"), command=func)

        #UIButton(Rect(0, 50, 50, 50), "", self.app.manager, side_panel, object_id=ObjectID("#undo_icon", "@round_big_button"), command=lambda: self.undo())
        #UIButton(Rect(50, 50, 50, 50), "", self.app.manager, side_panel, object_id=ObjectID("#redo_icon", "@round_big_button"), command=lambda: self.redo())
        #UIButton(Rect(100, 50, 50, 50), "", self.app.manager, side_panel, object_id=ObjectID("#cursor_icon", "@round_big_button"), command=lambda: self.SetCursorMode(MouseMode.CURSOR))
        #UIButton(Rect(150, 50, 50, 50), "", self.app.manager, side_panel, object_id=ObjectID("#trash_icon", "@round_big_button"), command=lambda: self.SetCursorMode(MouseMode.DELETE))
        #UIButton(Rect(0, 100, 50, 50), "", self.app.manager, side_panel, object_id=ObjectID("#insert_icon", "@round_big_button"), command=lambda: self.SetCursorMode(MouseMode.INSERT))
        #UIButton(Rect(0, 100, 50, 50), "", self.app.manager, side_panel, object_id=ObjectID("#save_icon", "@round_big_button"), command=lambda: self.save_window.show())

        return not self.running, "Editor" # Ok now push.

    def SetCursorMode(self, cursor_mode: MouseMode):
        self.cursor_mode = cursor_mode

    def to_dict(self) -> dictStrAny:
        return {
            "Materials": self.key
        }

    @classmethod
    def from_dict(cls, data: dictStrAny):
        return cls(key=data["Materials"])