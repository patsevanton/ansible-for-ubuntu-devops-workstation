# TODO: кандидаты из трендов GitHub, которые не попали в плейбук

Остаток разбора трендовых утилит GitHub: трекер `TODO-trend-github.md` разобран
полностью (последняя партия — 2026-10-23) и удалён, здесь только те кандидаты,
которые осознанно не добавлены. Свежая партия на рассмотрение — в разделе
[«Тренды GitHub, 2026-10-23»](#тренды-github-2026-10-23), вторая выборка того
же дня — в разделе
[«Партия за последний год, 2026-10-23»](#партия-за-последний-год-2026-10-23).
Добавленные
утилиты перечислены в [`TODO.md`](TODO.md), причины отказов по конкретным
инструментам — в [`not-install.md`](not-install.md).

Проверено 2026-10-23 по `releases/latest` и `expanded_assets`; новая партия —
через `gh api repos/{owner}/{repo}/releases/latest`, потому что нужны точные
имена ассетов. Для apt — по `getPublishedSources` в Launchpad (серия
`resolute`).

Как читать: `- [ ]` — не добавлен; в заметке — причина и условие, при котором
кандидата стоит пересмотреть.

Заброшенные проекты (архив GitHub, годы без обновлений) сюда не входят: они
описаны только в [`TODO-abandoned.md`](TODO-abandoned.md).

---

## Тренды GitHub, 2026-10-23

Новая партия: тренды за день/неделю/месяц плюс свежие репозитории
(`created:>2026-01-01`) по темам `cli`, `tui`, `terminal`, `kubernetes`,
`security`, `devops`, `self-hosted`. По каждому кандидату проверены
`releases/latest` и наличие linux-amd64 артефакта.

Пока ничего не добавлено: сначала нужно решить, нужен ли инструмент, и
проверить лицензию — у части она не MIT/Apache, а проекты молодые (2026 год)
и звёзды у многих раздуты хайпом вокруг агентов. Для каждого кандидата в
заметке указано, при каком условии к нему стоит вернуться.

### Общего назначения

- [ ] **xerj** — локальный поисковик и MCP-сервер: код, логи, CSV/JSONL,
      PDF, BM25 и вектор, Elasticsearch-совместимый API. *(13.3k ⭐,
      `tar.gz`/`.deb`)* — [xerj-org/xerj](https://github.com/xerj-org/xerj)
      — не добавлен: свежий (`1.0.0-rc.98`) и пересекается с `ripgrep` +
      `fd`; MCP-поиск по репозиторию нужен не каждый день. Проверено
      2026-10-24: один статический бинарь без зависимостей, 400 МБ в
      простое, ~2 ГБ на активный индекс, x86-64-v2 или arm64/NEON. RAM
      зависит не от объёма корпуса, а от числа индексов: `autoindex` делает
      индекс на датасет (в примере из README 25 329 файлов → 593 индекса).
      На `~/magnitonline` (78 ГБ, 1,1 млн файлов; `.git` 17 ГБ,
      `.terragrunt-cache` 21 ГБ, чистых ~31 ГБ в 842 тыс. файлов) целиком
      индексировать не стоит — это порядка 10–20 тыс. индексов, 1,5–3 ч на
      16 ядрах и 15–25 ГБ на диске. Рабочий вариант — 3–5 узких корней по
      0,5–2 ГБ текста, сначала `xerj autoindex --dry-run` и запуск с
      `--no-semantic --workers 8`, `data_dir` вне индексируемого дерева.
      Где выигрывает: вопросы «как это устроено» и reference coding по
      нишевому стеку (Yandex Cloud, Flux, собственные Ansible-роли), где
      модель не помнит API; там замерено 2,7× меньше output-токенов, чем у
      агента с grep. Где не выигрывает: точные токены (`:80`, хост в
      конфиге) — `rg` по 78 ГБ отвечает за 17 с и даёт полный список, а не
      top-N пассажей; логи и метрики уже закрыты VictoriaLogs и
      Elasticsearch. Пересматривать после стабильного 1.0 и при появлении
      корпуса на 1–5 ГБ текста, по которому `rg` не даёт ответа.
- [ ] **Filee** — офлайн-конвертер 255 форматов: изображения, PDF, Office,
      видео, аудио, архивы. *(10.8k ⭐, `linux-x64.tar.gz`)* —
      [KnifeLemon/Filee](https://github.com/KnifeLemon/Filee)
      — не добавлен: это GUI-приложение, а конвертацию в плейбуке закрывают
      `ffmpeg` и разовые CLI-инструменты. Пересматривать, если понадобится
      конвертация «перетащил и готово» без терминала.
- [ ] **VoiceStudio** — полностью локальная диктовка, транскрипция, TTS,
      дубляж и озвучка на 646 языках. *(83.6k ⭐, `.deb`/AppImage, AGPL-3.0)* —
      [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio)
      — не добавлен: голосовой ввод не используется, текст набирается руками,
      а подмену голоса на созвоне проект не делает — виртуального микрофона и
      real-time voice conversion в нём нет. Разбор и оговорки —
      [`not-install.md`](not-install.md#voicestudio--голосовой-ввод-не-используется).
      Пересматривать, если понадобится локальная расшифровка встреч, дубляж
      или диктовка без облака.
- [ ] **googleworkspace/cli** — один CLI на Drive, Gmail, Calendar, Sheets,
      Docs, Chat и Admin. *(31.8k ⭐, `linux-gnu.tar.gz`)* —
      [googleworkspace/cli](https://github.com/googleworkspace/cli)
      — не добавлен: завязан на Google Workspace, которого в сценарии
      ноутбука нет. Пересматривать, если появится рабочий аккаунт Google.

### Для AI-агентов

- [ ] **OfficeCLI** — чтение, редактирование и автоматизация Word, Excel и
      PowerPoint без установленного Office, одиночный бинарник.
      *(32.4k ⭐, `officecli-linux-x64`)* —
      [iOfficeAI/OfficeCLI](https://github.com/iOfficeAI/OfficeCLI)
      — не добавлен: офисные файлы в работе не генерируются. Пересматривать,
      если агентам понадобится править `.docx`/`.xlsx` без LibreOffice.
- [ ] **anydoc** — конвертация Word, PowerPoint, Excel, OpenDocument, RTF,
      EPUB, CSV и PDF в чистый Markdown. *(23.1k ⭐, npm/pip, отдельного
      бинарника нет)* — [firecrawl/anydoc](https://github.com/firecrawl/anydoc)
      — ⏸ **отложено на будущее** (решение 2026-10-24): постоянная установка
      есть только через `npm install -g @firecrawl/anydoc` (нужен Node.js ≥ 20,
      версия 0.2.4) или `pip install firecrawl-anydoc` (Python ≥ 3.10, 0.2.4),
      готового релизного бинарника нет — под роль `binaries` это не ложится.
      Плюсы: 14 форматов, медиана конвертации 4.4 мс, MIT-лицензия, офлайн
      (кроме `--ocr hosted`). Пересматривать, если понадобится массовая
      конвертация документов в Markdown для агентов. CLI есть только в
      npm-пакете, Python-пакет — библиотека без консольной команды, поэтому
      `pipx` не подойдёт: либо `npm install -g`, либо venv под задачу.
- [ ] **openwiki** — CLI, который пишет и поддерживает документацию для
      агентов по коду. *(17.4k ⭐, npm, релизных ассетов нет)* —
      [langchain-ai/openwiki](https://github.com/langchain-ai/openwiki)
      — не добавлен: только npm, а документация в репозиториях ведётся
      вручную. Пересматривать, если понадобится автогенерация `AGENTS.md`/
      wiki для чужих проектов.

### Аналоги herdr

- [ ] **agent-deck** — TUI-центр управления сессиями агентов (Claude,
      Codex, Gemini, OpenCode): статусы running/waiting/done, группы, поиск,
      форки, worktrees, учёт стоимости, управление с телефона.
      *(1.1k ⭐, `linux_amd64.tar.gz`)* —
      [asheshgoplani/agent-deck](https://github.com/asheshgoplani/agent-deck)
      — не добавлен: herdr уже стоит и закрывает похожий сценарий.
      Пересматривать, если herdr перестанет хватать для обзора всех сессий
      или понадобится телефонный пульт.
- [ ] **workmux** — git-worktree плюс окно tmux/zellij/kitty на задачу,
      чтобы гонять агентов параллельно без конфликтов. *(2.9k ⭐,
      `linux-amd64.tar.gz`)* — [raine/workmux](https://github.com/raine/workmux)
      — не добавлен: пересекается с `wt` (worktrunk) и `zellij`. Сильная
      сторона — связка worktree + мультиплексор из коробки. Пересматривать,
      если параллельные агенты станут обычной практикой.
- [ ] **alethe-agents** — локальный desktop-воркспейс для нескольких
      агентов и шеллов: настоящие PTY, сплиты, сохраняемые раскладки, история.
      *(974 ⭐, `.deb`/AppImage/`.rpm`)* —
      [Kc1t/alethe-agents](https://github.com/Kc1t/alethe-agents)
      — не добавлен: ещё один GUI-воркспейс поверх уже стоящих herdr,
      `zellij` и T3 Code. Пересматривать, если понадобится именно настольное
      приложение с PTY-сплитами.
- [ ] **cmux** — терминал на Ghostty с вертикальными вкладками и
      уведомлениями под агентов. *(28.4k ⭐, только macOS)* —
      [manaflow-ai/cmux](https://github.com/manaflow-ai/cmux)
      — ⛔ не подходит: сборок под Linux нет, а ноутбук на Ubuntu.

### Аналоги rtk

- [ ] **caveman** — прокси и skill, которые режут около 65% токенов,
      работают с 30+ агентами, включая OpenCode. *(114.5k ⭐,
      `npx @caveman-ai/cli`, Apache-2.0)* —
      [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
      — не добавлен: rtk уже стоит и делает то же самое, а caveman
      распространяется только через npm. Пересматривать, если rtk перестанет
      покрывать нужные команды или понадобится именно «caveman»-стиль ответов.
- [ ] **context-mode** — прячет вывод инструментов в песочницу (заявлено до
      98%), хранит память сессии и разводит маршрутизацию по 17 платформам
      через MCP и hooks. *(31.9k ⭐, npm/MCP, релизных ассетов нет)* —
      [mksglu/context-mode](https://github.com/mksglu/context-mode)
      — не добавлен: npm + hooks, под роль `binaries` не ложится, а rtk уже
      закрывает сжатие вывода. Пересматривать, если понадобится именно
      песочница для tool-output, а не прокси.
- [ ] **sqz** — точечное сжатие вывода инструментов и дедуп повторов до
      ссылок, Rust, без вызовов LLM. *(660 ⭐,
      `sqz-v*-x86_64-unknown-linux-musl.tar.gz`)* —
      [ojuschugh1/sqz](https://github.com/ojuschugh1/sqz)
      — не добавлен: заметно менее популярен, чем rtk, и решает ту же задачу.
      Пересматривать, если понадобится MCP-вариант сжатия без прокси.
- [ ] **codeburn** — локальный учёт токенов и стоимости по 37 инструментам
      и агентам, разбивка по модели, проекту и задаче. *(11.6k ⭐,
      `npx codeburn`)* — [getagentseal/codeburn](https://github.com/getagentseal/codeburn)
      — не добавлен: это `npx`, и это наблюдение, а не сжатие. Пересматривать,
      если понадобится регулярно смотреть расход по агентам.
- [ ] **cost-xray** — показывает, что именно Claude Code и Codex отправляют
      в API и сколько стоит каждая часть. *(6.1k ⭐, Python)* —
      [tigerless-labs/cost-xray](https://github.com/tigerless-labs/cost-xray)
      — не добавлен: Python-инструмент для разового разбора, а не для
      постоянной установки. Пересматривать при расследовании роста расходов.

### Аналоги T3 Code

- [ ] **orca** — десктоп, мобильный клиент и удалённый рантайм для флота
      агентов, любой агент со своей подпиской. *(103.4k ⭐,
      `.deb`/AppImage/`.rpm`)* — [stablyai/orca](https://github.com/stablyai/orca)
      — не добавлен: T3 Code уже стоит и закрывает тот же сценарий.
      Пересматривать, если понадобится именно удалённый рантайм или
      мобильный клиент лучше, чем у T3.
- [ ] **paperclip** — приложение для управления агентами на работе.
      *(106.4k ⭐, релизных бинарников нет)* —
      [paperclipai/paperclip](https://github.com/paperclipai/paperclip)
      — не добавлен: нет linux-артефакта, только исходники/контейнер.
      Пересматривать, если появится `.deb` или AppImage.
- [ ] **multica** — люди и агенты как одна команда, self-hosted, desktop и
      CLI. *(53.6k ⭐, `.deb`/AppImage/`multica-cli-linux-amd64.tar.gz`)* —
      [multica-ai/multica](https://github.com/multica-ai/multica)
      — не добавлен: это командный сервер, а не пульт к локальным агентам.
      Пересматривать, если понадобится совместная работа с агентами.
- [ ] **cc-switch** — all-in-one переключатель провайдеров и аккаунтов для
      Claude Code, Codex, OpenCode, OpenClaw, Grok Build и Hermes Agent.
      *(148k ⭐, `.deb`/AppImage/`.rpm`)* —
      [farion1231/cc-switch](https://github.com/farion1231/cc-switch)
      — не добавлен: решает другую задачу — смену моделей и аккаунтов, а не
      управление сессиями. Пересматривать, если появится несколько
      провайдеров и нужно быстро переключаться.
- [ ] **atlas** — source control для агентов: несколько агентов, их
      изменения и запросы в одном месте. *(9.6k ⭐,
      `.deb`/AppImage/`linux-x86_64.tar.gz`)* —
      [pacifio/atlas](https://github.com/pacifio/atlas)
      — не добавлен: пересекается с git-воркфлоу и worktree-инструментами.
      Пересматривать, если несколько агентов начнут менять один репозиторий.

### Аналоги Ouroboros

- [ ] **openclaw** — «AI, который реально делает вещи», любая ОС, десктоп и
      несколько платформ. *(392.8k ⭐, `.deb`/AppImage)* —
      [openclaw/openclaw](https://github.com/openclaw/openclaw)
      — не добавлен: Ouroboros уже стоит, а два general-purpose агента на
      ноутбуке избыточны. Пересматривать, если Ouroboros окажется слишком
      тяжёлым или не устроит качество.
- [ ] **nanobot** — лёгкий self-hosted агент: WebUI, инструменты, память,
      MCP, чаты. *(49.3k ⭐, `nanobot-tui-linux-x64.zip`, Python)* —
      [HKUDS/nanobot](https://github.com/HKUDS/nanobot)
      — не добавлен: Python-фреймворк, а не одиночный бинарник; Ouroboros
      покрывает сценарий. Пересматривать, если понадобится свой агент с
      WebUI и минимальными зависимостями.
- [ ] **Octop** — self-hosted ассистент на несколько пользователей и
      агентов. *(10.8k ⭐, `Octop-desktop-linux-amd64.tar.gz`)* —
      [TencentCloud/Octop](https://github.com/TencentCloud/Octop)
      — не добавлен: многопользовательский сервер, на ноутбуке не нужен.
      Пересматривать, если понадобится общий ассистент для команды.
- [ ] **QwenPaw** — персональный ассистент с установкой на свою машину или
      в облако, поддержка нескольких чатов. *(36.0k ⭐, только
      macOS/Windows)* — [agentscope-ai/QwenPaw](https://github.com/agentscope-ai/QwenPaw)
      — ⛔ не подходит: Linux-сборки в релизе нет.
- [ ] **OpenShell** — безопасный приватный рантайм и песочница для
      автономных агентов. *(18.4k ⭐, `.deb`/`tar.gz`)* —
      [NVIDIA/OpenShell](https://github.com/NVIDIA/OpenShell)
      — не добавлен: это не агент, а рантайм под него; отдельного сценария
      на ноутбуке пока нет. Пересматривать, если понадобится изолировать
      агентов с доступом к файлам и сети.
- [ ] **ruflo** — агентский harness со swarm-ами, памятью и RAG.
      *(78.7k ⭐, npm, релизных ассетов нет)* —
      [ruvnet/ruflo](https://github.com/ruvnet/ruflo)
      — не добавлен: npm-пакет и пересекается с opencode/herdr. Пересматривать,
      если понадобятся именно мультиагентные swarm-сценарии.

### Дубли и уже описанные кандидаты

- [ ] **treehouse** — управление git-worktree. *(1.9k ⭐,
      `linux-amd64.tar.gz`)* —
      [kunchenguid/treehouse](https://github.com/kunchenguid/treehouse)
      — ⛔ дублирует `wt` (worktrunk).

**Floci** (AWS-эмулятор) в эту партию не заводится: он уже описан в
[`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md) как контейнерный сервис.

---

## Партия за последний год, 2026-10-23

Вторая выборка того же дня. Источники: тренды GitHub за день/неделю/месяц
(`github.com/trending`) и поиск `created:>2025-10-23 stars:>500` по темам
`cli`, `tui`, `terminal`, `kubernetes`, `devops`, `docker`, `security`,
`self-hosted`, `monitoring`, `observability`, `git`, `sql`, `dns`, `ssh`,
`terraform` (плюс ключевые слова `cli`/`tui` в имени и описании). По каждому
кандидату проверены лицензия, `releases/latest`, наличие linux-amd64
артефакта, дата последнего пуша и отсутствие в плейбуке (README и все
`TODO-*.md`, `not-install.md`).

Наблюдение по выдаче: в месячных трендах половина — обвязки вокруг
coding-агентов, плюс старые репозитории, которые к «последнему году»
не относятся (Ghidra 2019, Supabase), и уже стоящий `t3code`. Ниже только
утилиты для ноутбука.

### Кандидаты на добавление

- [ ] **lazyrsync** — TUI к `rsync`: профили, предпросмотр переноса в виде
      структурированного диффа до запуска, живой прогресс и отмена.
      *(936 ⭐, `x86_64-unknown-linux-gnu.tar.gz`, MIT)* —
      [westpoint-io/lazyrsync](https://github.com/westpoint-io/lazyrsync)
      — не добавлен: `rsync` в плейбуке есть как системная утилита, но
      сценария регулярной синхронизации каталогов на ноутбуке нет, а бэкапы
      описаны `nxs-backup`. Пересматривать, если появится вторая машина или
      NAS: сухой прогон в виде диффа — главное, чего не хватает голому
      `rsync --dry-run`.
- [ ] **xleak** — просмотр Excel в терминале: TUI, полнотекстовый поиск,
      отображение формул, переход по листам. *(1.5k ⭐,
      `xleak-linux-x86_64.tar.gz`, MIT)* —
      [bgreenwell/xleak](https://github.com/bgreenwell/xleak)
      — не добавлен: CSV/Parquet разбирает `duckdb`, Excel на ноутбуке
      встречается редко. Пересматривать, если регулярно приходят `.xlsx`
      от заказчиков: конвертировать их в CSV ради `duckdb` — лишний шаг.
- [ ] **cass** (coding-agent-search) — TUI и CLI для индексации и поиска
      истории сессий локальных coding-агентов (OpenCode, Claude Code, Codex,
      Gemini CLI, Cursor и ещё десятки) в одной временной шкале.
      *(1.2k ⭐, `cass-linux-amd64.tar.gz`, MIT + оговорки OpenAI/Anthropic)* —
      [Dicklesworthstone/coding_agent_session_search](https://github.com/Dicklesworthstone/coding_agent_session_search)
      — не добавлен: лицензия помечена как `NOASSERTION` — к MIT добавлены
      тексты-оговорки вендоров, и это надо читать перед установкой. Плюс
      `opencode` и `herdr` уже хранят сессии, а поиск по ним — редкая задача.
      Пересматривать, если сессий станет много и понадобится «где я это уже
      решал».

### Под условием или рано

- [ ] **vykar** — бэкапы на Rust: YAML-конфиг, дедупликация FastCDC,
      шифрование AES-256-GCM/ChaCha20, локальный диск, S3, SFTP, REST-сервер,
      встроенный демон вместо cron. Бинарник называется `vger`.
      *(714 ⭐, `vger-v0.2.0-x86_64-unknown-linux-gnu.tar.gz`, GPL-3.0)* —
      [borgbase/vykar](https://github.com/borgbase/vykar)
      — не добавлен: автор прямо пишет «не для продакшена, но протестируйте
      рядом с другими бэкапами», а YAML-бэкапы уже делает `nxs-backup`
      (без дедупликации). Пересматривать к 1.0, если понадобится
      дедуплицированный репозиторий на S3.
- [ ] **deja** — предиктивные inline-подсказки для zsh «как в fish».
      *(914 ⭐, `deja_0.1.0_linux_amd64.tar.gz`, MIT)* —
      [Giammarco-Ferranti/deja](https://github.com/Giammarco-Ferranti/deja)
      — не добавлен: историей и подсказками уже занимаются `atuin`, `mcfly`
      и `zoxide`. Пересматривать только если убрать `mcfly`: два механизма
      подсказок в одной строке конфликтуют.
- [ ] **weathr** — погода в терминале с ASCII-анимацией.
      *(3.1k ⭐, одиночный `weathr-linux-amd64`, GPL-3.0)* —
      [Veirt/weathr](https://github.com/Veirt/weathr)
      — не добавлен: полезной нагрузки для DevOps-ноутбука нет, только
      эстетика. Держать в уме как «одна команда, один бинарник», если
      захочется.
- [ ] **Surge** — TUI-менеджер загрузок на Go: многопоточные загрузки,
      докачка, очередь. *(3.6k ⭐, `*_linux_amd64.tar.gz`, MIT)* —
      [SurgeDM/Surge](https://github.com/SurgeDM/Surge)
      — не добавлен: релиз помечен `0.1.0-SNAPSHOT`, а скачивание закрывают
      `curl` и `wget` из роли `base` — очередей и докачки они не умеют, но и
      потребности в них пока нет. Пересматривать, если понадобится качать
      крупные образы с докачкой после обрыва.
- [ ] **eilmeldung** — TUI RSS-ридер на библиотеке news-flash.
      *(1.0k ⭐, `x86_64-unknown-linux-gnu.tar.gz`, GPL-3.0)* —
      [christo-auer/eilmeldung](https://github.com/christo-auer/eilmeldung)
      — не добавлен: чтение лент не входит в сценарии ноутбука.
      Пересматривать, если появится привычка читать релиз-ноуты через RSS.

### Не приложение или не для Linux

- [ ] **polyglot** — транспайлер SQL на 30+ диалектов. *(973 ⭐, MIT)* —
      [tobilg/polyglot](https://github.com/tobilg/polyglot)
      — ⛔ в релизах только FFI-библиотеки (`polyglot-sql-ffi-*.tar.gz`),
      CLI-бинарника нет: это библиотека для встраивания, а не утилита.
- [ ] **ghui** — TUI-клиент GitHub. *(1.1k ⭐, MIT)* —
      [kitlangton/ghui](https://github.com/kitlangton/ghui)
      — ⛔ релизных ассетов нет (сборка через bun/npm), а функционально
      дублирует `gh` и `ghgrab`.
- [ ] **look** — кросс-платформенный лаунчер в духе Spotlight/Raycast.
      *(1.2k ⭐, GPL-3.0)* — [kunkka19xx/look](https://github.com/kunkka19xx/look)
      — ⛔ в релизе только `Look-0.1.0-macOS.zip`: Linux-сборки нет, несмотря
      на заявленную кросс-платформенность.
- [ ] **Kaku** — терминал для macOS. *(6.1k ⭐, MIT)* —
      [tw93/Kaku](https://github.com/tw93/Kaku)
      — ⛔ единственный ассет — `Kaku.dmg`.
- [ ] **muxy** — терминальный мультиплексор на Rust. *(2.3k ⭐, MIT)* —
      [muxy-app/muxy](https://github.com/muxy-app/muxy)
      — ⛔ Linux-сборки нет (в релизе `.dmg`), да и мультиплексор в плейбуке —
      `zellij`.
- [ ] **tcpfit** — подбор TCP-параметров по замеру BDP на конкретной машине.
      *(909 ⭐, MIT)* — [Kylin010/tcpfit](https://github.com/Kylin010/tcpfit)
      — ⛔ это shell-скрипт без бинарника и с пояснениями на китайском;
      менять `sysctl` на ноутбуке ради тюнинга смысла нет.
- [ ] **plexo** — ускорение загрузок через несколько соединений.
      *(4.9k ⭐, MIT)* — [anmolkapil/plexo](https://github.com/anmolkapil/plexo)
      — ⛔ GUI (`.dmg`/`.exe`/AppImage, deb только arm64), CLI-режима нет.
- [ ] **fakecloud** — локальный эмулятор AWS, 107 сервисов, альтернатива
      LocalStack. *(768 ⭐, `fakecloud-v0.1.1-linux-amd64.tar.gz`, AGPL-3.0)* —
      [faiscadev/fakecloud](https://github.com/faiscadev/fakecloud)
      — ⛔ конкурирует с `Floci`, который уже описан в
      [`TODO-server-apps.md`](https://github.com/patsevanton/ansible-for-ubuntu-llm-agent-server/blob/main/TODO-server-apps.md); держать как замену, если
      `Floci` не покроет нужный сервис. AGPL-3.0 для локального сервиса
      допустима, но лишняя.

### Дубли уже стоящего в плейбуке

- [ ] **elio** — терминальный файловый менеджер «всё в комплекте».
      *(902 ⭐, `x86_64-unknown-linux-gnu.tar.gz`, MIT)* —
      [elio-fm/elio](https://github.com/elio-fm/elio)
      — ⛔ дублирует `yazi` и `lf`.
- [ ] **keifu** — TUI для навигации по графу коммитов. *(811 ⭐, Rust)* —
      [trasta298/keifu](https://github.com/trasta298/keifu)
      — ⛔ дублирует `lazygit`/`gitui`: граф коммитов там есть.
- [ ] **syswatch** — диагностика одного хоста в TUI.
      *(916 ⭐, `syswatch-linux-x86_64.tar.gz`, MIT)* —
      [matthart1983/syswatch](https://github.com/matthart1983/syswatch)
      — ⛔ дублирует `btm`/`bottom` и `procs`.
- [ ] **sqlit** — TUI к SQL Server, MySQL, Postgres, SQLite и Turso.
      *(4.9k ⭐, Python, MIT)* — [Maxteabag/sqlit](https://github.com/Maxteabag/sqlit)
      — ⛔ дублирует `lazysql` и `harlequin`.
- [ ] **vex-tui** — редактор Excel/CSV в терминале. *(943 ⭐, MIT)* —
      [CodeOne45/vex-tui](https://github.com/CodeOne45/vex-tui)
      — ⛔ альтернатива `xleak` из списка выше; выбран `xleak` (свежие
      коммиты, режим только для чтения), `vex-tui` — если понадобится
      именно правка таблиц.
- [ ] **leaf** — просмотр Markdown в терминале «как в GUI».
      *(2.2k ⭐, Rust)* — [RivoLink/leaf](https://github.com/RivoLink/leaf)
      — ⛔ дублирует `glow`.
- [ ] **git-wt** — подкоманда `git worktree` без боли. *(563 ⭐, Go)* —
      [k1LoW/git-wt](https://github.com/k1LoW/git-wt)
      — ⛔ дублирует `wt` (worktrunk).
- [ ] **Netcatty**, **Voltius**, **RustConn**, **uniterm**, **navop**,
      **nyaterm**, **KKTerm**, **oxideterm**, **sshdesk** — SSH-клиенты и
      «рабочие пространства» с SFTP, RDP, VNC и вкладками (6.8k, 783, 632,
      906 ⭐ и т. д.) — ⛔ класс уже закрыт `assh` для конфигов, `sshx` для
      совместных сессий и `omnyssh` (TUI `omny` + GUI `OmnySSH`) для
      подключений из одного окна. Пересматривать не нужно.
- [ ] **rune** — GPU-ускоренный IDE-мультиплексор. *(1.3k ⭐,
      `rune-linux-amd64.tar.gz`, GPL-3.0)* —
      [unstablebuild/rune](https://github.com/unstablebuild/rune)
      — ⛔ дублирует `zellij` и редактор, которым пользуется владелец.
- [ ] **spotatui**, **gloomberb**, **bookokrat**, **late-sh**, **tuxedo**,
      **micasa** — Spotify-клиент, финансовый терминал, читалка EPUB,
      «клуб» по SSH, todo.txt и учёт домашних дел в терминале
      — ⛔ полезной нагрузки для DevOps-ноутбука нет; перечислены, чтобы
      не разбирать их повторно.
