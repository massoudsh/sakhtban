"""Import همه‌ی مدل‌ها تا Base.metadata کامل باشد (برای Alembic autogenerate)."""
from app.models.cost import Budget, CostEntry, ProcurementItem  # noqa: F401
from app.models.decision import AmbiguityFlag, Decision, DecisionDocument  # noqa: F401
from app.models.deviation import ActionItem, Deviation, RiskItem  # noqa: F401
from app.models.onboarding import PilotLead  # noqa: F401
from app.models.project import Project, ProjectMember, User  # noqa: F401
from app.models.qa import Defect, PunchItem, ReworkPattern  # noqa: F401
from app.models.report import ReportEntity, SiteReport  # noqa: F401
from app.models.schedule import ScheduleImport, ScheduleTask, TaskDependency  # noqa: F401
