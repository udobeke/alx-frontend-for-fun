#!/usr/bin/python3
'''
A script that converts Markdown to HTML
'''
import sys
import os
import re

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
            elif line.startswith('* '):
                # Start of an unordered list
                if not in_list:
                    html_content.append('<ul>\n')
                    in_list = True
                # Remove the '*' and space, and wrap the line in <li> tags
                html_content.append(f'<li>{line[2:]}</li>\n')
            elif line.startswith('1. '):
                # Start of an ordered list
                if not in_list:
                    html_content.append('<ol>\n')
                    in_list = True
                # Remove the '1.' and space, and wrap the line in <li> tags
                html_content.append(f'<li>{line[3:]}</li>\n')
            else:
                # Regular text line
                html_content.append(line)

        # Close the list if the last line was part of a list
        if in_list:
            html_content.append('</ul>\n')

    with open(output_file, 'w', encoding='utf-8') as file_2:
        file_2.writelines(html_content)
