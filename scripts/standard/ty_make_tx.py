""" MtoAの TxUtilityManager を使ったテクスチャーコンバートツール
* TEXTURE_ROOT_PATH にあるテクスチャーファイルを TX に変換する
* 色空間の変換
* Mipmap化作成

Info:
    * Created : v0.0.1 2024-12-21 Tatsuya YAMAGISHI
    * Coding : Python 3.11.9 & PySide6
    * Author : Tatsuya Yamagishi <tayama27@gmail.com>

Reference From:
    * https://help.autodesk.com/view/ARNOL/JPN/?guid=arnold_for_maya_utils_am_Tx_Manager_html
    

Examples:
    >>> OpenImageIO-Arnold 2.4.1.1dev : maketx {ASSET}\Textures\colorchecker\v0001\colorchecker_acescg_v0001.exr --opaque-detect --constant-color-detect --monochrome-detect --fixnan box3 --oiio --attrib tiff:half 1 -v --unpremult --oiio -u --colorconvert Raw "scene-linear Rec 709/sRGB" --format exr
 
Release Note:
    * v0.0.1 2024-12-21 Tatsuya Yamagishi
        * New
"""

global logger

VERSION = 'v0.0.1'
NAME = 'MakeTx'

import logging
import os
from pathlib import Path
import re
import subprocess

#=======================================#
# SETTINGS
#=======================================#
# Set Path
TEXTURE_ROOT_PATH = Path(r'D:\temp\usd_ac2024\06_legacy\asset\MoxRig\SHARE\texture\v0001')

MAKETX_EXE = r'C:\Program Files\Autodesk\Arnold\maya2025\bin\maketx.exe'
OCIO_CONFIG = r'D:\temp\usd_ac2024\06_legacy\config\ocio_v2\custom-v0.0.1_aces-v1.3_ocio-v2.1.ocio'
os.environ['PATH'] = r'C:\Program Files\Autodesk\Arnold\maya2025\bin'

RENDER_COLORSPACE = 'ACEScg'
FILE_FORMAT = 'exr' # or tif

COLORSPACE_DICT = {
    'ACEScg': 'ACEScg',
    'sRGB': 'sRGB - Texture',
    'Raw' : 'ACEScg',
}

FILTER_IMAGE_FILE = re.compile(r'.+\.(bmp|cin|dds|dpx|fits|hdr|ico|iff|jpeg|jpg|exr|png|pnm|psd|rla|sgi|pic|tga|tif|tiff|zfile)')
OPTION = '--opaque-detect --constant-color-detect --monochrome-detect --fixnan box3 --oiio --attrib tiff:half 1 -v --checknan --unpremult --oiio --colorconvert'

#=======================================#
# Main
#=======================================#
def convert_to_tx(logger: logging.Logger, filepath: Path):
    src = str(filepath)
    dst = str(filepath.with_suffix('.tx'))

    if os.path.exists(dst):
        return
    else:
        src_colorspace = 'Raw'
        for colorspace in sorted(COLORSPACE_DICT):
            if colorspace in src:
                src_colorspace = COLORSPACE_DICT[colorspace]


        cmd = f'maketx {src} {OPTION} "{src_colorspace}" "{RENDER_COLORSPACE}" --format {FILE_FORMAT} -o {dst}'
        

        logger.info(f'{NAME} | [ Name : {filepath.stem} ]')
        logger.info(f'{NAME} | {src=}')
        logger.info(f'{NAME} | {src_colorspace=}')
        logger.info(f'{NAME} | {dst=}')
        logger.info(f'{NAME} | [ Command ]')
        logger.info(f'{NAME} | {cmd}')
        
        # _cmd = f'maketx --help'
        process = subprocess.run(cmd, shell=True)
        logger.info(process)


def main(logger: logging.Logger):
    logger.info('-----------------------------------')
    logger.info(f'{NAME} {VERSION}')
    logger.info('-----------------------------------')

    # Set OCIO
    if os.path.exists(OCIO_CONFIG):
        os.environ['OCIO'] = OCIO_CONFIG
    else:
        raise FileNotFoundError()
    
    logger.info(f'{NAME} | OCIO = {os.environ.get("OCIO")}')


    # Collect Image File
    image_file_list = [ texture_path for texture_path in TEXTURE_ROOT_PATH.iterdir()
                                if FILTER_IMAGE_FILE.match(str(texture_path))]

    logger.info(f'{NAME} | [Image file list]')
    logger.info(image_file_list)


    # Convert to TX
    for image_filepath in image_file_list:
        convert_to_tx(logger, image_filepath)


#=======================================#
# Debug
#=======================================#
if __name__ == '__main__':
    #-------------------------#
    # Setup Logger
    #-------------------------#
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter(
            '[%(levelname)s][%(name)s][%(funcName)s:%(lineno)s] %(message)s'))
    
    logger.addHandler(stream_handler)


    #-------------------------#
    # Main
    #-------------------------#
    main(logger)