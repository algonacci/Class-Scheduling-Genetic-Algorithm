import pandas as pd


class Course:
    def __init__(self, kode_matakuliah, nama_matakuliah, jenis, times, days, rooms, lecturer1, lecturer2, assistant1, assistant2, kelas, semester):
        self.kode_matakuliah = kode_matakuliah
        self.nama_matakuliah = nama_matakuliah
        self.jenis = jenis
        self.times = times
        self.days = days
        self.rooms = rooms
        self.lecturer1 = lecturer1
        self.lecturer2 = lecturer2
        self.assistant1 = assistant1
        self.assistant2 = assistant2
        self.kelas = kelas
        self.semester = semester
        self.time = None
        self.room = None
        self.day = None
