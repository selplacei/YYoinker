#!/usr/bin/python3
# SPDX-License-Identifier: MIT
import sys
import os
import subprocess
import pathlib
import argparse

argparser = argparse.ArgumentParser(
	prog='yyoinker',
	description='Download videos and playlists from YouTube into separate audio files using youtube-dl.',
	epilog='The remaining parameters will be passed to youtube_dl.'
)
argparser.add_argument('-o', metavar='DIRECTORY', default='.', help='Directory to download the files to')
argparser.add_argument('--batch-file', metavar='FILE', default='-',
						help='File to read URLs from. "-" (STDIN) by default.')
argparser.add_argument('--sep', metavar='SEPARATOR', default='\n',
						help='URL separator in the input file (newline by default).')
argparser.add_argument('--video', action='store_true', help='Keep the video; don\'t convert to audio.')

args, ytdl_args = argparser.parse_known_args()
urls = []
if args.batch_file == '-':
	urls += sys.stdin.read().split(args.sep)
else:
	with open(args.batch_file) as l:
		urls += l.read().split(args.sep)
urls = set(urls)

out_path = pathlib.Path(args.o)
if out_path.exists() and not out_path.is_dir():
	raise Exception(f'Output path {str(out_path)} is not a directory.')
if not out_path.exists():
	out_path.mkdir(parents=True)

if args.video:
	ytdl_args = [
		'youtube-dl',
		'--ignore-errors',
		'--geo-bypass',
		'--add-metadata',
		'-o', f'{out_path.resolve()}/%(title)s.%(ext)s',
		'--download-archive', f'{out_path.resolve()}/archive.txt'
	] + ytdl_args
else:
	ytdl_args = [
		'youtube-dl',
		'--ignore-errors',
		'--geo-bypass',
		'--extract-audio',
		'--audio-format', 'best',
		'--audio-quality', '0',
		'--add-metadata',
		'-o', f'{out_path.resolve()}/%(title)s.%(ext)s',
		'--download-archive', f'{out_path.resolve()}/archive.txt',
		'--metadata-from-title', '%(artist)s - %(track)s'
	] + ytdl_args

for url in urls:
	try:
		subprocess.run(ytdl_args + [f'{url}'], stderr=sys.stderr, stdout=sys.stdout, cwd=os.getcwd())
	except subprocess.CalledProcessError as e:
		print(f'\u001b[31mFailed to download \u001b[39m{url}\u001b[31m: error code {e.returncode}\u001b[0m')
