class ScheduleHourError(Exception):
    MESSAGE = "A hora inicial deve ser menor que a hora final"


class StudentNotAvailableError(Exception):
    MESSAGE = "Profissional não esta disponível para estas data"


class InstructorNotAvailableError(Exception):
    MESSAGE = "Cliente não esta disponível para esta datas"


class ScheduleNotFoundError(Exception):
    MESSAGE = "Schedule not found"


class ScheduleNotRemoveError(Exception):
    MESSAGE = "Não foi possível uma agenda inciada"


class ProcedureScheduleExists(Exception):
    MESSAGE = "Esta objetivo ja está adicionado a esta agenda"

class SkillScheduleExists(Exception):
    MESSAGE = "Esta habilidade ja está adicionado a esta agenda"

class SkillScheduleLimit(Exception):
    MESSAGE = "Essa agenda possui apenas 1 habilidade cadastrada"
