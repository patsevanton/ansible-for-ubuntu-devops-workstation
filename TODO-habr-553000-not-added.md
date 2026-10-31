# TODO: утилиты из статьи Habr «Полезные консольные Linux утилиты», которых нет в плейбуке

Живые кандидаты из статьи
[«Полезные консольные Linux утилиты»](https://habr.com/ru/articles/553000/)
(Habr, 18.04.2021). Здесь только то, чего нет в плейбуке и что ещё живо.

Дедупликация: каждый кандидат описан ровно в одном трекере, как принято в
[`TODO.md`](TODO.md). Уже поставленные утилиты из статьи в этом файле не
перечислены; заброшенные — в [`TODO-abandoned.md`](TODO-abandoned.md), без
linux-бинарника — в
[`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md), сознательные отказы
(включая «только скрипт») — в [`not-install.md`](not-install.md), сервисы не для
ноутбука — в [`TODO-server-apps.md`](TODO-server-apps.md).

Способ установки сверен 2026-10-24: пакеты — `apt-cache policy` на Ubuntu,
релизы — последний GitHub-релиз (`gh api .../releases/latest`). Наличие пакета в
Ubuntu не значит, что плейбук его ставит — это отдельное решение. Перед
добавлением проверять актуальность релизных ассетов, как в
[`TODO-no-prebuilt-binary.md`](TODO-no-prebuilt-binary.md).

---

## Сеть, DNS, туннели

| Утилита | Что это | Как ставится и что проверить |
| --- | --- | --- |
| [pingtop](https://github.com/laixintao/pingtop) | TUI, пингует несколько хостов одновременно | PyPI → роль `pipx_apps`, релизов на GitHub нет |
| [frp](https://github.com/fatedier/frp) | обратный прокси: доступ к локальному серверу за NAT | GitHub: `frp_*_linux_amd64.tar.gz` |

## SSH и удалённые сессии

| Утилита | Что это | Как ставится и что проверить |
| --- | --- | --- |
| [tmate](https://tmate.io/) | мгновенный доступ к терминалу через tmux-сервер | пакет Ubuntu `tmate` (2.4.0) |

## HTTP, JSON и анализ логов

| Утилита | Что это | Как ставится и что проверить |
| --- | --- | --- |
| [rebound](https://github.com/shobrook/rebound) | при исключении сразу ищет вопрос на Stack Overflow | пакет Ubuntu `rebound` (тот же проект, 2.0.0) |
| [jql](https://github.com/cube2222/jql) | альтернатива jq с более простым синтаксисом | GitHub: `jql_*_linux_amd64.tar.gz` |
| [topngx](https://github.com/gsquire/topngx) | `top` по access-логам nginx (замена ngxtop) | GitHub: `topngx-*_x86_64-unknown-linux-musl.tar.gz` |

## Система, файлы, диагностика

| Утилита | Что это | Как ставится и что проверить |
| --- | --- | --- |
| [watchman](https://github.com/facebook/watchman) | следит за файлами и триггерит действия при изменениях | пакет Ubuntu `watchman` (4.9.0) |
| [tlog](https://github.com/Scribery/tlog) | запись и воспроизведение терминальных сессий | пакет Ubuntu `tlog` (14) |
| [whatfiles](https://github.com/spieglt/whatfiles) | какие файлы открыл процесс (упрощённый strace) | GitHub: `whatfiles-v*_linux-x86_64` |
| [sysdig](https://github.com/draios/sysdig) | трассировка системных вызовов с фильтрами | пакет Ubuntu `sysdig` (0.40) |
| [hstr](https://github.com/dvorka/hstr) | TUI-поиск по истории команд | пакет Ubuntu `hstr` (3.1) |
| [pastebinit](https://github.com/pastebinit/pastebinit) | отправка текста на pastebin из CLI | пакет Ubuntu `pastebinit` (1.8) |

## Безопасность и TLS

| Утилита | Что это | Как ставится и что проверить |
| --- | --- | --- |
| [ssl-cert-check](https://github.com/Matty9191/ssl-cert-check) | проверка срока действия сертификатов + письмо | пакет Ubuntu `ssl-cert-check` (4.14) |

## Разработка, shell, шпаргалки

| Утилита | Что это | Как ставится и что проверить |
| --- | --- | --- |
| [clog-cli](https://github.com/clog-tool/clog-cli) | CHANGELOG из истории git-коммитов | GitHub: `clog-*_x86_64-unknown-linux-gnu.tar.gz` |
| [cheat.sh](https://github.com/chubin/cheat.sh) | шпаргалки по командам из терминала | пакет Ubuntu `cht.sh` или установочный скрипт с cheat.sh |
