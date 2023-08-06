import logging

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from domain.label import Label
from output.database.database_base import Base, engine


class Labels(Base, Label):
    __tablename__ = "Labels"

    id = Column(Integer, primary_key=True)
    label_name = Column(String(50))

    contacts = relationship("Contacts", secondary="Labels_Contacts")

    @staticmethod
    def get_all():
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(Labels).all()
                json_all_labels = {}

                for label in data:
                    json_all_labels[label.id] = {
                        "id": label.id,
                        "label_name": label.label_name,
                        "contacts": label.get_contacts_by_label_id()
                    }
                return json_all_labels
        except Exception as e:
            logging.error(e)

    @staticmethod
    def get_label_by_id(id_label):
        try:
            with sessionmaker(bind=engine)() as session:
                return session.query(Labels).filter(Labels.id == id_label).first()
        except Exception as e:
            logging.error(e)

    def get_contacts_by_label_id(self):
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(LabelsContacts).join(Labels).filter(Labels.id == self.id).all()
                json_contacts_by_label_id = {}

                for label_contact in data:
                    json_contacts_by_label_id[label_contact.contact_id] = {
                        "contact_id": label_contact.contact_id
                    }
                return json_contacts_by_label_id
        except Exception as e:
            logging.error(e)







class LabelsContacts(Base):
    __tablename__ = "Labels_Contacts"
    label_id = Column(Integer, ForeignKey('Labels.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('Contacts.id'), primary_key=True)
