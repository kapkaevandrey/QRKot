from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate
from app.crud.base import BaseCRUD


donation_crud = BaseCRUD[Donation, DonationCreate, DonationUpdate](Donation)
