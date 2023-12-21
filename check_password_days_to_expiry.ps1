Import-Module ActiveDirectory
# OU, которые нужно проверить
$ouList = "OU=Accounts,DC=YOURDOMAIN,DC=local"

# Файл для вывода результатов
$outputFile = "\\network\output.txt"
# Очищаем файл перед записью новых данных
Clear-Content -Path $outputFile

# Регулярное выражение для извлечения даты и времени
$regex = [regex] "(?<date>\d{2}.\d{2}.\d{4})"

# Обход каждого OU
foreach ($ou in $ouList) {
    # Получение всех пользователей из OU
    $users = Get-ADUser -Filter * -SearchBase $ou -Properties SamAccountName

    # Обход каждого пользователя
    foreach ($user in $users) {
        $userName = $user.SamAccountName
        $userInfo = net user $userName /domain

        if ($null -eq $userInfo) {
            continue
        } else {
            $passwordInfo = $userInfo | Where-Object { $_ -like "*Действие пароля завершается*" }

            if ($null -eq $passwordInfo) {
                continue
            } else {
                $passwordExpiresMatch = $regex.Match($passwordInfo)

                if ($passwordExpiresMatch.Success) {
                    $passwordExpires = $passwordExpiresMatch.Groups['date'].Value

                    if ($passwordExpires -eq "Никогда") {
                        continue
                    } else {
                        $passwordExpiryDate = [DateTime]::ParseExact($passwordExpires, "dd.MM.yyyy", [System.Globalization.CultureInfo]::InvariantCulture)
                        $daysToExpiry = ($passwordExpiryDate - (Get-Date)).Days
                        
                        if ($daysToExpiry -ge 0 -and $daysToExpiry -le 30) {
                            Add-Content -Path $outputFile -Value "$userName $daysToExpiry"
                        }
                    }
                } else {
                    continue
                }
            }
        }
    }
}
# Файл с данными о пользователях и сроках истечения их паролей
$inputFile = "\\network\output.txt"

# Чтение всех строк из файла
$userInfoLines = Get-Content -Path $inputFile

# Обход каждой строки
foreach ($userInfoLine in $userInfoLines) {
    # Извлечение имени пользователя и количества дней до истечения срока действия пароля
    $userName, $daysToExpiryInFile = $userInfoLine.Split(' ')

    # Отправка сообщения пользователю
    msg $userName /SERVER:SERVERNAME "Ваш пароль истечет через $daysToExpiryInFile дней. Пожалуйста, измените его."
}
