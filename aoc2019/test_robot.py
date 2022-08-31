from robot import Robot, VISUAL_DIRECTION, TURNS

def test_test_0():

    robot = Robot()
    robot.make_step(1,0)
    assert robot.position == (-1,0)
    assert robot.map[(0,0)] == 1
    robot.make_step(0,0)
    assert robot.position == (-1,1)
    robot.make_step(1,0)
    assert robot.position == (0,1)
    robot.make_step(1,0)
    print(robot.map)
    draw_robot_map()
    assert robot.position == (0,0)
    robot.make_step(0,1)
    # draw_robot_map()
    assert robot.position == (1,0)

    robot.make_step(1,0)
    assert robot.position == (1,-1)
    robot.make_step(1,0)
    print(robot.map)
    draw_robot_map()
    assert robot.position == (0,-1)