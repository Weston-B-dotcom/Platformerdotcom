import os, json, random, pygame, pygame_gui, DataValues.Constants as Constants, shutil
from typing import Any

VOWELS = ["a", "e", "i", "o", "u"]
VOWEL_PAIRS = ['ai', 'au', 'aw', 'ay', 'ea', 'ee', 'ei', 'eigh', 'ew', 'ey', 'ie', 'igh', 'oa', 'oe', 'oi', 'oo', 'ou', 'ow', 'oy', 'ue', 'ui', 'uy']
CONSONANTS = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
CONSONANT_PAIRS = ["bl", "br", "ch", "ck", "cl", "cr", "ct", "cth", "dr", "dw", "fl", "fr", "ft", "gh", "gl", "gn", "gr", "kh", "kn", "kth", "lk", "lp", "lt", "mb", "mp", "nc", "nd", "ng", "nk", "nt", "ph", "pl", "pr", "pt", "qu", "sc", "scr", "sh", "shr", "sk", "sl", "sm", "sn", "sp", "spl", "spr", "squ", "ss", "st", "str", "sw", "th", "thr", "tr", "tw", "wh", "wr","ght"]

V_USE = VOWELS + VOWEL_PAIRS
C_USE = CONSONANTS + CONSONANT_PAIRS

FILEPATH: str = "something"
MAX_DEPTH: int = 4
MIN_FILES: int = 3
MAX_FILES: int = 15
MIN_DIRECTORY: int = 0
MAX_DIRECTORY: int = 4



def random_string(a_min_length: int, a_max_length: int) -> str:
    length: int = random.randint(a_min_length, a_max_length)
    on_vowel: bool = random.randint(0, 1) == 0
    to_return: str = ""
    for i in range(length):
        to_return += random.choice(V_USE) if on_vowel else random.choice(C_USE)
        on_vowel = not on_vowel
    return to_return

class ExampleData:
    def __init__(self, name: str, number: int):
        self.name = name
        self.number = number

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "number": self.number
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExampleData":
        return cls(data["name"], data["number"])

    @classmethod
    def random(cls):
        return cls(random_string(5, 15), random.randint(0, 0b11111111111111111111111111111111))

def renuke_directory(filepath: str):
    shutil.rmtree(filepath)
    os.mkdir(filepath)

def generate_directory(filepath: str, depth: int = 0):
    for i in range(random.randint(MIN_FILES, MAX_FILES)):
        b = ExampleData.random().to_dict()
        with open(f"{filepath}/{b["name"]}.json", "w") as file:
            json.dump(b, file)
    if depth > MAX_DEPTH:
        return
    for j in range(random.randint(MIN_DIRECTORY, MAX_DIRECTORY)):
        name = f"{filepath}/{random_string(3, 7)}"
        os.mkdir(name)
        generate_directory(name, depth + 1)

def scan(filepath: str) -> list[ExampleData|list]:
    a = []
    for path in os.scandir(filepath):
        if path.is_dir():
            a = a + scan(path.path)
        elif path.is_file() and path.name[-5::] == ".json":
            with open(path.path, "r") as file:
                try:
                    a.append(ExampleData.from_dict(json.load(file)))
                except BaseException as _:
                    print(f"{path.name[:-5]} didn't have valid data. Idiot.")
    return a

if True:
    renuke_directory(FILEPATH)

if True:
    generate_directory(FILEPATH)

noodless: list[ExampleData|list] = scan(FILEPATH)

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
manager: pygame_gui.UIManager = pygame_gui.UIManager((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))

a = pygame_gui.elements.UIScrollingContainer(pygame.Rect(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), manager, should_grow_automatically=True)

i: int = 0

def bob(noodles):
    global i, manager, a
    for entry in noodles:
        if isinstance(entry, ExampleData):
            pygame_gui.elements.UILabel(pygame.Rect(0, i * 32, Constants.SCREEN_WIDTH, 32), f"{entry.name} - {entry.number}", manager, a)
            i += 1
        elif isinstance(entry, list):
            bob(entry)

bob(noodless)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.process_events(event)

    manager.update(0.1)

    screen.fill(Constants.WHITE)  # Fill background

    manager.draw_ui(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()

