import asyncio
import os

import aiofiles

from classes.course import Course
from core.web import ep_courses, get_json, download_file
from ui.messages import print_list_courses


class Courses:

    def __init__(self, role: str):
        self.role = role
        self.courses = []
        self.all_videos = {}
        self.has_refreshed = False

    def list_courses(self):
        print_list_courses()
        for course in self.courses:
            print(course)
        print()

    async def download_files(self) -> None:
        await asyncio.gather(*[course.download_files() for course in self.courses])

    async def refresh_list(self) -> None:
        courses_json = await get_json(ep_courses())

        # TODO reinstate remove if statement
        self.courses = [Course(c["id"], c["name"], c["course_code"], c["enrollments"][0]['type'])
                        for c in courses_json]

    async def refresh_contents(self) -> None:
        if not self.has_refreshed:
            await asyncio.gather(*[course.refresh_contents() for course in self.courses])

        self.has_refreshed = True

    async def refresh_videos_list(self):
        for course in self.courses:
            await course.get_videos()
            self.all_videos.update(course.videos)

    async def download_videos(self):
        await self.create_video_dirs()

        await asyncio.gather(*[download_file(video_url, video_path)
                               for video_path, video_url
                               in self.all_videos.items()])

    async def create_video_dirs(self) -> None:
        for video_path in self.all_videos:
            await aiofiles.os.makedirs(os.path.dirname(video_path), exist_ok=True)
