[CmdletBinding()]
param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]] $DeployArguments
)

$ErrorActionPreference = 'Stop'
$packageDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$envPath = Join-Path $packageDirectory '.env.local'

if (-not (Test-Path -LiteralPath $envPath -PathType Leaf)) {
  throw '.env.local is missing'
}

$tokenLine = [System.IO.File]::ReadAllLines($envPath) |
  Where-Object { $_ -match '^DENO_DEPLOY_TOKEN=' } |
  Select-Object -First 1

if (-not $tokenLine) {
  throw 'DENO_DEPLOY_TOKEN is missing from .env.local'
}

$token = $tokenLine.Substring('DENO_DEPLOY_TOKEN='.Length).Trim()
if ($token -notmatch '^[A-Za-z0-9_-]{40}$') {
  throw 'DENO_DEPLOY_TOKEN has an invalid format'
}

$denoCommand = Get-Command 'deno.exe' -ErrorAction SilentlyContinue
if (-not $denoCommand) {
  throw 'deno.exe is not available on PATH'
}

$hadPreviousToken = Test-Path Env:DENO_DEPLOY_TOKEN
$previousToken = $env:DENO_DEPLOY_TOKEN
$exitCode = 1

try {
  $env:DENO_DEPLOY_TOKEN = $token
  & $denoCommand.Source deploy @DeployArguments
  $exitCode = $LASTEXITCODE
} finally {
  $token = $null
  if ($hadPreviousToken) {
    $env:DENO_DEPLOY_TOKEN = $previousToken
  } else {
    Remove-Item Env:DENO_DEPLOY_TOKEN -ErrorAction SilentlyContinue
  }
  $previousToken = $null
}

exit $exitCode
