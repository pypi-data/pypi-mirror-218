from database.models import Dynamogram, Graph, GraphObj
from database.connection import create_session
from sqlalchemy import Column

from typing import List, Union


# TODO: filter by dynamogram type

class DynamogramService:

    def get_dynamogram(self, dynamogram_id: int, db_url: str) -> Dynamogram:
        session = create_session(db_url)
        dynamogram = session.query(Dynamogram).filter_by(
            id=dynamogram_id).first()
        session.close()
        return dynamogram

    def get_all_dynamograms(self, db_url: str) -> List[Dynamogram]:
        session = create_session(db_url)
        dynamograms = session.query(
            Dynamogram).all()
        session.close()
        return dynamograms

    def get_dynamogram_for_well_id(self, well_id: int, db_url: str) -> List[Dynamogram]:
        session = create_session(db_url)
        dynamograms = session.query(
            Dynamogram).filter_by(well_id=well_id).limit(2).all()  # TODO: just .all()
        session.close()
        return dynamograms

    def get_graph_for_dynamogram_id(self, dynamogram_id: Union[int, Column[int]], db_url: str) -> GraphObj:
        session = create_session(db_url)
        graph = session.query(
            Graph).filter_by(dynamogram_id=dynamogram_id).order_by(Graph.point_no).all()
        session.close()

        graph_obj = GraphObj(graph=graph)
        return graph_obj
