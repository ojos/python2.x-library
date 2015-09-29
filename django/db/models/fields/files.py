# -*- coding: utf-8 -*-
from django.db.models.fields import files


class FieldFile(files.FieldFile):
    def _get_size(self):
        self._require_file()
        if not self._committed:
            print dir(self.file)
            try:
                return self.file.size
            except AttributeError:
                return len(self.file.getvalue())
        return self.storage.size(self.name)
    size = property(_get_size)


class FileField(files.FileField):
    attr_class = FieldFile
    descriptor_class = files.FileDescriptor
