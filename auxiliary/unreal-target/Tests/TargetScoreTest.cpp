#include "../Source/AlvoMovel/TargetScore.h"
#include <cstdio>
int main()
{
    if (ScoreAfterShot(0, true) != 1) { std::puts("FAIL hit must add one point"); return 1; }
    if (ScoreAfterShot(7, false) != 7) { std::puts("FAIL miss must preserve score"); return 1; }
    if (ScoreAfterShot(7, true) != 8) { std::puts("FAIL subsequent hit must add one point"); return 1; }
    std::puts("PASS hit and miss scoring");
    return 0;
}
