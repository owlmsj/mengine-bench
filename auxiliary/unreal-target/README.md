# Alvo Móvel: jogo Unreal auxiliar

Protótipo 3D para experimentos locais, fora do catálogo e da pontuação do benchmark.
Uma rodada dura 15 segundos. Mire com o mouse, clique para atirar e some um ponto
por acerto. Clique ou Enter inicia; ao final, R reinicia imediatamente ou um clique reinicia após um segundo. Esc fecha.
A ferramenta opcional `AlvoMovelPlaytest.exe` usa os pixels da janela e envia
entradas de mouse e teclado. Ela consome CPU: para medir só o jogo, rode-o sozinho.

O projeto usa Unreal Engine 5.8, DirectX 11, janela de 960 x 540, VSync desligado,
FPS sem limite, sem sombras ou pós-processamento. O cenário usa cubos básicos e o
alvo usa uma esfera com um material vermelho. O pacote Windows inclui bibliotecas
locais de execução e dispensa instalador. Requer Windows 64 bits e GPU com DirectX 11.

## Como criar o jogo

- `Source/AlvoMovel/TargetGame.cpp` cria a arena, a iluminação e o alvo usando
  primitivas da engine; movimenta o alvo e faz o teste de colisão do tiro.
- `TargetGame.h` e `TargetGame.cpp` implementam estados de início, rodada e fim,
  temporizador, pontuação e HUD. `TargetGameTests.cpp` exercita esses comportamentos.
- `Content/M_Target.uasset` é um material simples criado no editor. Para recriá-lo,
  crie `M_Target` em `/Game`, adicione um `Constant3Vector` com valores lineares
  R=0,8, G=0,025, B=0,015, conecte-o a `Base Color`, compile e salve. Mantenha
  o material `Default Lit`. O C++ referencia `/Game/M_Target.M_Target`.
- `Config` define mapa vazio, modo de jogo, controles e opções gráficas. O plugin
  AndroidFileServer está desativado. O editor expõe o MCP nativo em `127.0.0.1:8000`;
  use apenas um editor por vez nessa porta.

## Compilar, testar e empacotar no Windows

Instale Unreal Engine 5.8, PowerShell 7, o Windows SDK e as ferramentas C++ do Visual Studio.
Abra o **Developer PowerShell** do Visual Studio na pasta deste projeto. As etapas
abaixo esperam a raiz da instalação da engine na variável `$ueRoot`:

```powershell
$ueRoot = Read-Host 'Pasta de instalação do Unreal Engine 5.8'
$projectFile = (Resolve-Path .\AlvoMovel.uproject).Path
$build = Join-Path $ueRoot 'Engine\Build\BatchFiles\Build.bat'
& $build AlvoMovelEditor Win64 Development "-Project=$projectFile" -WaitMutex -NoHotReloadFromIDE -MaxParallelActions=4
if ($LASTEXITCODE -ne 0) { throw 'A compilação do editor falhou' }

cl.exe /nologo /std:c++17 /EHsc /O2 /MT /utf-8 /Fo:Tools\AlvoMovelPlaytest.obj /Fe:Tools\AlvoMovelPlaytest.exe Tools\AlvoMovelPlaytest.cpp user32.lib gdi32.lib
if ($LASTEXITCODE -ne 0) { throw 'A compilação do playtest falhou' }

pwsh -NoProfile -File .\Tools\Test-Gameplay.ps1 -EngineRoot $ueRoot
if ($LASTEXITCODE -ne 0) { throw 'O teste do jogo falhou' }
pwsh -NoProfile -File .\Tools\Package-Windows.ps1 -EngineRoot $ueRoot
if ($LASTEXITCODE -ne 0) { throw 'O empacotamento falhou' }
```

O teste lê o relatório do Unreal: o código de saída do editor sozinho não garante
que os testes passaram. O empacotamento cria uma pasta nova em `Packaged/` e um
`AlvoMovel.zip` sem símbolos de depuração; falha se o ZIP superar 300.000.000 bytes.
Extraia **todo** o ZIP e abra `AlvoMovel.exe`. Para testar automaticamente, execute
`AlvoMovelPlaytest.exe`; com `--keep-open`, o resultado fica aberto ao final.

Esta fixture não implementa resultado assinado, placar máximo ou anticheat e não
ativa as tarefas propostas na issue #157. O tamanho e o desempenho dependem da build
e da máquina; meça-os na cópia extraída antes de publicar resultados.
