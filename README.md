# PySeExt Module Repository

This project contains a package to aid the testing of ExtJS applications from Python using Selenium.

I have previously used JavaScript testing frameworks to test ExtJS code (such as the excellent [Siesta](https://www.bryntum.com/products/siesta/)), but understand that Python is more widely used by automated testers generally. The issue with it and testing ExtJS is the fact the finding components is challenging, and interacting with any of the data underneath nigh-on impossible.

I had the idea of trying to inject JavaScript into the DOM to help, and use that from the Python. After a quick proof of concept
that it was indeed possible, I started pulling this together.

---
## How to Use
It seems that GitHub does not allow publishing to PyPi yet, and it's not looking like it's coming [soon](https://github.community/t/pypi-compatible-github-package-registry/14615), since the roadmap looks empty.

You can direct pip at GitHub though. Simply run `pip install git+https://github.com/westy/pyseext`

Alternatively, add this to your `requirements.txt`:
```
pyseext @ git+https://github.com/westy/pyseext
```

And then run `pip install -r requirements.txt`

---
## Generated Documentation

You can find the generated documentation for the library [here](https://westy.github.io/pyseext/).

---
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
I have also settled on a standard of having a single class per source file (that I now understand are called modules), although inner classes are allowed.
This is pretty much standard practice in other languages, and makes source control and managing conflicts far easier.