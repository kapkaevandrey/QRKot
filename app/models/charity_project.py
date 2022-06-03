from sqlalchemy import Column, String, Text

from app.models import ProjectDonation


class CharityProject(ProjectDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (f'Проект - "{self.name}" осталось собрать '
                f'{self.full_amount} руб.')
