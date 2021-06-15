from core.stage_generator import StageGenerator

map_generator = StageGenerator(
    vertical_length=8, horizontal_length=18, original_entrance_position="UP"
)
[print(x) for x in map_generator.generate_stage()]
