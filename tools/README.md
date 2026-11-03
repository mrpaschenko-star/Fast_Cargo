# Воспроизведение артефактов Sprint 8

## Диаграммы

Нужны установленная Java и PlantUML JAR. Скрипт не скачивает библиотеки; C4-PlantUML v2.12.0 лежит в `vendor/C4-PlantUML`, используется Smetana без Graphviz.

```sh
python3 Fast_Cargo/tools/render_diagrams.py --java /path/to/java --jar /path/to/plantuml.jar
```

Сначала выполняется синтаксическая проверка, затем создаются три PNG рядом с `.puml`. Для просмотра готовых PNG Java не нужна.

## Три страницы плана

```sh
python3 Fast_Cargo/tools/render_plan.py
```

Зависимости Python: `reportlab`, `pypdf`, `pypdfium2`, `Pillow`. По умолчанию шрифты Arial из macOS; на другой системе передайте `--font /path/regular.ttf --bold-font /path/bold.ttf` с поддержкой кириллицы.

Скрипт читает весь `Task1/transformation-plan.md`, учитывает два явных разделителя страниц, создаёт временный A4 PDF, проверяет ровно три страницы и расположение разделов 1/5/7. Затем выводит PNG в `Task1/preview` и удаляет временный PDF. Печатная версия использует основной кегль 10.5 pt и таблицу 9.2 pt; не сокращает содержимое Markdown. Произвольный редактор может печатать Markdown иначе — эталонные страницы находятся в `preview`.

## Проверка

```sh
python3 Fast_Cargo/tools/validate.py
```
