from radical.entk import Pipeline


class Protocol(object):

    def __init__(self):
        self._stages = list()

    def add_stage(self, stage):

        if self._stages:
            # Set the input of this stage to be the output of the previous stage
            pass

        self._stages.append(stage)

        # self.stage.

    def generate_pipeline(self):
        p = Pipeline

        return p


