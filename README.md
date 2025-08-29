# Accounting Tables and XBRL

Provides accounting and finance Tables and Taxonomies with transformations to: i) XBRL data storage, ii) HTML display.


# Test

```
source .venv/bin/activate
uv run pytest

```


# TODO

* ~~initial Table class~~
* apply and integrate arelle, but give manual examples in lxml
  - ~~validate: instance, taxonomy~~
  - ~~load: ...~~
  - display: ...
  - create: ...
  - add transaction: ...
  - ...
* test simple
  - general data: ...
  - usgaap: ...
  - t-acct tool: ...
  - sec: ...
* test advanced
  - ffiec call report
  - frb h8
  - sec json