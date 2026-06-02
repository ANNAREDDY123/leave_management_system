-- 1. Employees with highest number of leaves

SELECT e.name,
       COUNT(l.leave_id) AS total_leaves
FROM employees e
JOIN leave_requests l
ON e.employee_id = l.employee_id
GROUP BY e.employee_id, e.name
ORDER BY total_leaves DESC;

-- 2. Department-wise leave count

SELECT e.department,
       COUNT(l.leave_id) AS leave_count
FROM employees e
JOIN leave_requests l
ON e.employee_id = l.employee_id
GROUP BY e.department;


-- 3. Pending leave requests

SELECT *
FROM leave_requests
WHERE status = 'Pending';

-- 4. Monthly leave report

SELECT strftime('%Y-%m', start_date) AS month,
       COUNT(*) AS total_leaves
FROM leave_requests
GROUP BY strftime('%Y-%m', start_date);

-- 5. Employees who never applied for leave

SELECT e.*
FROM employees e
LEFT JOIN leave_requests l
ON e.employee_id = l.employee_id
WHERE l.leave_id IS NULL;

-- 6. Rank employees by leave count using Window Functions

SELECT
    employee_name,
    total_leaves,
    RANK() OVER (ORDER BY total_leaves DESC) AS leave_rank
FROM (
    SELECT
        e.name AS employee_name,
        COUNT(l.leave_id) AS total_leaves
    FROM employees e
    LEFT JOIN leave_requests l
    ON e.employee_id = l.employee_id
    GROUP BY e.employee_id, e.name
) ranked_data;
