import click

@click.command(name="get")
def get_variable_group():
    """Gets a variable group in the form of a dictionary"""

@click.group()
def main():
    """Script to update the azure library from the provided json file."""

if __name__ == "__main__":
    main.add_command(get_variable_group)
    main()