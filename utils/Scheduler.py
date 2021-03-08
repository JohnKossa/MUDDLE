import datetime
import asyncio


class Scheduler:
    def __init__(self, async_loop, resolution=60):
        self.scheduled_tasks = []
        self.async_loop = async_loop
        self.resolution = resolution
        self.looping = False

    async def process_loop(self):
        self.looping = True
        while len(self.scheduled_tasks):
            for task in self.scheduled_tasks:
                if datetime.datetime.now() > task.time:
                    await task.func(*task.f_args, **task.f_kwargs)
                    try:
                        self.scheduled_tasks.remove(task)
                    except ValueError:
                        print("scheduled task could not be found")
            await asyncio.sleep(self.resolution)
        self.looping = False

    def schedule_task(self, task):
        need_to_start = False
        if len(self.scheduled_tasks) == 0:
            need_to_start = True
        self.scheduled_tasks.append(task)
        if need_to_start and not self.looping:
            self.async_loop.create_task(self.process_loop())

    def unschedule_task(self, task):
        try:
            if task in self.scheduled_tasks:
                self.scheduled_tasks.remove(task)
                return True
        except ValueError:
            return False
        return False


class ScheduledTask:
    def __init__(self, wake_up_time, func, *f_args, **f_kwargs):
        self.time = wake_up_time
        self.func = func
        self.f_args = f_args
        self.f_kwargs = f_kwargs
