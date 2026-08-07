# ƒ installer for Windows — 14 style modes for Claude Code
# Usage:  irm https://marcyy.me/ƒ/install.ps1 | iex
# Status: untested — feedback welcome.
$ErrorActionPreference = "Stop"

$BaseUrl = if ($env:SKILLS_BASE_URL) { $env:SKILLS_BASE_URL } else { "https://marcyy.me/ƒ" }
$Claude  = if ($env:CLAUDE_HOME) { $env:CLAUDE_HOME } else { Join-Path $HOME ".claude" }
$Tmp     = Join-Path $env:TEMP ("fmodes-" + [guid]::NewGuid().ToString("N"))

$Skills = @(
  "godmode", "artifacts", "eli5", "ghost", "brief", "nocode", "silent", "ooda", "step",
  "devil", "roast", "matrix", "why", "steal"
)

Write-Host ""
Write-Host "  f — 14 style modes for Claude Code"
Write-Host "  9 persistent modes + 5 one-shot analyses. One SKILL.md each, zero dependencies."
Write-Host ""

New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
Invoke-WebRequest "$BaseUrl/skills.zip" -OutFile (Join-Path $Tmp "skills.zip")
Expand-Archive (Join-Path $Tmp "skills.zip") -DestinationPath $Tmp
$Src = Join-Path $Tmp "skills-dist"
if (-not (Test-Path (Join-Path $Src "skills\godmode\SKILL.md"))) { throw "bundle looks broken" }

$SkillsDir = Join-Path $Claude "skills"
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null
$BackedUp = @()
foreach ($sk in $Skills) {
  $dst = Join-Path $SkillsDir $sk
  if (Test-Path $dst) {
    Remove-Item "$dst.bak" -Recurse -Force -ErrorAction SilentlyContinue
    Move-Item $dst "$dst.bak"
    $BackedUp += $sk
  }
  Copy-Item (Join-Path $Src "skills\$sk") $dst -Recurse
}
Copy-Item (Join-Path $Src "README-SKILLS.md") $SkillsDir -Force
Remove-Item $Tmp -Recurse -Force
if ($BackedUp.Count -gt 0) { Write-Host "  existing skills backed up to <name>.bak: $($BackedUp -join ' ')" }

Write-Host ""
Write-Host "OK - f installed: 14 modes."
Write-Host ""
Write-Host "   persistent - /godmode  /artifacts  /eli5   /ghost  /brief"
Write-Host "                /nocode   /silent     /ooda   /step"
Write-Host "   one-shot   - /devil    /roast      /matrix /why    /steal"
Write-Host ""
Write-Host "   /xxx          turn the mode on for the rest of the session"
Write-Host "   /xxx [thing]  apply it once, without entering the mode"
Write-Host ""
Write-Host "   Reference: $SkillsDir\README-SKILLS.md"
