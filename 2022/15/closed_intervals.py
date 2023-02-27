from typing import NamedTuple
import math

class Interval(NamedTuple):
    a: int
    b: int
    
    is_divisor = False
    
class DivisorInterval(Interval):
    is_divisor = True

class ClosedIntervals:
    def __init__(self) -> None:
        self.intervals: list[Interval] = [DivisorInterval(-math.inf, math.inf)]

    def add(self, a: int, b: int):
        if a > b:
            a,b = b,a

        a_interval = self.where(a)
        b_interval = self.where(b)

        num_intervals = len(self.intervals)
        new_intervals = []
        id = 0
        while id < num_intervals:
            if id < a_interval or id > b_interval:
                new_intervals.append(self.intervals[id])
                id += 1
            else: 
                new_a = self.intervals[a_interval].a
                if self.intervals[a_interval].is_divisor:
                    if self.intervals[a_interval].a <= a-1:
                        new_intervals.append(DivisorInterval(self.intervals[a_interval].a, a-1))
                    new_a = a
                
                new_b = self.intervals[b_interval].b
                if self.intervals[b_interval].is_divisor:
                    new_b = b
                    new_intervals.append(Interval(new_a, new_b))

                    if new_b+1 <= self.intervals[b_interval].b:
                        new_intervals.append(DivisorInterval(new_b+1, self.intervals[b_interval].b))
                else:
                    new_intervals.append(Interval(new_a, new_b))
                
                id = b_interval + 1
        
        self.intervals = new_intervals

    def where(self, c: int):
        for id, interval in enumerate(self.intervals):
            if c >= interval.a and c <= interval.b:
                return id

    def is_in(self, c: int):
        c_interval = self.where(c)
        return not self.intervals[c_interval].is_divisor

    def count(self, limits=(-math.inf, math.inf)):
        count = 0
        init_limits_interval = self.where(limits[0])
        final_limits_interval = self.where(limits[1])

        for id, interval in enumerate(self.intervals):
            if id < init_limits_interval or id > final_limits_interval:
                continue

            if not interval.is_divisor:
                if id == init_limits_interval:
                    count += interval.b - limits[0] + 1
                elif id == final_limits_interval:
                    count += limits[1] - interval.a + 1
                else:
                    count += interval.b - interval.a + 1
        
        return count

if __name__ == "__main__":
    intervals = ClosedIntervals()
    intervals.add(2, 5)
    intervals.add(10, 12)
    # intervals.add(15, 16)
    # intervals.add(20, 30)

    # intervals.add(7, 19)


    print(intervals.intervals)
    print(intervals.count())