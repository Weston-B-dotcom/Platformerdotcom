from pygame import Surface, Clock, Rect, Font
from pygame_gui.core import ObjectID
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UILabel, UIButton, UITextBox
from DataValues import Constants, Assets
import pygame

def main():
    pygame.init()
    screen: Surface = pygame.display.set_mode(Constants.SCREEN_SIZE)
    uiManager: UIManager = UIManager(Constants.SCREEN_SIZE, "Data/Themes/launcher_theme.json")
    clock: Clock = Clock()

    def m_RunGame():
        ...
    def m_RunEditor():
        ...
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
    title = UITextBox("Platformer<font color=#000000>dot</font>com", Rect(60, 17, Constants.SCREEN_WIDTH - 124, 75), uiManager, container=panel, object_id=ObjectID("#title", "@main_menu"))
    play = UIButton(Rect(60, 97, Constants.SCREEN_WIDTH - 124, 75), "Play Game", uiManager, panel, object_id=ObjectID("#play", "@main_menu"), command=lambda: m_RunGame)
    play.set_tooltip(text="Uh... Plays the game?", delay=30000)
    editor = UIButton(Rect(60, 192, Constants.SCREEN_WIDTH - 124, 75), "Editor", uiManager, panel, "You get to create your own levels and use other people's levels!", object_id=ObjectID("#editor", "@main_menu"), command=lambda: m_RunEditor)
    achievement = UIButton(Rect(60, 287, Constants.SCREEN_WIDTH - 124, 75), "Achievements", uiManager, panel, "Take a look at your hard work!", object_id=ObjectID("#achievements", "@main_menu"), command=lambda: m_RunAchievement)
    debug = UIButton(Rect(60, 382, Constants.SCREEN_WIDTH - 124, 75), "Debug Panel", uiManager, panel, "Early bird gets the worm...", object_id=ObjectID("#debug", "@main_menu"), command=lambda: m_RunDebug)
    porter = UIButton(Rect(60, 477, Constants.SCREEN_WIDTH - 124, 75), "Porter", uiManager, panel, "Teleporter!!! (jk it for updates :3)", object_id=ObjectID("#porter", "@main_menu"), command=lambda: m_RunPorter)

    #TODO: Make Achievement button, Editor button, Debug button, and Porter button

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            uiManager.process_events(event)

        uiManager.update(clock.tick())

        screen.fill(Assets.WHITE)

        uiManager.draw_ui(screen)

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()