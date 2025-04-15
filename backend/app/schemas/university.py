from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---------------------------
# Faculty Schemas
# ---------------------------
class FacultyBase(BaseModel):
    name: str
    description: Optional[str] = None
    faculty_code: Optional[str] = None

class FacultyCreate(FacultyBase):
    pass

class FacultyOut(FacultyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class FacultyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    faculty_code: Optional[str] = None

# ---------------------------
# Major Schemas
# ---------------------------
class MajorBase(BaseModel):
    faculty_id: int
    major_code: Optional[str] = None
    name: str
    seats: int
    description: Optional[str] = None

class MajorCreate(MajorBase):
    pass

class MajorOut(MajorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MajorUpdate(BaseModel):
    faculty_id: Optional[int] = None
    major_code: Optional[str] = None
    name: Optional[str] = None
    seats: Optional[int] = None
    description: Optional[str] = None

# ---------------------------
# AdmissionMethod Schemas
# ---------------------------
class AdmissionMethodBase(BaseModel):
    name: str
    description: Optional[str] = None
    min_score: float
    max_score: float

class AdmissionMethodCreate(AdmissionMethodBase):
    pass

class AdmissionMethodOut(AdmissionMethodBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AdmissionMethodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None

# ---------------------------
# AdmissionMethodMajor Schemas
# ---------------------------
class AdmissionMethodMajorBase(BaseModel):
    major_id: int
    admission_methods_id: int

class AdmissionMethodMajorCreate(AdmissionMethodMajorBase):
    pass

class AdmissionMethodMajorOut(AdmissionMethodMajorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AdmissionMethodMajorUpdate(BaseModel):
    major_id: Optional[int] = None
    admission_methods_id: Optional[int] = None

# ---------------------------
# Subject Schemas
# ---------------------------
class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SubjectUpdate(BaseModel):
    name: Optional[str] = None

# ---------------------------
# SubjectScoreMethodGroup Schemas
# ---------------------------
class SubjectScoreMethodGroupBase(BaseModel):
    name: str

class SubjectScoreMethodGroupCreate(SubjectScoreMethodGroupBase):
    pass

class SubjectScoreMethodGroupOut(SubjectScoreMethodGroupBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SubjectScoreMethodGroupUpdate(BaseModel):
    name: Optional[str] = None

# ---------------------------
# SubjectGroupDetail Schemas
# ---------------------------
class SubjectGroupDetailBase(BaseModel):
    group_id: int
    subject_id: int
    coefficient: float

class SubjectGroupDetailCreate(SubjectGroupDetailBase):
    pass

class SubjectGroupDetailOut(SubjectGroupDetailBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SubjectGroupDetailUpdate(BaseModel):
    group_id: Optional[int] = None
    subject_id: Optional[int] = None
    coefficient: Optional[float] = None

# ---------------------------
# SubjectScoreMethodMajor Schemas
# ---------------------------

class SubjectScoreMethodMajorBase(BaseModel):
    group_id: int
    admission_method_major_id: int

class SubjectScoreMethodMajorCreate(SubjectScoreMethodMajorBase):
    pass

class SubjectScoreMethodMajorOut(SubjectScoreMethodMajorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SubjectScoreMethodMajorUpdate(BaseModel):
    group_id: Optional[int] = None
    admission_method_major_id: Optional[int] = None

# ---------------------------
# ConvertPoint Schemas
# ---------------------------
class ConvertPointBase(BaseModel):
    admission_methods_id: int
    origin_min: float
    origin_max: float
    convert_score_min: float
    convert_score_max: float

class ConvertPointCreate(ConvertPointBase):
    pass

class ConvertPointOut(ConvertPointBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ConvertPointUpdate(BaseModel):
    admission_methods_id: Optional[int] = None
    origin_min: Optional[float] = None
    origin_max: Optional[float] = None
    convert_score_min: Optional[float] = None
    convert_score_max: Optional[float] = None

# ---------------------------
# PreviousAdmission Schemas
# ---------------------------
class PreviousAdmissionBase(BaseModel):
    major_id: int
    year: int
    admission_methods_id: int
    score: float

class PreviousAdmissionCreate(PreviousAdmissionBase):
    pass

class PreviousAdmissionOut(PreviousAdmissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PreviousAdmissionUpdate(BaseModel):
    major_id: Optional[int] = None
    year: Optional[int] = None
    admission_methods_id: Optional[int] = None
    score: Optional[float] = None

# ---------------------------
# Course Schemas
# ---------------------------
class CourseBase(BaseModel):
    course_code: str
    name: str
    credits: float

class CourseCreate(CourseBase):
    pass

class CourseOut(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CourseUpdate(BaseModel):
    course_code: Optional[str] = None
    name: Optional[str] = None
    credits: Optional[float] = None

# ---------------------------
# MajorCourse Schemas
# ---------------------------
class MajorCourseBase(BaseModel):
    major_id: int
    year: int

class MajorCourseCreate(MajorCourseBase):
    pass

class MajorCourseOut(MajorCourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MajorCourseUpdate(BaseModel):
    major_id: Optional[int] = None
    year: Optional[int] = None

# ---------------------------
# MajorCourseDetail Schemas
# ---------------------------
class MajorCourseDetailBase(BaseModel):
    major_course_id: int
    course_id: int
    semester: int
    elective_course: bool
    pre_capstone: bool
    mandatory_capstone: bool

class MajorCourseDetailCreate(MajorCourseDetailBase):
    pass

class MajorCourseDetailOut(MajorCourseDetailBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MajorCourseDetailUpdate(BaseModel):
    major_course_id: Optional[int] = None
    course_id: Optional[int] = None
    semester: Optional[int] = None
    elective_course: Optional[bool] = None
    pre_capstone: Optional[bool] = None
    mandatory_capstone: Optional[bool] = None

# ---------------------------
# CoursePriorCourse Schemas
# ---------------------------
class CoursePriorCourseBase(BaseModel):
    major_course_detail_id: int
    prior_course_detail_id: int

class CoursePriorCourseCreate(CoursePriorCourseBase):
    pass

class CoursePriorCourseOut(CoursePriorCourseBase):
    id: int

    class Config:
        orm_mode = True

class CoursePriorCourseUpdate(BaseModel):
    major_course_detail_id: Optional[int] = None
    prior_course_detail_id: Optional[int] = None

# ---------------------------
# CoursePrerequisite Schemas
# ---------------------------
class CoursePrerequisiteBase(BaseModel):
    major_course_detail_id: int
    prerequisite_major_course_detail_id: int

class CoursePrerequisiteCreate(CoursePrerequisiteBase):
    pass

class CoursePrerequisiteOut(CoursePrerequisiteBase):
    id: int

    class Config:
        orm_mode = True

class CoursePrerequisiteUpdate(BaseModel):
    major_course_detail_id: Optional[int] = None
    prerequisite_major_course_detail_id: Optional[int] = None

# ---------------------------
# CourseCorequisite Schemas
# ---------------------------
class CourseCorequisiteBase(BaseModel):
    major_course_detail_id: int
    corequisite_major_course_detail_id: int

class CourseCorequisiteCreate(CourseCorequisiteBase):
    pass

class CourseCorequisiteOut(CourseCorequisiteBase):
    id: int

    class Config:
        orm_mode = True

class CourseCorequisiteUpdate(BaseModel):
    major_course_detail_id: Optional[int] = None
    corequisite_major_course_detail_id: Optional[int] = None
