# Источники и границы интерпретации

## Исходное задание

Изображение исходной архитектуры — [as-is.png](as-is.png). 

Примеры UUID-«обезличивания», подсчёта доступности по всем 2xx/3xx и безусловной окупаемости не приняты как доказанные технические утверждения. В решении уточнены идентифицируемость данных, бизнес-семантика успешного ответа и условия подтверждения ROI.

## Технические источники

Обосновывают возможности технологий, но не подтверждают состояние инфраструктуры Fast Cargo.

| Источник | Использование |
|---|---|
| [PostgreSQL 16 — Logical Decoding Concepts](https://www.postgresql.org/docs/16/logicaldecoding-explanation.html) | Логическое декодирование на hot standby, feedback/physical slot, возможность повторов и риск удержания ресурсов. Настройка оценивается на конкретной версии |
| [Debezium — PostgreSQL connector](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) | Snapshot/права/publication, особенности PG16/17 и восстановления. Не является доказательством совместимости произвольного initial snapshot с read-only standby |
| [PCI SSC FAQ 1438](https://www.pcisecuritystandards.org/faqs/1438/) | Требования к принадлежности элементов iframe поставщику платежей; размещение карточных полей Fast Cargo не допускается |
| [PCI SSC FAQ 1439](https://www.pcisecuritystandards.org/faqs/1439/) | Аутсорсинг платежа не исключает сайт/redirect-инфраструктуру из всей области контроля. Точный scope и применимый SAQ подтверждаются отдельно |
| [C4-PlantUML v2.12.0](https://github.com/plantuml-stdlib/C4-PlantUML/tree/v2.12.0) | Нотация Container; локальная копия с [лицензией](../vendor/C4-PlantUML/LICENSE), без сетевых include |

## Трассировка задания

| Пункт документа | Где выполнен |
|---|---|
| Task1, пункты 1–7 | [transformation-plan.md](../Task1/transformation-plan.md), проверенные три страницы в `Task1/preview` |
| Task2, расширенная матрица | [stakeholder-matrix.md](../Task2/stakeholder-matrix.md) |
| Task2, три заданных возражения | [objections.md](../Task2/objections.md) |
| Task3, панель эксплуатации | [operational-kpi.md](../Task3/operational-kpi.md) |
| Task3, performance argument | [ceo-conclusion.md](../Task3/ceo-conclusion.md) |

Требования 152-ФЗ/ГОСТ приведены из задания; юридическое заключение и аттестация не проводились. Неизвестные бюджет, версия БД, параметры банка/EDI и состав команды отмечены как решения до внедрения. Для схем не использовались секреты или production-данные.
