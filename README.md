# regulations-stub

[eRegulations](http://cfpb.github.io/eRegulations) is a web-based tool that makes regulations easier to find, read and understand with features such as inline official interpretations, highlighted defined terms, and a revision comparison view.

eRegs is made up of three core components:

* [regulations-parser](https://github.com/cfpb/regulations-parser): Parse regulations
* [regulations-core](https://github.com/cfpb/regulations-core): Regulations API
* [regulations-site](https://github.com/cfpb/regulations-site): Display the regulations

This repository contains JSON that corrosponds to CFPB regulations that
have been parsed by [regulations-parser](https://github.com/cfpb/regulations-parser) 
and which can be loaded into [regulations-core](https://github.com/cfpb/regulations-core)
with the scripts included in this responsitory. This allows a working
eRegulations setup to be created without needing to run the parser. 

To get the rest of the eRegulations stack up and working, please see the 
[regulations-bootstrap](https://github.com/cfpb/regulations-bootstrap)
repository.


## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


