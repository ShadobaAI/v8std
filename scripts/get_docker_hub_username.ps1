$ErrorActionPreference = "Stop"

$configPath = Join-Path $env:USERPROFILE ".docker\config.json"
try {
    if (-not (Test-Path -LiteralPath $configPath)) {
        exit 1
    }
    $config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
} catch {
    exit 1
}

$dockerHubRegistries = @(
    "https://index.docker.io/v1/",
    "https://registry-1.docker.io",
    "registry-1.docker.io",
    "docker.io"
)

function Get-PropertyValue {
    param(
        [object] $Object,
        [string] $Name
    )

    if ($null -eq $Object) {
        return $null
    }

    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) {
        return $null
    }

    return $property.Value
}

$credentialHelper = $null
foreach ($registry in $dockerHubRegistries) {
    $credentialHelper = Get-PropertyValue -Object $config.credHelpers -Name $registry
    if ($credentialHelper) {
        break
    }
}

if (-not $credentialHelper) {
    $credentialHelper = $config.credsStore
}

if ($credentialHelper) {
    try {
        $credentialEntriesJson = & "docker-credential-$credentialHelper" list 2>$null
        if ($LASTEXITCODE -eq 0 -and $credentialEntriesJson) {
            $credentialEntries = ($credentialEntriesJson -join [Environment]::NewLine) | ConvertFrom-Json
            foreach ($registry in $dockerHubRegistries) {
                $username = Get-PropertyValue -Object $credentialEntries -Name $registry
                if ($username) {
                    Write-Output $username
                    exit 0
                }
            }
        }
    } catch {
        # Fall back to an inline auth entry below.
    }
}

foreach ($registry in $dockerHubRegistries) {
    $registryConfig = Get-PropertyValue -Object $config.auths -Name $registry
    $encodedAuth = Get-PropertyValue -Object $registryConfig -Name "auth"
    if (-not $encodedAuth) {
        continue
    }

    try {
        $decodedAuth = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($encodedAuth))
        $username = $decodedAuth.Split(":", 2)[0]
        if ($username) {
            Write-Output $username
            exit 0
        }
    } catch {
        continue
    }
}

exit 1
