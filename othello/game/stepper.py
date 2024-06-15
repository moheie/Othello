class DirectionStepper:
    def __init__(self, rows: int, columns: int) -> None:
        self.rows = rows
        self.columns = columns

    # This condition can be applied after stepping to check that the position is valid
    def check_condition(self, position: tuple[int, int]) -> bool:
        pass

    # This condition can be applied before stepping to check that the position to be stepped into is valid
    def check_pre_condition(self, position: tuple[int, int]) -> bool:
        pass

    def step(self, position: tuple[int, int]) -> tuple[int, int]:
        pass

class LeftStepper(DirectionStepper):
    def check_condition(self, position: tuple[int, int]) -> bool:
        return position[1] >= 0
    
    def check_pre_condition(self, position: tuple[int, int]) -> bool:
        return position[1] > 0
    
    def step(self, position: tuple[int, int]) -> tuple[int, int]:
        return (position[0], position[1] - 1)

class RightStepper(DirectionStepper):
    def check_condition(self, position: tuple[int, int]) -> bool:
        return position[1] < self.columns
    
    def check_pre_condition(self, position: tuple[int, int]) -> bool:
        return position[1] < self.columns - 1
    
    def step(self, position: tuple[int, int]) -> tuple[int, int]:
        return (position[0], position[1] + 1)

class UpStepper(DirectionStepper):
    def check_condition(self, position: tuple[int, int]) -> bool:
        return position[0] >= 0
    
    def check_pre_condition(self, position: tuple[int, int]) -> bool:
        return position[0] > 0
    
    def step(self, position: tuple[int, int]) -> tuple[int, int]:
        return (position[0] - 1, position[1])

class DownStepper(DirectionStepper):
    def check_condition(self, position: tuple[int, int]) -> bool:
        return position[0] < self.rows
    
    def check_pre_condition(self, position: tuple[int, int]) -> bool:
        return position[0] < self.rows - 1
    
    def step(self, position: tuple[int, int]) -> tuple[int, int]:
        return (position[0] + 1, position[1])