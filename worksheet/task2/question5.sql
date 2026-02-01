-- Work by Majeedah Khan

-- For each student, calculate the total number of credits from courses they passed. Assume a passing grade is 40 or higher.
-- Expected Columns:
-- StudentId, FirstName, LastName, TotalCreditsPassed

SELECT student.StudentId, student.FirstName, student.LastName, SUM(enrolment.Grade) AS TotalCreditsPassed FROM student 

JOIN enrolment ON student.StudentId = enrolment.StudentId 

WHERE enrolment.Grade >= 40

GROUP BY student.StudentId
;

