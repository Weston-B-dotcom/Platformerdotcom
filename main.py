from pygame import Surface, Clock, Rect, Font
from pygame_gui.core import ObjectID
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UILabel, UIButton, UITextBox
from Editoor.Editor import Editor
from DataValues import Constants, Assets
from Application import Application
import pygame

def main():
    pygame.init()
    screen: Surface = pygame.display.set_mode(Constants.SCREEN_SIZE)
    #Constants.SCREEN_SIZE = screen.get_size()
    #Constants.SCREEN_WIDTH = screen.get_width()
    #Constants.SCREEN_HEIGHT = screen.get_height()
    uiManager: UIManager = UIManager(Constants.SCREEN_SIZE, "Data/Themes/launcher_theme.json")
    clock: Clock = Clock()
    uiManager.preload_fonts([
        {'name': 'montserrat', 'point_size': 72, 'style': 'regular', 'antialiased': '1'},
        {'name': 'montserrat', 'point_size': 64, 'style': 'regular', 'antialiased': '1'},
        {'name': 'montserrat', 'point_size': 36, 'style': 'regular', 'antialiased': '1'},
        {'name': 'montserrat', 'point_size': 32, 'style': 'regular', 'antialiased': '1'},
        {'name': 'montserrat', 'point_size': 16, 'style': 'regular', 'antialiased': '1'}
    ])

    def m_RunGame():
        ...
    def m_RunEditor():
        nonlocal running, m_type
        running, m_type = edit.init()

    def m_RunAchievement():
        ...
    def m_RunDebug():
        ...
    def m_RunPorter():
        ...


    uiManager.clear_and_reset()
    panel = UIPanel(Rect((0, 0), Constants.SCREEN_SIZE), manager=uiManager)
    panel.border_colour = Assets.BLACK
    panel.background_colour = Assets.LIGHT_GRAY
    UITextBox("Platformer<font color=#000000>dot</font>com", Rect(60, 17, Constants.SCREEN_WIDTH - 124, 80), uiManager, container=panel, object_id=ObjectID("#title", "@main_menu"))
    play = UIButton(Rect(60, 97, Constants.SCREEN_WIDTH - 124, 80), "Play Game", uiManager, panel, object_id=ObjectID("#play", "@main_menu_button"), command=lambda: m_RunGame())
    play.set_tooltip(text="Uh... Plays the game?", delay=30)
    UIButton(Rect(60, 197, Constants.SCREEN_WIDTH - 124, 80), "Editor", uiManager, panel, "You get to create your own levels and use other people's levels!", object_id=ObjectID("#editor", "@main_menu_button"), command=lambda: m_RunEditor())
    UIButton(Rect(60, 297, Constants.SCREEN_WIDTH - 124, 80), "Achievements", uiManager, panel, "Take a look at your hard work!", object_id=ObjectID("#achievements", "@main_menu_button"), command=lambda: m_RunAchievement())
    UIButton(Rect(60, 397, Constants.SCREEN_WIDTH - 124, 80), "Debug Panel", uiManager, panel, "Early bird gets the worm...", object_id=ObjectID("#debug", "@main_menu_button"), command=lambda: m_RunDebug())
    UIButton(Rect(60, 497, Constants.SCREEN_WIDTH - 124, 80), "Porter", uiManager, panel, "Teleporter!!! (jk it for updates :3)", object_id=ObjectID("#porter", "@main_menu_button"), command=lambda: m_RunPorter())

    app: Application = Application(Constants.VERSION, screen, uiManager, clock)
    edit: Editor = Editor(app)

    running: bool = True
    m_type = ""
    while running:
        app.StepDeltaTime()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            uiManager.process_events(event)

        uiManager.update(app.delta_time)

        screen.fill(Assets.WHITE)

        uiManager.draw_ui(screen)

        pygame.display.flip()

    match m_type:
        case "Game":
            ...
        case "Editor":
            edit.run()
        case "Achievements":
            ...
        case "Debug":
            ...
        case "Porter":
            ...
    pygame.quit()

if __name__ == "__main__":
    main()