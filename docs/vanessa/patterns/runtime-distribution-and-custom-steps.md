---
id: vanessa:patterns:runtime-distribution-and-custom-steps
title: "Single, полная поставка и собственные шаги Vanessa"
description: "Выбор готового runtime, библиотеки и разработки собственных шагов; границы старых рецептов совместимости и сборки Single."
collection: "vanessa"
type: "pattern"
aliases: ["Vanessa Single или полная поставка", "собственный шаг Vanessa", "step definitions", "сборка MakeVASingle", "режим совместимости 8.2 Vanessa"]
tags: ["vanessa", "runtime-distribution-and-custom-steps", "Vanessa Single или полная поставка", "собственный шаг Vanessa", "step definitions"]
publish_publicly: false
source_urls: ["https://github.com/Pr-Mex/vanessa-automation/blob/develop/README.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/index.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/examples/README.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/NotAdd.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/Режим%20совместимости%208.2.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MakeVASingle/MakeVASingle.md", "https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/index.md"]
---

# Single, полная поставка и собственные шаги Vanessa

## Готовый runtime и исходники

Single предоставляет функциональность Vanessa в одной EPF со встроенной библиотекой и кешем шагов. Полная поставка удобна для разработки самой Vanessa и библиотек. Каталог исходников без сборки не равен готовой обработке. Для обычного использования документация предлагает готовую сборку; доступ к upstream при каждом написании теста не требуется.

Примеры из self-tests поставки могут требовать служебную конфигурацию и специальные данные. Их нельзя считать smoke-тестами произвольной пользовательской базы только потому, что это `.feature`.

## Когда нужен собственный шаг

Библиотечный шаг покрывает технологическое действие; [экспортный сценарий](subscenarios-and-libraries.md) собирает из действий повторяющийся процесс. Если доступные шаги не выражают нужное устойчивое поведение, может понадобиться собственная реализация шага. Его определение и регистрация принадлежат библиотеке шагов, а не продуктовой конфигурации по умолчанию. Текст описания шага, процедура реализации и загружаемая библиотека — разные сущности.

## Сборка Single

MakeVASingle документирует предварительную сборку артефактов через Compile.bat и отдельный вызов OneScript с исходниками, выходным каталогом, библиотеками, bin платформы и файловой базой для вычисления кеша. Выходной каталог очищается сборщиком и не должен находиться внутри исходников. Этот режим нужен при подготовке собственного runtime; он не является обязательным действием автора каждого UI-сценария.

## Совместимость относится к владельцу кода

Исторический FAQ для разработки Vanessa в режиме 8.2 перечисляет её функции-обёртки и ограничения методов языка. Это требование разработки самого фреймворка в указанном режиме, а не универсальная норма для всех конфигураций и feature-файлов. API платформы и API Vanessa имеют разных владельцев и источники проверки.

Связанные темы: [библиотеки](subscenarios-and-libraries.md), [контекст кода](embedded-code-and-context.md), [окружение](environment-readiness.md).

## Источники

[README](https://github.com/Pr-Mex/vanessa-automation/blob/develop/README.md); [index](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/index.md); [README](https://github.com/Pr-Mex/vanessa-automation/blob/develop/examples/README.md); [NotAdd](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/NotAdd.md); [Режим совместимости 8.2](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/Режим%20совместимости%208.2.md); [MakeVASingle](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/MakeVASingle/MakeVASingle.md); [index](https://github.com/Pr-Mex/vanessa-automation/blob/develop/docs/FAQ/index.md).
