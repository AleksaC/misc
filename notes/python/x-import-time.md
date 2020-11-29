# `PYTHONPROFILEIMPORTTIME`

Setting this environment variable to nonempty string makes python print how long
each import takes. The equivalent to setting this variable is adding `-X importtime`
flag when running the interpreter.

The output looks something like this:

```
import time: self [us] | cumulative | imported package
import time:       599 |        599 | _frozen_importlib_external
import time:       111 |        111 |   time
import time:       333 |        444 | zipimport
import time:        76 |         76 |     _codecs
import time:       621 |        696 |   codecs
import time:       569 |        569 |   encodings.aliases
import time:       797 |       2062 | encodings
import time:       305 |        305 | encodings.utf_8
import time:       273 |        273 | _signal
import time:       340 |        340 | encodings.latin_1
import time:        66 |         66 |     _abc
import time:       332 |        398 |   abc
import time:       395 |        793 | io
import time:        87 |         87 |       _stat
import time:       368 |        454 |     stat
import time:      1440 |       1440 |     _collections_abc
import time:       205 |        205 |       genericpath
import time:       380 |        585 |     posixpath
import time:       931 |       3408 |   os
import time:       267 |        267 |   _sitebuiltins
import time:       330 |        330 |   sitecustomize
import time:       122 |        122 |   usercustomize
import time:       700 |       4825 | site
```

The output above is part of normal python interpreter startup so it should be there
every time, maybe with minor differences on various python interpreters or if some
other flags are passed.

The import chains depend on the indentation, e.g. in the example above `time` is
imported by `zipimport`.

The self and cumulative columns tell how much the import took only counting the
module itself and including the imports from the module respectively.

This feature is available for `python >=3.7`.

When running with pytest `-s` flag needs to be added so that imports aren't swallowed
by pytest.

---

I learned about this feature on Anthony Sottile's [twitch stream](https://www.twitch.tv/anthonywritescode).
He also made [importtime-waterfall](https://github.com/asottile/importtime-waterfall)
which makes it easier to profile import times.
