#pragma once
inline int ScoreAfterShot(int currentScore, bool targetHit)
{
    return currentScore + (targetHit ? 1 : 0);
}
