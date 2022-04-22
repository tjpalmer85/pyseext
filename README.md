# PySeExt Module Repository

This project contains a package to aid the testing of ExtJS applications from Python using Selenium.

## Documentation

You can find the documentation for the library [here](./docs/pyseext/index.html).

## Naming Standards

This is the first time I have written any Python, so I have looked around for standards that seem to be common.
I have settled on those listed [here](https://namingconvention.org/python/).

### TL;DR
**Type** | **Public** | **Internal**
--- | --- | ---
Packages | `lower_with_under` |
Modules | `lower_with_under` | `_lower_with_under`
Classes | `CapWords` | `_CapWords`
Exceptions | `CapWords` |
Functions | `lower_with_under()` | `_lower_with_under()`
Global/Class Constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER`
Global/Class Variables | `lower_with_under` | `_lower_with_under`
Instance Variables | `lower_with_under` | `_lower_with_under`
Method Names | `lower_with_under()` | `_lower_with_under()`
Function/Method Parameters | `lower_with_under` |
Local Variables | `lower_with_under` |

### Additional Notes
I have also settled on a standard of having a single class per source file, although inner classes are allowed.
This is pretty much standard practice in other languages, and makes source control and managing conflicts far easier.