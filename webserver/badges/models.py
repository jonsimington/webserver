from brabeion import badges
from brabeion.base import Badge, BadgeAwarded

from competition.models import Competition

import signals

import logging

from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class CompetitionVeteranBadge(Badge):
    slug = "competition_veteran"
    levels = [
        "Bronze",
        "Silver",
        "Gold",
    ]
    description = "For those who have competed in MegaMinerAI Competitions"
    events = [
        "competition_finished",
    ]
    multiple = False

    def has_participated(self, team):
        try:
          repo_head = team.teamclient.repository.repo.head()
          base_head = team.teamclient.base.repository.repo.head()

          return repo_head != base_head
        except ObjectDoesNotExist:
          logger.debug("DoesNotExist")
          return False
        except KeyError:
          logger.debug("KeyError")
          return False


    def award(self, user=None, **state):
        logger.debug("Checking {} for Veteran".format(user.username))
        if user is None:
            logger.warning("Must provide a user for Veteran badge")

        participated = 0

        # users who have participated are not getting badges...
        for team in user.team_set.all():
            if self.has_participated(team):
                participated += 1

        if participated > 5:
            logger.debug("Awarding Veteran Level 3 to {}".format(user.username))
            return BadgeAwarded(level=2)
        elif participated > 3:
            logger.debug("Awarding Veteran Level 2 to {}".format(user.username))
            return BadgeAwarded(level=1)
        elif participated > 0:
            logger.debug("Awarding Veteran Level 1 to {}".format(user.username))
            return BadgeAwarded(level=0)
        else:
            return

badges.register(CompetitionVeteranBadge)
