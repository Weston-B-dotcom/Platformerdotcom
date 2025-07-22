import pygame
from DataValues import Constants, Assets
from pygame import Surface, Clock, Rect
from pygame.key import ScancodeWrapper
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UILabel, UIButton

class Application:
    def __init__(self):
        self.running: bool = True
        self.screen: Surface|None = None
        self.clock: Clock|None = None
        self.uiManager: UIManager|None = None
        self.deltaTime: float = 0
        self.deltaAccumulator: float = 0

    def StepDeltaTime(self):
        self.deltaTime = min(self.clock.tick(Constants.FPS) / 1000.0, Constants.DELTA_TIME)
        self.deltaAccumulator += self.deltaTime

def initApplication() -> Application:
    """A factory for creating an Application instance.

    Returns:
        (Application): The application instance.
    """
    app: Application = Application()
    app.screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
    app.clock = Clock()
    app.uiManager = UIManager(Constants.SCREEN_SIZE)
    return app

def RecreateUI(app: Application):
    def m_DoSomethingAction(a_app: Application):
        a_app.screen.fill(Assets.GREEN)
    def m_ExitAction(a_app: Application):
        a_app.running = False

    app.uiManager.clear_and_reset()
    panel = UIPanel(Rect((0, 0), Constants.SCREEN_SIZE), manager=app.uiManager)
    panel.border_colour = Assets.BLACK
    panel.background_colour = Assets.LIGHT_GRAY
    UILabel(Rect(60, 20, Constants.SCREEN_WIDTH - 124, 32), "GUI Example", app.uiManager, panel)
    UIButton(Rect(60, 72, Constants.SCREEN_WIDTH - 124, 32), "Do Something", app.uiManager, panel, "Does something when you click it.", command=lambda: m_DoSomethingAction(app))
    UIButton(Rect(60, 124, Constants.SCREEN_WIDTH - 124, 32), "Exit", app.uiManager, panel, "Exits, duh.", command=lambda: m_ExitAction(app))


def main():
    pygame.init()
    app: Application = initApplication()

    RecreateUI(app)

    while app.running:
        app.StepDeltaTime()

        #region Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app.running = False

            app.uiManager.process_events(event)

        while app.deltaAccumulator >= Constants.DELTA_TIME:
            mods: int = pygame.key.get_mods()
            keys: ScancodeWrapper = pygame.key.get_pressed()
            mouse: tuple[bool, bool, bool] = pygame.mouse.get_pressed()
            app.deltaAccumulator -= Constants.DELTA_TIME
        #endregion

        #region Updates
        # Game update code goes here.

        app.uiManager.update(app.deltaTime)
        #endregion

        #region Rendering
        app.screen.fill(Assets.WHITE)

        # Your rendering code before the UI rendering (You can have multiple UIManagers)


        app.uiManager.draw_ui(app.screen)
        #endregion

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()