#!/usr/bin/python3
'''
A script that converts Markdown to HTML
'''
import sys
import os
import re
import hashlib

def remove_character(string, char):
    return string.replace(char, '')

if __name__ == '__main__':

    # Test that the number of arguments passed is 2
    if len(sys.argv[1:]) != 2:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        sys.exit(1)

    # Store the arguments into variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Checks that the markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    with open(input_file, encoding='utf-8') as file_1:
        html_content = []
        md_content = [line[:-1] for line in file_1.readlines()]
        in_list = False  # Flag to track if currently inside a list
        in_paragraph = False  # Flag to track if currently inside a paragraph

        for line in md_content:
            heading = re.split(r'#{1,6} ', line)
            if len(heading) > 1:
                # Compute the number of the # present to
                # determine heading level
                h_level = len(line[:line.find(heading[1])-1])
                # Append the html equivalent of the heading
                html_content.append(
                    f'<h{h_level}>{heading[1]}</h{h_level}>\n'
                )
                in_list = False  # Reset list flag when a heading is encountered
                in_paragraph = False  # Reset paragraph flag when a heading is encountered
            elif line.startswith('- '):
                # Start of an unordered list
                if not in_list:
                    html_content.append('<ul>\n')
                    in_list = True
                    in_paragraph = False  # Reset paragraph flag when a list starts
                # Remove the '-' and space, and wrap the line in <li> tags
                line = line[2:]
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # Replace ** with <b> tags
                html_content.append(f'<li>{line}</li>\n')
            else:
                # Regular text line
                if not in_paragraph:
                    html_content.append('<p>\n')
                    in_paragraph = True
                    # Indent the line with 4 spaces
                    html_content.append(f'    {line}\n')
                else:
                    # Indent the line with 8 spaces
                    html_content.append(f'        {line}\n')
                # Replace ** with <b> tags
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                # Replace __ with <em> tags
                line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)
                # Replace [[text]] with MD5 hash (lowercase) of text
                line = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), line)
                # Remove ((text)) with 'c' removed from text (case insensitive)
                line = re.sub(r'\(\((.*?)\)\)', lambda match: remove_character(match.group(1), 'c'), line)
                html_content.append(f'    {line}\n')

        # Close the list if the last line was part of a list
        if in_list:
            html_content.append('</ul>\n')
        # Close the paragraph if the last line was part of a paragraph
        if in_paragraph:
            html_content.append('</p>\n')

    with open(output_file, 'w', encoding='utf-8') as file_2:
        file_2.writelines(html_content)
