import os
import re
import sys
from base64 import b64decode
from optparse import OptionParser


IMG_PAT = r"""
^Content-Type: image/([a-zA-Z]+)$
^Content-Transfer-Encoding: ([a-zA-Z0-9]+)$
^Content-Location: ([a-zA-Z0-9_.]+)$
^([a-zA-Z0-9+/=\r\n]{76,})
"""


def extract_images(mht, output_dir):
    with open(mht, 'r') as fp:
        mht_text = fp.read()
    matches = re.findall(IMG_PAT, mht_text, re.M)
    for match in matches:
        img_type = match[0]
        img_enc = match[1]
        img_fname = match[2]
        img_data = match[3]

        if img_enc == 'base64':
            dec_img_data = b64decode(img_data.replace('\r\n', ''))
        else:
            raise ValueError("I only base64 decode.")

        with open(os.path.join(output_dir, img_fname), 'wb') as fp:
            fp.write(dec_img_data)

if __name__ == "__main__":
    USAGE = """
    Script needs an input file and an output directory!
    \nExample:
    \tpython extract_img.py -i c:\\spam\\and\\eggs.mht -o c:\\output\\foo\\bar
    \npython extract_img.py --help for more info
    """
    parser = OptionParser()
    parser.add_option('-i', '--input', dest="mht", help='The tarball to '
                      'unpack.', metavar='FILE')
    parser.add_option('-o', '--output-dir', dest="output_dir", help='The '
                      'path to output the unpacked files and folders.',
                      metavar='DIR')
    options, _ = parser.parse_args()

    if not hasattr(options, 'mht') or not hasattr(options, 'output_dir'):
        print USAGE
        sys.exit(1)

    extract_images(options.mht, options.output_dir)