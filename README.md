# Ru!
Приветствую, это обновлятор на tkinter который ищет обновления в github репозитории, и умеет искать самую свежую версию вашего проекта

для настройки обновляемого репозитория найдите в коде **GITHUB_API_RELEASES**

```
GITHUB_API_RELEASES = "https://api.github.com/repos/<USER>/<REPO>/releases/latest"
VERSION_FILE....
```
и в строчке <USER> укажите свой у меня к примеру он user30092, а репозиторий <REPO> Updater и в данном параметре должно быть так

```
GITHUB_API_RELEASES = "https://api.github.com/repos/user30092/Updater/releases/latest"
VERSION_FILE....
```

__ВНИМАНИЕ__ установите requests. НАДЕЮСЬ это уже разжовывать не надо

# En
Welcome! This is an updater built with tkinter that checks for updates in a GitHub repository and can find the latest version of your project.

To configure the repository to be updated, find the **GITHUB_API_RELEASES** line in the code:

```
GITHUB_API_RELEASES = "https://api.github.com/repos/<USER>/<REPO>/releases/latest"
VERSION_FILE....
```
In the <USER> part, enter your GitHub username (for example, mine is user30092), and in <REPO> enter your repository name (for example, Updater). The parameter should look like this:

```
GITHUB_API_RELEASES = "https://api.github.com/repos/user30092/Updater/releases/latest"
VERSION_FILE....
```

__ATTENTION__ Install the requests library. I hope you already know how