# Domini

A small, simple package for generating HTML documents.
The syntax aims to immitate HTML as closely as possible for legibility and ease of use.

### Index

- [HTML](#html)
    - [Attributes](#attributes)
    - [Content](#content)
    - [Closing tags](#closing-tags)
    - [Event attributes](#event-attributes)
- [JavaScript](#javascript)
    - [JSON type hints](#json-type-hints)

## HTML

### Attributes

Attributes *without* a value are entered as *positional arguments*.<br>
Attributes *with* a value are entered as *keyword arguments*.

To specify attributes that collide with reserved Python keywords,
append an underscore and it will be removed.

#### Python

```py
from domini.html import dialog

dialog('open', class_='mydialog')
```

#### HTML

```html
<dialog open class='mydialog'>
```

### Content

To add children to an element, there are a few different methods you can use. The content can be either an iterable or a lone element. These elements can be either other tags or plain strings.

- `add` adds the children to the current object.
- `>` returns a shallow copy of the element with the children added.
- `>>` returns a deep copy of the element with the children added.

```py
ul(class_='todo')> (
    li()> 'Buy a fruit basket.',
    li()> (
        'Read ', a(href='https://wikipedia.org/')> 'Wikipedia',
        ' to learn more about things you may not have otherwise cared about.',
    ),
)
```

### Closing tags

A tag is only closed if content is provided. E.g. `<p></p>` as opposed to `<p>`. This can be an empty tuple.

```py
p()> ()
```

For open tags like `<br>` and `<hr>`, you simply do `br()` and `hr()`.

### Event attributes

Enumerators for event attributes are available at `domini.html.events`. You can either use `Event`, which contains all different event attributes in one, or use an enumerator for a specific category of events.

```py
from domini.html.events import (
    # These are the categories.
    WindowEvent, FormEvent, KeyboardEvent,
    MouseEvent, DragEvent, ClipboardEvent,
    MediaEvent, MiscEvent,
)
```

## JavaScript

### JSON type hints

Type hints for the types that are typically used to represent JSON data in Python.

```python
# Either of the following JSON types;
#   JSONBasic | JSONArray | JSONObject
from domini.js import JSON

# The basic, immutable types;
#   None | bool | int | float | str.
from domini.js import JSONBasic

# List and dictionary of JSON values
#   list[JSON] and dict[str, JSON]
from domini.js import JSONArray, JSONObject
```
