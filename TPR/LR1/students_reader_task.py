from typing import Union, List, Dict
from collections import namedtuple
from datetime import datetime
import csv
import os.path
import json


LAB_WORK_SESSION_KEYS = ("presence", "lab_work_n", "lab_work_mark", "date")
STUDENT_KEYS = ("unique_id", "name", "surname", "group", "subgroup", "lab_works_sessions")


class LabWorkSession(namedtuple('LabWorkSession', 'presence, lab_work_number, lab_work_mark, lab_work_date')):
    """
    Информация о лабораторном занятии, которое могло или не могло быть посещено студентом
    """

    def __new__(cls, presence: bool, lab_work_number: int, lab_work_mark: int, lab_work_date: datetime):
        """
            param: presence: присутствие студента на л.р.(bool)
            param: lab_work_number: номер л.р.(int)
            param: lab_work_mark: оценка за л.р.(int)
            param: lab_work_date: дата л.р.(date)
        """
        if LabWorkSession._validate_args(presence, lab_work_number, lab_work_mark, lab_work_date):
            return super(LabWorkSession, cls).__new__(cls, presence, lab_work_number, lab_work_mark, lab_work_date)
        
        raise ValueError(f"LabWorkSession ::"
                         f"incorrect args :\n"
                         f"presence       : {presence},\n"
                         f"lab_work_number: {lab_work_number},\n"
                         f"lab_work_mark  : {lab_work_mark},\n"
                         f"lab_work_date  : {lab_work_date}")

    @staticmethod
    def _validate_args(presence: bool, lab_work_number: int, lab_work_mark: int, lab_work_date: datetime) -> bool:
        if not isinstance(presence, bool):
            return False
        if not isinstance(lab_work_number, int) or lab_work_number < 0:
            return False
        if not isinstance(lab_work_mark, int) or lab_work_mark < 0:
            return False
        if not isinstance(lab_work_date, datetime):
            return False
        return True

    def __str__(self) -> str:
        return json.dumps({
            "presence": self.presence,
            "lab_work_number": self.lab_work_number,
            "lab_work_mark": self.lab_work_mark,
            "date": str(self.lab_work_date)
        })



class Student:
    __slots__ = ('_unique_id', '_name', '_surname', '_group', '_subgroup', '_lab_work_sessions')

    def __init__(self, unique_id: int, name: str, surname: str, group: int, subgroup: int):

        if not self._validate_args(unique_id, name, surname, group, subgroup):
            raise ValueError("Student :: incorrect args...")
        self._unique_id = unique_id
        self._name = name
        self._surname = surname
        self._group = group
        self._subgroup = subgroup
        self._lab_work_sessions = []

    @staticmethod
    def _validate_args(unique_id: int, name: str, surname: str, group: int, subgroup: int) -> bool:
        if not isinstance(unique_id, int) or unique_id < 0:
            return False
        if not isinstance(name, str) or len(name) == 0:
            return False
        if not isinstance(surname, str) or len(surname) == 0:
            return False
        if not isinstance(group, int) or group < 0:
            return False
        if not isinstance(subgroup, int) or subgroup < 0:
            return False
        return True





    def __str__(self) -> str:
        return json.dumps({
            "unique_id": self._unique_id,
            "name": self._name,
            "surname": self._surname,
            "group": self._group,
            "subgroup": self._subgroup,
            "lab_works_sessions": [session.__dict__ for session in self._lab_work_sessions]
        })

    @property
    def unique_id(self) -> int:
        return self._unique_id

    @property
    def group(self) -> int:
        return self._group

    @property
    def subgroup(self) -> int:
        return self._subgroup

    @property
    def name(self) -> str:
        return self._name

    @property
    def surname(self) -> str:
        return self._surname

    @name.setter
    def name(self, val: str) -> None:
        """
        Метод для изменения значения имени студента
        """
        # Если хотим жёстко мониторить некорректные аргументы сеттера
        #assert isinstance(val, str)
        #assert len(val) != 0
        # Если не хотим жёстко мониторить некорректные аргументы сеттера
        if not isinstance(val, str):
            return
        if len(val) == 0:
            return
        self._name = val

    @surname.setter
    def surname(self, val: str) -> None:
        self._surname = val

    @property
    def lab_work_sessions(self):
        for lab_session in self._lab_work_sessions:
            yield lab_session

    def append_lab_work_session(self, session: LabWorkSession):
        self._lab_work_sessions.append(session)


def _load_lab_work_session(json_node) -> LabWorkSession:
    for key in LAB_WORK_SESSION_KEYS:
        if key not in json_node:
            raise KeyError(f"load_lab_work_session :: key \"{key}\" not present in json_node")
    presence = bool(json_node['presence'])
    lab_work_number = int(json_node['lab_work_number'])
    lab_work_mark = int(json_node['lab_work_mark'])
    date_parts = list(map(int, json_node['date'].split(':')))
    lab_work_date = datetime(*date_parts)
    return LabWorkSession(presence, lab_work_number, lab_work_mark, lab_work_date)


def _load_student(json_node) -> Student:
    for key in STUDENT_KEYS:
        if key not in json_node:
            raise KeyError(f"load_student :: key \"{key}\" not present in json_node")
    unique_id = int(json_node['unique_id'])
    name = json_node['name']
    surname = json_node['surname']
    group = int(json_node['group'])
    subgroup = int(json_node['subgroup'])
    student = Student(unique_id, name, surname, group, subgroup)
    lab_work_sessions = json_node['lab_works_sessions']
    for session_data in lab_work_sessions:
        lab_work_session = _load_lab_work_session(session_data)
        student.append_lab_work_session(lab_work_session)
    return student


# csv header
#     0    |   1  |   2   |   3  |    4    |  5  |    6    |        7       |       8     |
# unique_id; name; surname; group; subgroup; date; presence; lab_work_number; lab_work_mark
UNIQUE_ID = 0
STUD_NAME = 1
STUD_SURNAME = 2
STUD_GROUP = 3
STUD_SUBGROUP = 4
LAB_WORK_DATE = 5
STUD_PRESENCE = 6
LAB_WORK_NUMBER = 7
LAB_WORK_MARK = 8



def load_students_csv(file_path: str) -> Union[List[Student], None]:
    # csv header
    #     0    |   1  |   2   |   3  |    4    |  5  |    6    |        7       |       8     |
    # unique_id; name; surname; group; subgroup; date; presence; lab_work_number; lab_work_mark
    assert isinstance(file_path, str)

    if not os.path.exists(file_path):
        return None

    students = []
    lab_work_sessions = []

    with open(file_path, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file, delimiter=';')

        for row in reader:
            unique_id = int(row['unique_id'])
            name = row['name']
            surname = row['surname']
            group = int(row['group'])
            subgroup = int(row['subgroup'])
            presence = bool(row['presence'])
            lab_work_number = int(row['lab_work_number'])
            lab_work_mark = int(row['lab_work_mark'])

            lab_work_date = datetime.strptime(row['date'], '%d:%m:%y')

            session = LabWorkSession(presence, lab_work_number, lab_work_mark, lab_work_date)

            # Check if the student is already in the list
            found_student = next((s for s in students if s.unique_id == unique_id), None)
            if not found_student:
                found_student = Student(unique_id, name, surname, group, subgroup)
                students.append(found_student)

            found_student.append_lab_work_session(session)

    return students







def load_students_json(file_path: str) -> Union[List[Student], None]:
    """
    Загрузка списка студентов из json файла.
    Ошибка создания экземпляра класса Student не должна приводить к поломке всего чтения.
    """
    # csv header
    #     0    |   1  |   2   |   3  |    4    |  5  |    6    |        7       |       8     |
    # unique_id; name; surname; group; subgroup; date; presence; lab_work_number; lab_work_mark
    if not isinstance(file_path, str):  # Путь к файлу должен быть строкой
        raise ValueError("File path must be a string.")
    if not os.path.exists(file_path):  # и, желательно, существовать...
        return None
    with open(file_path, 'rt', encoding='utf-8') as input_file:
        for line in input_file:
                fields = line.strip().split(';')
                if len(fields) != 9:  # Ожидается 9 полей
                    continue
        # создаём пустой словарь [целочисленный ключ, значение - Student]
        students_raw: Dict[int, Student] = {}
        for line in input_file:
            # итерируемся по файлу, каждую строку разбиваем символом ";"
            ...
            try:
                unique_id = int(fields[0])
                if unique_id not in students_raw:
                    name = fields[1]
                    surname = fields[2]
                    group = int(fields[3])
                    subgroup = int(fields[4])
                    student = Student(unique_id, name, surname, group, subgroup)
                    students_raw[unique_id] = student

                presence = bool(int(fields[6]))
                lab_work_number = int(fields[7])
                lab_work_mark = int(fields[8])
                lab_work_date = datetime.strptime(fields[5], '%d:%m:%y')
                lab_work_session = LabWorkSession(presence, lab_work_number, lab_work_mark, lab_work_date)
                students_raw[unique_id].append_lab_work_session(lab_work_session)
            except Exception as ex:
                print(ex)
                continue
    # конвертируем значения из словаря в лист
    return list(students_raw.values())


def save_students_json(file_path: str, students: List[Student]):
    data = [student.__dict__ for student in students]
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)


def save_students_csv(file_path: str, students: List[Student]):
    if not isinstance(file_path, str):
        raise ValueError("File path must be a string.")

    if not students or not isinstance(students, list):
        print("No data to save.")
        return

    fieldnames = ["unique_id", "name", "surname", "group", "subgroup", "date", "presence", "lab_work_number", "lab_work_mark"]
    
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()

            for student in students:
                for lab_session in student.lab_work_sessions:
                    writer.writerow({
                        "unique_id": student.unique_id,
                        "name": student.name,
                        "surname": student.surname,
                        "group": student.group,
                        "subgroup": student.subgroup,
                        "date": lab_session.lab_work_date.strftime('%d:%m:%y'),
                        "presence": int(lab_session.presence),
                        "lab_work_number": lab_session.lab_work_number,
                        "lab_work_mark": lab_session.lab_work_mark
                    })

        print("Data saved to", file_path)
    except Exception as ex:
        print(f"Error while saving the data: {ex}")


if __name__ == '__main__':
    # Задание на проверку json читалки:
    # 1. прочитать файл "students.json"
    # 2. сохранить прочитанный файл в "saved_students.json"
    # 3. прочитать файл "saved_students.json"
    students = load_students_json('students.json')
    save_students_json('saved_students.json',students)
    students = load_students_json('saved_students.json')
    # Задание на проверку csv читалки:
    # 1.-3. аналогично
    
    students = load_students_csv('students.csv')
    save_students_csv('saved_students.csv',students)
    students =load_students_csv('saved_students.csv')
    
    for s in students:
        print(s)

