from grave import tag
from grave import game_object
from grave import videogame
from grave import grave_tester

from grave.scene_dict_videogame import SceneDictVideogame
from grave.signal import Signal

def main() -> None:
    print(tag.TagTester())
    print(game_object.GameObjectTester())
    print(grave_tester.GraveTesterTester())

    b = SceneDictVideogame(level_dir_list=["./test_scene"], game_module_override="test_scene")
    b.run()

if __name__ == "__main__":
    main()
