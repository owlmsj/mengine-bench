#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/HUD.h"
#include "GameFramework/Pawn.h"
#include "TargetGame.generated.h"

class UCameraComponent;
class UStaticMeshComponent;
class UStaticMesh;

enum class ETargetPhase : uint8 { Ready, Playing, Finished };

UCLASS()
class ALVOMOVEL_API AMovingTarget : public AActor
{
    GENERATED_BODY()
public:
    AMovingTarget();
    virtual void Tick(float DeltaSeconds) override;
    void Relocate();
private:
    UPROPERTY()
    TObjectPtr<UStaticMeshComponent> TargetMesh;
    FVector Velocity;
    float DirectionTimer = 0.0f;
};

UCLASS()
class ALVOMOVEL_API ATargetPawn : public APawn
{
    GENERATED_BODY()
public:
    ATargetPawn();
    virtual void BeginPlay() override;
    virtual void SetupPlayerInputComponent(UInputComponent* Input) override;
    virtual void Tick(float DeltaSeconds) override;
    int32 GetScore() const { return Score; }
    float GetSecondsLeft() const { return SecondsLeft; }
    ETargetPhase GetPhase() const { return Phase; }
private:
    void Turn(float Value);
    void LookUp(float Value);
    friend class FTargetGameShotTest;
    void Shoot();
    void StartGame();
    void QuitGame();
    UPROPERTY()
    TObjectPtr<UCameraComponent> Camera;
    int32 Score = 0;
    float SecondsLeft = 15.0f;
    float ReplayDelay = 0.0f;
    ETargetPhase Phase = ETargetPhase::Ready;
};

UCLASS()
class ALVOMOVEL_API ATargetHUD : public AHUD
{
    GENERATED_BODY()
public:
    virtual void DrawHUD() override;
};

UCLASS()
class ALVOMOVEL_API ATargetGameMode : public AGameModeBase
{
    GENERATED_BODY()
public:
    ATargetGameMode();
    virtual AActor* ChoosePlayerStart_Implementation(AController* Player) override;
    virtual void BeginPlay() override;
private:
    UPROPERTY()
    TObjectPtr<UStaticMesh> ArenaMesh;
};
