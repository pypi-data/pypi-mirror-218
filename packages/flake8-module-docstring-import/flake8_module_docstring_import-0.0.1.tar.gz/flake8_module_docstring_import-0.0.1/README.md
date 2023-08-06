Very simple flake8 plugin to check if there is one new line between module docstring and imports at the top of the file.

## Installation:
```python
pip install flake8-module-docstring-import
```

## List of warnings
**MDL001**: There is no one new line between module docstring and imports at the top of the file.

## Examples
These examples will trigger problem:
```python
"Very important docstring"
import sys
```
```python
"Very important docstring"


import sys
```
This is correct:
```python
"Very important docstring"

import sys
```

