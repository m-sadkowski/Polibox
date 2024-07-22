#include"Game.h"

Game::Game() {}

Game::~Game() {}

void Game::Init()
{
	isRunning = true;
}

void Game::Update()
{
}

void Game::Render()
{
}

void Game::Destroy()
{
	isRunning = false;
}
