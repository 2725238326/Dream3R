param(
    [ValidateSet("push", "pull", "verify", "test")]
    [string]$Mode = "verify",
    [string]$RemoteHost = "BUAA-Server",
    [string]$RemoteRoot = "/hdd3/kykt26/code/dream3r",
    [switch]$FullTests
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LocalRoot = Split-Path -Parent $ScriptDir
$RemotePackage = "$RemoteRoot/dream3r"

function Get-ProjectFiles {
    Get-ChildItem -Path $LocalRoot -Recurse -File -Include *.py,*.md |
        Where-Object {
            $_.FullName -notmatch "\\__pycache__\\" -and
            $_.FullName -notmatch "\\scripts\\"
        } |
        ForEach-Object {
            $_.FullName.Substring($LocalRoot.Length + 1).Replace("\", "/")
        } |
        Sort-Object
}

function Invoke-Remote($Command) {
    ssh $RemoteHost $Command
}

function Copy-ToServer {
    foreach ($rel in Get-ProjectFiles) {
        $local = Join-Path $LocalRoot ($rel -replace "/", "\")
        $remote = "$RemotePackage/$rel"
        $remoteDir = $remote.Substring(0, $remote.LastIndexOf("/"))
        Invoke-Remote "mkdir -p '$remoteDir'"
        scp $local "${RemoteHost}:$remote"
    }

    foreach ($doc in @("CYCLE_033_PLAN.md", "CYCLE_034_PLAN.md", "PLAN.md", "REVIEW_PROMPT.md")) {
        $local = Join-Path $LocalRoot $doc
        if (Test-Path $local) {
            scp $local "${RemoteHost}:$RemoteRoot/$doc"
        }
    }
}

function Copy-FromServer {
    foreach ($rel in Get-ProjectFiles) {
        $local = Join-Path $LocalRoot ($rel -replace "/", "\")
        New-Item -ItemType Directory -Force -Path (Split-Path $local) | Out-Null
        scp "${RemoteHost}:$RemotePackage/$rel" $local
    }

    foreach ($doc in @("CYCLE_033_PLAN.md", "CYCLE_034_PLAN.md", "PLAN.md", "REVIEW_PROMPT.md")) {
        $local = Join-Path $LocalRoot $doc
        scp "${RemoteHost}:$RemoteRoot/$doc" $local 2>$null
    }
}

function Test-Sync {
    $localManifest = Join-Path $env:TEMP "dream3r_local_manifest.sha256"
    $remoteManifest = "/tmp/dream3r_server_manifest.sha256"
    $remoteLocal = Join-Path $env:TEMP "dream3r_server_manifest.sha256"

    Get-ProjectFiles | ForEach-Object {
        $path = Join-Path $LocalRoot ($_ -replace "/", "\")
        $hash = (Get-FileHash $path -Algorithm SHA256).Hash.ToLower()
        "$hash  $_"
    } | Set-Content $localManifest

    Invoke-Remote "cd '$RemotePackage' && find . -type f \( -name '*.py' -o -name '*.md' \) ! -path '*/__pycache__/*' -printf '%P\0' | sort -z | xargs -0 sha256sum > '$remoteManifest'"
    scp "${RemoteHost}:$remoteManifest" $remoteLocal

    $local = @{}
    Get-Content $localManifest | ForEach-Object {
        if ($_ -match "^([0-9a-f]+)\s+(.+)$") { $local[$Matches[2]] = $Matches[1] }
    }

    $remote = @{}
    Get-Content $remoteLocal | ForEach-Object {
        if ($_ -match "^([0-9a-f]+)\s+(.+)$") { $remote[$Matches[2].Replace('\', '/')] = $Matches[1] }
    }

    $diffs = foreach ($key in @($local.Keys + $remote.Keys | Sort-Object -Unique)) {
        if (-not $local.ContainsKey($key)) { "ONLY_SERVER $key" }
        elseif (-not $remote.ContainsKey($key)) { "ONLY_LOCAL  $key" }
        elseif ($local[$key] -ne $remote[$key]) { "DIFF        $key" }
    }

    if ($diffs) {
        $diffs
        throw "Local and server package files differ."
    }

    "Local and server package files match."
}

function Invoke-ServerTests {
    Invoke-Remote "cd '$RemoteRoot' && CUDA_VISIBLE_DEVICES=0 conda run -n dream3r python -m dream3r.smoke_test"
    if ($FullTests) {
        Invoke-Remote "cd '$RemoteRoot' && for f in `$(find dream3r/tests -maxdepth 1 -name 'test_*.py' -printf '%f\n' | sort); do m=`${f%.py}; echo RUN `$m; conda run -n dream3r python -m dream3r.tests.`$m || exit 1; done"
    }
}

switch ($Mode) {
    "push" {
        Copy-ToServer
        Test-Sync
    }
    "pull" {
        Copy-FromServer
        Test-Sync
    }
    "verify" {
        Test-Sync
    }
    "test" {
        Invoke-ServerTests
    }
}
