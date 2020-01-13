# YYoinker
A tiny wrapper around youtube-dl that makes it easy to download a list of videos and/or playlists.  
Features in addition to youtube-dl:  
- Easier specification of the output directory
- Take input from STDIN or a batch file, with customizable separators
- Several default parameters for both video and audio downloads.

Example usage:  
`./yyoinker.py -o ~/Music/Lofi --batch-file=~/urls.txt`  
All you have to do is put a list of URLs into ~/urls.txt, and voila, all the audio files are downloaded.

Enter `./yyoinker.py -h` for detailed help.

### License: MIT
