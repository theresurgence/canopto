import asyncio

from canopto.classes.course import Course
from canopto.core.web import ep_courses, get_json
from canopto.ui.messages import print_list_courses


class Courses:

    def __init__(self, role: str):
        self.role = role
        self.courses = []

    def list_courses(self):
        print_list_courses()
        for course in self.courses:
            print(course)
        print()

    async def download_files(self) -> None:
        await asyncio.gather(*[course.download_files() for course in self.courses])

    async def refresh(self) -> None:
        courses_json = await get_json(ep_courses())

        self.courses = [Course(c["id"], c["name"], c["course_code"])
                        for c in courses_json]

        await asyncio.gather(*[course.refresh() for course in self.courses])

    async def download_videos(self):
        await asyncio.gather(*[course.download_videos() for course in self.courses])
