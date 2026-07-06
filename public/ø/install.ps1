# ø / Omega installer for Windows — core only (skills + agents; no weekly automation)
# Usage:  irm https://marcyy.me/omega/install.ps1 | iex
# Status: untested — feedback welcome. Automation (Friday scan/notifications) is macOS/Linux only; see README-OMEGA.md.
$ErrorActionPreference = "Stop"

$BaseUrl  = if ($env:OMEGA_BASE_URL) { $env:OMEGA_BASE_URL } else { "https://marcyy.me/ø" }
$Tmp      = Join-Path $env:TEMP ("omega-" + [guid]::NewGuid().ToString("N"))
$Claude   = Join-Path $HOME ".claude"
$OmegaDir = if ($env:OMEGA_DIR) { $env:OMEGA_DIR } else { Join-Path $HOME "omega" }

Write-Host ""
Write-Host "  ø / Omega — symbiotic meta-cognition layer for Claude Code (Windows: core install)"
Write-Host ""

New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
Invoke-WebRequest "$BaseUrl/omega.zip" -OutFile (Join-Path $Tmp "omega.zip")
Expand-Archive (Join-Path $Tmp "omega.zip") -DestinationPath $Tmp
$Src = Join-Path $Tmp "omega-dist"

New-Item -ItemType Directory -Force -Path (Join-Path $Claude "skills"), (Join-Path $Claude "agents"), $OmegaDir | Out-Null
foreach ($sk in "omega", "omega-update") {
  $dst = Join-Path $Claude "skills\$sk"
  if (Test-Path $dst) { Remove-Item "$dst.bak" -Recurse -Force -ErrorAction SilentlyContinue; Move-Item $dst "$dst.bak" }
  Copy-Item (Join-Path $Src "skills\$sk") $dst -Recurse
}
Copy-Item (Join-Path $Src "agents\omega-*.md") (Join-Path $Claude "agents") -Force
Copy-Item (Join-Path $Src "README-OMEGA.md"), (Join-Path $Src "example-settings.json"), (Join-Path $Src "VERSION") $OmegaDir -Force
Remove-Item $Tmp -Recurse -Force

Write-Host "✅ ø core installed: /omega + /omega-update skills, 7 omega-* council agents."
Write-Host "   Weekly automation & notifications are macOS/Linux only — see $OmegaDir\README-OMEGA.md"
Write-Host "   NOTE: Marc's personal system shared as-is; adapt paths to your own knowledge base."
