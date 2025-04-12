from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz
from app.models.base import Base  # Dùng Base chung

# Thiết lập timezone GMT+7 (Asia/Bangkok)
tz = pytz.timezone("Asia/Bangkok")  
# Bảng về Khoa
class Faculty(Base):
    __tablename__ = "faculties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    faculty_code = Column(String(255))
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    majors = relationship(
        "Major",
        back_populates="faculty",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

#Bảng về Ngành đào tạo
class Major(Base):
    __tablename__ = "majors"
    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id", ondelete="CASCADE"))
    major_code = Column(String(255))
    name = Column(String(255))
    seats = Column(Integer)
    description = Column(String(255))
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    faculty = relationship("Faculty", back_populates="majors")
    admission_method_majors = relationship(
        "AdmissionMethodMajor",
        back_populates="major",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    previous_admissions = relationship(
        "PreviousAdmission",
        back_populates="major",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    major_courses = relationship(
        "MajorCourse",
        back_populates="major",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

#Bảng về phương thức xét tuyển
class AdmissionMethod(Base):
    __tablename__ = "admission_methods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(2000))
    min_score = Column(Float)
    max_score = Column(Float)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    admission_method_majors = relationship(
        "AdmissionMethodMajor",
        back_populates="admission_method",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    convert_points = relationship(
        "ConvertPoint",
        back_populates="admission_method",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    previous_admissions = relationship(
        "PreviousAdmission",
        back_populates="admission_method",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

#Bảng về phương thức xét tuyển theo ngành
class AdmissionMethodMajor(Base):
    __tablename__ = "admission_method_majors"
    id = Column(Integer, primary_key=True, index=True)
    major_id = Column(Integer, ForeignKey("majors.id", ondelete="CASCADE"))
    admission_methods_id = Column(Integer, ForeignKey("admission_methods.id", ondelete="CASCADE"))
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    major = relationship("Major", back_populates="admission_method_majors")
    admission_method = relationship("AdmissionMethod", back_populates="admission_method_majors")
    subject_score_method_groups = relationship(
        "SubjectScoreMethodGroup",
        back_populates="admission_method_major",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# Bảng về môn học xét tuyển theo học bạ - Điểm THPT
class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    subject_group_details = relationship(
        "SubjectGroupDetail",
        back_populates="subject",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# Bảng về nhóm môn học xét tuyển theo học bạ - Điểm THPT
class SubjectScoreMethodGroup(Base):
    __tablename__ = "subject_score_method_group"
    id = Column(Integer, primary_key=True, index=True)
    admission_method_major_id = Column(Integer, ForeignKey("admission_method_majors.id", ondelete="CASCADE"))
    name = Column(String(255))
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    admission_method_major = relationship("AdmissionMethodMajor", back_populates="subject_score_method_groups")
    subject_group_details = relationship(
        "SubjectGroupDetail",
        back_populates="group",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# Bảng về chi tiết nhóm môn học xét tuyển theo học bạ - Điểm THPT
class SubjectGroupDetail(Base):
    __tablename__ = "subject_group_details"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("subject_score_method_group.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    coefficient = Column(Float)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    group = relationship("SubjectScoreMethodGroup", back_populates="subject_group_details")
    subject = relationship("Subject", back_populates="subject_group_details")

# Bảng về điểm chuyển đổi các phương thức xét tuyển
class ConvertPoint(Base):
    __tablename__ = "convert_points"
    id = Column(Integer, primary_key=True, index=True)
    admission_methods_id = Column(Integer, ForeignKey("admission_methods.id", ondelete="CASCADE"))
    origin_min = Column(Float)
    origin_max = Column(Float)
    convert_score_min = Column(Float)
    convert_score_max = Column(Float)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    # Sửa: Loại bỏ cascade từ phía "many" (ConvertPoint)
    admission_method = relationship(
        "AdmissionMethod",
        back_populates="convert_points",
        passive_deletes=True
    )

# Bảng về điểm chuẩn các phương thức xét tuyển trong quá khứ
class PreviousAdmission(Base):
    __tablename__ = "previous_admissions"
    id = Column(Integer, primary_key=True, index=True)
    major_id = Column(Integer, ForeignKey("majors.id", ondelete="CASCADE"))
    year = Column(Integer)
    admission_methods_id = Column(Integer, ForeignKey("admission_methods.id", ondelete="CASCADE"))
    score = Column(Float)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    major = relationship("Major", back_populates="previous_admissions")
    admission_method = relationship("AdmissionMethod", back_populates="previous_admissions")

# Bảng về các lớp học phần - CTĐT
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(255))
    name = Column(String(255))
    credits = Column(Float)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    major_course_details = relationship(
        "MajorCourseDetail",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# Bảng về các khung CTĐT - Theo năm
class MajorCourse(Base):
    __tablename__ = "major_courses"
    id = Column(Integer, primary_key=True, index=True)
    major_id = Column(Integer, ForeignKey("majors.id", ondelete="CASCADE"))
    year = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    major = relationship("Major", back_populates="major_courses")
    course_details = relationship(
        "MajorCourseDetail",
        back_populates="major_course",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

# Bảng về chi tiết môn học trong khung CTĐT - Theo học phần
class MajorCourseDetail(Base):
    __tablename__ = "major_course_details"
    id = Column(Integer, primary_key=True, index=True)
    major_course_id = Column(Integer, ForeignKey("major_courses.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    semester = Column(Integer)
    elective_course = Column(Boolean)
    pre_capstone = Column(Boolean)
    mandatory_capstone = Column(Boolean)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz)
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz),
        onupdate=lambda: datetime.now(tz)
    )

    major_course = relationship("MajorCourse", back_populates="course_details")
    course = relationship("Course", back_populates="major_course_details")
    prior_courses = relationship(
        "CoursePriorCourse",
        back_populates="major_course_detail",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="CoursePriorCourse.major_course_detail_id"
    )
    prerequisites = relationship(
        "CoursePrerequisite",
        back_populates="major_course_detail",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="CoursePrerequisite.major_course_detail_id"
    )
    corequisites = relationship(
        "CourseCorequisite",
        back_populates="major_course_detail",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="CourseCorequisite.major_course_detail_id"
    )


# Học trước
class CoursePriorCourse(Base):
    __tablename__ = "course_prior_courses"
    id = Column(Integer, primary_key=True, index=True)
    major_course_detail_id = Column(Integer, ForeignKey("major_course_details.id", ondelete="CASCADE"))
    prior_course_detail_id = Column(Integer, ForeignKey("major_course_details.id", ondelete="CASCADE"))

    major_course_detail = relationship(
        "MajorCourseDetail",
        foreign_keys=[major_course_detail_id],
        back_populates="prior_courses"
    )
    # Nếu cần, có thể thêm relationship cho prior_course_detail_id


# Tiên quyết
class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"
    id = Column(Integer, primary_key=True, index=True)
    major_course_detail_id = Column(Integer, ForeignKey("major_course_details.id", ondelete="CASCADE"))
    prerequisite_major_course_detail_id = Column(Integer, ForeignKey("major_course_details.id", ondelete="CASCADE"))

    major_course_detail = relationship(
        "MajorCourseDetail",
        foreign_keys=[major_course_detail_id],
        back_populates="prerequisites"
    )
    prerequisite_major_course_detail = relationship(
        "MajorCourseDetail",
        foreign_keys=[prerequisite_major_course_detail_id],
        back_populates="prerequisites"
    )
    # Nếu cần, có thể thêm relationship cho prerequisite_major_course_detail_id


# Song hành
class CourseCorequisite(Base):
    __tablename__ = "course_corequisites"
    id = Column(Integer, primary_key=True, index=True)
    major_course_detail_id = Column(Integer, ForeignKey("major_course_details.id", ondelete="CASCADE"))
    corequisite_major_course_detail_id = Column(Integer, ForeignKey("major_course_details.id", ondelete="CASCADE"))

    major_course_detail = relationship(
        "MajorCourseDetail",
        foreign_keys=[major_course_detail_id],
        back_populates="corequisites"
    )
    corequisite_major_course_detail = relationship(
        "MajorCourseDetail",
        foreign_keys=[corequisite_major_course_detail_id],
        back_populates="corequisites"
    )
    # Nếu cần, có thể thêm relationship cho corequisite_major_course_detail_id
