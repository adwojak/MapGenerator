from core.stage_generator2 import StageGenerator

map_generator = StageGenerator(
    # vertical_length=8, horizontal_length=18, entrance_face="LEFT", exit_face="RIGHT"
    vertical_length=8,
    horizontal_length=18,
    entrance_face="RIGHT",
)
# TODO vertical > horizontal, error for LEFT/RIGHT
# TODO vertical < horizontal, error for UP/DOWN
# for x in range(111111):
#     StageGenerator(
#         vertical_length=18, horizontal_length=8, exit_face="DOWN"
#     ).generate_stage()
[print(x) for x in map_generator.generate_stage()]
