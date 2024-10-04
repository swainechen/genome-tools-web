# genome-tools-web
Web interface for genome-tools project.

This was originally written in 2002 for a typical LAMP stack. I always used Debian / Ubuntu with Apache.

## Installation
To install this:
* Set things up so the `html` directory is getting served by your web server. You want `index.shtml` to come up, which means you need scripting turned on.
* The files in `cgi-bin` need to be available to your webserver (on Debian / Ubuntu with the default Apache, this was in `/usr/lib/cgi-bin`). The `web.conf` file should be edited, and this should typically just be in the same directory as the other cgi files.
* You need `logs` and `tmp` directories under the `html` directory, and these need write access for the web server (and read access for `tmp`, which is where results are served from)

I used to maintain a "standard" org-map, and the `org-map.directories` was used to help download all the files from NCBI. Then I would generate `org-map.standard`, and this could be used as the org-map for the genome-tools project (https://github.com/swainechen/genome-tools).

## Disclaimer
All this is provided as-is. I make no warranties, claims, or guarantees about this software.

Currently I don't have a server that I can ensure will be running this any longer, but genomics has moved on a lot, making this original project somewhat obsolete. This web interface was still useful, however, for helping out folks in the lab who needed to do some simple tasks with genome sequences for individual strains.
