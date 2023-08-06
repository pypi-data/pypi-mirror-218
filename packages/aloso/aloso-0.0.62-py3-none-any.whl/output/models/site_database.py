import logging

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

from domain.site import Site
from output.database.database_base import Base, engine


class Sites(Base, Site):
    __tablename__ = "Sites"

    id = Column(Integer, primary_key=True)
    site_name = Column(String(50))
    contacts = relationship("Contacts", secondary="Sites_Contacts", lazy="immediate")

    @staticmethod
    def get_all():
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(Sites).all()
                json_all_sites = {}

                for site in data:
                    json_all_sites[site.id] = {
                        "id": site.id,
                        "site_name": site.site_name,
                        "contacts": site.get_contacts_by_site_id()
                    }
                return json_all_sites
        except Exception as e:
            logging.error(e)

    def get_contacts_by_site_id(self):
        try:
            with sessionmaker(bind=engine)() as session:
                data = session.query(SitesContacts).join(Sites).filter(Sites.id == self.id).all()
                json_contacts_by_site_id = {}

                for site_contact in data:
                    json_contacts_by_site_id[site_contact.contact_id] = {
                        "contact_id": site_contact.contact_id
                    }
                return json_contacts_by_site_id
        except Exception as e:
            logging.error(e)


class SitesContacts(Base):
    __tablename__ = "Sites_Contacts"
    site_id = Column(Integer, ForeignKey('Sites.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('Contacts.id'), primary_key=True)

    @staticmethod
    def remove_link_between_contacts_sites(id_site, id_contact):
        try:
            with sessionmaker(bind=engine)() as session:
                session.query(SitesContacts).filter(SitesContacts.site_id == id_site,
                                                    SitesContacts.contact_id == id_contact).delete()
                session.commit()
        except Exception as e:
            logging.error(e)
