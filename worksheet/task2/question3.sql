-- Work by Majeedah Khan

-- For each department, calculate the number of enrolments in its courses.
-- Expected Columns:
-- DepartmentName, TotalEnrolments


SELECT department.DepartmentName, COUNT(enrolment.EnrolmentId) AS TotalEnrolments

FROM department

JOIN course ON department.DepartmentId = course.DepartmentId

JOIN enrolment ON course.CourseId = enrolment.CourseId

GROUP BY department.DepartmentName;
