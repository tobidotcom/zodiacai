$body = @{
    name = "John Doe"
    zodiac_sign = "Aries"
    birth_date = "1990-04-15"
    birth_location = "New York"
    birth_time = "08:30"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri "http://localhost:5002/moon-reading" -Method Post -Body $body -Headers $headers -ContentType "application/json"

    if ($response) {
        [System.IO.File]::WriteAllBytes("moon_reading.mp3", $response)
        Write-Host "Moon reading audio saved as moon_reading.mp3"
    } else {
        Write-Host "Response is empty. Check if the API returned any data."
    }
} catch {
    Write-Host "An error occurred: $_"
    Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
    Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
}