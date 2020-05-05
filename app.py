import click

from policy_iteration import iterate_policy


@click.command()
def approximate_policy():
    iterate_policy()


if __name__ == '__main__':
    approximate_policy()
