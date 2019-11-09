# Virtual com port changer

> Утилита для привязки отдельного типа устройств в системе к конкретному порту

## Содержание

- [Описание](#Описание)
- [Применимость](#Применимость)
- [Принцип работы](#Принцип работы)
- [Юзкейс](#Юзкейс)
- [Конфигурация](#features)
- [Пример файла конфигурации](#Пример файла конфигурации)


## Описание
Скрипт для привязки виртуального COM-порта устройтсв к конкретному номеру порта.
Решает проблему когда нужно установить определенные устройства на один порт.
Скрипт не предназначен для случаев когда два одинаковых устройства должны иметь разные порты.

## Применимость
1. Если у вас несколько рабочих станций, использующие одинаковый набор устройств,
но в каждом случае они имеют различающиеся номера портов.
2. Если у вас есть несколько идентичных устройств, подключаемых через USB порт, и использующие
протокол виртуального COM-порта для идентификации, обычно система по-умолчанию задает первый
COM-порт, который не был использован в системе ранее.

## Юзкейс
На предприятии используются терминалы сбора данных CipherLab 8001, есть несколько групп
ревизоров, каждая из которых имеет собственную подставку (IR-Cradle) для подключения к 1С.
Проблема в том что в настройках 1С выбирается одновременно только один порт.
С помощью утилиты можно присвоить вновь подключаемым подставкам конкретный порт.

## Принцип работы
Скрипт указывает принудительно порт для устройств из конфига, путем редактирования реестра по ветке\
```shell
\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USB\
```
**Чтобы настройка прошла успешно, необходимо чтобы устройство было хотя бы раз подключено к системе** (и о нем имелась запись в реестре). Порт проставляется для всех когда-либо подключенных устройств с одинаковым идентификатором.
**Нужны права администратора (изменение ветки SYSTEM реестра)**

## Конфигурация

По соседству со скриптом должен лежать port_config.ini (при отсутствии, будет создан при запуске), заполняется он по шаблону. Количество устройств не ограничено.

[Device 1]
device-id = VID_0123&PID_0123
port = COM5

[Device 2]
device-id = VID_2345&PID_2345
port = COM6

Где в [] произвольный текст по желанию (Порядковый номер, название, и т.д.)
device-id - идентификатор устройства, можно посмотреть в диспетчере задач - Свойства - Сведения, и выбрать свойство ИД оборудования
port - номер COM порта к которому будет привязано устройство (COM обязательно писать на латинице)

В файле допускаются комментарии, если строка начинается с #

##Пример файла конфигурации

### port_config.ini
```shell
[Device 1]
device-id = VID_0123&PID_0123
port = COM5

[Device 2]
device-id = VID_2345&PID_2345
port = COM6
```
