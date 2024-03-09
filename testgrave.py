from sys import exit

from grave import tag
from grave import game_object
from grave import videogame
from grave import grave_tester

from grave.scene_dict_videogame import SceneDictVideogame
from grave.signal import Signal

from grave.implement import Implement, implements, __implements__


def main() -> None:
    #print(tag.TagTester())
    print(game_object.GameObjectTester())
    #print(grave_tester.GraveTesterTester())
    #print(videogame.VideoGameTester())

    game = SceneDictVideogame(1920, 1080, scene_dir_list=["test_scene"])
    exit(game.run())

if __name__ == "__main__":
    main()
