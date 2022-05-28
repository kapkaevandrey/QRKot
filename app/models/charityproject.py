from sqlalchemy import Column, String, Text

from .abstract_base import ProjectDonation


class CharityProject(ProjectDonation):
    name = Column(String(100), unique=True)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f'Project {self.name} it remains to deposit {self.full_amount}'
