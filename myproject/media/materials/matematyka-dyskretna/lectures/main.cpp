#include<iostream>
#include"Engine/Game.h"

int main()
{
	Game game;
	game.Init();
	while (game.IsRunning())
	{
		game.Update();
		game.Render();
	}
	game.Destroy();
	return 0;
}