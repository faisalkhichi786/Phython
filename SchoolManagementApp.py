import json
import re
from abc import ABC, abstractmethod
from pathlib import Path
from statistics import mean
from shutil import copy2

import streamlit as st

# ============================================================
# DATABASE SETTINGS
# ============================================================

DATABASE_FILE = Path("Datamanagement.json")
BACKUP_FILE = Path("Datamanagement_backup.json")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="School Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');

    :root {
        --bg: #EEF1F5;
        --panel: #FFFFFF;
        --panel-alt: #F4F6F9;
        --border: #D6DCE3;
        --text: #1F2933;
        --text-dim: #5B6672;
        --teal: #1E8F82;
        --teal-hover: #17756A;
        --amber: #C97A1A;
        --red: #C6433B;
        --red-hover: #A83730;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"],
    [data-testid="stMarkdownContainer"], p, span, div, label {
        font-family: 'Inter', sans-serif;
        color: var(--text) !important;
    }

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
    [data-testid="stMain"], [data-testid="stMainBlockContainer"],
    [data-testid="stBottomBlockContainer"] {
        background-color: var(--bg) !important;
    }
    [data-testid="stHeader"] { background-color: transparent !important; }

    div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"],
    div[data-testid="column"] {
        background-color: transparent !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background-color: var(--panel);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] * {
        color: var(--text) !important;
    }

    .brand {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.05rem;
        font-weight: 700;
        padding: 1.1rem 0 0.2rem 0;
        letter-spacing: 0.2px;
    }
    .brand-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: var(--text-dim) !important;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-dim) !important;
        padding: 0.4rem 0;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        color: var(--teal) !important;
    }

    /* ---------- Path breadcrumb ---------- */
    .path-bar {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.85rem;
        color: var(--text-dim) !important;
        background-color: var(--panel-alt);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 0.5rem 0.9rem;
        margin-bottom: 1.4rem;
    }
    .path-bar span { color: var(--teal) !important; }

    /* ---------- Panels / cards ---------- */
    .panel {
        background-color: var(--panel);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 1.4rem 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 2px rgba(31, 41, 51, 0.06);
    }
    .panel h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1rem;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 1rem;
    }

    .entry-card {
        background-color: var(--panel-alt);
        border: 1px solid var(--border);
        border-left: 4px solid var(--teal);
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.8rem;
    }
    .entry-card.teacher { border-left-color: var(--amber); }
    .entry-card .entry-name {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.35rem;
    }
    .entry-card .entry-row {
        font-size: 0.86rem;
        color: var(--text-dim) !important;
        font-weight: 600;
    }
    .entry-card .entry-row b { color: var(--text) !important; }
    .badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.78rem;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        background-color: var(--teal);
        color: #FFFFFF !important;
        margin-left: 0.5rem;
    }

    /* ---------- Stat cards ---------- */
    .stat-card {
        background-color: var(--panel);
        border: 1px solid var(--border);
        border-top: 4px solid var(--teal);
        border-radius: 6px;
        padding: 1.1rem 1.2rem;
        text-align: center;
        box-shadow: 0 1px 2px rgba(31, 41, 51, 0.06);
    }
    .stat-card.amber { border-top-color: var(--amber); }
    .stat-card.red { border-top-color: var(--red); }
    .stat-card .stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 2rem;
    }
    .stat-card .stat-label {
        font-weight: 700;
        font-size: 0.82rem;
        color: var(--text-dim) !important;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    /* ---------- Labels ---------- */
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    .stRadio label p,
    .stCheckbox label p {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-dim) !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label {
        color: var(--text) !important;
        font-weight: 600 !important;
    }

    /* ---------- Inputs (white bold text on dark field) ---------- */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #2B333B !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: 1px solid var(--border) !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 1px var(--teal) !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #B8C0C9 !important;
        opacity: 1;
    }

    /* ---------- Buttons ---------- */
    .stButton button {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.9rem;
        background-color: var(--teal);
        color: #FFFFFF !important;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.1rem;
        transition: background-color 0.15s ease;
    }
    .stButton button:hover { background-color: var(--teal-hover); color: #FFFFFF !important; }
    .danger-zone .stButton button { background-color: var(--red); color: #FFFFFF !important; }
    .danger-zone .stButton button:hover { background-color: var(--red-hover); }

    /* ---------- Console / activity log ---------- */
    .console {
        background-color: var(--panel-alt);
        border: 1px solid var(--border);
        border-radius: 6px;
        padding: 0.9rem 1.1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        max-height: 220px;
        overflow-y: auto;
    }
    .console-line {
        padding: 0.25rem 0;
        border-left: 3px solid var(--border);
        padding-left: 0.7rem;
        margin-bottom: 0.3rem;
        color: var(--text-dim) !important;
        font-weight: 600;
    }
    .console-line.ok { border-left-color: var(--teal); color: var(--text) !important; }
    .console-line.err { border-left-color: var(--red); color: var(--text) !important; }
    .console-line.info { border-left-color: var(--amber); color: var(--text) !important; }
    .console-time { color: var(--text-dim) !important; margin-right: 0.6rem; }

    hr { border-color: var(--border); }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PERSON ABSTRACT CLASS
# ============================================================

class Person(ABC):

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass


# ============================================================
# STUDENT CLASS
# ============================================================

class Student(Person):

    def __init__(self, name, email, phone, roll_number, department):
        super().__init__(name, email, phone)
        self.roll_number = roll_number
        self.department = department
        self.grades = {}

    def get_role(self):
        return "Student"

    def add_grade(self, subject, marks):
        self.grades[subject] = marks

    def calculate_average(self):
        if not self.grades:
            return 0
        return mean(self.grades.values())

    def performance_grade(self):
        average = self.calculate_average()
        if average >= 90:
            return "A+"
        elif average >= 80:
            return "A"
        elif average >= 70:
            return "B"
        elif average >= 60:
            return "C"
        elif average >= 50:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "roll_number": self.roll_number,
            "department": self.department,
            "grades": self.grades,
        }

    @staticmethod
    def from_dict(data):
        student = Student(
            data["name"],
            data["email"],
            data["phone"],
            data["roll_number"],
            data["department"],
        )
        student.grades = data.get("grades", {})
        return student


# ============================================================
# TEACHER CLASS
# ============================================================

class Teacher(Person):

    def __init__(self, name, email, phone, employee_id, subject):
        super().__init__(name, email, phone)
        self.employee_id = employee_id
        self.subject = subject

    def get_role(self):
        return "Teacher"

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "employee_id": self.employee_id,
            "subject": self.subject,
        }

    @staticmethod
    def from_dict(data):
        return Teacher(
            data["name"],
            data["email"],
            data["phone"],
            data["employee_id"],
            data["subject"],
        )


# ============================================================
# SCHOOL MANAGEMENT SYSTEM (non-interactive core, reused by the UI)
# ============================================================

class SchoolManagementSystem:

    def __init__(self):
        self.students = []
        self.teachers = []
        self.status = None  # last load/save status message, set during init
        self.load_data()

    # ---------------- Database ----------------

    def load_data(self):
        if not DATABASE_FILE.exists():
            self.students = []
            self.teachers = []
            self.save_data()
            self.status = ("info", "New database created successfully.")
            return

        try:
            with open(DATABASE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.students = [Student.from_dict(s) for s in data.get("students", [])]
            self.teachers = [Teacher.from_dict(t) for t in data.get("teachers", [])]
            self.status = ("ok", "Database loaded successfully.")

        except json.JSONDecodeError:
            self.students = []
            self.teachers = []
            self.save_data()
            self.status = ("err", "Database file was corrupted — a fresh database was created.")

        except Exception as error:
            self.students = []
            self.teachers = []
            self.status = ("err", f"Error loading database: {error}")

    def save_data(self):
        data = {
            "students": [s.to_dict() for s in self.students],
            "teachers": [t.to_dict() for t in self.teachers],
        }
        try:
            if DATABASE_FILE.exists():
                try:
                    copy2(DATABASE_FILE, BACKUP_FILE)
                except Exception:
                    pass

            with open(DATABASE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return True, "Saved."

        except Exception as error:
            return False, f"Unable to save data: {error}"

    def reset_database(self):
        self.students = []
        self.teachers = []
        self.save_data()
        return True, "Database has been reset. You now have a fresh, empty database."

    # ---------------- Validation ----------------

    @staticmethod
    def validate_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    # ---------------- Student operations ----------------

    def find_student_by_roll(self, roll_number):
        for student in self.students:
            if student.roll_number.lower() == roll_number.strip().lower():
                return student
        return None

    def add_student(self, name, email, phone, roll_number, department):
        name = name.strip()
        email = email.strip()
        phone = phone.strip()
        roll_number = roll_number.strip()
        department = department.strip()

        if not all([name, email, phone, roll_number, department]):
            return False, "All fields are required."

        if not self.validate_email(email):
            return False, "Invalid email format."

        if self.find_student_by_roll(roll_number) is not None:
            return False, f"A student with roll number '{roll_number}' already exists."

        student = Student(name, email, phone, roll_number, department)
        self.students.append(student)
        self.save_data()
        return True, f"Student '{name}' added successfully."

    def update_student(self, roll_number, name, email, phone, department):
        student = self.find_student_by_roll(roll_number)
        if student is None:
            return False, f"No student found with roll number '{roll_number}'."

        messages = []

        if name.strip():
            student.name = name.strip()
        if phone.strip():
            student.phone = phone.strip()
        if department.strip():
            student.department = department.strip()

        if email.strip():
            if self.validate_email(email.strip()):
                student.email = email.strip()
            else:
                messages.append("invalid email was ignored, old email kept")

        self.save_data()
        base = f"Student '{student.name}' updated successfully."
        if messages:
            base += " (" + "; ".join(messages) + ")"
        return True, base

    def delete_student(self, roll_number):
        student = self.find_student_by_roll(roll_number)
        if student is None:
            return False, f"No student found with roll number '{roll_number}'."
        self.students.remove(student)
        self.save_data()
        return True, f"Student '{student.name}' deleted successfully."

    def add_or_update_grade(self, roll_number, subject, marks):
        student = self.find_student_by_roll(roll_number)
        if student is None:
            return False, f"No student found with roll number '{roll_number}'."
        subject = subject.strip()
        if not subject:
            return False, "Subject cannot be empty."
        if not (0 <= marks <= 100):
            return False, "Marks must be between 0 and 100."
        student.add_grade(subject, marks)
        self.save_data()
        return True, f"Grade for '{subject}' saved for {student.name}."

    def search_students(self, keyword):
        keyword = keyword.strip().lower()
        if not keyword:
            return list(self.students)
        return [
            s for s in self.students
            if keyword in s.name.lower() or keyword in s.roll_number.lower()
        ]

    # ---------------- Teacher operations ----------------

    def find_teacher_by_id(self, employee_id):
        for teacher in self.teachers:
            if teacher.employee_id.lower() == employee_id.strip().lower():
                return teacher
        return None

    def add_teacher(self, name, email, phone, employee_id, subject):
        name = name.strip()
        email = email.strip()
        phone = phone.strip()
        employee_id = employee_id.strip()
        subject = subject.strip()

        if not all([name, email, phone, employee_id, subject]):
            return False, "All fields are required."

        if not self.validate_email(email):
            return False, "Invalid email format."

        if self.find_teacher_by_id(employee_id) is not None:
            return False, f"A teacher with employee ID '{employee_id}' already exists."

        teacher = Teacher(name, email, phone, employee_id, subject)
        self.teachers.append(teacher)
        self.save_data()
        return True, f"Teacher '{name}' added successfully."

    def update_teacher(self, employee_id, name, email, phone, subject):
        teacher = self.find_teacher_by_id(employee_id)
        if teacher is None:
            return False, f"No teacher found with employee ID '{employee_id}'."

        messages = []

        if name.strip():
            teacher.name = name.strip()
        if phone.strip():
            teacher.phone = phone.strip()
        if subject.strip():
            teacher.subject = subject.strip()

        if email.strip():
            if self.validate_email(email.strip()):
                teacher.email = email.strip()
            else:
                messages.append("invalid email was ignored, old email kept")

        self.save_data()
        base = f"Teacher '{teacher.name}' updated successfully."
        if messages:
            base += " (" + "; ".join(messages) + ")"
        return True, base

    def delete_teacher(self, employee_id):
        teacher = self.find_teacher_by_id(employee_id)
        if teacher is None:
            return False, f"No teacher found with employee ID '{employee_id}'."
        self.teachers.remove(teacher)
        self.save_data()
        return True, f"Teacher '{teacher.name}' deleted successfully."

    def search_teachers(self, keyword):
        keyword = keyword.strip().lower()
        if not keyword:
            return list(self.teachers)
        return [
            t for t in self.teachers
            if keyword in t.name.lower()
            or keyword in t.employee_id.lower()
            or keyword in t.subject.lower()
        ]

    # ---------------- Dashboard ----------------

    def dashboard_stats(self):
        total_students = len(self.students)
        total_teachers = len(self.teachers)
        total_grades = sum(len(s.grades) for s in self.students)

        averages = [s.calculate_average() for s in self.students if s.grades]
        school_average = mean(averages) if averages else None

        return {
            "total_students": total_students,
            "total_teachers": total_teachers,
            "total_grades": total_grades,
            "school_average": school_average,
        }


# ============================================================
# SESSION STATE
# ============================================================

if "system" not in st.session_state:
    st.session_state.system = SchoolManagementSystem()

if "history" not in st.session_state:
    st.session_state.history = []
    if st.session_state.system.status:
        status, msg = st.session_state.system.status
        st.session_state.history.insert(0, {
            "status": status, "message": msg,
        })

system = st.session_state.system


def log(status, message):
    """status: ok | err | info"""
    st.session_state.history.insert(0, {"status": status, "message": message})


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown('<div class="brand">SCHOOL MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">students · teachers · grades</div>', unsafe_allow_html=True)

    section = st.radio(
        "Section",
        ["Dashboard", "Students", "Teachers", "Grades", "Database"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown('<div class="panel"><h3>Activity log</h3>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown(
            '<div class="console"><div class="console-line">No activity yet.</div></div>',
            unsafe_allow_html=True,
        )
    else:
        lines = "".join(
            f'<div class="console-line {h["status"]}">{h["message"]}</div>'
            for h in st.session_state.history[:15]
        )
        st.markdown(f'<div class="console">{lines}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown(
    f'<div class="path-bar">~/school-system/<span>{section.lower()}</span></div>',
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS TO RENDER CARDS
# ============================================================

def render_student_card(student):
    grades_html = ""
    if student.grades:
        grades_html = " &nbsp;·&nbsp; ".join(
            f"{subject}: <b>{marks}</b>" for subject, marks in student.grades.items()
        )
    else:
        grades_html = "no grades recorded yet"

    st.markdown(
        f"""
        <div class="entry-card">
            <div class="entry-name">{student.name}
                <span class="badge">{student.performance_grade()}</span>
            </div>
            <div class="entry-row"><b>Roll:</b> {student.roll_number} &nbsp;·&nbsp;
                <b>Dept:</b> {student.department} &nbsp;·&nbsp;
                <b>Email:</b> {student.email} &nbsp;·&nbsp;
                <b>Phone:</b> {student.phone}</div>
            <div class="entry-row"><b>Average:</b> {student.calculate_average():.2f} &nbsp;·&nbsp;
                <b>Grades:</b> {grades_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_teacher_card(teacher):
    st.markdown(
        f"""
        <div class="entry-card teacher">
            <div class="entry-name">{teacher.name}
                <span class="badge" style="background-color:var(--amber);">{teacher.subject}</span>
            </div>
            <div class="entry-row"><b>Employee ID:</b> {teacher.employee_id} &nbsp;·&nbsp;
                <b>Email:</b> {teacher.email} &nbsp;·&nbsp;
                <b>Phone:</b> {teacher.phone}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DASHBOARD
# ============================================================

if section == "Dashboard":
    stats = system.dashboard_stats()
    avg_display = f"{stats['school_average']:.2f}" if stats["school_average"] is not None else "—"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{stats["total_students"]}</div>'
            '<div class="stat-label">Students</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="stat-card amber"><div class="stat-value">{stats["total_teachers"]}</div>'
            '<div class="stat-label">Teachers</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{stats["total_grades"]}</div>'
            '<div class="stat-label">Grades Recorded</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div class="stat-card amber"><div class="stat-value">{avg_display}</div>'
            '<div class="stat-label">School Average</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="panel"><h3>Recent students</h3>', unsafe_allow_html=True)
        if not system.students:
            st.markdown('<div class="console-line">No students yet.</div>', unsafe_allow_html=True)
        else:
            for s in system.students[-5:][::-1]:
                render_student_card(s)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="panel"><h3>Recent teachers</h3>', unsafe_allow_html=True)
        if not system.teachers:
            st.markdown('<div class="console-line">No teachers yet.</div>', unsafe_allow_html=True)
        else:
            for t in system.teachers[-5:][::-1]:
                render_teacher_card(t)
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# STUDENTS
# ============================================================

elif section == "Students":
    tab = st.radio(
        "Student action",
        ["List", "Add", "Search", "Update", "Delete"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if tab == "List":
        st.markdown('<div class="panel"><h3>All students</h3>', unsafe_allow_html=True)
        if not system.students:
            st.markdown('<div class="console-line">No students found.</div>', unsafe_allow_html=True)
        else:
            for s in system.students:
                render_student_card(s)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "Add":
        st.markdown('<div class="panel"><h3>Add a student</h3>', unsafe_allow_html=True)
        name = st.text_input("Full name", key="add_stu_name")
        email = st.text_input("Email", key="add_stu_email")
        phone = st.text_input("Phone", key="add_stu_phone")
        roll = st.text_input("Roll number", key="add_stu_roll")
        dept = st.text_input("Department", key="add_stu_dept")

        if st.button("Add student", key="add_stu_btn"):
            ok, msg = system.add_student(name, email, phone, roll, dept)
            log("ok" if ok else "err", msg)
            (st.success if ok else st.error)(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "Search":
        st.markdown('<div class="panel"><h3>Search students</h3>', unsafe_allow_html=True)
        keyword = st.text_input("Name or roll number", key="search_stu_kw")
        results = system.search_students(keyword) if keyword.strip() else []

        if keyword.strip() and not results:
            st.markdown('<div class="console-line">No matching students.</div>', unsafe_allow_html=True)
        for s in results:
            render_student_card(s)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "Update":
        st.markdown('<div class="panel"><h3>Update a student</h3>', unsafe_allow_html=True)
        roll = st.text_input("Roll number to update", key="update_stu_roll")
        student = system.find_student_by_roll(roll) if roll.strip() else None

        if roll.strip() and student is None:
            st.markdown('<div class="console-line">No student found with that roll number.</div>', unsafe_allow_html=True)

        if student is not None:
            st.markdown(f"**Editing:** {student.name} (leave a field blank to keep its current value)")
            name = st.text_input("Name", placeholder=student.name, key="update_stu_name")
            email = st.text_input("Email", placeholder=student.email, key="update_stu_email")
            phone = st.text_input("Phone", placeholder=student.phone, key="update_stu_phone")
            dept = st.text_input("Department", placeholder=student.department, key="update_stu_dept")

            if st.button("Save changes", key="update_stu_btn"):
                ok, msg = system.update_student(roll, name, email, phone, dept)
                log("ok" if ok else "err", msg)
                (st.success if ok else st.error)(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "Delete":
        st.markdown('<div class="panel danger-zone"><h3>Delete a student</h3>', unsafe_allow_html=True)
        roll = st.text_input("Roll number to delete", key="delete_stu_roll")
        student = system.find_student_by_roll(roll) if roll.strip() else None

        if student is not None:
            render_student_card(student)
            confirm = st.checkbox("I understand this cannot be undone", key="delete_stu_confirm")
            if st.button("Delete student", key="delete_stu_btn"):
                if not confirm:
                    log("info", "Delete cancelled — confirmation not checked.")
                    st.info("Please check the confirmation box first.")
                else:
                    ok, msg = system.delete_student(roll)
                    log("ok" if ok else "err", msg)
                    (st.success if ok else st.error)(msg)
        elif roll.strip():
            st.markdown('<div class="console-line">No student found with that roll number.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# TEACHERS
# ============================================================

elif section == "Teachers":
    tab = st.radio(
        "Teacher action",
        ["List", "Add", "Search", "Update", "Delete"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if tab == "List":
        st.markdown('<div class="panel"><h3>All teachers</h3>', unsafe_allow_html=True)
        if not system.teachers:
            st.markdown('<div class="console-line">No teachers found.</div>', unsafe_allow_html=True)
        else:
            for t in system.teachers:
                render_teacher_card(t)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "Add":
        st.markdown('<div class="panel"><h3>Add a teacher</h3>', unsafe_allow_html=True)
        name = st.text_input("Full name", key="add_tch_name")
        email = st.text_input("Email", key="add_tch_email")
        phone = st.text_input("Phone", key="add_tch_phone")
        emp_id = st.text_input("Employee ID", key="add_tch_id")
        subject = st.text_input("Subject", key="add_tch_subject")

        if st.button("Add teacher", key="add_tch_btn"):
            ok, msg = system.add_teacher(name, email, phone, emp_id, subject)
            log("ok" if ok else "err", msg)
            (st.success if ok else st.error)(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "Search":
        st.markdown('<div class="panel"><h3>Search teachers</h3>', unsafe_allow_html=True)
        keyword = st.text_input("Name, employee ID or subject", key="search_tch_kw")
        results = system.search_teachers(keyword) if keyword.strip() else []

        if keyword.strip() and not results:
            st.markdown('<div class="console-line">No matching teachers.</div>', unsafe_allow_html=True)
        for t in results:
            render_teacher_card(t)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "Update":
        st.markdown('<div class="panel"><h3>Update a teacher</h3>', unsafe_allow_html=True)
        emp_id = st.text_input("Employee ID to update", key="update_tch_id")
        teacher = system.find_teacher_by_id(emp_id) if emp_id.strip() else None

        if emp_id.strip() and teacher is None:
            st.markdown('<div class="console-line">No teacher found with that employee ID.</div>', unsafe_allow_html=True)

        if teacher is not None:
            st.markdown(f"**Editing:** {teacher.name} (leave a field blank to keep its current value)")
            name = st.text_input("Name", placeholder=teacher.name, key="update_tch_name")
            email = st.text_input("Email", placeholder=teacher.email, key="update_tch_email")
            phone = st.text_input("Phone", placeholder=teacher.phone, key="update_tch_phone")
            subject = st.text_input("Subject", placeholder=teacher.subject, key="update_tch_subject")

            if st.button("Save changes", key="update_tch_btn"):
                ok, msg = system.update_teacher(emp_id, name, email, phone, subject)
                log("ok" if ok else "err", msg)
                (st.success if ok else st.error)(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "Delete":
        st.markdown('<div class="panel danger-zone"><h3>Delete a teacher</h3>', unsafe_allow_html=True)
        emp_id = st.text_input("Employee ID to delete", key="delete_tch_id")
        teacher = system.find_teacher_by_id(emp_id) if emp_id.strip() else None

        if teacher is not None:
            render_teacher_card(teacher)
            confirm = st.checkbox("I understand this cannot be undone", key="delete_tch_confirm")
            if st.button("Delete teacher", key="delete_tch_btn"):
                if not confirm:
                    log("info", "Delete cancelled — confirmation not checked.")
                    st.info("Please check the confirmation box first.")
                else:
                    ok, msg = system.delete_teacher(emp_id)
                    log("ok" if ok else "err", msg)
                    (st.success if ok else st.error)(msg)
        elif emp_id.strip():
            st.markdown('<div class="console-line">No teacher found with that employee ID.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# GRADES
# ============================================================

elif section == "Grades":
    tab = st.radio(
        "Grades action",
        ["Add / Update grade", "View grades"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if tab == "Add / Update grade":
        st.markdown('<div class="panel"><h3>Add or update a grade</h3>', unsafe_allow_html=True)
        roll = st.text_input("Student roll number", key="grade_add_roll")
        student = system.find_student_by_roll(roll) if roll.strip() else None

        if roll.strip() and student is None:
            st.markdown('<div class="console-line">No student found with that roll number.</div>', unsafe_allow_html=True)

        if student is not None:
            st.markdown(f"**Student:** {student.name} &nbsp;·&nbsp; **Department:** {student.department}")
            subject = st.text_input("Subject", key="grade_add_subject")
            marks = st.number_input("Marks (0–100)", min_value=0.0, max_value=100.0, step=0.5, key="grade_add_marks")

            if st.button("Save grade", key="grade_add_btn"):
                ok, msg = system.add_or_update_grade(roll, subject, marks)
                log("ok" if ok else "err", msg)
                (st.success if ok else st.error)(msg)
        st.markdown("</div>", unsafe_allow_html=True)

    elif tab == "View grades":
        st.markdown('<div class="panel"><h3>View a student\'s grades</h3>', unsafe_allow_html=True)
        roll = st.text_input("Student roll number", key="grade_view_roll")
        student = system.find_student_by_roll(roll) if roll.strip() else None

        if roll.strip() and student is None:
            st.markdown('<div class="console-line">No student found with that roll number.</div>', unsafe_allow_html=True)

        if student is not None:
            render_student_card(student)
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================

elif section == "Database":
    st.markdown('<div class="panel"><h3>Database info</h3>', unsafe_allow_html=True)
    st.markdown(
        f"**File:** `{DATABASE_FILE.resolve()}`  \n"
        f"**Backup file:** `{BACKUP_FILE.resolve()}`  \n"
        f"**Students stored:** {len(system.students)}  \n"
        f"**Teachers stored:** {len(system.teachers)}"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel danger-zone"><h3>Reset database</h3>', unsafe_allow_html=True)
    st.markdown("This permanently deletes **all** students, teachers and grades.")
    confirm_text = st.text_input('Type RESET to confirm', key="reset_confirm_text")
    if st.button("Reset database", key="reset_db_btn"):
        if confirm_text.strip() != "RESET":
            log("info", "Database reset cancelled — confirmation text did not match.")
            st.info("Type RESET exactly (all caps) to confirm.")
        else:
            ok, msg = system.reset_database()
            log("ok" if ok else "err", msg)
            (st.success if ok else st.error)(msg)
    st.markdown("</div>", unsafe_allow_html=True)