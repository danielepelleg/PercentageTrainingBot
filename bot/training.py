class User:
    def __init__(self, name = None, id = None, type = None, training = None):
        self.name = name
        self.id = id
        self.type = type
        self.training = training
    
    def to_dict(self):
        if self.training != None:
            return {
                "name": self.name,
                "id": self.id,
                "type": self.type,
                "training": self.training.to_dict()
            }
        else:
            return {
                "name": self.name,
                "id": self.id
            }

class Training:
    def __init__(self, bench_press = None, deadlift = None, squat = None):
        self.bench_press = bench_press
        self.deadlift = deadlift
        self.squat = squat
    
    def to_dict(self):
        return {
            "bench_press": self.bench_press,
            "deadlift": self.deadlift,
            "squat": self.squat
        }

class Crossfit(Training):
    def __init__(self, bench_press = None, deadlift = None, squat = None, clean = None, snatch = None, jerk = None):
        super().__init__(bench_press, deadlift, squat)
        self.clean = clean
        self.snatch = snatch
        self.jerk = jerk
    
    def to_dict(self):
        return {
            "bench_press": self.bench_press,
            "deadlift": self.deadlift,
            "squat": self.squat,
            "clean": self.clean,
            "snatch": self.snatch,
            "jerk": self.jerk
        }