# SendMailAuto

Этот проект представляет собой скрипт на Python, который использует библиотеку Selenium для автоматизированной отправки писем через веб-интерфейс e.mail.ru. Сценарий написан с использованием модуля unittest для тестирования и логирования.

## Установка зависимостей
Прежде чем запустить скрипт, убедитесь, что у вас установлены необходимые зависимости. Вы можете установить их, выполнив следующую команду:

  ```bash
  pip install -r requirements.txt
  ```

## Подготовка к запуску
Создайте файл .env в корне проекта и укажите в нем необходимые переменные окружения:

  ```bash
  PROFILE_PATH=/путь/к/профилю/firefox
  SCREEN_LINK_PATH=/путь/к/скриншотам
  ```

## Запуск скрипта
Выполните скрипт, используя следующую команду:

  ```bash
  python main.py
  ```

## Логирование
Логирование ведется с использованием библиотеки logging. Логи записываются в консоль и могут быть регулированы изменением уровня логирования в коде.

## Примечание
Убедитесь, что у вас установлен браузер Firefox, так как скрипт использует его для взаимодействия с веб-интерфейсом. Так же перед использованием этого скрипта ознакомьтесь с условиями использования веб-сайта e.mail.ru, чтобы удостовериться, что его использование не нарушает правила этого сайта.
