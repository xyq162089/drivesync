#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import threading
import hashlib
import logging


class ImgSync:
    """
    """

    def __init__(self, pool, database, toPath, detailshow=None, syncExt=[]):
        self.toPath = toPath
        self.syncExt = syncExt
        self.detailShow = detailshow
        self.pool = pool
        self.database = database

    def error_callback(self, error):
        print(f"Error info: {error}")

    def ExecuteSync(self, basePath):
        logging.info('开始任务')
        if self.detailShow != None:
            self.detailShow.emit('处理路径： ' + basePath)
        dirList = self._dirList(basePath, [])
        if self.pool != None:
            for l in dirList:
                self.pool.apply_async(self._do, args=(l, self.toPath, self.syncExt, self.database),
                                      error_callback=self.error_callback)
        else:
            for l in dirList:
                self._do(l, self.toPath, self.syncExt, self.database)

    def _dirList(self, basePath, dirList=[]):
        for character_folder in os.listdir(basePath):
            if os.path.isdir(os.path.join(basePath, character_folder)) and character_folder[0] != '.':
                p = os.path.join(basePath, character_folder)
                dirList.append(p)
                self._dirList(p)
        return dirList

    @staticmethod
    def _do(fileBasePath, toPath, syncExt, database):
        logging.critical('处理路径： ' + fileBasePath)
        try:
            # lock.acquire()
            for filePath in os.listdir(fileBasePath):
                file_name, file_extension = os.path.splitext(filePath)
                file_name = os.path.basename(filePath)
                if file_extension in syncExt and file_name[0] != '.' and os.path.isfile(
                        os.path.join(fileBasePath, filePath)):
                    file = open(os.path.join(fileBasePath, filePath), 'rb')  # rb 用来读取二进制文件,(图片,视频,音频....文件都是二进制文件)
                    f = file.read()  # 先把二进制文件读取出来
                    file.close()
                    code = hashlib.md5(f).hexdigest()
                    # if len(database.gets('imgsynclist', {'path': character_folder}, ['id'], 1)) > 0:
                    res = database.gets('imgsynclist', {'code': code}, 'id', 1)
                    if len(res) > 0:
                        logging.info(file_name + ' 已同步')
                        continue
                    try:
                        nf = open(os.path.join(toPath, file_name), 'wb')
                        nf.write(f)
                        nf.close()
                        database.add('imgsynclist', {'code': code, 'path': os.path.join(toPath, file_name), 'sync': 1})
                        logging.info(file_name + ' 同步成功')
                    except Exception as e:
                        # self.database.add('imgsynclist', {'code': code, 'path': file_path, 'sync': 0})
                        print(file_name + ' 同步失败')
                        print(e)
                        print("写入失败", e.__traceback__.tb_frame.f_globals["__file__"], e.__traceback__.tb_lineno)
            # lock.release()

        except Exception as e:
            # logging.ERROR(e)
            print(e)
            print("执行失败", e.__traceback__.tb_frame.f_globals["__file__"], e.__traceback__.tb_lineno)
            # lock.release()
            pass


if __name__ == "__main__":
    pass
