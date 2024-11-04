setting_insert_query = """
INSERT INTO `settings` (`name`, `value`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE id=id;
"""

setting_insert_args = [
    (
        "parameter_int", "123",
    ),
    (
        "parameter_str","abc"
    )
]
