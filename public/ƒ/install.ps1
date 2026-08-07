# f installer for Windows - 14 style modes for Claude Code
# Usage:  irm https://marcyy.me/f/install.ps1 | iex
#
# This file is deliberately pure ASCII. Windows PowerShell 5.1 decodes a
# response with no charset as latin-1, which corrupts any non-ASCII byte in the
# script - including the glyph in a base URL. Keep it that way: /f is the ASCII
# mirror of /<f-with-hook>, and the two serve identical bytes.
$ErrorActionPreference = "Stop"

$BaseUrl = if ($env:SKILLS_BASE_URL) { $env:SKILLS_BASE_URL } else { "https://marcyy.me/f" }
$Claude  = if ($env:CLAUDE_HOME) { $env:CLAUDE_HOME } else { Join-Path $HOME ".claude" }
$Tmp     = Join-Path $env:TEMP ("fmodes-" + [guid]::NewGuid().ToString("N"))

$Skills = @(
  "godmode", "artifacts", "eli5", "ghost", "brief", "nocode", "silent", "ooda", "step",
  "devil", "roast", "matrix", "why", "steal"
)

Write-Host ""
Write-Host "  f - 14 style modes for Claude Code"
Write-Host "  9 persistent modes + 5 one-shot analyses. One SKILL.md each, zero dependencies."
Write-Host ""

$Version = try { (Invoke-WebRequest "$BaseUrl/VERSION" -UseBasicParsing).Content.Trim() } catch { "unknown" }
Write-Host "-- 1/2  Downloading bundle ($Version)"

New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
$Zip = Join-Path $Tmp "skills.zip"
Invoke-WebRequest "$BaseUrl/skills.zip" -OutFile $Zip -UseBasicParsing
Expand-Archive $Zip -DestinationPath $Tmp
$Src = Join-Path $Tmp "skills-dist"
if (-not (Test-Path (Join-Path $Src "skills\godmode\SKILL.md"))) { throw "bundle looks broken" }

$SkillsDir = Join-Path $Claude "skills"
Write-Host "-- 2/2  Installing into $SkillsDir"
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

$BackedUp = @()
foreach ($sk in $Skills) {
  $src = Join-Path $Src "skills\$sk"
  if (-not (Test-Path (Join-Path $src "SKILL.md"))) { throw "missing '$sk' in bundle" }
  $dst = Join-Path $SkillsDir $sk
  if (Test-Path $dst) {
    Remove-Item "$dst.bak" -Recurse -Force -ErrorAction SilentlyContinue
    Move-Item $dst "$dst.bak"
    $BackedUp += $sk
  }
  Copy-Item $src $dst -Recurse
}
Copy-Item (Join-Path $Src "README-SKILLS.md") $SkillsDir -Force
Remove-Item $Tmp -Recurse -Force
if ($BackedUp.Count -gt 0) { Write-Host "   existing skills backed up to <name>.bak: $($BackedUp -join ' ')" }

Write-Host ""
Write-Host "OK - f installed: 14 modes."
Write-Host ""
Write-Host "   persistent  /godmode  /artifacts  /eli5    /ghost  /brief"
Write-Host "               /nocode   /silent     /ooda    /step"
Write-Host "   one-shot    /devil    /roast      /matrix  /why    /steal"
Write-Host ""
Write-Host "   /xxx          turn the mode on for the rest of the session"
Write-Host "   /xxx [thing]  apply it once, without entering the mode"
Write-Host "   modes stack - say 'turn off ghost' to drop one"
Write-Host ""
Write-Host "   Reference: $SkillsDir\README-SKILLS.md"
Write-Host "   Undo:"
Write-Host "     @('$($Skills -join "','")') | % { Remove-Item -Recurse -Force `"$SkillsDir\`$_`" }"
