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
    type: str

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
    type: Optional[str] = None

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

# ---------------------------
# Admission Description Schemas
# ---------------------------
class AdmissionDescriptionBase(BaseModel):
    major_id: int
    field_or_subject_name: str

class AdmissionDescriptionCreate(AdmissionDescriptionBase):
    pass

class AdmissionDescriptionOut(AdmissionDescriptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AdmissionDescriptionUpdate(BaseModel):
    major_id: Optional[int] = None
    field_or_subject_name: Optional[str] = None

class PointCountRequest(BaseModel):
    group: str
    achievement: Optional[str] = None
    score10: Optional[float] = 0
    score11: Optional[float] = 0
    score12: Optional[float] = 0
    school_id: Optional[int] = None
    priority_area: Optional[str] = ""
    priority_object: Optional[str] = ""

class PointCountResponse(BaseModel):
    group: str
    achievement_points: float
    academic_score: float
    converted_priority: float
    total_score: float

class SubjectScore(BaseModel):
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    scores: list[float]

class ScoreCalculationRequest(BaseModel):
    scores_type: str  # "semester" for 6 semesters, "year" for 3 years, "exam" for high school exam scores
    subjects: list[SubjectScore]
    
class CombinationScore(BaseModel):
    group_id: int
    group_name: str
    score: float
    subjects: list[dict] = []  # Details of subjects used in this combination
    
class ScoreCalculationResponse(BaseModel):
    combinations: list[CombinationScore]

class PriorityCalculationRequest(BaseModel):
    score: float  # Original score on 30-point scale
    school_id: Optional[int] = None  # School ID (if provided, will be used to determine priority area)
    priority_area: Optional[str] = None  # KV1, KV2, KV2NT, etc.
    priority_object: str  # ĐT01, ĐT02, etc.

class PriorityCalculationResponse(BaseModel):
    origin_point: float  # Original score input
    origin_priority: float  # Raw priority points before reduction
    convert_priority: float  # Priority points after possible reduction
    total_point: float  # Total score after adding priority
    priority_area: str  # The priority area used in calculation
