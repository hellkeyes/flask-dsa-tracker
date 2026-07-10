Five tables:

User
- id
- username
- password
- email
- phone_no
- created_at

Pattern
- id
- user_id (NULL = default pattern, otherwise belongs to a user)
- pattern_name
- description
- created_at

Problem
- problem_id
- problem_number
- title
- difficulty
- link

UserProblem
- id
- user_id
- problem_id
- created_at

Attempt
- id
- user_problem_id
- confidence
- time_taken_mins
- solved
- notes
- created_at

Association Table

userproblem_pattern
- user_problem_id
- pattern_id



Relationships

User
├── has many UserProblems
└── can create many custom Patterns

Problem
└── can appear in many UserProblems

UserProblem
├── belongs to one User
├── belongs to one Problem
├── has many Attempts
└── can have many Patterns

Pattern
└── can be attached to many UserProblems

Attempt
└── belongs to one UserProblem