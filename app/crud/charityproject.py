from app.models.charity_project import CharityProject
from app.schemas.charityproject import ProjectCreate, ProjectUpdate
from app.crud.base import BaseCRUD


class ProjectCRUD(BaseCRUD[CharityProject, ProjectCreate, ProjectUpdate]):
    pass


project_crud = ProjectCRUD(CharityProject)
