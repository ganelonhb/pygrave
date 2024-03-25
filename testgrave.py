from sys import exit

from grave.Game import SceneDictVideogame


def main() -> None:
    game = SceneDictVideogame(1920, 1080, scene_dir_list=["test_scene"])
    exit(game.run())

if __name__ == "__main__":
    main()
