#if WITH_DEV_AUTOMATION_TESTS
#include "TargetGame.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Engine/StaticMeshActor.h"
#include "Components/StaticMeshComponent.h"
#include "EngineUtils.h"
#include "Misc/AutomationTest.h"
#include "Materials/MaterialInterface.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FTargetGameShotTest, "AlvoMovel.Gameplay.HitMissAndMovement", EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FTargetGameShotTest::RunTest(const FString& Parameters)
{
    FWorldContext& Context = GEngine->CreateNewWorldContext(EWorldType::Game);
    UWorld* World = UWorld::CreateWorld(EWorldType::Game, false, NAME_None, GetTransientPackage());
    if (!TestNotNull(TEXT("test world"), World)) return false;
    Context.SetCurrentWorld(World);
    World->InitializeActorsForPlay(FURL());
    ATargetGameMode* Mode = World->SpawnActor<ATargetGameMode>();
    if (TestNotNull(TEXT("game mode"), Mode))
    {
        TestNotNull(TEXT("empty map provides a player start"), Mode->ChoosePlayerStart_Implementation(nullptr));
        Mode->DispatchBeginPlay();
        int32 ArenaParts = 0;
        for (TActorIterator<AStaticMeshActor> It(World); It; ++It) if (It->GetStaticMeshComponent()->GetStaticMesh()) ++ArenaParts;
        TestTrue(TEXT("arena has at least floor and backdrop"), ArenaParts >= 2);
        for (TActorIterator<AMovingTarget> It(World); It; ++It) It->Destroy();
    }
    ATargetPawn* Pawn = World->SpawnActor<ATargetPawn>(FVector::ZeroVector, FRotator::ZeroRotator);
    AMovingTarget* Target = World->SpawnActor<AMovingTarget>(FVector(1200, 0, 220), FRotator::ZeroRotator);
    if (TestNotNull(TEXT("pawn"), Pawn) && TestNotNull(TEXT("target"), Target))
    {
        UStaticMeshComponent* TargetVisual = Target->FindComponentByClass<UStaticMeshComponent>();
        if (TestNotNull(TEXT("target has a mesh"), TargetVisual))
        {
            UMaterialInterface* Material = TargetVisual->GetMaterial(0);
            if (TestNotNull(TEXT("target has a material"), Material))
                TestEqual(TEXT("target uses its red material"), Material->GetPathName(), FString(TEXT("/Game/M_Target.M_Target")));
        }
        Target->SetActorTickEnabled(false);
        Pawn->Tick(3.0f);
        TestEqual(TEXT("timer waits for start"), Pawn->GetSecondsLeft(), 15.0f);
        Pawn->Shoot();
        TestEqual(TEXT("shot before start does not score"), Pawn->GetScore(), 0);
        TestTrue(TEXT("first click starts the round"), Pawn->GetPhase() == ETargetPhase::Playing);
        Pawn->Tick(1.25f);
        TestEqual(TEXT("timer advances while playing"), Pawn->GetSecondsLeft(), 13.75f);
        Pawn->Score = 0;
        Target->SetActorLocation(FVector(1200, 0, 220));
        Pawn->Shoot();
        TestEqual(TEXT("one hit adds one point"), Pawn->GetScore(), 1);
        Pawn->StartGame();
        TestEqual(TEXT("start key does not reset active round"), Pawn->GetScore(), 1);
        Target->SetActorLocation(FVector(1200, 700, 220));
        Pawn->Shoot();
        TestEqual(TEXT("a miss does not add a point"), Pawn->GetScore(), 1);
        Target->SetActorLocation(FVector(1200, 0, 220));
        Pawn->Shoot();
        TestEqual(TEXT("a second hit adds one point"), Pawn->GetScore(), 2);
        Pawn->Tick(20.0f);
        TestTrue(TEXT("round ends at zero"), Pawn->GetPhase() == ETargetPhase::Finished);
        TestEqual(TEXT("timer stops at zero"), Pawn->GetSecondsLeft(), 0.0f);
        TestEqual(TEXT("final score is retained"), Pawn->GetScore(), 2);
        Pawn->Shoot();
        TestTrue(TEXT("immediate click cannot skip result"), Pawn->GetPhase() == ETargetPhase::Finished);
        TestEqual(TEXT("immediate click preserves final score"), Pawn->GetScore(), 2);
        Pawn->Tick(1.0f);
        Pawn->Shoot();
        TestTrue(TEXT("click replays after finish"), Pawn->GetPhase() == ETargetPhase::Playing);
        TestEqual(TEXT("replay clears score"), Pawn->GetScore(), 0);
        TestEqual(TEXT("replay resets timer"), Pawn->GetSecondsLeft(), 15.0f);
        Target->SetActorLocation(FVector(1200, 0, 220));
        const FVector Before = Target->GetActorLocation();
        Target->Tick(0.1f);
        TestTrue(TEXT("target moves over time"), !Target->GetActorLocation().Equals(Before, 0.01));
    }
    World->DestroyWorld(false);
    GEngine->DestroyWorldContext(World);
    return true;
}
#endif
