import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, render_template, request

import module as md

plt.switch_backend('agg')


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/schedule", methods=["POST"])
def schedule():
    if request.method == "POST":
        df_dataset_T = pd.read_excel(request.files["file1"])
        df_dataset_P = pd.read_excel(request.files["file2"])
        df_ruangan = pd.read_excel(request.files["file3"])
        df_hari = pd.read_excel(request.files["file4"])
        df_jam = pd.read_excel(request.files["file5"])

        ruangan_list = df_ruangan.to_dict(orient='records')
        array_ruangan = [d['Ruangan'] for d in ruangan_list]

        hari_list = df_hari.to_dict(orient='records')
        array_hari = [h['Hari'] for h in hari_list]

        grouped_jam = df_jam.groupby(" Durasi")["Jam"].apply(list)
        mapped_jam = grouped_jam.to_dict()

        courses_T = md.generate_course_list(
            df_dataset_T, array_ruangan, array_hari, mapped_jam)
        courses_P = md.generate_course_list(
            df_dataset_P, array_ruangan, array_hari, mapped_jam)

        population = md.generate_schedule(courses_T)

        best_schedule_T, best_fitness_per_generation_T = md.genetic_algorithm(
            courses_T, 100, 2)
        best_schedule_P, best_fitness_per_generation_P = md.genetic_algorithm(
            courses_P, 100, 2)

        plt.plot(best_fitness_per_generation_T)
        plt.xlabel("Generation")
        plt.ylabel("Best Fitness")
        plt.title("Best Fitness per Generation For Theory")
        plt.savefig("static/Theory.png")

        plt.plot(best_fitness_per_generation_P)
        plt.xlabel("Generation")
        plt.ylabel("Best Fitness")
        plt.title("Best Fitness per Generation for Practicum")
        plt.savefig("static/Practicum.png")

        for value in population:
            print(value.kode_matakuliah)

        days_order = {'Senin': 1, 'Selasa': 2,
                      'Rabu': 3, 'Kamis': 4, 'Jumat': 5}

        best_schedule_T.sort(key=lambda x: (days_order[x.day], x.time))
        courses_data_T = []
        for course in best_schedule_T:
            print('---------------------')
            print(f'Kode matakuliah\t:{course.kode_matakuliah}')
            print(f'Nama matakuliah\t:{course.nama_matakuliah}')
            print(f'Jenis\t\t:{course.jenis}')
            print(f'Jam\t\t:{course.time}')
            print(f'Hari\t\t:{course.day}')
            print(f'Ruangan\t\t:{course.room}')
            print(f'Dosen1\t\t:{course.lecturer1}')
            print(f'Dosen2\t\t:{course.lecturer2}')
            print(f'Asisten Dosen1\t:{course.assistant1}')
            print(f'Asisten Dosen2\t:{course.assistant2}')
            print(f'Kelas\t\t:{course.kelas}')
            print(f'Semester\t:{course.semester}')
            print('---------------------')
            course_dict = {
                'Kode matakuliah': course.kode_matakuliah,
                'Nama matakuliah': course.nama_matakuliah,
                'Jenis': course.jenis,
                'Jam': course.time,
                'Hari': course.day,
                'Ruangan': course.room,
                'Dosen1': course.lecturer1,
                'Dosen2': course.lecturer2,
                'Asisten Dosen1': course.assistant1,
                'Asisten Dosen2': course.assistant2,
                'Kelas': course.kelas,
                'Semester': course.semester
            }
            courses_data_T.append(course_dict)

        days_order = {'Senin': 1, 'Selasa': 2,
                      'Rabu': 3, 'Kamis': 4, 'Jumat': 5}
        best_schedule_P.sort(key=lambda x: (days_order[x.day], x.time))
        courses_data_P = []
        for course in best_schedule_P:
            print('---------------------')
            print(f'Kode matakuliah\t:{course.kode_matakuliah}')
            print(f'Nama matakuliah\t:{course.nama_matakuliah}')
            print(f'Jenis\t\t:{course.jenis}')
            print(f'Jam\t\t:{course.time}')
            print(f'Hari\t\t:{course.day}')
            print(f'Ruangan\t\t:{course.room}')
            print(f'Dosen1\t\t:{course.lecturer1}')
            print(f'Dosen2\t\t:{course.lecturer2}')
            print(f'Asisten Dosen1\t:{course.assistant1}')
            print(f'Asisten Dosen2\t:{course.assistant2}')
            print(f'Kelas\t\t:{course.kelas}')
            print(f'Semester\t:{course.semester}')
            print('---------------------')
            course_dict = {
                'Kode matakuliah': course.kode_matakuliah,
                'Nama matakuliah': course.nama_matakuliah,
                'Jenis': course.jenis,
                'Jam': course.time,
                'Hari': course.day,
                'Ruangan': course.room,
                'Dosen1': course.lecturer1,
                'Dosen2': course.lecturer2,
                'Asisten Dosen1': course.assistant1,
                'Asisten Dosen2': course.assistant2,
                'Kelas': course.kelas,
                'Semester': course.semester
            }
            courses_data_P.append(course_dict)

        df_predict = pd.DataFrame(courses_data_T + courses_data_P)

        df_predict_T = pd.DataFrame(courses_data_T)
        df_predict_T = df_predict[['Jam', 'Hari', 'Semester', 'Kode matakuliah', 'Nama matakuliah', 'Jenis', 'Ruangan',
                                   'Dosen1', 'Dosen2', 'Asisten Dosen1', 'Asisten Dosen2', 'Kelas',]]
        df_predict_T.sort_values(by=['Jam', 'Semester', 'Hari'])

        df_predict_P = pd.DataFrame(courses_data_P)
        df_predict_P = df_predict_P[['Jam', 'Hari', 'Semester', 'Kode matakuliah', 'Nama matakuliah', 'Jenis', 'Ruangan',
                                     'Dosen1', 'Dosen2', 'Asisten Dosen1', 'Asisten Dosen2', 'Kelas',]]
        df_predict_P.sort_values(by=['Jam', 'Semester', 'Hari'])

        df_predict = df_predict.to_html(
            index=False, classes="table table-responsive table-striped")
        df_predict_T = df_predict_T.to_html(
            index=False, classes="table table-responsive table-striped")
        df_predict_P = df_predict_P.to_html(
            index=False, classes="table table-responsive table-striped")

        return render_template("schedule.html",
                               theory_graph="static/Theory.png",
                               practicum_graph="static/Practicum.png",
                               df_predict=df_predict,
                               df_predict_T=df_predict_T,
                               df_predict_P=df_predict_P
                               )
