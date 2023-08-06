# MIT License

# Copyright (c) 2022-present Rahman Yusuf

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import shutil
import os
import tqdm

from pathvalidate import sanitize_filename
from .base import (
    ConvertedChaptersFormat,
    ConvertedVolumesFormat,
    ConvertedSingleFormat
)
from .utils import (
    get_chapter_info,
    NumberWithLeadingZeros,
    get_volume_cover
)
from ..utils import create_directory, delete_file
from ..errors import MangaDexException
from ..progress_bar import progress_bar_manager as pbm

try:
    import py7zr
except ImportError:
    PY7ZR_OK = False
else:
    PY7ZR_OK = True

class py7zrNotInstalled(MangaDexException):
    """Raised when py7zr is not installed"""
    pass

log = logging.getLogger(__name__)

class SevenZipFile:
    file_ext = ".cb7"

    def check_dependecies(self):
        if not PY7ZR_OK:
            raise py7zrNotInstalled("py7zr is not installed")

    def convert(self, images, path):
        pbm.set_convert_total(len(images))
        progress_bar = pbm.get_convert_pb(recreate=not pbm.stacked)

        for im_path in images:

            with py7zr.SevenZipFile(path, "a" if os.path.exists(path) else "w") as zip_obj:
                zip_obj.write(im_path, im_path.name)
                progress_bar.update(1)

    def check_write_chapter_info(self, path, target):
        if not os.path.exists(path):
            return True

        with py7zr.SevenZipFile(path, 'r') as zip_obj:
            return target not in zip_obj.getnames()

    def insert_ch_info_img(self, images, chapter, path, count):
        """Insert chapter info (cover) image"""
        img_name = count.get() + '.png'
        img_path = path / img_name

        if self.config.use_chapter_cover:
            get_chapter_info(self.manga, chapter, img_path)
            images.append(img_path)
            count.increase()

    def insert_vol_cover_img(self, images, volume, path, count):
        """Insert volume cover"""
        img_name = count.get() + '.png'
        img_path = path / img_name

        if self.config.use_volume_cover:
            get_volume_cover(self.manga, volume, img_path, self.replace)
            images.append(img_path)
            count.increase()

class SevenZip(ConvertedChaptersFormat, SevenZipFile):
    def on_finish(self, file_path, chapter, images):
        chap_name = chapter.get_simplified_name()

        pbm.logger.info(f"{chap_name} has finished download, converting to cb7...")
        self.worker.submit(lambda: self.convert(images, file_path))

class SevenZipVolume(ConvertedVolumesFormat, SevenZipFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # See `PDFVolume.__init__()` why i did this
        self.images = []

    def on_prepare(self, file_path, volume, count):
        self.images.clear()

        volume_name = self.get_volume_name(volume)
        self.volume_path = create_directory(volume_name, self.path)

        self.insert_vol_cover_img(self.images, volume, self.volume_path, count)

    def on_iter_chapter(self, file_path, chapter, count):
        self.insert_ch_info_img(self.images, chapter, self.volume_path, count)

    def on_received_images(self, file_path, chapter, images):
        self.images.extend(images)

    def on_convert(self, file_path, volume, images):
        volume_name = self.get_volume_name(volume)

        pbm.logger.info(f"{volume_name} has finished download, converting to cb7...")
        self.worker.submit(lambda: self.convert(self.images, file_path))

class SevenZipSingle(ConvertedSingleFormat, SevenZipFile):
    def download_single(self, worker, total, merged_name, chapters):
        images = []
        manga = self.manga
        count = NumberWithLeadingZeros(total)
        manga_zip_path = self.path / (merged_name + self.file_ext)

        if manga_zip_path.exists():
            if self.replace:
                delete_file(manga_zip_path)
            elif self.check_fi_completed(merged_name):
                log.info(f"'{manga_zip_path.name}' is exist and replace is False, cancelling download...")
                self.add_fi(merged_name, None, manga_zip_path, chapters)
                return

        path = create_directory(merged_name, self.path)

        for chap_class, chap_images in chapters:
            self.insert_ch_info_img(images, chap_class, path, count)

            images.extend(self.get_images(chap_class, chap_images, path, count))
        
        # Begin converting
        log.info(f"Manga '{manga.title}' has finished download, converting to cb7...")
        self.convert(images, manga_zip_path)

        # Remove original manga folder
        shutil.rmtree(path, ignore_errors=True)

        self.add_fi(merged_name, None, manga_zip_path, chapters)
