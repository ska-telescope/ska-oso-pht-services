import os


def load_string_from_file(filename):
    """
    Return a file from the current directory as a string
    """
    cwd, _ = os.path.split(__file__)
    path = os.path.join(cwd, filename)
    with open(path, "r", encoding="utf-8") as json_file:
        json_data = json_file.read()
        return json_data


SB_INSTANCE_JSON = load_string_from_file("testfile_sample_sbi.json")
EXECUTION_BLOCK_JSON = load_string_from_file("testfile_sample_execution_block.json")
PROJECT_JSON = load_string_from_file("testfile_sample_project.json")
OBSERVING_PROGRAMME_JSON = load_string_from_file(
    "testfile_sample_observing_program.json"
)
LOW_SBD_JSON = load_string_from_file("../schema/common/testfile_sample_low_sb.json")
MID_SBD_JSON = load_string_from_file("../schema/common/testfile_sample_mid_sb.json")
