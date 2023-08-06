<!--- This is a markdown file.  Comments look like this --->
<table>
  <tr>
    <td colspan=2><strong>
    shimport
      </strong>&nbsp;&nbsp;&nbsp;&nbsp;
      <small><small>
      </small></small>
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/icon.png style="width:150px"></td>
    <td>
    Import utilities for python
    </td>
  </tr>
</table>

  * [Overview](#overview)
  * [Installation](#installation)
  * [Usage](#usage)


---------------------------------------------------------------------------------
## Overview

Import utilities for python 

---------------------------------------------------------------------------------

## Installation

See [pypi](https://pypi.org/project/shimport/) for available releases.

```
pip install shimport
```

---------------------------------------------------------------------------------

## Usage

```

# Simple lazy modules
import shimport 
pathlib = shimport.lazy('pathlib')
print(pathlib.Path('.').absolute())

# Filtering module contents
....

# Automatically importing submodules
....

```

---------------------------------------------------------------------------------
