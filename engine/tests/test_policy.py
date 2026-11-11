import unittest

from policy import Action, decide


class DecisionPolicyTests(unittest.TestCase):
    def test_missing_docker_escalates(self):
        self.assertEqual(decide(docker_available=False, active_exists=True,
                                active_healthy=False, restart_attempted=False,
                                previous_healthy=True), Action.ESCALATE)

    def test_healthy_service_is_held(self):
        self.assertEqual(decide(docker_available=True, active_exists=True,
                                active_healthy=True, restart_attempted=False,
                                previous_healthy=False), Action.HOLD)

    def test_unhealthy_service_gets_one_restart(self):
        self.assertEqual(decide(docker_available=True, active_exists=True,
                                active_healthy=False, restart_attempted=False,
                                previous_healthy=True), Action.RESTART)

    def test_missing_active_uses_known_good_rollback(self):
        self.assertEqual(decide(docker_available=True, active_exists=False,
                                active_healthy=False, restart_attempted=True,
                                previous_healthy=True), Action.ROLLBACK)

    def test_no_verified_recovery_escalates(self):
        self.assertEqual(decide(docker_available=True, active_exists=True,
                                active_healthy=False, restart_attempted=True,
                                previous_healthy=False), Action.ESCALATE)


if __name__ == "__main__":
    unittest.main()
