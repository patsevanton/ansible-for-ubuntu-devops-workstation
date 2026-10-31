# TODO: утилиты для ноутбука из трендов GitHub за последние 3 года

Срезка на **2026-10-24**. Окно поиска — репозитории, созданные после
**2023-10-24**. Источники: `github.com/trending` (день/неделя/месяц) и GitHub
Search API (`created:>2023-10-24`, сортировка по звёздам) по темам `cli`,
`tui`, `terminal`, `developer-tools`, `devops`, `linux`, `kubernetes`,
`security`, `productivity`, `monitoring`, `networking`, `ssh`, `docker`, `git`,
`sql`, `file-manager`, `backup`, `shell`.

По каждому кандидату через `gh api repos/{owner}/{repo}` проверены дата
создания, лицензия, архивность, последний push, а через
`releases/latest` — наличие Linux-сборки под x86_64. Звёзды и версии — на дату
срезки. Утилиты, которые уже описаны в `README.md`, `not-install.md` или
других `TODO-*.md`, в список не попадали.

Как читать: `- [ ]` — не добавлен. В заметке — что даёт утилита, чем
отличается от уже установленного и при каком условии к ней стоит вернуться.
Утилиты, которые уже добавлены из этой партии, перечислены в
[`TODO.md`](TODO.md), `bluetui` — в [`not-install.md`](not-install.md).
Кандидаты, добавленные по запросу, а не из трендов, помечены в заметке
явно (`cachelint`).

Кандидаты, которые не подошли, не удалены: они разнесены по профильным
трекерам — [`not-install.md`](not-install.md),
[`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md) и
[`TODO-server-apps.md`](TODO-server-apps.md). Если кандидат окажется
заброшенным, его место — [`TODO-abandoned.md`](TODO-abandoned.md).

Связанные трекеры: [`TODO.md`](TODO.md) — сводка, что уже ставится;
[`not-install.md`](not-install.md) — осознанные отказы;
[`TODO-trend-github-not-added.md`](TODO-trend-github-not-added.md) — прошлая
партия трендов; [`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md) —
кандидаты без готового бинарника; [`TODO-server-apps.md`](TODO-server-apps.md)
— серверные приложения.

## Файлы и навигация

- [ ] **lstr** — минималистичный просмотр дерева каталогов на Rust, с
      `--icons` и подсветкой. *(1.5k ⭐, MIT, `tar.xz`)* —
      [bgreenwell/lstr](https://github.com/bgreenwell/lstr) — не добавлен:
      то же даёт `eza --tree` и `tree`. Пересматривать, если понадобится
      отдельный бинарник без зависимости от `eza`.
- [ ] **doxx** — чтение `.docx` прямо в терминале: текст, таблицы, без
      LibreOffice. *(3.8k ⭐, MIT, `tar.xz`)* —
      [bgreenwell/doxx](https://github.com/bgreenwell/doxx) — не добавлен:
      документы Word на ноутбуке открываются редко. Пересматривать, если
      придётся часто смотреть вложения из почты без офисного пакета.
- [ ] **MangoDisk** — анализатор диска и безопасная чистка: дубликаты,
      кэши, удаление приложений; GUI. *(4.6k ⭐, GPL-3.0, `.deb`/AppImage)* —
      [harry0703/MangoDisk](https://github.com/harry0703/MangoDisk) — не
      добавлен: анализ уже закрывают `dust`, `gdu` и `duf`, а чистка — задача
      не ежедневная. Пересматривать, когда диск заполнится и понадобится
      именно «удалить лишнее», а не просто посмотреть размеры.

## Система и железо

- [ ] **usbtree** — живое дерево USB-устройств в TUI: VID/PID, скорость,
      активность; без root и libusb. *(706 ⭐, MIT, `tar.gz`)* —
      [gnomeria/usbtree](https://github.com/gnomeria/usbtree) — не добавлен:
      для редкой диагностики хватает `dmesg` и `/sys/bus/usb`. Пересматривать
      при проблемах с док-станцией, хабом или внешними дисками.
- [ ] **jolt** — TUI-монитор батареи и энергопотребления для Linux и macOS:
      заряд, расход, температура. *(573 ⭐, MIT, `tar.gz`)* —
      [jordond/jolt](https://github.com/jordond/jolt) — не добавлен:
      индикатор батареи GNOME закрывает базовый сценарий. Пересматривать,
      если понадобится разбираться, что именно съедает батарею.
- [ ] **pik** — интерактивное завершение процессов: выбор из списка, дерево
      родителей, подтверждение. *(581 ⭐, MIT, `tar.gz`)* —
      [jacek-kurlit/pik](https://github.com/jacek-kurlit/pik) — не добавлен:
      `procs` и `btop` уже показывают процессы, а `kill` есть всегда.
      Пересматривать, если понадобится часто убивать зависшие процессы без
      поиска PID.
- [ ] **systemd-manager-tui** — управление юнитами systemd: статус, запуск,
      остановка, логи. *(1.6k ⭐, MIT, `.deb`)* —
      [matheus-git/systemd-manager-tui](https://github.com/matheus-git/systemd-manager-tui)
      — не добавлен: `systemctl` и `journalctl` уже есть, а плейбук не
      управляет пользовательскими сервисами. Пересматривать, если появится
      много собственных unit-файлов.
- [ ] **net-merge** — агрегация Wi-Fi, Ethernet и USB-модема: балансировка
      новых соединений между адаптерами, без VPN и аккаунта. *(2.0k ⭐, MIT,
      `tar.gz`/`install.sh`)* — [rohit267/net-merge](https://github.com/rohit267/net-merge)
      — не добавлен: свежий (2026), требует прав на сеть и полезен только при
      нескольких каналах одновременно. Пересматривать, если одного канала
      перестанет хватать.

## Терминал, логи и SSH

- [ ] **sesh** — умный менеджер tmux-сессий через `zoxide` и `fzf`.
      *(2.9k ⭐, MIT, `tar.gz`)* —
      [joshmedeski/sesh](https://github.com/joshmedeski/sesh) — не добавлен:
      в плейбуке `zellij`, а `sesh` работает только с tmux. Пересматривать
      только вместе с решением поставить tmux.
- [ ] **ggh** — поиск по истории SSH-сессий и `~/.ssh/config`, быстрый повтор
      подключения. *(959 ⭐, Apache-2.0, бинарник)* —
      [byawitz/ggh](https://github.com/byawitz/ggh) — не добавлен: частично
      дублирует `zoxide` + `fzf`. Пересматривать, если понадобится именно
      история подключений (хосты уже закрывает установленный `lazyssh`).
- [ ] **edit** — современный терминальный текстовый редактор от Microsoft:
      мышь, меню, подсветка, без обучения vim. *(14.7k ⭐, MIT, `tar.gz`)* —
      [microsoft/edit](https://github.com/microsoft/edit) — не добавлен:
      `mcedit6` уже есть в составе M-Commander. Пересматривать, если
      понадобится редактор для тех, кто не пользуется vim/mcedit.
- [ ] **hints** — навигация по GUI с клавиатуры: подсказки поверх окон,
      клик, перетаскивание, скролл. *(1.4k ⭐, GPL-3.0, `install.sh` через
      `uv tool`)* — [AlfredoSequeida/hints](https://github.com/AlfredoSequeida/hints)
      — не добавлен: на Wayland перетаскивание зависит от композитора, а
      сценарий пока не ежедневный. Пересматривать, если понадобится работать
      без мыши.

## Буфер обмена и обмен файлами

- [ ] **rquickshare** — Quick Share / Nearby Share для Linux: передача файлов
      с Android и на Android. *(3.7k ⭐, GPL-3.0, `.deb`/AppImage)* —
      [Martichou/rquickshare](https://github.com/Martichou/rquickshare) — не
      добавлен: файлы с телефона приходят редко. Пересматривать при активном
      обмене с Android без кабеля и облака.
- [ ] **ClipCascade** — синхронизация буфера обмена между устройствами в
      реальном времени, P2P или через свой сервер. *(1.9k ⭐, GPL-3.0,
      `tar.xz`)* — [Sathvik-Rao/ClipCascade](https://github.com/Sathvik-Rao/ClipCascade)
      — не добавлен: нужен второй компьютер и запущенный сервер. Добавлять,
      если появится постоянная связка «ноутбук + десктоп».
- [ ] **Windows-11-Clipboard-History** — менеджер истории буфера обмена в
      стиле Windows 11, работает на Wayland и X11. *(1.0k ⭐, MIT,
      `.deb`/AppImage)* —
      [gustavosett/Windows-11-Clipboard-History-For-Linux](https://github.com/gustavosett/Windows-11-Clipboard-History-For-Linux)
      — не добавлен: истории буфера в GNOME нет, но и потребность не
      постоянная. Пересматривать, если понадобится часто возвращаться к
      скопированному.

## Git и CI

- [ ] **gh-stack** — расширение `gh` для stacked pull request'ов: цепочки
      зависимых PR и их синхронизация. *(1.7k ⭐, MIT, расширение `gh`)* —
      [github/gh-stack](https://github.com/github/gh-stack) — не добавлен:
      работа идёт через одиночные PR. Пересматривать, если появится практика
      больших изменений, разбитых на цепочку.
- [ ] **serie** — красивый граф git-коммитов в терминале, с ветками и
      тегами. *(2.2k ⭐, MIT, `tar.gz`)* —
      [lusingander/serie](https://github.com/lusingander/serie) — не
      добавлен: `lazygit` и `gitui` уже показывают историю. Пересматривать,
      если нужен именно компактный граф без полноценного клиента.
- [ ] **diffnav** — постраничный просмотр git-diff с деревом файлов, поверх
      `delta`. *(1.6k ⭐, MIT, `tar.gz`)* —
      [dlvhdr/diffnav](https://github.com/dlvhdr/diffnav) — не добавлен:
      `delta` уже настроен. Пересматривать, если диффы станут большими и
      понадобится навигация по файлам, как на GitHub.

## CLI-данные и секреты

- [ ] **otree** — просмотр JSON/YAML/TOML/XML в виде интерактивного дерева.
      *(523 ⭐, MIT, `tar.gz`)* —
      [fioncat/otree](https://github.com/fioncat/otree) — не добавлен: `jq`,
      `yq` и `jnv` уже есть. Пересматривать, если понадобится именно
      дерево с навигацией по большим конфигам.

## Сеть

- [ ] **xfr** — альтернатива `iperf3` с живым TUI, мультиклиентским сервером
      и QUIC. *(568 ⭐, Apache-2.0, `tar.gz`)* —
      [lance0/xfr](https://github.com/lance0/xfr) — не добавлен: `iperf3` в
      плейбуке нет, а измерение канала — разовая задача. Добавлять как замену
      `iperf3`, если понадобится гонять трафик между ноутбуком и сервером.
- [ ] **portr** — self-hosted туннель для localhost: HTTP, TCP, WebSocket,
      без стороннего сервиса. *(3.2k ⭐, AGPL-3.0, `zip`)* —
      [amalshaji/portr](https://github.com/amalshaji/portr) — не добавлен:
      постоянного сценария «показать localhost наружу» нет. Пересматривать
      для вебхуков и демонстраций без ngrok.
- [ ] **subtrace** — инспектор HTTP-запросов бэкенда: запросы, ответы,
      заголовки, задержки; запускается в Docker. *(3.1k ⭐, BSD-3-Clause,
      бинарник)* — [subtrace/subtrace](https://github.com/subtrace/subtrace)
      — не добавлен: это серверный инструмент, а локально хватает `curl -v`
      и логов приложения. Пересматривать при отладке своего API.

## Kubernetes и контейнеры

- [ ] **unregistry** — отправка Docker-образов на удалённый сервер напрямую,
      без внешнего registry. *(4.9k ⭐, Apache-2.0, `tar.gz`)* —
      [psviderski/unregistry](https://github.com/psviderski/unregistry) — не
      добавлен: образы собираются локально и публикуются в registry. Добавлять
      для homelab-сценария «собрал на ноутбуке — запустил на сервере».
- [ ] **microsandbox** — локальные microVM-песочницы для недоверенного кода,
      с CLI, SDK и OpenAI-совместимым API. *(8.8k ⭐, Apache-2.0,
      `install.sh`)* — [superradcompany/microsandbox](https://github.com/superradcompany/microsandbox)
      — не добавлен: требует KVM и пока избыточен рядом с Docker. Добавлять,
      если понадобится запускать чужой код с сильной изоляцией.
- [ ] **cachelint** — статический анализ Dockerfile по кэшу слоёв: находит
      дорогой `RUN npm ci`/`pip install` после широкого `COPY . .`, оценивает
      потерянные секунды по истории git и печатает переставленный Dockerfile
      (`--fix` с резервной копией `.bak`). *(1 ⭐, MIT, Python ≥ 3.11,
      `pipx`)* — [0xABCD01/cachelint](https://github.com/0xABCD01/cachelint) —
      не добавлен (кандидат от 2026-10-24, не из трендов): проект новый
      (создан 2026-06-29, последний пуш 2026-10-21), на PyPI только
      pre-alpha `0.1.0a1`, в GitHub-релизе `v0.1.0` нет ассетов, а README
      советует `pipx install "cachelint @ git+https://github.com/0xABCD01/cachelint.git"`
      — установка из плавающего `main` не пинится и не обновляется.
      Пересматривать, когда на PyPI появится стабильная версия: тогда роль
      `pipx_apps` с зафиксированной версией, команда `cachelint`. Место в
      наборе — рядом с `hadolint`: тот проверяет стиль и ошибки инструкций,
      `cachelint` — порядок слоёв и время сборки; `dive` для этого не годится,
      он разбирает уже собранный образ. Отслеживается в
      [#3](https://github.com/0xABCD01/cachelint/issues/3) (стабильный релиз на
      PyPI) и [#1](https://github.com/0xABCD01/cachelint/issues/1)
      (Docker-образ).

## Безопасность и доступ

- [ ] **opkssh** — SSH-доступ по OpenID Connect вместо статических ключей,
      с короткоживущими сертификатами. *(2.1k ⭐, Apache-2.0, бинарник)* —
      [openpubkey/opkssh](https://github.com/openpubkey/opkssh) — не добавлен:
      нет IdP и парка серверов, где это окупится. Пересматривать при переходе
      на SSO для инфраструктуры.
- [ ] **kingfisher** — поиск секретов в коде и файлах с живой проверкой
      валидности и оценкой blast radius. *(1.3k ⭐, Apache-2.0, `.deb`/`tgz`)*
      — [mongodb/kingfisher](https://github.com/mongodb/kingfisher) — не
      добавлен: `gitleaks` и `trufflehog` уже стоят. Добавлять, если
      понадобится именно live-валидация найденных ключей.

## Прочее

- [ ] **vicinae** — быстрый расширяемый лаунчер для Linux в духе Raycast:
      приложения, файлы, буфер, расширения. *(10.4k ⭐, GPL-3.0,
      AppImage/`tar.gz`)* — [vicinaehq/vicinae](https://github.com/vicinaehq/vicinae)
      — не добавлен: в GNOME есть Activities и поиск. Пересматривать, если
      понадобится лаунчер с плагинами и clipboard-историей в одном месте.
- [ ] **winboat** — запуск Windows-приложений на Linux с интеграцией в
      рабочий стол, через VM. *(23.3k ⭐, MIT, `.deb`/AppImage)* —
      [winboat-org/winboat](https://github.com/winboat-org/winboat) — не
      добавлен: требует KVM и лицензию Windows, а нужных Windows-программ
      нет. Пересматривать, если появится ПО без Linux-версии.
- [ ] **jiratui** — TUI для Jira: задачи, фильтры, комментарии, переходы по
      статусам. *(1.7k ⭐, MIT, `pipx`)* —
      [whyisdifficult/jiratui](https://github.com/whyisdifficult/jiratui) —
      не добавлен: Jira на ноутбуке не используется. Добавлять, если Jira
      станет частью рабочего процесса.

