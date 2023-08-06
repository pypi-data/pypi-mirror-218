from typing import List
from sqlalchemy import and_, or_

import cstore.schemes as schemes
from cstore.models import Command, Tag, CommandTag
from cstore.database import LocalSession


class RepoCommand:
    def __init__(self) -> None:
        self.db = LocalSession()

    def create(self, command_data: schemes.CommandCreateWithTagsSchema) -> Command:
        db_command = Command(**command_data.dict())
        self.db.add(db_command)
        self.db.commit()
        self.db.refresh(db_command)
        self.db.close()
        return db_command

    def get_by_id(self, command_id: int) -> Command:
        result = self.db.query(Command).filter(
            Command.id == command_id).first()
        self.db.close()
        return result

    def get_by_body(self, command_body: str) -> Command:
        result = self.db.query(Command).filter(
            Command.body == command_body
        ).first()
        self.db.close()
        return result

    def get_or_create(self, command_data: schemes.CommandCreateWithTagsSchema) -> any:
        is_new_command = False
        command = self.get_by_body(command_data.body)
        if not command:
            command = self.create(command_data)
            is_new_command = True
        return command, is_new_command

    def remove_tag(self, command_id: int, tag_id: int):
        self.db.query(CommandTag).filter(
            and_(CommandTag.command_id == command_id, CommandTag.tag_id == tag_id)).delete()
        self.db.commit()
        self.db.close()

    def add_tag(self, command_id: int, tag_id: int):
        db_commandTag = CommandTag(command_id=command_id, tag_id=tag_id)
        self.db.add(db_commandTag)
        self.db.commit()
        self.db.close()

    def remove(self, command_id: int):
        self.db.query(Command).filter(
            Command.id == command_id).delete()
        self.db.commit()
        self.db.close()

    def search_and_filter(self,
                          entities: schemes.EntitiesSchema
                          ) -> List[Command] | None:
        result = None
        query_object = None

        if entities.command or entities.tags:
            query_object = self.db.query(Command)

        if entities.command:
            command_query = "%" + entities.command.body + "%"
            description_query = "%" + entities.command.body + "%"
            query_object = query_object.filter(or_(Command.body.ilike(command_query),
                                                   Command.description.ilike(description_query)))

        if entities.tags:
            tags_names = []
            for tag in entities.tags:
                tags_names.append(tag.name)

            if len(tags_names):
                query_object = query_object.filter(
                    Command.tags.any(Tag.name.in_(tags_names)))

        if query_object:
            result = query_object.order_by(Command.body).all()

        return result
