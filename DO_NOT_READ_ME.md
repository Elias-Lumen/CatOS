# CatOS Development Sprints

## Sprint 1 --- Foundation, User Accounts and Basic Task System

### User Accounts

- [x] User registration

- [x] User login

- [x] User logout

- [x] Session-based authentication

- [x] Secure password hashing

- [x] Unique usernames

- [x] User data separation

- [x] Prevent unauthenticated users from accessing private pages

### Basic Task Management

- [x] Create tasks

- [x] Task title

- [x] Task description

- [x] Due date

- [x] Priority

- [x] Basic task status

- [x] Not started

- [x] Completed

- [x] Ensure users can only access their own tasks

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

- [x] Task creation form

- [x] Consistent basic styling

### Sprint 1 Testing

#### Registration Testing

- [x] Register with a valid username and password

- [x] Register with an empty username

- [x] Register with an empty password

- [x] Register with both fields empty

- [x] Register using an existing username

- [x] Test a very short username

- [x] Test a very long username

- [ ] Test usernames containing spaces or unusual characters

- [x] Test password confirmation does not match

- [ ] Confirm passwords are stored as hashes rather than plain text

#### Login Testing

- [x] Login with a valid username and password

- [x] Login with a correct username and incorrect password

- [x] Login with a username that does not exist

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

## Sprint 2 --- Complete Task Management and Date-Based

Organisation

### Task Management

- [x] Edit tasks

- [x] Delete tasks

- [x] overdue date change color

- [x] Reschedule tasks

- [x] Mark tasks as completed

- [x] Change task status

- [x] Change task priority

- [x] Edit task description

- [x] Edit task due date

### Subtasks

- [x] Create subtasks

- [x] Display subtasks under their parent task

- [x] Edit subtasks

- [x] Delete subtasks

- [x] Mark subtasks as completed

### Today

- [x] Automatically identify tasks due today

- [x] Display today's tasks

- [x] Separate completed and incomplete tasks

- [x] Display the number of tasks due today

- [x] Quickly add tasks from the Today page

- [x] Display overdue tasks as reminders

### Overdue

- [x] Automatically identify overdue tasks using the due date

- [x] Exclude completed tasks from overdue tasks

- [ ] Create a separate Overdue page

- [x] Display all overdue tasks

- [x] Quickly reschedule overdue tasks

- [x] Display the number of overdue tasks

### Upcoming

- [x] Create an Upcoming page

- [x] Display future tasks

- [x] Sort future tasks by date

- [x] Group future tasks by date

- [x] Allow users to view tasks for upcoming days

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

## Sprint 3 --- Search, Progress Tracking, Personalisation and Final

Refinement

### Search

- [x] Create Search page

- [x] Search tasks by title

- [x] Search tasks by description

- [x] Only return search results belonging to the current user

- [x] Filter search results by tag

- [x] Filter search results by priority

- [x] Filter search results by status

- [x] Handle searches with no results

### Labels / Tags

- [x] Add tags to tasks

- [x] Create Labels page

- [x] View tasks by tag

- [ ] Edit tags

- [x] Delete tags

### Progress and Statistics

- [x] Display total number of tasks

- [x] Display number of completed tasks

- [x] Display number of incomplete tasks

- [x] Calculate today's completion rate

- [x] Display dynamic completion percentage

- [x] Add a dynamic progress bar

- [x] Update progress immediately when task status changes

- [x] Display daily task statistics

- [x] Display weekly task statistics

- [x] Create / complete the Data page

### User Profile

- [x] User profile

- [x] User avatar

- [x] Upload avatar

- [x] Change avatar

- [x] Settings page

- [ ] Edit user profile

### Virtual Cat

- [x] Each user has their own virtual cat

- [x] Cat page

- [x] Cat name

- [x] Rename cat

- [ ] Cat appearance / colour

- [ ] Cat status

- [ ] Mood

- [ ] Energy

- [ ] Hunger

- [ ] Cat statistics change dynamically

- [x] Completing tasks affects the cat

- [ ] Interact with the cat

- [ ] Coin / reward system

- [ ] Purchase items

- [ ] Equip items

### Remaining Pages

- [ ] Complete Help page

- [x] Complete Data page

- [x] Complete Search page

- [x] Complete Labels page

- [ ] Complete Cat page

- [x] Complete Settings page

- [ ] Remove or complete unused placeholder pages/routes

### Final UI Refinement

- [ ] Make visual design consistent across all pages

- [x] Improve spacing and alignment

- [ ] Improve forms and buttons

- [x] Improve navigation clarity

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

- [ ] Visit a route that does not exist and confirm the 404 page

appears

- [ ] Test invalid task IDs

- [ ] Test malformed form input

- [ ] Test missing required form data

- [ ] Confirm database constraint errors are handled appropriately

- [ ] Confirm the application does not expose sensitive error

information to users

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

- [ ] Explain how iteration improved the final outcom