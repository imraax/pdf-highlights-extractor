# -*- coding: utf-8 -*-
"""
@Time ： 2022/11/7
@Auth ： raax
@File ：test.py
@IDE ：PyCharm
"""
from abc import ABCMeta, abstractmethod
import os
import io


class Exporter(metaclass=ABCMeta):
    def __init__(self, notes_data, name="Exporter"):
        self.name = name
        self.notes_data = notes_data

    @abstractmethod
    def run(self):
        pass


class NoteTypeExporter(Exporter):
    def __init__(self, notes_data, file, notetype, ):
        super().__init__(notes_data, "NoteTypeExporter")
        self.notetype = notetype
        self.file = file

    def run(self):
        with io.open(self.file, 'a+', encoding="utf8") as result_file:
            # print("## "+self.notetype)
            result_file.write("## " + self.notetype + '\n')
            for page, notes in self.notes_data.items():
                if (len(notes[self.notetype]) != 0):
                    # print("### Page %d : " % page)
                    result_file.write("### Page %d : \n" % (page + 1))
                    for note_highlight in notes[self.notetype]:
                        # print('> ' + note_highlight + '\n')
                        result_file.write('> ' + note_highlight + '\n')


class FileExporter(Exporter):
    def __init__(self, notes_data, output_file, file_type="md"):
        super().__init__(notes_data, "FileExporter")
        self.file_type = file_type
        self.output_file = output_file

    def validate_file(self, target_ext):
        if (os.path.isfile(self.output_file) and self.output_file.endswith(target_ext)):
            file_confirm = input("File exist,please input y to recover:\n")
            if (file_confirm == 'y' or file_confirm == 'Y'):
                with io.open(self.output_file, 'w', encoding="utf8") as result_file:
                    return True
            else:
                return False
        else:
            return True

    def run(self):
        if self.file_type == 'md':
            if (self.validate_file('.md')):
                highlight_exporter = NoteTypeExporter(
                    self.notes_data, self.output_file, "highlights")
                highlight_exporter.run()
                comment_exporter = NoteTypeExporter(
                    self.notes_data, self.output_file, "comments")
                comment_exporter.run()
            else:
                raise Exception('File error.')
        elif self.type == 'csv':
            pass
