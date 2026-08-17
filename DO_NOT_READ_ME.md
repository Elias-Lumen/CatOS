# CatOS Development Sprints

## Sprint 1 — Foundation, User Accounts and Basic Task System

### User Accounts
- [x] User registration
- [x] User login
- [x] User logout
- [x] Session-based authentication
- [x] Secure password hashing
- [ ] Unique usernames
- [ ] User data separation
- [ ] Prevent unauthenticated users from accessing private pages

### Basic Task Management
- [x] Create tasks
- [x] Task title
- [x] Task description
- [x] Due date
- [x] Priority
- [ ] Basic task status
  - [ ] Not started
  - [ ] Completed
- [ ] Ensure users can only access their own tasks

### Database Foundation
- [x] Create users table
- [x] Create tasks table
- [x] Set up foreign key relationships
- [x] Enable foreign key constraints
- [x] Add database constraints for task status and priority
- [x] Connect the Flask application to SQLite
- [x] Display database task data on the website

### Basic User Interface
- [x] Base page layout
- [x] Sidebar navigation
- [x] Login page
- [x] Register page
- [x] Today page structure
- [ ] Task creation form
- [ ] Consistent basic styling

### Sprint 1 Testing

#### Registration Testing
- [ ] Register with a valid username and password
- [ ] Register with an empty username
- [ ] Register with an empty password
- [ ] Register with both fields empty
- [ ] Register using an existing username
- [ ] Test a very short username
- [ ] Test a very long username
- [ ] Test usernames containing spaces or unusual characters
- [ ] Test password confirmation does not match
- [ ] Confirm passwords are stored as hashes rather than plain text

#### Login Testing
- [ ] Login with a valid username and password
- [ ] Login with a correct username and incorrect password
- [ ] Login with a username that does not exist
- [ ] Login with an empty username
- [ ] Login with an empty password
- [ ] Login with both fields empty
- [ ] Test very long input values
- [ ] Test unusual characters in username/password fields
- [ ] Confirm successful login creates the correct session
- [ ] Confirm logout clears the session
- [ ] Confirm a logged-out user cannot access the Today page

#### Task Creation Testing
- [ ] Create a task with all fields completed
- [ ] Create a task with only a title
- [ ] Attempt to create a task with an empty title
- [ ] Create a task with a very long title
- [ ] Create a task with a very long description
- [ ] Test each priority value
- [ ] Test each task status value
- [ ] Create a task without a due date
- [ ] Create a task with a valid due date
- [ ] Confirm task data is correctly stored in the database
- [ ] Confirm a task is connected to the correct user

### Sprint 1 Review
- [ ] Record problems discovered during testing
- [ ] Record changes made after testing
- [ ] Add screenshots of important bugs or improvements
- [ ] Record relevant GitHub commits
- [ ] Identify improvements required for Sprint 2


---

## Sprint 2 — Complete Task Management and Date-Based Organisation

### Task Management
- [ ] Edit tasks
- [ ] Delete tasks
- [ ] Reschedule tasks
- [ ] Mark tasks as completed
- [ ] Change task status
- [ ] Change task priority
- [ ] Edit task description
- [ ] Edit task due date

### Subtasks
- [ ] Create subtasks
- [ ] Display subtasks under their parent task
- [ ] Edit subtasks
- [ ] Delete subtasks
- [ ] Mark subtasks as completed

### Today
- [ ] Automatically identify tasks due today
- [ ] Display today's tasks
- [ ] Separate completed and incomplete tasks
- [ ] Display the number of tasks due today
- [ ] Quickly add tasks from the Today page
- [ ] Display overdue tasks as reminders

### Overdue
- [ ] Automatically identify overdue tasks using the due date
- [ ] Exclude completed tasks from overdue tasks
- [ ] Create a separate Overdue page
- [ ] Display all overdue tasks
- [ ] Quickly reschedule overdue tasks
- [ ] Display the number of overdue tasks

### Upcoming
- [ ] Create an Upcoming page
- [ ] Display future tasks
- [ ] Sort future tasks by date
- [ ] Group future tasks by date
- [ ] Allow users to view tasks for upcoming days

### All Tasks
- [ ] Create an All Tasks page
- [ ] Display all tasks belonging to the current user
- [ ] Display completed tasks
- [ ] Sort tasks by due date
- [ ] Filter tasks by status
- [ ] Filter tasks by priority

### Task Interface Improvements
- [ ] Custom paw icons for task priority
- [ ] Different visual indicators for different priority levels
- [ ] Improve task row layout
- [ ] Add empty states when no tasks are available
- [ ] Add success and error messages

### Sprint 2 Testing

#### Edit and Delete Testing
- [ ] Edit a valid task
- [ ] Edit the title only
- [ ] Edit the description only
- [ ] Edit the priority only
- [ ] Edit the due date only
- [ ] Attempt to save an empty title
- [ ] Attempt to edit an invalid task ID
- [ ] Delete a valid task
- [ ] Attempt to delete a task that does not exist
- [ ] Confirm deleted tasks are removed from the database
- [ ] Confirm deleting a task also removes its subtasks if required

#### User Data Separation Testing
- [ ] Create two different user accounts
- [ ] Create tasks under User A
- [ ] Create tasks under User B
- [ ] Confirm User A cannot see User B's tasks
- [ ] Confirm User B cannot see User A's tasks
- [ ] Attempt to access another user's task by changing the URL/task ID
- [ ] Attempt to edit another user's task
- [ ] Attempt to delete another user's task
- [ ] Confirm unauthorised operations are rejected

#### Today Testing
- [ ] Create a task due today
- [ ] Confirm it appears on the Today page
- [ ] Create a task due tomorrow
- [ ] Confirm it does not appear as a Today task
- [ ] Create a completed task due today
- [ ] Confirm completed status is displayed correctly
- [ ] Test behaviour when there are no Today tasks
- [ ] Test multiple Today tasks

#### Overdue Testing
- [ ] Create a task with a due date before today
- [ ] Confirm it appears as overdue
- [ ] Create a completed task with a past due date
- [ ] Confirm it is not treated as an active overdue task
- [ ] Create a task due today
- [ ] Confirm it is not incorrectly classified as overdue
- [ ] Create a future task
- [ ] Confirm it is not overdue
- [ ] Reschedule an overdue task to a future date
- [ ] Confirm it disappears from the Overdue page

#### Upcoming Testing
- [ ] Create tasks due on different future dates
- [ ] Confirm tasks appear in the correct order
- [ ] Confirm tasks are grouped under the correct dates
- [ ] Test an Upcoming page with no future tasks

### Sprint 2 Review
- [ ] Record problems discovered during testing
- [ ] Record changes made after testing
- [ ] Add before-and-after screenshots
- [ ] Record database changes
- [ ] Record relevant GitHub commits
- [ ] Identify improvements required for Sprint 3


---

## Sprint 3 — Search, Progress Tracking, Personalisation and Final Refinement

### Search
- [ ] Create Search page
- [ ] Search tasks by title
- [ ] Search tasks by description
- [ ] Only return search results belonging to the current user
- [ ] Filter search results by tag
- [ ] Filter search results by priority
- [ ] Filter search results by status
- [ ] Handle searches with no results

### Labels / Tags
- [ ] Add tags to tasks
- [ ] Create Labels page
- [ ] View tasks by tag
- [ ] Edit tags
- [ ] Delete tags

### Projects
- [ ] Create Projects page
- [ ] Create projects
- [ ] Add tasks to projects
- [ ] View tasks within a project
- [ ] Edit projects
- [ ] Delete projects

### Progress and Statistics
- [ ] Display total number of tasks
- [ ] Display number of completed tasks
- [ ] Display number of incomplete tasks
- [ ] Calculate today's completion rate
- [ ] Display dynamic completion percentage
- [ ] Add a dynamic progress bar
- [ ] Update progress immediately when task status changes
- [ ] Display daily task statistics
- [ ] Display weekly task statistics
- [ ] Create / complete the Data page

### User Profile
- [ ] User profile
- [ ] User avatar
- [ ] Upload avatar
- [ ] Change avatar
- [ ] Settings page
- [ ] Edit user profile

### Virtual Cat
- [ ] Each user has their own virtual cat
- [ ] Cat page
- [ ] Cat name
- [ ] Rename cat
- [ ] Cat appearance / colour
- [ ] Cat status
- [ ] Mood
- [ ] Energy
- [ ] Hunger
- [ ] Cat statistics change dynamically
- [ ] Completing tasks affects the cat
- [ ] Interact with the cat
- [ ] Coin / reward system
- [ ] Purchase items
- [ ] Equip items

### Remaining Pages
- [ ] Complete Help page
- [ ] Complete Data page
- [ ] Complete Search page
- [ ] Complete Labels page
- [ ] Complete Cat page
- [ ] Complete Settings page
- [ ] Remove or complete unused placeholder pages/routes

### Final UI Refinement
- [ ] Make visual design consistent across all pages
- [ ] Improve spacing and alignment
- [ ] Improve forms and buttons
- [ ] Improve navigation clarity
- [ ] Check text contrast
- [ ] Add appropriate form labels
- [ ] Add empty states
- [ ] Add success messages
- [ ] Add error messages
- [ ] Make layout reasonably responsive

### Validation, Security and Error Handling
- [ ] Validate all task form inputs
- [ ] Validate task priority
- [ ] Validate task status
- [ ] Handle invalid task IDs
- [ ] Handle missing database records
- [ ] Prevent users from modifying another user's data
- [ ] Add 404 error handling
- [ ] Add 500 error handling
- [ ] Improve database error handling
- [ ] Remove duplicated or unnecessary code
- [ ] Remove unused routes or templates

### Sprint 3 Testing

#### Search Testing
- [ ] Search using an exact task title
- [ ] Search using part of a task title
- [ ] Search using task description text
- [ ] Search using different letter cases
- [ ] Search with an empty query
- [ ] Search for text that does not exist
- [ ] Search using unusual characters
- [ ] Confirm another user's tasks never appear in results
- [ ] Test filters individually
- [ ] Test multiple filters together

#### Progress Testing
- [ ] Test progress with 0 tasks
- [ ] Test progress with 1 incomplete task
- [ ] Test progress with 1 completed task
- [ ] Test progress with multiple completed and incomplete tasks
- [ ] Test 0% completion
- [ ] Test 50% completion
- [ ] Test 100% completion
- [ ] Confirm progress updates after completing a task
- [ ] Confirm progress updates after reopening a task
- [ ] Confirm division-by-zero does not occur when there are no tasks

#### Avatar Testing
- [ ] Upload a valid image
- [ ] Change an existing avatar
- [ ] Test behaviour when no avatar has been uploaded
- [ ] Attempt to upload an unsupported file type
- [ ] Attempt to upload a very large file
- [ ] Confirm one user's avatar does not affect another user

#### Virtual Cat Testing
- [ ] Confirm each user receives the correct cat
- [ ] Confirm one user cannot access another user's cat
- [ ] Rename the cat
- [ ] Test an empty cat name
- [ ] Test a very long cat name
- [ ] Test mood boundary value `0`
- [ ] Test mood boundary value `100`
- [ ] Test energy boundary value `0`
- [ ] Test energy boundary value `100`
- [ ] Test hunger boundary value `0`
- [ ] Test hunger boundary value `100`
- [ ] Attempt values below `0`
- [ ] Attempt values above `100`
- [ ] Confirm completing a task changes cat data correctly
- [ ] Confirm cat data remains stored after logout/login

#### Error Handling Testing
- [ ] Visit a route that does not exist and confirm the 404 page appears
- [ ] Test invalid task IDs
- [ ] Test malformed form input
- [ ] Test missing required form data
- [ ] Confirm database constraint errors are handled appropriately
- [ ] Confirm the application does not expose sensitive error information to users
- [ ] Test important functions after logging out
- [ ] Test important functions with two separate user accounts

### Sprint 3 Final Review
- [ ] Record all final testing results
- [ ] Record bugs found and fixes made
- [ ] Include evidence of iterative improvements
- [ ] Include final ERD
- [ ] Include final UI screenshots
- [ ] Include relevant GitHub commits
- [ ] Review all relevant implications
- [ ] Explain how testing improved the final outcome
- [ ] Explain how iteration improved the final outcome