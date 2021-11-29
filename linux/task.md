Taskwarrior
===
> http://taskwarrior.org/docs/  
> http://taskwarrior.org/docs/examples.html  
> http://taskwarrior.org/docs/workflow.html  
> http://taskwarrior.org/docs/best-practices.html  

# Basic usage

list task

`$ task`, `$ task ls`, `$ task list`, `$ task long`, `$ task all`

show next task

`$ task next`

task stat

`$ task stat`, `$ task summary`

add new task

`$ task add describe your task here`

your task 2 is done, where 2 is the task id

`$ task 2 done`

remove task 1

`$ task 1 delete`, `$ task 1 rm`

# advanced

add new task of high priority

`$ task add priority:H what is your task of high priority`

change task priority

`$ task ID mod priority:H`

assign project to a task

`$ task ID mod project:homework`

assign deadline to task

`$ task ID mod due:today`, available date e.g. `today, tomorrow, eom, 31st`

start a task

`$ task ID start`

assign tags to a task

`$ task ID mod +tag1 +tag2`. Note, `$ task +tag1` will list all tasks tagged with 'tag1'

assign special tag to a task

`$ task ID mod +next`, this will get the affected task the highest priority.

block a task

`$ task ID mod depends:BLOCKER_ID`
