from magicbot import StateMachine, state, timed_state

from components.lifter import Lifter
from components.intake import Intake


class LifterAutomation(StateMachine):
    lifter: Lifter
    intake: Intake

    @state(first=True, must_finish=True)
    def move_upper_scale(self):
        self.lifter.move(self.lifter.UPPER_SCALE)
        self.next_state("move_complete")

    @state(must_finish=True)
    def move_balanced_scale(self):
        self.lifter.move(self.lifter.BALANCED_SCALE)
        self.next_state("move_complete")

    @state(must_finish=True)
    def move_lower_scale(self):
        self.lifter.move(self.lifter.LOWER_SCALE)
        self.next_state("move_complete")

    @state(must_finish=True)
    def move_switch(self):
        self.lifter.move(self.lifter.SWITCH)
        self.next_state("move_complete")

    @state(must_finish=True)
    def move_complete(self):
        """Move to lifter height according to default height"""
        if self.lifter.at_pos() and self.lifter.at_pos_switch_pressed():
            self.lifter.stop()
            self.done()

    @timed_state(duration=0.5, next_state="reset", must_finish=True)
    def eject(self):
        """Ejects cube from mechanism when height is reached."""
        self.intake.intake_clamp(False)
        self.intake.intake_push(True)

    @state(must_finish=True)
    def reset(self):
        """Resets the rest of the intake mechanism(Kicker)"""
        self.intake.intake_push(False)
        self.lifter.reset()
        self.done()
