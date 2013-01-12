Scheduler
=========

The scheduler is responsible for queuing tasks for execution at a later time.
It must support multiple queues, and must place tasks in order on those queues.
The executor should execute tasks in order on those queues.

The simplest implementation is the synchronous scheduler, which doesn't
background any tasks, and executes everything in order as it arrives.

