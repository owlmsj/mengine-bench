#include "TargetGame.h"
#include "TargetScore.h"
#include "Camera/CameraComponent.h"
#include "Components/InputComponent.h"
#include "Components/PointLightComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/PointLight.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/PlayerStart.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Materials/MaterialInterface.h"
#include "UObject/ConstructorHelpers.h"

AMovingTarget::AMovingTarget()
{
    PrimaryActorTick.bCanEverTick = true;
    TargetMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("TargetMesh"));
    RootComponent = TargetMesh;
    static ConstructorHelpers::FObjectFinder<UStaticMesh> Sphere(TEXT("/Engine/BasicShapes/Sphere.Sphere"));
    if (Sphere.Succeeded()) TargetMesh->SetStaticMesh(Sphere.Object);
    static ConstructorHelpers::FObjectFinder<UMaterialInterface> RedMaterial(TEXT("/Game/M_Target.M_Target"));
    if (RedMaterial.Succeeded()) TargetMesh->SetMaterial(0, RedMaterial.Object);
    TargetMesh->SetWorldScale3D(FVector(1.3));
    TargetMesh->SetCollisionEnabled(ECollisionEnabled::QueryOnly);
    TargetMesh->SetCollisionResponseToAllChannels(ECR_Ignore);
    TargetMesh->SetCollisionResponseToChannel(ECC_Visibility, ECR_Block);
}

void AMovingTarget::Relocate()
{
    SetActorLocation(FVector(1200.0, FMath::FRandRange(-420.0f, 420.0f), FMath::FRandRange(150.0f, 450.0f)));
    DirectionTimer = 0.0f;
}

void AMovingTarget::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    DirectionTimer -= DeltaSeconds;
    if (DirectionTimer <= 0.0f)
    {
        FVector Direction(0.0, FMath::FRandRange(-1.0f, 1.0f), FMath::FRandRange(-0.6f, 0.6f));
        Velocity = Direction.GetSafeNormal(UE_SMALL_NUMBER, FVector::RightVector) * 350.0;
        DirectionTimer = FMath::FRandRange(0.8f, 1.7f);
    }
    FVector Location = GetActorLocation() + Velocity * DeltaSeconds;
    if (Location.Y < -500.0 || Location.Y > 500.0) Velocity.Y *= -1.0;
    if (Location.Z < 120.0 || Location.Z > 500.0) Velocity.Z *= -1.0;
    Location.Y = FMath::Clamp(Location.Y, -500.0, 500.0);
    Location.Z = FMath::Clamp(Location.Z, 120.0, 500.0);
    SetActorLocation(Location);
}

ATargetPawn::ATargetPawn()
{
    PrimaryActorTick.bCanEverTick = true;
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("PawnRoot"));
    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("AimCamera"));
    Camera->SetupAttachment(RootComponent);
    Camera->SetRelativeLocation(FVector(0.0, 0.0, 220.0));
    Camera->bUsePawnControlRotation = true;
    AutoPossessPlayer = EAutoReceiveInput::Player0;
}

void ATargetPawn::BeginPlay()
{
    Super::BeginPlay();
    if (APlayerController* Player = Cast<APlayerController>(GetController()))
    {
        Player->bShowMouseCursor = false;
        Player->SetInputMode(FInputModeGameOnly());
    }
}

void ATargetPawn::SetupPlayerInputComponent(UInputComponent* Input)
{
    Super::SetupPlayerInputComponent(Input);
    Input->BindAxis(TEXT("Turn"), this, &ATargetPawn::Turn);
    Input->BindAxis(TEXT("LookUp"), this, &ATargetPawn::LookUp);
    Input->BindAction(TEXT("Shoot"), IE_Pressed, this, &ATargetPawn::Shoot);
    Input->BindAction(TEXT("Quit"), IE_Pressed, this, &ATargetPawn::QuitGame);
    Input->BindAction(TEXT("Start"), IE_Pressed, this, &ATargetPawn::StartGame);
}

void ATargetPawn::Turn(float Value) { AddControllerYawInput(Value); }
void ATargetPawn::LookUp(float Value) { AddControllerPitchInput(Value); }

void ATargetPawn::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    if (Phase == ETargetPhase::Finished)
    {
        ReplayDelay = FMath::Max(0.0f, ReplayDelay - DeltaSeconds);
        return;
    }
    if (Phase != ETargetPhase::Playing) return;
    SecondsLeft = FMath::Max(0.0f, SecondsLeft - DeltaSeconds);
    if (SecondsLeft <= 0.0f)
    {
        Phase = ETargetPhase::Finished;
        ReplayDelay = 1.0f;
    }
}

void ATargetPawn::StartGame()
{
    if (Phase == ETargetPhase::Playing) return;
    Score = 0;
    SecondsLeft = 15.0f;
    ReplayDelay = 0.0f;
    Phase = ETargetPhase::Playing;
}

void ATargetPawn::Shoot()
{
    if (Phase == ETargetPhase::Finished && ReplayDelay > 0.0f) return;
    if (Phase != ETargetPhase::Playing)
    {
        StartGame();
        return;
    }
    FHitResult Hit;
    const FVector Start = Camera->GetComponentLocation();
    const FVector End = Start + Camera->GetForwardVector() * 10000.0;
    FCollisionQueryParams Query(SCENE_QUERY_STAT(TargetShot), true, this);
    const bool DidHit = GetWorld()->LineTraceSingleByChannel(Hit, Start, End, ECC_Visibility, Query);
    AMovingTarget* Target = DidHit ? Cast<AMovingTarget>(Hit.GetActor()) : nullptr;
    Score = ScoreAfterShot(Score, Target != nullptr);
    if (Target) Target->Relocate();
}

void ATargetPawn::QuitGame()
{
    UKismetSystemLibrary::QuitGame(this, Cast<APlayerController>(GetController()), EQuitPreference::Quit, false);
}

void ATargetHUD::DrawHUD()
{
    Super::DrawHUD();
    if (!Canvas || !GEngine) return;
    const ATargetPawn* Pawn = GetOwningPlayerController() ? Cast<ATargetPawn>(GetOwningPlayerController()->GetPawn()) : nullptr;
    if (!Pawn) return;
    const float X = Canvas->ClipX * 0.5f;
    const float Y = Canvas->ClipY * 0.5f;
    const FString ScoreLabel = FString::Printf(TEXT("PONTOS: %d"), Pawn->GetScore());
    const FString TimeLabel = FString::Printf(TEXT("TEMPO: %d"), FMath::CeilToInt(Pawn->GetSecondsLeft()));
    DrawText(ScoreLabel, FLinearColor::White, 24.0f, 20.0f, GEngine->GetLargeFont());
    DrawText(TimeLabel, FLinearColor::White, Canvas->ClipX - 180.0f, 20.0f, GEngine->GetLargeFont());
    if (Pawn->GetPhase() == ETargetPhase::Playing)
    {
        DrawLine(X - 10.0f, Y, X + 10.0f, Y, FLinearColor::Black, 4.0f);
        DrawLine(X, Y - 10.0f, X, Y + 10.0f, FLinearColor::Black, 4.0f);
        DrawLine(X - 10.0f, Y, X + 10.0f, Y, FLinearColor::White, 2.0f);
        DrawLine(X, Y - 10.0f, X, Y + 10.0f, FLinearColor::White, 2.0f);
        return;
    }
    DrawRect(FLinearColor(0.0f, 0.0f, 0.0f, 0.75f), X - 250.0f, Y - 100.0f, 500.0f, 200.0f);
    const auto CenterText = [this, X](const FString& Text, float Top, UFont* Font)
    {
        float Width = 0.0f, Height = 0.0f;
        GetTextSize(Text, Width, Height, Font);
        DrawText(Text, FLinearColor::White, X - Width * 0.5f, Top, Font);
    };
    if (Pawn->GetPhase() == ETargetPhase::Ready)
    {
        CenterText(TEXT("ALVO MOVEL"), Y - 70.0f, GEngine->GetLargeFont());
        CenterText(TEXT("15 SEGUNDOS PARA ACERTAR O ALVO"), Y - 25.0f, GEngine->GetSmallFont());
        CenterText(TEXT("CLIQUE OU ENTER PARA INICIAR"), Y + 15.0f, GEngine->GetSmallFont());
    }
    else
    {
        CenterText(TEXT("FIM DE JOGO"), Y - 70.0f, GEngine->GetLargeFont());
        CenterText(ScoreLabel, Y - 25.0f, GEngine->GetLargeFont());
        CenterText(TEXT("CLIQUE OU R PARA JOGAR NOVAMENTE"), Y + 15.0f, GEngine->GetSmallFont());
    }
    CenterText(TEXT("ESC PARA SAIR"), Y + 55.0f, GEngine->GetSmallFont());
}

ATargetGameMode::ATargetGameMode()
{
    DefaultPawnClass = ATargetPawn::StaticClass();
    HUDClass = ATargetHUD::StaticClass();
    static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));
    ArenaMesh = Cube.Object;
}

AActor* ATargetGameMode::ChoosePlayerStart_Implementation(AController* Player)
{
    if (AActor* Start = Super::ChoosePlayerStart_Implementation(Player)) return Start;
    return GetWorld()->SpawnActor<APlayerStart>(FVector::ZeroVector, FRotator::ZeroRotator);
}

void ATargetGameMode::BeginPlay()
{
    Super::BeginPlay();
    const FTransform ArenaParts[] = {
        FTransform(FRotator::ZeroRotator, FVector(850.0, 0.0, -25.0), FVector(28.0, 22.0, 0.5)),
        FTransform(FRotator::ZeroRotator, FVector(1800.0, 0.0, 500.0), FVector(0.4, 22.0, 10.0)),
        FTransform(FRotator::ZeroRotator, FVector(1550.0, -800.0, 175.0), FVector(1.5, 1.5, 3.5)),
        FTransform(FRotator::ZeroRotator, FVector(1550.0, 800.0, 175.0), FVector(1.5, 1.5, 3.5))
    };
    for (const FTransform& Placement : ArenaParts)
    {
        AStaticMeshActor* Shape = GetWorld()->SpawnActor<AStaticMeshActor>(Placement.GetLocation(), Placement.Rotator());
        if (!Shape) continue;
        UStaticMeshComponent* Mesh = Shape->GetStaticMeshComponent();
        Mesh->SetMobility(EComponentMobility::Movable);
        Mesh->SetStaticMesh(ArenaMesh);
        Mesh->SetCollisionEnabled(ECollisionEnabled::NoCollision);
        Mesh->SetCastShadow(false);
        Shape->SetActorScale3D(Placement.GetScale3D());
    }
    GetWorld()->SpawnActor<AMovingTarget>(FVector(1200.0, 0.0, 220.0), FRotator::ZeroRotator);
    APointLight* Light = GetWorld()->SpawnActor<APointLight>(FVector(750.0, 0.0, 550.0), FRotator::ZeroRotator);
    if (Light)
    {
        Light->GetLightComponent()->SetMobility(EComponentMobility::Movable);
        Light->GetLightComponent()->SetCastShadows(false);
        Light->GetLightComponent()->SetIntensity(200000.0f);
        CastChecked<UPointLightComponent>(Light->GetLightComponent())->SetAttenuationRadius(3000.0f);
    }
}
