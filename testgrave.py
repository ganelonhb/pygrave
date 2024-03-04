from grave import tag
from grave import game_object
from grave import videogame
from grave import grave_tester

from grave.signal import Signal

def main() -> None:
    print(tag.TagTester())
    print(game_object.GameObjectTester())
    print(grave_tester.GraveTesterTester())

if __name__ == "__main__":
    main()
