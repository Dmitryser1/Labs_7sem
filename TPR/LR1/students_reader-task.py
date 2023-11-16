from typing import Union, List, Dict
from collections import namedtuple
from datetime import date
import os.path
import json

LAB_WORK_SESSION_KEYS = ("presence", "lab_work_n", "lab_work_mark", "date")
STUDENT_KEYS = ("unique_id", "name", "surname", "group", "subgroup", "lab_works_sessions")


class LabWorkSession(namedtuple('LabWorkSession', 'presence, lab_work_n, lab_work_mark, lab_work_date')):
    def __new__(cls, presence: bool, lab_work_n: int, lab_work_mark: int, lab_work_date: date):
        if LabWorkSession._validate_session(presence, lab_work_n, lab_work_mark, lab_work_date):
            return super(LabWorkSession, cls).__new__(cls, presence, lab_work_n, lab_work_mark, lab_work_date)
        raise ValueError(f"LabWorkSession ::"
                         f"incorrect args :\n"
                         f"presence       : {presence},\n"
                         f"lab_work_n:      {lab_work_n},\n"
                         f"lab_work_mark  : {lab_work_mark},\n"
                         f"lab_work_date  : {lab_work_date}")

    @staticmethod
    def _validate_session(presence: bool, lab_work_n: int, lab_work_mark: int, lab_work_date: date) -> bool:
        if not isinstance(presence, bool):
            return False
        if not isinstance(lab_work_n, int) or lab_work_n < 0:
            return False
        if not isinstance(lab_work_mark, int) or lab_work_mark < 0 or lab_work_mark > 5:
            return False
        if not isinstance(lab_work_date, date):
            return False
        return True

    def __str__(self) -> str:
       return (f"\t{{\n"
               f"\t\t\"presence\":      {'1' if self.presence else '0'},\n"
               f"\t\t\"lab_work_n\":    {self.lab_work_n},\n"
               f"\t\t\"lab_work_mark\": {self.lab_work_mark},\n"
               f"\t\t\"date\":          \"{self.lab_work_date.strftime('%d:%m:%Y')}\"\n"
               f"\t}}")

class Student:
    __slots__ = ('_unique_id', '_name', '_surname', '_group', '_subgroup', '_lab_work_sessions')

    def __init__(self, unique_id: int, name: str, surname: str, group: int, subgroup: int):

        if not self._validate_args(unique_id, name, surname, group, subgroup):
            raise ValueError(f"Student ::"
                             f"incorrect args :\n"
                             f"unique_id : {unique_id},\n"
                             f"name      : {name},\n"
                             f"surname   : {surname},\n"
                             f"group     : {group},\n"
                             f"subgroup  : {subgroup}")

        self._unique_id = unique_id
        self.name = name
        self.surname = surname
        self._group = group
        self._subgroup = subgroup
        self._lab_work_sessions: List[LabWorkSession] = []

    @staticmethod
    def _validate_args(unique_id: int, name: str, surname: str, group: int, subgroup: int) -> bool:
        if not isinstance(unique_id, int):
            return False
        if not isinstance(name, str):
            return False
        if len(name) == 0:
            return False
        if not isinstance(surname, str):
            return False
        if len(surname) == 0:
            return False
        if not isinstance(group, int):
            return False
        if group < 0:
            return False
        if subgroup < 0:
            return False
        return True
    
    def __len__(self):
        return 1
    
    def __str__(self) -> str:
        chtoetotakoe = ',\n'
        return (f"\t{{\n"
                f"\t\"unique_id\":        {self.unique_id},\n"
                f"\t\"name\":             \"{self.name}\",\n"
                f"\t\"surname\":          \"{self.surname}\",\n"
                f"\t\"group\":            {self.group},\n"
                f"\t\"subgroup\":         {self.subgroup}, \n"
                f"\t\"lab_works_sessions\": [\n {chtoetotakoe.join(str(ws) for ws in self.lab_work_sessions)}]\n"
                f"\t}}")

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
        if not (isinstance(val, str) or not len(val) > 0):
            raise ValueError("name")
        self._name = val

    @surname.setter
    def surname(self, val: str) -> None:
        if not (isinstance(val, str)) or not (len(val) > 0):
            raise ValueError("surname")
        self._surname = val

    @property
    def lab_work_sessions(self):
        for session in self._lab_work_sessions:
            yield session

    def append_lab_work_session(self, session: LabWorkSession):
        assert isinstance(session, LabWorkSession)
        self._lab_work_sessions.append(session)


def _load_lab_work_session(json_node) -> LabWorkSession:
    for key in LAB_WORK_SESSION_KEYS:
        if key not in json_node:
            raise KeyError(f"load_lab_work_session:: key \"{key}\" not present in json_node")
    preDate = json_node["date"].split(":")[::-1]
    if len(preDate[0]) < 4:
        preDate[0] = "20" + preDate[0]
    return LabWorkSession(True if int(json_node['presence']) == 1 else False,
                          int(json_node["lab_work_n"]),
                          int(json_node["lab_work_mark"]),
                          date(*map(int, preDate)))


def _load_student(json_node) -> Student:
    for key in STUDENT_KEYS:
        if key not in json_node:
            raise KeyError(f"load_student:: key \"{key}\" not present in json_node")
    student = Student(json_node['unique_id'], json_node['name'], json_node['surname'], int(json_node['group']),
                      int(json_node['subgroup']))
    for sline in json_node['lab_works_sessions']:
        try:
            session = _load_lab_work_session(sline)
            student.append_lab_work_session(session)
        except ValueError as er:
            print(er)
            continue
        except KeyError as er:
            print(er)
            continue
        except Exception as er:
            print(er)
            continue
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

    with open(file_path, "rt", encoding='utf-8') as input_file:
        students_raw: Dict[int, Student] = {}
        input_file.readline()
        for line in input_file:
            sline = line.split(";")
            try:
                student_id = int(sline[0])
                if student_id not in students_raw:
                    students_raw.update({student_id: Student(int(sline[UNIQUE_ID]),
                                                             str(sline[STUD_NAME]),
                                                             str(sline[STUD_SURNAME]),
                                                             int(sline[STUD_GROUP]),
                                                             int(sline[STUD_SUBGROUP]))})
                lab_work_preDate = sline[LAB_WORK_DATE].replace('\"', '').split(':')[::-1]
                if len(lab_work_preDate[0]) < 4:
                    lab_work_preDate[0] = "20" + lab_work_preDate[0]
                lab_work_date = date(*map(int, lab_work_preDate))
                students_raw[student_id].append_lab_work_session(
                    LabWorkSession(True if int(sline[STUD_PRESENCE]) else False,
                                   int(sline[LAB_WORK_NUMBER]), int(sline[LAB_WORK_MARK]), lab_work_date))
            except Exception as e:
                print(e)
                continue
    if len(students_raw) == 0:
        return None
    return list(students_raw.values())


def load_students_json(file_path: str) -> Union[List[Student], None]:
    assert isinstance(file_path, str)
    if not os.path.exists(file_path):
        return None

    with open(file_path, "rt", encoding='utf-8') as input_file:
        jsonfile = json.load(input_file)
        if "students" not in jsonfile:
            return None
        istudents = []
        for node in jsonfile["students"]:
            try:
                istudents.append(_load_student(node))
            except Exception as ex:
                print(ex)
                continue
        return list(istudents)


def save_students_json(file_path: str, istudents: List[Student]):
    assert isinstance(file_path, str)

    with open(file_path, 'w', encoding='utf-8') as file:
        sep = ',\n'
        print(f'{{\n\"students\":[\n{sep.join(str(v)for v in istudents)}]\n}}', file=file)


def save_students_csv(file_path: str, istudents: List[Student]):
    assert isinstance(file_path, str)

    with open(file_path, 'wt', encoding='utf-8', newline='') as output_file:
        print("unique_id;name;surname;group;subgroup;date;presence;lab_work_number;lab_work_mark", file=output_file)
        for student in istudents:
            for session in student.lab_work_sessions:
                print(
                f"{student.unique_id};"
                f"{student.name};"
                f"{student.surname};"
                f"{student.group};"
                f"{student.subgroup};"
                f"\"{session.lab_work_date.strftime('%d:%m:%Y')}\";"
                f"{1 if session.presence else 0};{session.lab_work_n};{session.lab_work_mark}", file=output_file)


if __name__ == '__main__':
    # Задание на проверку json читалки:
    # 1. прочитать файл "students.json"
    # 2. сохранить прочитанный файл в "saved_students.json"
    # 3. прочитать файл "saved_students.json"
    # Задание на проверку csv читалки:
    # 1.-3. аналогично

    students = load_students_json('students.json')
    save_students_json('students_saved.json', students)
    students = load_students_json('students_saved.json')
    [print(v) for v in students]

    students = load_students_csv('students.csv')
    save_students_csv('students_saved.csv', students)
    students = load_students_csv('students_saved.csv')
    [print(v) for v in students]