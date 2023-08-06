import json
from datetime import datetime, timedelta

import requests
from loguru import logger

from intellect_core.dto.dto import IntellectConfigDto, AutarizationInfo, ObjectType, CoreCommand, IntellectVisitDto
from intellect_core.handler import IntellectError, ErrorClass, ErrorSubClass


class Intellect:
    log_debug: bool = False
    config: IntellectConfigDto
    autarization_info: AutarizationInfo | None
    expire_token_date: str

    def init(self, intellect_config: IntellectConfigDto):
        self.config = intellect_config

    def _get_url(self, object_type: ObjectType, command: CoreCommand,
                 dto: IntellectVisitDto.Create | IntellectVisitDto.Update | None,
                 objid: int | None) -> str:
        url = ""
        if self.config.https:
            url = f"https://{self.config.intellect_host}/intellect_core/Event?command={command.value}objtype{object_type.value},"
        if not self.config.https:
            url = f"http://{self.config.intellect_host}:{self.config.intellect_port}" \
                  f"/intellect_core/Event?command={command.value}objtype{object_type.value},"

        if dto:
            for key, value in dto.dict().items():
                if value:
                    url = url + f"{key}<{value}>,"
            return url[0:-1]
        else:
            url = url + f"objid<{objid}>"
            return url

    def autarization(self):
        session = requests.Session()
        try:
            if not self.config.https:
                url = f"http://{self.config.host_user}:{self.config.host_password}@{self.config.intellect_host}:{self.config.intellect_port}/token?expires_in={self.config.token_expires}"
                response = session.get(url)

            if self.config.https:
                url = f"https://{self.config.intellect_host}/token?expires_in={self.config.token_expires}"
                response = requests.get(url,
                                        verify=self.config.certificate_path if self.config.certificate_path else False)

            string = "{" + (response.text).replace("\n", ",")[2:-2] + "}"
            self.autarization_info = AutarizationInfo(**json.loads(string))
            self.expire_token_date = datetime.now() + timedelta(
                seconds=self.autarization_info.expires_in)

            if self.log_debug:
                logger.debug(
                    f"response: {response.text}")

        except requests.exceptions.ConnectionError as e:
            self.expire_token_date = datetime.now()
            logger.warning(f"Intellect connection error: {e}\n"
                           f"Next try in {self.expire_token_date + timedelta(minutes=self.config.retry_to_connection_in_minute)}")
            session.close()
            return

    def _connection(self, session: requests.Session, url: str):
        try:
            response = session.get(url,
                                   verify=self.config.certificate_path if self.config.certificate_path else False)
            if self.log_debug:
                logger.debug(
                    f"response: {response.text}")
        except requests.exceptions.ConnectionError as e:
            session.close()
            logger.error(f"Intellect connection error: {e}")

    def logic(self, object_type: ObjectType,
              command: CoreCommand,
              dto: IntellectVisitDto.Create | IntellectVisitDto.Update | None,
              objid: int | None):
        session = requests.Session()
        match command:
            case CoreCommand.CREATE | CoreCommand.UPDATE:
                if dto:
                    dto.level_id = self.config.access_level
                    url = self._get_url(object_type, command, dto, objid)
                    self._connection(session, url)
                else:
                    session.close()
                    raise IntellectError(message="You need set dto for update or create object",
                                         context={"class": ErrorClass.CREATE_OR_UPDATE,
                                                  "subclass": ErrorSubClass.DTO_NOT_FOUND})
            case CoreCommand.DELETE:
                if objid:
                    url = self._get_url(object_type=object_type, command=command, dto=None, objid=objid)
                    self._connection(session, url)
                else:
                    session.close()
                    raise IntellectError(message="You need set object id for delete object",
                                         context={"class": ErrorClass.DELETE,
                                                  "subclass": ErrorSubClass.OBJECT_ID_NOT_FOUND})
