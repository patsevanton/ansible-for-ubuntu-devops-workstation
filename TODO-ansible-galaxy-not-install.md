# TODO-ansible-galaxy: коллекции и playbook'и Ansible — не ставим

Плейбук не устанавливает ничего из Ansible Galaxy: ни коллекций, ни ролей, ни
готовых playbook'ов — ни из списка ниже, ни любых других.

Не ставим, потому что это строительные блоки для чужих проектов, а не утилиты
для ноутбука: их место — в `requirements.yml` конкретного проекта с фиксацией
версий (`ansible-galaxy install -r requirements.yml`), а не в общем
`~/.ansible` на каждой машине.

Из Ansible плейбук ставит только `ansible-core`, `ansible-lint` и `molecule`
с `molecule-plugins[docker]`; коллекции, нужные молекуле, она доставит сама.

Проверенные коллекции, попавшие в отказ:

- [dev-sec/ansible-collection-hardening](https://github.com/dev-sec/ansible-collection-hardening)
  — готовый харденинг Linux/SSH/nginx (5.5k ⭐). Не ставим: это зависимость
  чужих плейбуков, а не утилита, и своих ролей, которым нужен готовый
  харденинг, в плейбуке нет. Пересматривать, если такие роли появятся.
