from sqlalchemy.orm import Session

from models.ocorrencias_recorrentes import OcorrenciasRecorrentes


class OcorrenciasRecorrentesRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, occurrence: OcorrenciasRecorrentes) -> OcorrenciasRecorrentes:
        self.session.add(occurrence)
        return occurrence

    def update(self, occurrence: OcorrenciasRecorrentes) -> OcorrenciasRecorrentes:
        self.session.add(occurrence)
        return occurrence
