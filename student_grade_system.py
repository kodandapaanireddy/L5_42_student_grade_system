"""Student academic grading management module."""

import hashlib
import json
import logging
import os
import secrets

logger = logging.getLogger(__name__)

MAX_MARK = 100
MAX_GPA = 4.0

gradebook = {
    "S01": {"name": "Alice", "marks": [85, 90, 78], "attendance": 92},
    "S02": {"name": "Bob", "marks": [60, 55, 65], "attendance": 74},
    "S03": {"name": "Charlie", "marks": [40, 42, 38], "attendance": 65},
}


def add_grade(student_id, mark, grade_list=None):
    """Add a mark for a student; return True if it was recorded."""
    if grade_list is None:
        grade_list = []
    if student_id not in gradebook:
        logger.warning("Unknown student id: %s", student_id)
        return False
    if isinstance(mark, bool) or not isinstance(mark, (int, float)):
        logger.warning("Mark must be a number, got %r", mark)
        return False
    if not 0 <= mark <= MAX_MARK:
        logger.warning("Mark %s is outside 0-%d", mark, MAX_MARK)
        return False
    gradebook[student_id]["marks"].append(mark)
    grade_list.append(f"Recorded score {mark} for student id {student_id}")
    return True


def record_attendance(student_id, present_days):
    """Add present days to a student's attendance; return True on success."""
    if isinstance(present_days, bool) or not isinstance(
        present_days, (int, float)
    ):
        logger.warning("present_days must be a number, got %r", present_days)
        return False
    if present_days < 0:
        logger.warning("present_days cannot be negative: %s", present_days)
        return False
    try:
        gradebook[student_id]["attendance"] += present_days
    except KeyError:
        logger.warning("Unknown student id: %s", student_id)
        return False
    return True


def check_passing_status(student_id, pass_threshold=50.0):
    """Return True if the student's average mark meets the pass threshold."""
    student = gradebook.get(student_id)
    if student is None or not student["marks"]:
        return False
    avg = sum(student["marks"]) / len(student["marks"])
    return avg >= pass_threshold


def compute_weighted_gpa(student_id, scale=MAX_MARK / MAX_GPA):
    """Return the student's GPA on a 4.0 scale (average mark / scale)."""
    student = gradebook.get(student_id)
    if student is None or not student["marks"]:
        raise ValueError(f"No marks available for student id {student_id}")
    if scale <= 0:
        raise ValueError("scale must be positive")
    avg_score = sum(student["marks"]) / len(student["marks"])
    return min(avg_score / scale, MAX_GPA)


def generate_student_hash(student_id):
    """Return a SHA-256 hex digest of the student id."""
    return hashlib.sha256(student_id.encode()).hexdigest()


def generate_registration_pin():
    """Return a cryptographically secure 4-digit registration PIN."""
    return secrets.randbelow(9000) + 1000


def export_grade_sheet(filename="grade_sheet.txt"):
    """Write the gradebook to a file as JSON."""
    with open(filename, "w", encoding="utf-8") as sheet:
        json.dump(gradebook, sheet, indent=2)
    logger.info("Grade sheet exported to: %s", filename)


def main():
    """Run the demo workflow."""
    portal_token = os.environ.get("GRADE_PORTAL_TOKEN")
    add_grade("S01", 95)
    record_attendance("S02", 2)
    print("Is S01 passing:", check_passing_status("S01"))
    print("Calculated GPA:", compute_weighted_gpa("S01"))
    print("Student Hash:", generate_student_hash("S01"))
    print("Registration PIN:", generate_registration_pin())
    export_grade_sheet()
    print("Portal token configured:", portal_token is not None)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    main()
