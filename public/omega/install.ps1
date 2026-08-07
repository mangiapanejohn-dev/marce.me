# Omega installer for Windows - core only (skills + agents; no weekly automation)
# Usage:  irm https://marcyy.me/omega/install.ps1 | iex
#
# This file is deliberately pure ASCII. Windows PowerShell 5.1 decodes a
# response with no charset as latin-1, which corrupts any non-ASCII byte in the
# script - including the glyph in a base URL. Keep it that way: /omega is the
# ASCII mirror of /<o-slash>, and the two serve identical bytes.
# Automation (Friday scan / notifications) is macOS/Linux only; see README-OMEGA.md.
$ErrorActionPreference = "Stop"

$BaseUrl  = if ($env:OMEGA_BASE_URL) { $env:OMEGA_BASE_URL } else { "https://marcyy.me/omega" }
$Claude   = if ($env:CLAUDE_HOME) { $env:CLAUDE_HOME } else { Join-Path $HOME ".claude" }
$OmegaDir = if ($env:OMEGA_DIR) { $env:OMEGA_DIR } else { Join-Path $HOME "omega" }
$Tmp      = Join-Path $env:TEMP ("omega-" + [guid]::NewGuid().ToString("N"))

Write-Host ""
Write-Host "  Omega - symbiotic meta-cognition layer for Claude Code (Windows: core install)"
Write-Host ""

$Version = try { (Invoke-WebRequest "$BaseUrl/VERSION" -UseBasicParsing).Content.Trim() } catch { "unknown" }
Write-Host "-- 1/2  Downloading bundle ($Version)"

New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
$Zip = Join-Path $Tmp "omega.zip"
Invoke-WebRequest "$BaseUrl/omega.zip" -OutFile $Zip -UseBasicParsing
Expand-Archive $Zip -DestinationPath $Tmp
$Src = Join-Path $Tmp "omega-dist"
if (-not (Test-Path (Join-Path $Src "skills\omega\SKILL.md"))) { throw "bundle looks broken" }

Write-Host "-- 2/2  Installing skills + agents into $Claude"
New-Item -ItemType Directory -Force -Path (Join-Path $Claude "skills"), (Join-Path $Claude "agents"), $OmegaDir | Out-Null
foreach ($sk in "omega", "omega-update") {
  $dst = Join-Path $Claude "skills\$sk"
  if (Test-Path $dst) {
    Remove-Item "$dst.bak" -Recurse -Force -ErrorAction SilentlyContinue
    Move-Item $dst "$dst.bak"
  }
  Copy-Item (Join-Path $Src "skills\$sk") $dst -Recurse
}
Copy-Item (Join-Path $Src "agents\omega-*.md") (Join-Path $Claude "agents") -Force
Copy-Item (Join-Path $Src "README-OMEGA.md"), (Join-Path $Src "example-settings.json"), (Join-Path $Src "VERSION") $OmegaDir -Force
Remove-Item $Tmp -Recurse -Force

Write-Host ""
Write-Host "OK - Omega core installed: /omega + /omega-update skills, 7 omega-* council agents."
Write-Host "   Weekly automation & notifications are macOS/Linux only - see $OmegaDir\README-OMEGA.md"
Write-Host "   NOTE: Marc's personal system shared as-is; adapt paths to your own knowledge base."
