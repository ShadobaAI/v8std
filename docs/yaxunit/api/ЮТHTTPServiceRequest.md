---
title: API ЮТHTTPServiceRequest
description: "Публичные экспортные методы модуля ЮТHTTPServiceRequest из ядра YaXUnit."
tags: [yaxunit, api, ЮТHTTPServiceRequest]
publish_publicly: false
---

# API ЮТHTTPServiceRequest

Компактный справочник по 12 экспортным методам. Сигнатуры получены из ядра YaXUnit ревизии `23fd2db738dbb26b7b43bdcf0c35fd2c263a3899`.

## ЮТHTTPServiceRequest.GetBodyAsBinaryData

`Function ЮТHTTPServiceRequest.GetBodyAsBinaryData() Export`

Возвращает тело HTTP-запроса в виде двоичных данных.
Преобразует тело запроса, если оно было установлено как строка.
Если тело не установлено, возвращает пустые двоичные данные.

**Возвращает:**
- `ДвоичныеДанные` — Тело запроса в виде двоичных данных.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:55`.

## ЮТHTTPServiceRequest.GetBodyAsStream

`Function ЮТHTTPServiceRequest.GetBodyAsStream() Export`

Возвращает тело HTTP-запроса как поток для чтения.
Удобно использовать для работы с большими объемами данных.

**Возвращает:**
- `Поток` — Тело запроса, представленное в виде потока.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:84`.

## ЮТHTTPServiceRequest.GetBodyAsString

`Function ЮТHTTPServiceRequest.GetBodyAsString(Encoding = Undefined) Export`

Возвращает тело HTTP-запроса как строку.
Позволяет указать кодировку для корректного преобразования двоичных данных в строку.
Если тело изначально было строкой, возвращает его без изменений.
Если тело не установлено, возвращает пустую строку.

**Параметры:**
- `Encoding` — КодировкаТекста, Строка, Неопределено — Кодировка для преобразования тела в строку. Можно указать объект КодировкаТекста (например, КодировкаТекста.UTF8) или имя кодировки строкой (например, "UTF-8"). Если Неопределено, используется кодировка по умолчанию (UTF-8).

**Возвращает:**
- `Строка` — Тело запроса в виде строки.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:111`.

## ЮТHTTPServiceRequest.УстановитьТелоКакДвоичныеДанные

`Function ЮТHTTPServiceRequest.УстановитьТелоКакДвоичныеДанные(Data) Export`

Устанавливает тело HTTP-запроса из двоичных данных.
Если тело запроса было ранее установлено в другом формате (например, строка), оно будет заменено.

**Параметры:**
- `Data` — ДвоичныеДанные — Двоичные данные, которые будут установлены как тело запроса.

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:139`.

## ЮТHTTPServiceRequest.УстановитьТелоКакСтроку

`Function ЮТHTTPServiceRequest.УстановитьТелоКакСтроку(String) Export`

Устанавливает тело HTTP-запроса из строки.
Если тело запроса было ранее установлено в другом формате (например, двоичные данные), оно будет заменено.

**Параметры:**
- `String` — Строка — Строковое представление тела запроса.

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:159`.

## ЮТHTTPServiceRequest.УстановитьТелоКакСтрокуJSON

`Function ЮТHTTPServiceRequest.УстановитьТелоКакСтрокуJSON(Data) Export`

Устанавливает тело HTTP-запроса как строку JSON, сериализуя переданные данные.
Сериализует предоставленные данные (например, Структура, Массив, Соответствие) в формат JSON
и устанавливает результат как тело запроса. Если тело было установлено ранее, оно заменяется.
Рекомендуется также установить заголовок "Content-Type" в "application/json".

**Параметры:**
- `Data` — Произвольный — Данные для сериализации в JSON (например, Структура, Массив, Соответствие).

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:183`.

## ЮТHTTPServiceRequest.ДобавитьЗаголовок

`Function ЮТHTTPServiceRequest.ДобавитьЗаголовок(HeaderName, Value) Export`

Добавляет HTTP-заголовок к запросу.
Если заголовок с указанным именем уже существует, его значение будет перезаписано новым.

**Параметры:**
- `HeaderName` — Строка — Имя HTTP-заголовка (например, "Content-Type", "Authorization", "Accept").
- `Value` — Строка — Значение HTTP-заголовка.

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:210`.

## ЮТHTTPServiceRequest.ДобавитьПараметрЗапроса

`Function ЮТHTTPServiceRequest.ДобавитьПараметрЗапроса(ParameterName, Value) Export`

Добавляет параметр в строку запроса (query string).
Параметры URL (query parameters) добавляются к URL после символа "?" и разделяются символом "&".
Например, для URL "http://example.com/api/items" добавление параметра "filter" со значением "active"
сформирует URL "http://example.com/api/items?filter=active".

**Параметры:**
- `ParameterName` — Строка — Имя параметра строки запроса (например, "filter", "limit", "page").
- `Value` — Строка — Значение параметра строки запроса.

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:236`.

## ЮТHTTPServiceRequest.ДобавитьПараметрURL

`Function ЮТHTTPServiceRequest.ДобавитьПараметрURL(ParameterName, Value) Export`

Добавляет параметр для подстановки в путь URL (path parameter).
Используется для формирования URL с динамическими сегментами пути.
Имена параметров должны соответствовать плейсхолдерам, указанным в ОтносительныйURL
(например, если ОтносительныйURL = "/users/{userId}/posts/{postId}", то имена параметров
должны быть "userId" и "postId" без фигурных скобок).

**Параметры:**
- `ParameterName` — Строка — Имя параметра пути (должно совпадать с плейсхолдером в ОтносительныйURL, без фигурных скобок).
- `Value` — Строка — Значение параметра пути для подстановки в URL.

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:264`.

## ЮТHTTPServiceRequest.Метод

`Function ЮТHTTPServiceRequest.Метод(Value) Export`

Устанавливает HTTP-метод для запроса.
Определяет тип выполняемого запроса (например, GET для получения данных, POST для создания, PUT для обновления).

**Параметры:**
- `Value` — Строка — Имя HTTP-метода (например, "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS").

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:284`.

## ЮТHTTPServiceRequest.БазовыйURL

`Function ЮТHTTPServiceRequest.БазовыйURL(Value) Export`

Устанавливает базовый URL для HTTP-запроса.
Базовый URL представляет собой основную часть адреса (схема, хост, порт, начальный путь),
к которой будет добавляться относительный URL (заданный через ОтносительныйURL())
и параметры запроса (заданные через ДобавитьПараметрЗапроса()).

**Параметры:**
- `Value` — Строка — Базовый URL (например, "http://localhost:8080/api", "https://services.example.com/v1"). Не должен заканчиваться на "/".

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:307`.

## ЮТHTTPServiceRequest.ОтносительныйURL

`Function ЮТHTTPServiceRequest.ОтносительныйURL(Value) Export`

Устанавливает относительный URL (путь) для HTTP-запроса.
Этот путь будет добавлен к базовому URL, установленному через БазовыйURL().
Относительный URL может содержать плейсхолдеры для параметров пути (например, "/resource/{id}"),
значения для которых задаются с помощью ДобавитьПараметрURL().

**Параметры:**
- `Value` — Строка — Относительный URL (например, "/users", "/items/{itemId}/details"). Должен начинаться с "/".

**Возвращает:**
- DataProcessors.ЮТHTTPServiceRequest - Текущий объект запроса для возможности цепочки вызовов.

Источник ядра: `exts/yaxunit/src/DataProcessors/ЮТHTTPServiceRequest/ObjectModule.bsl:331`.
