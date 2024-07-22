#pragma once
#include<vector>

class Game
{
private:
	bool isRunning;
public:
	Game();
	~Game();
	void Init();
	void Update();
	void Render();
	void Destroy();
	bool IsRunning() { return isRunning; };
};