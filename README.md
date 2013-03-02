Scripts and Parsers
===================

Initially set up to track one small project of taking a JSON feed of addresses and allow for some DNS-based outputs, this repo was only tracking one script, which seemed inefficient when I hit my second similar need.  I don't want my public github set up with a thousand individual repos for tracking simple scripts, especially if I ever start to find needs to reuse elements of one of these in another.

now for the projects:

dnsjsonparser
-------------

Parse JSON data list for dns testing.  The structure can be seen in the example file feed_structure.json  this project was built to allow parsing of the json data into a list of addresses that can then be queried individually via dns.  Future revisions may add in connecting via http in order to determine if the page shows normally or is blocked by some higher network level security tool.

version
-------

This script reads a version number from a file called KVersion and creates a version of the command-line supplied file 'x.in' that subsitutes the version number in all appropriate locations.  This was built to allow CI-built artifacts to match the legacy build system artifacts at my office.  Future versions will make it more flexible & robust, as well as change the structure to a cleaner class based system.
