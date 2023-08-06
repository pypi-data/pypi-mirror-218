from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

import config
from domain.building import Building
from output.database.database_base import Base, Session
from output.database.repository import RepositoryDB
from output.models.equipments_database import EquipmentsData
from output.shell.shell import Shell


class BuildingData(Base, Building):
    __tablename__ = "Building"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    equipments = relationship("EquipmentsData", back_populates="building")

    @property
    def repository(self):
        return RepositoryDB(model=self)

    @classmethod
    def get_by_id(cls, obj_id: int, db_session=Session):
        repository = RepositoryDB(model=cls())
        return repository.get_by_id(obj_id=obj_id, db_session=db_session, load_related=True)

    def update_building_equipment_link(self, equipments: List[EquipmentsData], session=Session):
        return self.repository.link(second_relation_objects=equipments, method=self.toggle_building_equipment_link,
                                    db_session=session)

    def execute(self, *args):
        conn = Shell.ssh_connection(host=self.equipment.ip,
                                    username=config.ssh_equipment_username,
                                    password=config.ssh_equipment_password,
                                    port=config.ssh_equipment_port)

        cmd = "energywise query importance 75 name set level 10" if args[0] is None else args[0]

        try:
            with conn:
                conn.run(cmd)
            print(f"Commande {cmd} executé avec succès")
        except Exception as e:
            print(f"Erreur d'execution de la commande : {e}")
