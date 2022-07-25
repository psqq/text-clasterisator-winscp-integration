# Кластеризатор сообщений журнальных файлов
Приложение предназначено для разбиения сообщений журнальных файлов (текстовых логов) на группы (кластеры) для удобства дальнейшего анализа.  
Приложение выполнено в виде интеграции к [WinSCP](https://winscp.net/eng/index.php) и интегрируется как пользовательский текстовый редактор.  
Для кластеризации используется алгоритм [BIRCH](https://scikit-learn.org/stable/modules/clustering.html#birch), который не требует предварительного указания количества кластеров и предназначен для кластеризации датасетов больших размеров.  
Приложение написано и тестировалось в ОС Windows10 (для определения пути к текстовому редактору по умолчанию и пути к папке с временными файлами используется реестр Windows)
## Порядок установки
1. Установить [Python](https://www.python.org/downloads/) (приложение разрабатывалось и тестировалось в версии Python 3.10). Затем убедиться, что все необходимые пути прописались в переменную PATH и python запускается из консоли без указания полного пути:
```
python -V
```
2. Установить необходимые модули для python:
```
pip install sklearn
pip install pandas
pip install numpy
pip install matplotlib
pip install cdbw
pip install nltk
```
3. Создать локальную папку и клонировать в нее данный репозиторий:
```
md "C:\borodin_admin\Институт\_ВКР\2022-06-14 Приложение\test-install"
cd "C:\borodin_admin\Институт\_ВКР\2022-06-14 Приложение\test-install"
git clone git@github.com:alborodin85/text-clasterisator-winscp-integration.git ./
```
3. В WinSCP в разделе "Настройки"-"Редакторы" нажать "Добавить" и добавить "Внешний редактор" (конструкцию в конце `!.!` также требуется указывать):
```
pythonw "C:\borodin_admin\Институт\_ВКР\2022-06-14 Приложение\test-install\clasterizator.py" !.!
```
4. Подключиться к серверу, выбрать нужный лог-файл, нажать правую кнопку мыши (ПКМ). В меню ПКМ навести мышь на "Править" и в выпадающем списке выбрать "Pythonw". Если "Внешний редактор" в настройках редактора поднят в самый верх, то приложение будет открываться просто по двойному щелчку по требуемому файлу.

## Начало работы и настройки приложения
### Настройки текстового редактора
При первых запусках приложения необходимо выбрать текстовый редактор путем указания полного пути к нему.
Пока редактор не указан, приложение использует редактор по умолчанию, путь к которому определяет из реестра Windows.  
Полный путь к требуемому редактору необходимо указать в поле "Путь к текст. редактору" и нажать "Проверить и сохранить".  
При этом откроется выбранный редактор с пустым файлом и в папке приложения (в нашем случае `C:\borodin_admin\Институт\_ВКР\2022-06-14 Приложение\test-install`) создастся файл `settings-text-editor.json` в котором сохранится указанный путь. Открывшийся редактор нужно просто закрыть.  
В случае если путь указан некорректно, приложение выведет ошибку и некорректный путь не сохранится, но в рамках текущей сессии будет использоваться именно этот введенный путь, даже если он некорректный, при этом при попытке использовать редактор приложение будет выводить ошибку.  
В дальнейшем путь к редактору можно указывать либо через поле в форме приложения, либо напрямую редактировать файл `settings-text-editor.json`, но при прямом редактировании файла возможны ошибки.  
Файл `settings-text-editor.json` можно удалять. При этом будет снова использоваться редактор Windows по умолчанию, информация о котором берется из реестра.
### Настройки регулярных выражений для определения начала сообщений
Так как сообщения журнальных файлов могут состоять из нескольких строк, приложение разбивает журнальный файл на сообщения с помощью регулярных выражений.  
Регулярное выражение, по которому определяется начало сообщения лога, необходимо указать в поле "RegExp для начала сообщения".  
Если это поле оставить пустым, то кнопки "Кластеризовать" и "Открыть кластер в редакторе" не будут производить никаких действий.  
Если это поле указать некорректным, то возможно поведение приложения, которое сложно предсказать.  
Копирование-вставка в поле "RegExp для начала сообщения" выполняется с помощью клавиш "Ctrl+Insert"/"Shift+Insert" (это стандартное поведение виджетов используемой библиотеки Python для форм Windows)
Примеры регулярных выражений для некоторых видов сообщений:
```
Сообщение: 2022-05-03 18:07:54 0 [Note] InnoDB: Compressed tables use zlib 1.2.11
RegExp: \d{4}-\d{2}-\d{2} {2}\d{2}:\d{2}:\d{2}

Сообщение: 20220724 13:22:13,it5-prod,dver29spb.ru_prod,localhost,80930,81274690,QUERY,dver29spb.ru_prod,'SELECT field_data_field_door_model.delta AS delta, field_data_field_door_model.field_door_model_value AS field_door_model_value\nFROM \nfield_data_field_door_model field_data_field_door_model\nWHERE  (entity_id = \'697\') AND (entity_type = \'node\')',0
RegExp: \d{6} \d{2}:\d{2}:\d{2}

Сообщение: [2022-07-23 02:05:02] local.ERROR: Facade\Ignition\Solutions\MakeViewVariableOptionalSolution::isSafePath(): Argument #1 ($path) must be of type string, null given, called in /var/www/vendor/facade/ignition/src/Solutions/MakeViewVariableOptionalSolution.php on line 88 {"exception":"[object] (TypeError(code: 0): Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution::isSafePath(): Argument #1 ($path) must be of type string, null given, called in /var/www/vendor/facade/ignition/src/Solutions/MakeViewVariableOptionalSolution.php on line 88 at /var/www/vendor/facade/ignition/src/Solutions/MakeViewVariableOptionalSolution.php:74)
RegExp: \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]
```
Введенные регулярные выражения после нажатия кнопки "Кластеризовать" сохраняются приложением в файле `settings.json` в папке приложения (в данном случае в `C:\borodin_admin\Институт\_ВКР\2022-06-14 Приложение\test-install`).
Привязка регулярного выражения к конкретному журнальному файлу осуществляется по пути к этому журнальному файлу в файловой системе удаленного сервера.  
Файл `settings.json` можно редактировать в ручную, при этом имя файла можно задавать с применением регулярных выражений. Это позволяет применять одно и то же выражение для лог-файлов, которые записываются, например с указанием даты в имени файла.  
Теоретически регулярные выражения в путях в файле `settings.json` можно указывать и для папок, но этот функционал не тестировался.  
Например, для файлов вида:
```
/opt/web/storage/logs/fpm-fcgi-laravel-2022-07-21.log
/opt/web/storage/logs/fpm-fcgi-laravel-2022-07-23.log
/opt/web/storage/logs/fpm-fcgi-laravel-2022-07-24.log
....
```
Путь в файле `settings.json` можно указать в следующем виде:
```
"path": "/opt/web/storage/logs/fpm-fcgi-laravel-\\d{4}-\\d{2}-\\d{2}.log",
```
А для файлов вида:
```
/var/log/mysql/server_audit.log.1
/var/log/mysql/server_audit.log.2
/var/log/mysql/server_audit.log.3
...
```
Путь в файле `settings.json` будет следующим:
```
"path": "/var/log/mysql/server_audit.log.\\d{1,2}",
```
Повторимся, что, чтобы увидеть сам файл `settings.json` и его полную структуру необходимо кластеризовать хотя бы один журнальный файл: `settings.json` создается после нажатия кнопки "Кластеризовать".  
Файл `settings.json` можно удалять, но при этом удалятся все привязки путей журнальных файлов к регулярным выражениям.
## Использование приложения
- Для проведения кластеризации необходимо выбрать в WinSCP требуемый журнальный файл на удаленном сервере.  
- С помощью меню правой кнопки мыши открыть этот файл в настроенном ранее внешнем редакторе ("Править" - "Pythonw"). Откроется форма приложения.  
- С помощью кнопки "Открыть весь лог в редакторе" можно открыть весь лог в текстовом редакторе. Это может быть удобным, когда для данного файла не настроен "RegExp для начала сообщения".  
- Если не указан "RegExp для начала сообщения" - указать его.
- Нажать кнопку "Кластеризовать". При этом запустится процесс обработки текста и кластеризации. Количество кластеров алгоритм BIRCH определяет автоматически.
- После окончания кластеризации в левом блоке "Кластеры" будут перечислены найденные кластеры. Количество найденных кластеров указано в скобках в названии блока.
- В списке кластеров для каждого кластера в начале в скобках указано количество сообщений, определенных для данного кластера и перечень ключевых слов, по которым приложение отнесло эти сообщения к данному кластеру.
- При выборе какого-либо кластера в списке заполняется правый список с сообщениями, отнесенными к данному кластеру.
- С помощью кнопки "Открыть кластер в редакторе" можно открыть сообщения кластера в выбранном ранее текстовом редакторе.
- При выборе какого либо сообщения в списке сообщений это сообщение открывается в нижнем правом блоке детального вывода сообщения с соблюдением переносов строк и пробелов.
- Для работы с другим журнальным файлом необходимо закрыть форму приложения и повторить операции с требуемым файлом.
