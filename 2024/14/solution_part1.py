"""
I'm a bit tired but I'll try, it's some vectors stuff
again so should not be that hard.
If I understood everything correctly, of course.
"""

from dataclasses import dataclass

@dataclass
class Vec2:
    x: int
    y: int

@dataclass
class Robot:
    pos: Vec2
    vel: Vec2

def day14(data_file_path, map_width, map_height) -> int:
    robots: list[Robot] = []

    file = open(data_file_path)
    for line in file:
        parts = line.strip().split(" ")
        parts_pos = parts[0][2:].split(",")
        parts_vel = parts[1][2:].split(",")
        pos = Vec2(int(parts_pos[0]), int(parts_pos[1]))
        vel = Vec2(int(parts_vel[0]), int(parts_vel[1]))
        robots.append(Robot(pos, vel))
    file.close()

    SECONDS = 100
    for robot in robots:
        for i in range(SECONDS):
            robot.pos.x += robot.vel.x
            if robot.pos.x >= map_width:
                robot.pos.x -= map_width
            elif robot.pos.x < 0:
                robot.pos.x += map_width

            robot.pos.y += robot.vel.y
            if robot.pos.y >= map_height:
                robot.pos.y -= map_height
            elif robot.pos.y < 0:
                robot.pos.y += map_height

    half_column = map_width // 2
    half_row = map_height // 2
    quadrants = [0] * 4 # topleft, bottomleft, topright, bottomright
    for robot in robots:
        # if robot.pos.x == half_column or robot.pos.y == half_row: continue

        if robot.pos.x < half_column:
            if robot.pos.y < half_row:
                quadrants[0] += 1
            elif robot.pos.y > half_row:
                quadrants[1] += 1
        elif robot.pos.x > half_column:
            if robot.pos.y < half_row:
                quadrants[2] += 1
            elif robot.pos.y > half_row:
                quadrants[3] += 1

    safety_factor = 1
    for n in quadrants:
        safety_factor *= n
    return safety_factor

"""
Done in 55 minutes, going at a tired, very comfortable pace.
As easy as it seemed, but I wasted ~15 minutes debugging
because i wrote "if robot.pos.x > map_width:" so using
the > instead of >=, which means robots were not "teleported"
to the other side of the map (I think this is called wrapping)
if a position index was equal to the size of the map,
which is actually an index out of bounds.
The proverbial off-by-one error?

I really don't like that I add the velocity to each iteration,
I suspect I can just multiply the velocity by 100
and directly find the final position with the % operator.
"""

answer_sample = day14("./sample_input.txt", 11, 7)
print("Answer (sample):", answer_sample)
assert(answer_sample == 12)

answer = day14("./input.txt", 101, 103)
print("Answer", answer)
assert(answer == 231782040)
