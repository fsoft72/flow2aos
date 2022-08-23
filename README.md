# Flow2AOS

## Introduction

Flow2AOS is a tool for converting [LiWE Flow](https://flow.liwe.org) diagrams into AOS definition files.

**NOTE**: this is in very early development and is not yet ready for use.

**NOTE2**: It does not yet support all features of AOS and it is very likely not to support all features of AOS in the future because LiWE Flow JSON file contains different features.


## How to use

Run the following command in the Flow2AOS folder:

```bash
./flow2aos.py <input_file> -o <output_file>
```

where `input_file` is the name of the LiWE Flow json file and `output_file` is the name of the output file.
You can omit the `-o` option to have the output directly printed to stdout.

```bash
./flow2aos.py flow.json
```

## Contributing

Contributions are more than welcome.

## License

Copyright (c) 2022, Fabio Rotondo. All rights reserved.
This software is licensed under the [MIT License](https://opensource.org/licenses/MIT).